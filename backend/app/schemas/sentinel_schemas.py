from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class TransactionBase(BaseModel):
    id: str
    account_id: str
    amount: float
    currency: str
    merchant: str
    merchant_category: str
    payment_method: str
    timestamp: datetime
    rule_flags: List[str]
    ml_risk_score: float
    anomaly_score: float
    is_fraud_simulated: bool

    class Config:
        from_attributes = True

class CaseBase(BaseModel):
    id: str
    account_id: str
    transaction_id: Optional[str]
    title: str
    priority: str
    status: str
    assigned_to_id: Optional[int]
    risk_score: float
    fraud_typology: Optional[str]
    ai_summary: Optional[str]
    ai_recommendation: Optional[str]
    ai_confidence: Optional[float]
    evidence_bundle: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CaseActionRequest(BaseModel):
    action: str # "APPROVE", "BAN_ACCOUNT", "RESTRICT_CARD", "FLAG_FALSE_POSITIVE"
    notes: Optional[str] = "Decision rendered by investigator."
    analyst_id: Optional[int] = 1

class TransactionSimulateRequest(BaseModel):
    account_id: str
    amount: float
    merchant: str
    merchant_category: str
    payment_method: str
    is_foreign_ip: bool = False
    is_vpn: bool = False
    device_anomaly: bool = False
    velocity_1h: int = 1

class ExecutiveAnalyticsResponse(BaseModel):
    total_transactions: int
    total_volume_usd: float
    flagged_cases_count: int
    prevented_fraud_loss_usd: float
    false_positive_rate: float
    avg_investigation_time_mins: float
    risk_distribution: Dict[str, int]
    top_fraud_typologies: List[Dict[str, Any]]
    daily_volume_trend: List[Dict[str, Any]]
