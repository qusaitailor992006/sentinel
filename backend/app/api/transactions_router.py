import random
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.core.database import get_db
from backend.app.models.sentinel_models import Transaction, Case
from backend.app.schemas.sentinel_schemas import TransactionBase, TransactionSimulateRequest
from backend.app.services.ml_engine import ml_engine

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.get("", response_model=List[TransactionBase])
def get_transactions(limit: int = 50, high_risk_only: bool = False, db: Session = Depends(get_db)):
    query = db.query(Transaction)
    if high_risk_only:
        query = query.filter(Transaction.ml_risk_score >= 60.0)
    return query.order_by(Transaction.timestamp.desc()).limit(limit).all()

@router.post("/simulate", response_model=TransactionBase)
def simulate_live_transaction(payload: TransactionSimulateRequest, db: Session = Depends(get_db)):
    """
    Simulates real-time transaction ingestion:
    1. Runs Scikit-learn Anomaly & Risk Evaluation
    2. Automatically creates an Investigation Case if risk exceeds threshold
    """
    scoring_payload = {
        "amount": payload.amount,
        "velocity_1h": payload.velocity_1h,
        "is_foreign_ip": payload.is_foreign_ip,
        "is_vpn": payload.is_vpn,
        "device_anomaly": payload.device_anomaly
    }
    anomaly_score, risk_score, rule_flags = ml_engine.score_transaction(scoring_payload)
    
    txn_id = f"TXN-LIVE-{random.randint(10000, 99999)}"
    new_txn = Transaction(
        id=txn_id,
        account_id=payload.account_id,
        amount=payload.amount,
        currency="USD",
        merchant=payload.merchant,
        merchant_category=payload.merchant_category,
        payment_method=payload.payment_method,
        ip_address="185.220.101.4",
        timestamp=datetime.utcnow(),
        velocity_1h=payload.velocity_1h,
        is_foreign_ip=payload.is_foreign_ip,
        device_anomaly=payload.device_anomaly,
        rule_flags=rule_flags,
        ml_risk_score=risk_score,
        anomaly_score=anomaly_score,
        is_fraud_simulated=risk_score > 60.0
    )
    db.add(new_txn)
    
    # Auto-generate Case if risk is high
    if risk_score >= 65.0:
        new_case = Case(
            id=f"CASE-LIVE-{random.randint(1000, 9999)}",
            account_id=payload.account_id,
            transaction_id=txn_id,
            title=f"Automated Real-Time Intercept: {payload.merchant} (${payload.amount:.2f})",
            priority="CRITICAL" if risk_score > 85.0 else "HIGH",
            status="NEW",
            risk_score=risk_score,
            fraud_typology="High-Velocity Anomaly" if "VELOCITY_SPIKE_1H" in rule_flags else "Risk Threshold Breach",
            evidence_bundle={
                "rules_triggered": rule_flags,
                "amount": payload.amount,
                "anomaly_score": anomaly_score
            }
        )
        db.add(new_case)
        
    db.commit()
    db.refresh(new_txn)
    return new_txn
