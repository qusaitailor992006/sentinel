import random
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import Session
from backend.app.models.sentinel_models import User, Account, Device, AccountDeviceLink, Transaction, Case, AuditLog
from backend.app.services.ml_engine import ml_engine
from backend.app.services.groq_service import groq_service

fake = Faker()
Faker.seed(42)
random.seed(42)

MERCHANTS = [
    ("Stripe Payments", "payment_gateway"),
    ("Amazon Marketplace", "ecommerce"),
    ("Apple Store Online", "electronics"),
    ("Steam Gaming", "digital_goods"),
    ("Uber Technologies", "rideshare"),
    ("Binance US", "crypto_exchange"),
    ("Airbnb Booking", "travel"),
    ("BestBuy Electronics", "retail"),
    ("DoorDash Deliveries", "food_delivery"),
    ("Nike Direct", "apparel")
]

class SyntheticDataGenerator:
    def seed_initial_platform_data(self, db: Session, num_accounts: int = 100, num_txns: int = 600):
        """
        Seeds initial demo dataset with:
        1. Default analysts & investigators
        2. Clean accounts & normal traffic
        3. Deliberate fraud typologies:
           - Card Testing / Velocity spikes
           - High-value Account Takeover (ATO)
           - Device Sharing Fraud Ring (Syndicate)
        """
        if db.query(User).count() > 0:
            return # Already seeded

        # 1. Seed Analysts
        lead_analyst = User(
            email="lead.analyst@sentinel.internal",
            hashed_password="hashed_demo_pw",
            full_name="Sarah Chen (Lead Fraud Investigator)",
            role="senior_lead"
        )
        analyst_2 = User(
            email="alex.kumar@sentinel.internal",
            hashed_password="hashed_demo_pw",
            full_name="Alex Kumar (Risk Analyst)",
            role="investigator"
        )
        db.add_all([lead_analyst, analyst_2])
        db.commit()

        # 2. Seed Devices
        devices = []
        for i in range(40):
            d = Device(
                id=f"DEV-{random.randint(10000, 99999)}",
                fingerprint=f"fp_{fake.sha256()[:16]}",
                ip_address=fake.ipv4(),
                user_agent=fake.user_agent(),
                is_vpn=random.random() < 0.15,
                is_emulator=random.random() < 0.05
            )
            devices.append(d)
        db.add_all(devices)
        db.commit()

        # 3. Seed Accounts
        accounts = []
        for i in range(num_accounts):
            acc = Account(
                id=f"ACC-{1000 + i}",
                email=fake.email(),
                full_name=fake.name(),
                country=random.choice(["US", "CA", "GB", "DE", "IN", "SG"]),
                status="active",
                risk_score=random.uniform(5.0, 25.0)
            )
            accounts.append(acc)
        db.add_all(accounts)
        db.commit()

        # 4. Link Accounts to Devices (Normal + Syndicate Cluster)
        # Normal 1-to-1 or 1-to-2 links
        for acc in accounts[:-5]:
            chosen_dev = random.choice(devices[:-3])
            link = AccountDeviceLink(account_id=acc.id, device_id=chosen_dev.id)
            db.add(link)

        # Deliberate Collusion Ring (4 accounts sharing 1 single emulator device)
        syndicate_device = devices[-1]
        syndicate_device.is_vpn = True
        syndicate_device.is_emulator = True
        
        syndicate_accounts = accounts[-5:]
        for s_acc in syndicate_accounts:
            s_acc.risk_score = random.uniform(78.0, 94.0)
            s_acc.status = "under_review"
            link = AccountDeviceLink(account_id=s_acc.id, device_id=syndicate_device.id)
            db.add(link)
        db.commit()

        # 5. Seed Transactions with Scored Fraud Scenarios
        transactions = []
        now = datetime.utcnow()
        
        # A. Normal baseline transactions
        for i in range(num_txns):
            acc = random.choice(accounts[:-5])
            merchant_name, category = random.choice(MERCHANTS)
            amount = round(random.lognormvariate(3.2, 0.8), 2) # realistic log-normal retail amounts
            is_foreign = random.random() < 0.05
            
            txn_dict = {
                "amount": amount,
                "velocity_1h": random.randint(1, 2),
                "is_foreign_ip": is_foreign,
                "is_vpn": False,
                "device_anomaly": False
            }
            anomaly_score, risk_score, rule_flags = ml_engine.score_transaction(txn_dict)
            
            t = Transaction(
                id=f"TXN-{random.randint(100000, 999999)}",
                account_id=acc.id,
                amount=amount,
                currency="USD",
                merchant=merchant_name,
                merchant_category=category,
                payment_method=random.choice(["credit_card", "debit_card", "apple_pay"]),
                ip_address=fake.ipv4(),
                timestamp=now - timedelta(minutes=random.randint(5, 4320)),
                velocity_1h=txn_dict["velocity_1h"],
                is_foreign_ip=is_foreign,
                device_anomaly=False,
                rule_flags=rule_flags,
                ml_risk_score=risk_score,
                anomaly_score=anomaly_score,
                is_fraud_simulated=False
            )
            transactions.append(t)
            
        # B. Fraud Scenario 1: High-Velocity Card Testing Attack (ACC-1010)
        card_tester = accounts[10]
        card_tester.status = "under_review"
        card_tester.risk_score = 88.5
        for v in range(6):
            txn_dict = {
                "amount": round(random.uniform(2.0, 9.99), 2),
                "velocity_1h": 8,
                "is_foreign_ip": True,
                "is_vpn": True,
                "device_anomaly": True
            }
            anomaly_score, risk_score, rule_flags = ml_engine.score_transaction(txn_dict)
            t = Transaction(
                id=f"TXN-TEST-{v+100}",
                account_id=card_tester.id,
                amount=txn_dict["amount"],
                currency="USD",
                merchant="Apple Store Online",
                merchant_category="digital_goods",
                payment_method="credit_card",
                ip_address="185.220.101.5",
                timestamp=now - timedelta(minutes=15 - v*2),
                velocity_1h=8,
                is_foreign_ip=True,
                device_anomaly=True,
                rule_flags=rule_flags,
                ml_risk_score=risk_score,
                anomaly_score=anomaly_score,
                is_fraud_simulated=True
            )
            transactions.append(t)

        # C. Fraud Scenario 2: High Value Account Takeover (ACC-1025)
        ato_account = accounts[25]
        ato_account.status = "under_review"
        ato_account.risk_score = 92.0
        txn_dict = {
            "amount": 4850.00,
            "velocity_1h": 4,
            "is_foreign_ip": True,
            "is_vpn": True,
            "device_anomaly": True
        }
        anomaly_score, risk_score, rule_flags = ml_engine.score_transaction(txn_dict)
        ato_txn = Transaction(
            id="TXN-ATO-9901",
            account_id=ato_account.id,
            amount=4850.00,
            currency="USD",
            merchant="Binance US",
            merchant_category="crypto_exchange",
            payment_method="wire_transfer",
            ip_address="194.26.29.112",
            timestamp=now - timedelta(minutes=45),
            velocity_1h=4,
            is_foreign_ip=True,
            device_anomaly=True,
            rule_flags=rule_flags,
            ml_risk_score=risk_score,
            anomaly_score=anomaly_score,
            is_fraud_simulated=True
        )
        transactions.append(ato_txn)

        db.add_all(transactions)
        db.commit()

        # 6. Seed Investigation Cases for the Incidents
        # Case 1: Card Testing Case
        case_1 = Case(
            id="CASE-2024-001",
            account_id=card_tester.id,
            transaction_id=f"TXN-TEST-100",
            title=f"Rapid Automated Card Testing Velocity Spike ({card_tester.full_name})",
            priority="HIGH",
            status="UNDER_REVIEW",
            assigned_to_id=lead_analyst.id,
            risk_score=88.5,
            fraud_typology="Card Testing Attack",
            evidence_bundle={
                "velocity_per_min": 1.2,
                "total_attempts": 6,
                "ip_origin": "Tor Exit Node",
                "risk_flags": ["VELOCITY_SPIKE_1H", "ANONYMOUS_PROXY_DETECTED", "DEVICE_FINGERPRINT_DRIFT"]
            }
        )
        
        # Case 2: Crypto ATO Case
        case_2 = Case(
            id="CASE-2024-002",
            account_id=ato_account.id,
            transaction_id=ato_txn.id,
            title=f"High-Value Account Takeover at Crypto Exchange ({ato_account.full_name})",
            priority="CRITICAL",
            status="NEW",
            risk_score=92.0,
            fraud_typology="Account Takeover (ATO)",
            evidence_bundle={
                "amount": 4850.00,
                "destination": "Binance US",
                "risk_flags": ["HIGH_TRANSACTION_VALUE", "GEO_IP_VPN_MISMATCH", "DEVICE_FINGERPRINT_DRIFT"]
            }
        )

        # Case 3: Device Sharing Syndicate Case
        case_3 = Case(
            id="CASE-2024-003",
            account_id=syndicate_accounts[0].id,
            title=f"Multi-Account Device Sharing Syndicate Cluster ({len(syndicate_accounts)} entities)",
            priority="CRITICAL",
            status="NEW",
            risk_score=94.2,
            fraud_typology="Syndicate Ring",
            evidence_bundle={
                "shared_device": syndicate_device.id,
                "linked_accounts": [s.id for s in syndicate_accounts],
                "emulator_detected": True,
                "risk_flags": ["COLLUSION_RING", "EMULATOR_DETECTED", "MULTI_ACCOUNTING"]
            }
        )

        db.add_all([case_1, case_2, case_3])
        db.commit()

        # Generate AI Forensic Summary for Case 1
        summary_payload = {
            "case_id": case_1.id,
            "account_id": card_tester.id,
            "risk_score": case_1.risk_score,
            "amount": 9.99,
            "merchant": "Apple Store Online",
            "merchant_category": "digital_goods",
            "device_id": devices[0].id,
            "ip_address": "185.220.101.5",
            "is_vpn": True,
            "rule_flags": ["VELOCITY_SPIKE_1H", "ANONYMOUS_PROXY_DETECTED", "DEVICE_FINGERPRINT_DRIFT"],
            "shared_accounts_count": 1,
            "anomaly_score": 0.88
        }
        forensic_res = groq_service.generate_case_summary(summary_payload)
        case_1.ai_summary = forensic_res.get("executive_summary")
        case_1.ai_recommendation = forensic_res.get("recommended_action")
        case_1.ai_confidence = forensic_res.get("confidence_score", 85.0)

        # Audit log for case 1
        audit = AuditLog(
            case_id=case_1.id,
            actor_id=lead_analyst.id,
            action="CASE_CLAIMED",
            previous_state="NEW",
            new_state="UNDER_REVIEW",
            notes="Case escalated due to velocity spike and proxy usage."
        )
        db.add(audit)
        db.commit()

synthetic_generator = SyntheticDataGenerator()
