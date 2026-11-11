from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.app.core.database import get_db
from backend.app.models.sentinel_models import Case, AuditLog, Account, Transaction, User
from backend.app.schemas.sentinel_schemas import CaseBase, CaseActionRequest
from backend.app.services.groq_service import groq_service

router = APIRouter(prefix="/api/cases", tags=["Investigation Cases"])

@router.get("", response_model=List[CaseBase])
def get_cases(status: str = None, priority: str = None, db: Session = Depends(get_db)):
    query = db.query(Case)
    if status:
        query = query.filter(Case.status == status)
    if priority:
        query = query.filter(Case.priority == priority)
    return query.order_by(Case.risk_score.desc()).all()

@router.get("/{case_id}")
def get_case_detail(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    account = db.query(Account).filter(Account.id == case.account_id).first()
    transaction = db.query(Transaction).filter(Transaction.id == case.transaction_id).first() if case.transaction_id else None
    audit_logs = db.query(AuditLog).filter(AuditLog.case_id == case.id).order_by(AuditLog.timestamp.desc()).all()
    
    return {
        "case": CaseBase.from_orm(case),
        "account": {
            "id": account.id if account else None,
            "full_name": account.full_name if account else "Unknown",
            "email": account.email if account else None,
            "country": account.country if account else None,
            "status": account.status if account else "active",
            "risk_score": account.risk_score if account else 0
        },
        "transaction": transaction,
        "audit_logs": [
            {
                "id": log.id,
                "action": log.action,
                "previous_state": log.previous_state,
                "new_state": log.new_state,
                "notes": log.notes,
                "timestamp": log.timestamp
            }
            for log in audit_logs
        ]
    }

@router.post("/{case_id}/ai-summarize")
def generate_ai_case_summary(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    account = db.query(Account).filter(Account.id == case.account_id).first()
    txn = db.query(Transaction).filter(Transaction.id == case.transaction_id).first() if case.transaction_id else None
    
    payload = {
        "case_id": case.id,
        "account_id": case.account_id,
        "risk_score": case.risk_score,
        "amount": txn.amount if txn else 0.0,
        "currency": txn.currency if txn else "USD",
        "merchant": txn.merchant if txn else "Unknown Merchant",
        "merchant_category": txn.merchant_category if txn else "General",
        "device_id": "DEV-SIMULATED",
        "ip_address": txn.ip_address if txn else "127.0.0.1",
        "is_vpn": True if txn and txn.is_foreign_ip else False,
        "rule_flags": txn.rule_flags if txn else ["ELEVATED_RISK"],
        "shared_accounts_count": 4 if "Syndicate" in (case.fraud_typology or "") else 1,
        "anomaly_score": txn.anomaly_score if txn else 0.75
    }
    
    forensic_result = groq_service.generate_case_summary(payload)
    
    case.ai_summary = forensic_result.get("executive_summary")
    case.ai_recommendation = forensic_result.get("recommended_action")
    case.ai_confidence = float(forensic_result.get("confidence_score", 85.0))
    case.fraud_typology = forensic_result.get("fraud_typology", case.fraud_typology)
    
    # Record audit log
    audit = AuditLog(
        case_id=case.id,
        actor_id=1,
        action="AI_SUMMARY_GENERATED",
        previous_state=case.status,
        new_state=case.status,
        notes=f"Groq LLaMA forensic synthesis generated with {case.ai_confidence}% confidence."
    )
    db.add(audit)
    db.commit()
    
    return {
        "status": "success",
        "forensic_report": forensic_result
    }

@router.post("/{case_id}/action")
def take_case_action(case_id: str, action_data: CaseActionRequest, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
        
    prev_status = case.status
    account = db.query(Account).filter(Account.id == case.account_id).first()
    
    if action_data.action == "BAN_ACCOUNT":
        case.status = "RESOLVED_FRAUD"
        if account:
            account.status = "banned"
            account.risk_score = 99.0
    elif action_data.action == "RESTRICT_CARD":
        case.status = "RESOLVED_FRAUD"
        if account:
            account.status = "restricted"
    elif action_data.action == "FLAG_FALSE_POSITIVE":
        case.status = "RESOLVED_FALSE_POSITIVE"
        if account:
            account.status = "active"
            account.risk_score = 15.0
    elif action_data.action == "ESCALATE":
        case.status = "ESCALATED"
    else:
        case.status = "UNDER_REVIEW"
        
    audit = AuditLog(
        case_id=case.id,
        actor_id=action_data.analyst_id or 1,
        action=f"DECISION_{action_data.action}",
        previous_state=prev_status,
        new_state=case.status,
        notes=action_data.notes
    )
    db.add(audit)
    db.commit()
    
    return {
        "status": "success",
        "case_id": case.id,
        "new_status": case.status,
        "account_status": account.status if account else "unknown"
    }
