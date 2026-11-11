import json
import logging
from typing import Dict, Any, Optional
from groq import Groq
from backend.app.core.config import settings

logger = logging.getLogger("sentinel.groq")

class GroqForensicService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.client = None
        if self.api_key and not self.api_key.startswith("your_"):
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")

    def generate_case_summary(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes case facts, anomaly flags, and graph linkage into a forensic investigation report.
        Uses primary model (LLaMA 3.3 70B) with automatic failover to LLaMA 3.1 8B, and offline mock fallback.
        """
        prompt = self._build_forensic_prompt(case_data)
        
        # 1. Try Primary Model: LLaMA 3.3 70B
        if self.client:
            try:
                return self._call_groq(prompt, model=settings.GROQ_PRIMARY_MODEL)
            except Exception as e_primary:
                logger.warning(f"Groq primary model failed ({e_primary}). Retrying with fallback {settings.GROQ_FALLBACK_MODEL}...")
                try:
                    return self._call_groq(prompt, model=settings.GROQ_FALLBACK_MODEL)
                except Exception as e_fallback:
                    logger.error(f"Groq fallback model also failed: {e_fallback}")
        
        # 2. Local Deterministic Mock Fallback (Guarantees zero crashes during demos/interviews)
        return self._generate_local_fallback(case_data)

    def _call_groq(self, prompt: str, model: str) -> Dict[str, Any]:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are SENTINEL's Lead Trust & Safety AI Forensic Analyst. "
                        "Evaluate the transaction signals, rule breaches, and graph entity linkages. "
                        "Return your findings STRICTLY as valid JSON matching this schema:\n"
                        "{\n"
                        '  "executive_summary": "1-2 sentence concise executive synthesis.",\n'
                        '  "anomaly_breakdown": ["bullet 1", "bullet 2", "bullet 3"],\n'
                        '  "fraud_typology": "e.g. Account Takeover / Card Testing / Syndicate Ring",\n'
                        '  "recommended_action": "BAN_ACCOUNT" | "RESTRICT_PAYMENTS" | "REQUEST_IDV" | "CLOSE_AS_FALSE_POSITIVE",\n'
                        '  "confidence_score": 85,\n'
                        '  "justification": "Detailed evidence justification for regulatory audit compliance."\n'
                        "}"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        response_text = chat_completion.choices[0].message.content
        return json.loads(response_text)

    def _build_forensic_prompt(self, data: Dict[str, Any]) -> str:
        return f"""
EVALUATION DOSSIER:
- Case ID: {data.get('case_id')}
- Account ID: {data.get('account_id')}
- Account Age: {data.get('account_age_days', 42)} days
- Overall Risk Score: {data.get('risk_score', 0)} / 100
- Recent Transaction Amount: ${data.get('amount', 0):.2f} {data.get('currency', 'USD')}
- Merchant & Category: {data.get('merchant')} ({data.get('merchant_category')})
- Device Fingerprint: {data.get('device_id')}
- Associated IP: {data.get('ip_address')} (VPN Detected: {data.get('is_vpn', False)})
- Rule Breaches Detected: {', '.join(data.get('rule_flags', []))}
- Shared Device Cluster Size: {data.get('shared_accounts_count', 1)} accounts linked to this device
- Anomaly Isolation Score: {data.get('anomaly_score', 0):.3f}
"""

    def _generate_local_fallback(self, data: Dict[str, Any]) -> Dict[str, Any]:
        risk = data.get("risk_score", 50)
        rules = data.get("rule_flags", [])
        shared = data.get("shared_accounts_count", 1)
        
        action = "REQUEST_IDV"
        typology = "High-Velocity Behavioral Anomaly"
        
        if shared > 2 or "COLLUSION_RING" in rules:
            typology = "Syndicate / Collusion Ring"
            action = "BAN_ACCOUNT"
        elif "VELOCITY_SPIKE" in rules and risk > 75:
            typology = "Card Testing Attack"
            action = "RESTRICT_PAYMENTS"
        elif risk < 35:
            action = "CLOSE_AS_FALSE_POSITIVE"

        return {
            "executive_summary": f"Automated risk profile indicates elevated exposure ({risk:.1f}/100) triggered by {len(rules)} distinct behavioral flags.",
            "anomaly_breakdown": [
                f"Flagged under rule set: {', '.join(rules) if rules else 'Heuristic velocity threshold'}",
                f"Device linked to {shared} distinct entity profile(s)",
                f"Observed anomalous amount of ${data.get('amount', 0):.2f} at {data.get('merchant', 'Unknown')}"
            ],
            "fraud_typology": typology,
            "recommended_action": action,
            "confidence_score": min(95.0, max(50.0, risk + 5.0)),
            "justification": f"Audit recommendation generated in compliance with Risk Policy Tier 2. Entity matches known {typology} characteristics with high anomaly divergence."
        }

groq_service = GroqForensicService()
