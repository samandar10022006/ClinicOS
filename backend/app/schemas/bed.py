from pydantic import BaseModel
from typing import Optional


class BedCreate(BaseModel):
    room_number: str
    ward: str
    category: str
    hospital_id: Optional[int] = 1


class BedResponse(BaseModel):
    id: int
    room_number: str
    ward: str
    category: str
    is_available: bool
    hospital_id: Optional[int] = None

    class Config:
        from_attributes = True
