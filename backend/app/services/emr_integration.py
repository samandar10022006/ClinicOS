import httpx
from app.core.config import settings
from typing import Dict, Any


class EMRIntegration:
    def __init__(self):
        self.api_url = settings.EMR_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def sync_patient(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Bemor ma'lumotlarini EMR tizimiga yuborish"""
        if not self.api_url:
            return {"status": "mock", "message": "EMR not configured"}

        try:
            response = await self.client.post(
                f"{self.api_url}/patients",
                json=patient_data
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def get_patient_history(self, patient_id: str) -> Dict[str, Any]:
        """Bemor tarixini olish"""
        if not self.api_url:
            return {"status": "mock", "history": []}

        try:
            response = await self.client.get(
                f"{self.api_url}/patients/{patient_id}/history"
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def create_appointment(self, appointment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Uchrashuv yaratish"""
        if not self.api_url:
            return {"status": "mock", "appointment_id": "mock-123"}

        try:
            response = await self.client.post(
                f"{self.api_url}/appointments",
                json=appointment_data
            )
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}


emr_integration = EMRIntegration()