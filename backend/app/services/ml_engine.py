import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression

class MLEngine:
    def __init__(self):
        # Isolation Forest for unsupervised anomaly detection
        self.iso_forest = IsolationForest(
            n_estimators=100,
            contamination=0.08, # Expect ~8% anomaly rate
            random_state=42
        )
        self.is_fitted = False

    def train_baseline_models(self, transactions: List[Dict[str, Any]]):
        """
        Trains Isolation Forest and calculates baseline risk scoring models on transaction batches.
        """
        if not transactions or len(transactions) < 20:
            return
            
        df = pd.DataFrame(transactions)
        features = self._extract_features(df)
        
        self.iso_forest.fit(features)
        self.is_fitted = True

    def score_transaction(self, txn_dict: Dict[str, Any]) -> Tuple[float, float, List[str]]:
        """
        Calculates:
        1. Isolation Forest Anomaly Score (0 to 1, where 1 is highly anomalous)
        2. Consolidated Risk Score (0 to 100)
        3. Triggered Rule Flags
        """
        amount = float(txn_dict.get("amount", 0))
        velocity = int(txn_dict.get("velocity_1h", 1))
        is_foreign = bool(txn_dict.get("is_foreign_ip", False))
        is_vpn = bool(txn_dict.get("is_vpn", False))
        device_anomaly = bool(txn_dict.get("device_anomaly", False))
        
        rule_flags = []
        base_risk = 5.0
        
        # Rule Breaches
        if amount > 1500:
            rule_flags.append("HIGH_TRANSACTION_VALUE")
            base_risk += 25
        elif amount > 500:
            base_risk += 10
            
        if velocity >= 5:
            rule_flags.append("VELOCITY_SPIKE_1H")
            base_risk += 35
        elif velocity >= 3:
            rule_flags.append("ELEVATED_VELOCITY")
            base_risk += 15
            
        if is_foreign and is_vpn:
            rule_flags.append("GEO_IP_VPN_MISMATCH")
            base_risk += 30
        elif is_vpn:
            rule_flags.append("ANONYMOUS_PROXY_DETECTED")
            base_risk += 15
            
        if device_anomaly:
            rule_flags.append("DEVICE_FINGERPRINT_DRIFT")
            base_risk += 25

        # Isolation forest scoring
        feature_vector = np.array([[amount, velocity, int(is_foreign), int(is_vpn), int(device_anomaly)]])
        
        if self.is_fitted:
            raw_iso_score = self.iso_forest.decision_function(feature_vector)[0]
            # Normalize to 0..1 scale (lower decision function = more anomalous)
            anomaly_score = float(np.clip(0.5 - raw_iso_score, 0.0, 1.0))
        else:
            anomaly_score = 0.85 if len(rule_flags) >= 2 else (0.4 if len(rule_flags) == 1 else 0.05)

        # Composite risk score weighted by rules and ML anomaly
        final_risk = float(np.clip(base_risk * 0.6 + (anomaly_score * 100) * 0.4, 0.0, 100.0))
        
        return round(anomaly_score, 3), round(final_risk, 1), rule_flags

    def _extract_features(self, df: pd.DataFrame) -> np.ndarray:
        amount = df["amount"].fillna(0).values
        velocity = df["velocity_1h"].fillna(1).values
        is_foreign = df["is_foreign_ip"].astype(int).values
        is_vpn = df["is_vpn"].astype(int).values if "is_vpn" in df else np.zeros(len(df))
        device_anomaly = df["device_anomaly"].astype(int).values if "device_anomaly" in df else np.zeros(len(df))
        
        return np.column_stack([amount, velocity, is_foreign, is_vpn, device_anomaly])

ml_engine = MLEngine()
