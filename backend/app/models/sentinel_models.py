from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="investigator") # admin, senior_lead, investigator, auditor
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    cases_assigned = relationship("Case", back_populates="assignee")
    audit_logs = relationship("AuditLog", back_populates="actor")

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. ACC-98421
    email = Column(String(255), index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    country = Column(String(10), default="US")
    account_type = Column(String(50), default="consumer") # consumer, merchant, business
    status = Column(String(50), default="active") # active, under_review, restricted, banned
    risk_score = Column(Float, default=10.0) # 0 to 100
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="account")
    device_links = relationship("AccountDeviceLink", back_populates="account")
    cases = relationship("Case", back_populates="account")

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. DEV-83921
    fingerprint = Column(String(255), index=True, nullable=False)
    ip_address = Column(String(64), index=True)
    user_agent = Column(Text)
    is_vpn = Column(Boolean, default=False)
    is_emulator = Column(Boolean, default=False)
    first_seen = Column(DateTime, default=datetime.utcnow)
    
    account_links = relationship("AccountDeviceLink", back_populates="device")

class AccountDeviceLink(Base):
    __tablename__ = "account_device_links"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String(64), ForeignKey("accounts.id"), nullable=False)
    device_id = Column(String(64), ForeignKey("devices.id"), nullable=False)
    linked_at = Column(DateTime, default=datetime.utcnow)
    
    account = relationship("Account", back_populates="device_links")
    device = relationship("Device", back_populates="account_links")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. TXN-73910
    account_id = Column(String(64), ForeignKey("accounts.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    merchant = Column(String(255), nullable=False)
    merchant_category = Column(String(100), nullable=False)
    payment_method = Column(String(50), default="credit_card")
    card_bin = Column(String(10))
    ip_address = Column(String(64))
    location_country = Column(String(10), default="US")
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Risk & Anomaly scoring attributes
    velocity_1h = Column(Integer, default=1)
    is_foreign_ip = Column(Boolean, default=False)
    device_anomaly = Column(Boolean, default=False)
    rule_flags = Column(JSON, default=list) # e.g. ["VELOCITY_SPIKE", "NEW_DEVICE", "HIGH_AMOUNT"]
    ml_risk_score = Column(Float, default=0.0) # 0 to 100
    anomaly_score = Column(Float, default=0.0) # Isolation forest output
    is_fraud_simulated = Column(Boolean, default=False)
    
    account = relationship("Account", back_populates="transactions")
    cases = relationship("Case", back_populates="transaction")

class Case(Base):
    __tablename__ = "cases"
    
    id = Column(String(64), primary_key=True, index=True) # e.g. CASE-2024-001
    account_id = Column(String(64), ForeignKey("accounts.id"), nullable=False, index=True)
    transaction_id = Column(String(64), ForeignKey("transactions.id"), nullable=True)
    title = Column(String(255), nullable=False)
    priority = Column(String(20), default="MEDIUM") # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String(50), default="NEW") # NEW, UNDER_REVIEW, ESCALATED, RESOLVED_FRAUD, RESOLVED_FALSE_POSITIVE
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    risk_score = Column(Float, default=50.0)
    fraud_typology = Column(String(100)) # e.g. "Card Testing", "Account Takeover", "Collusion Ring"
    
    # Forensic AI outputs
    ai_summary = Column(Text, nullable=True)
    ai_recommendation = Column(Text, nullable=True)
    ai_confidence = Column(Float, default=0.0)
    evidence_bundle = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    account = relationship("Account", back_populates="cases")
    transaction = relationship("Transaction", back_populates="cases")
    assignee = relationship("User", back_populates="cases_assigned")
    audit_logs = relationship("AuditLog", back_populates="case")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(64), ForeignKey("cases.id"), nullable=True)
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False) # e.g. "STATUS_CHANGE", "NOTE_ADDED", "DECISION_BAN"
    previous_state = Column(String(100), nullable=True)
    new_state = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    case = relationship("Case", back_populates="audit_logs")
    actor = relationship("User", back_populates="audit_logs")
