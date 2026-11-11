import pytest
from backend.app.services.ml_engine import ml_engine
from backend.app.services.groq_service import groq_service

def test_ml_scoring_high_risk():
    """Verify that multi-signal anomaly triggers appropriate risk score and flags."""
    sample_txn = {
        "amount": 2500.0,
        "velocity_1h": 7,
        "is_foreign_ip": True,
        "is_vpn": True,
        "device_anomaly": True
    }
    anomaly_score, risk_score, rule_flags = ml_engine.score_transaction(sample_txn)
    
    assert risk_score >= 70.0
    assert "HIGH_TRANSACTION_VALUE" in rule_flags
    assert "VELOCITY_SPIKE_1H" in rule_flags
    assert "GEO_IP_VPN_MISMATCH" in rule_flags

def test_ml_scoring_clean_transaction():
    """Verify that normal retail activity remains low risk."""
    clean_txn = {
        "amount": 34.50,
        "velocity_1h": 1,
        "is_foreign_ip": False,
        "is_vpn": False,
        "device_anomaly": False
    }
    anomaly_score, risk_score, rule_flags = ml_engine.score_transaction(clean_txn)
    
    assert risk_score < 35.0
    assert len(rule_flags) == 0

def test_groq_forensic_fallback():
    """Verify that Groq forensic service returns valid structured JSON even in fallback mode."""
    payload = {
        "case_id": "CASE-TEST-001",
        "account_id": "ACC-TEST",
        "risk_score": 88.0,
        "amount": 1200.0,
        "merchant": "Apple Store",
        "merchant_category": "electronics",
        "device_id": "DEV-TEST",
        "ip_address": "127.0.0.1",
        "is_vpn": True,
        "rule_flags": ["VELOCITY_SPIKE", "NEW_DEVICE"],
        "shared_accounts_count": 3,
        "anomaly_score": 0.9
    }
    res = groq_service.generate_case_summary(payload)
    
    assert "executive_summary" in res
    assert "recommended_action" in res
    assert "confidence_score" in res
    assert res["confidence_score"] >= 50.0
