from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.core.database import get_db
from backend.app.models.sentinel_models import Transaction, Case
from backend.app.schemas.sentinel_schemas import ExecutiveAnalyticsResponse

router = APIRouter(prefix="/api/analytics", tags=["Executive Analytics"])

@router.get("/dashboard", response_model=ExecutiveAnalyticsResponse)
def get_executive_dashboard(db: Session = Depends(get_db)):
    total_txns = db.query(Transaction).count() or 1
    total_vol = db.query(func.sum(Transaction.amount)).scalar() or 0.0
    cases_count = db.query(Case).count()
    
    # Calculate simulated fraud metrics
    fraud_txns = db.query(Transaction).filter(Transaction.is_fraud_simulated == True).all()
    prevented_loss = sum(t.amount for t in fraud_txns)
    
    false_positives = db.query(Case).filter(Case.status == "RESOLVED_FALSE_POSITIVE").count()
    resolved_fraud = db.query(Case).filter(Case.status == "RESOLVED_FRAUD").count()
    
    fpr = round((false_positives / (false_positives + resolved_fraud + 1)) * 100, 1)
    
    # Risk Distribution
    low_risk = db.query(Transaction).filter(Transaction.ml_risk_score < 30).count()
    medium_risk = db.query(Transaction).filter(Transaction.ml_risk_score >= 30, Transaction.ml_risk_score < 70).count()
    high_risk = db.query(Transaction).filter(Transaction.ml_risk_score >= 70).count()
    
    return {
        "total_transactions": total_txns,
        "total_volume_usd": round(total_vol, 2),
        "flagged_cases_count": cases_count,
        "prevented_fraud_loss_usd": round(prevented_loss, 2),
        "false_positive_rate": fpr,
        "avg_investigation_time_mins": 14.5,
        "risk_distribution": {
            "Low Risk (<30)": low_risk,
            "Medium Risk (30-70)": medium_risk,
            "High / Critical (>=70)": high_risk
        },
        "top_fraud_typologies": [
            {"typology": "Card Testing Velocity", "count": 14, "loss_exposure": 1240.00},
            {"typology": "Account Takeover (ATO)", "count": 6, "loss_exposure": 18450.00},
            {"typology": "Syndicate / Device Ring", "count": 5, "loss_exposure": 9800.00},
            {"typology": "Foreign Proxy Drift", "count": 8, "loss_exposure": 3200.00}
        ],
        "daily_volume_trend": [
            {"day": "Mon", "legit_volume": 42000, "fraud_attempted": 2100},
            {"day": "Tue", "legit_volume": 48000, "fraud_attempted": 1800},
            {"day": "Wed", "legit_volume": 53000, "fraud_attempted": 3400},
            {"day": "Thu", "legit_volume": 61000, "fraud_attempted": 2900},
            {"day": "Fri", "legit_volume": 72000, "fraud_attempted": 5400},
            {"day": "Sat", "legit_volume": 85000, "fraud_attempted": 7200},
            {"day": "Sun", "legit_volume": 67000, "fraud_attempted": 4100}
        ]
    }
