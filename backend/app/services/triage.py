import pickle
import re
import os
from pathlib import Path
import joblib
import numpy as np


# Haqiqiy ML model (keyinchalik train.py bilan yaratiladi)
class TriageClassifier:
    def __init__(self):
        self.model_path = Path(__file__).resolve().parents[3] / "ai-model" / "model.pkl"
        self.vectorizer_path = Path(__file__).resolve().parents[3] / "ai-model" / "vectorizer.pkl"
        alt_model = Path("/ai-model/model.pkl")
        alt_vectorizer = Path("/ai-model/vectorizer.pkl")
        if alt_model.exists():
            self.model_path = alt_model
            self.vectorizer_path = alt_vectorizer
        self.model = None
        self.vectorizer = None
        self._load_model()

    def _load_model(self):
        if self.model_path.exists():
            self.model = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)

    def _rule_based_classify(self, text: str) -> str:
        """Fallback: qoidaviy tasniflagich"""
        text_lower = text.lower()
        urgent = ["yurak", "infarkt", "insult", "qon ketish", "nafas", "hush", "tutqanoq", "shok"]
        chronic = ["diabet", "gipertoniya", "astma", "surunkali", "doimiy", "artrit"]
        fast = ["isitma", "og'riq", "yo'tal", "bosh og'rig'i", "shikast", "yara"]

        if any(word in text_lower for word in urgent):
            return "urgent"
        elif any(word in text_lower for word in chronic):
            return "chronic"
        else:
            return "fast"

    def predict(self, text: str) -> dict:
        if self.model and self.vectorizer:
            try:
                X = self.vectorizer.transform([text])
                probs = self.model.predict_proba(X)[0]
                categories = ["urgent", "chronic", "fast"]
                pred_class = self.model.predict(X)[0]
                confidence = float(max(probs))
                return {
                    "category": pred_class,
                    "confidence": confidence,
                    "probabilities": dict(zip(categories, probs.tolist()))
                }
            except:
                pass

        # Fallback to rule-based
        category = self._rule_based_classify(text)
        return {
            "category": category,
            "confidence": 0.7,
            "probabilities": {"urgent": 0.0, "chronic": 0.0, "fast": 0.0}
        }


triage_classifier = TriageClassifier()


def classify_complaint(complaint: str) -> dict:
    return triage_classifier.predict(complaint)