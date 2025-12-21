from pydantic import BaseModel
from typing import List, Optional

class Doctor(BaseModel):
    doctor_id: int
    name: str
    specialization: str
    address: str
    latitude: float
    longitude: float
    rating: float
    contact: str
    distance: Optional[float] = None

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    address: str
    latitude: float
    longitude: float
    rating: float
    contact: str

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[float] = None
from pydantic import BaseModel
from typing import List, Optional

class Doctor(BaseModel):
    doctor_id: int
    name: str
    specialization: str
    address: str
    latitude: float
    longitude: float
    rating: float
    contact: str
    distance: Optional[float] = None

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    address: str
    latitude: float
    longitude: float
    rating: float
    contact: str

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rating: Optional[float] = None
    contact: Optional[str] = None

class DoctorListResponse(BaseModel):
    doctors: List[Doctor]
    message: str

class DoctorResponse(BaseModel):
    doctor: Doctor
    message: str

class Medication(BaseModel):
    med_id: int
    user_id: int
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    time: Optional[str] = None
    taken: bool
    color: str

class MedicationCreate(BaseModel):
    user_id: int
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    time: Optional[str] = None
    color: Optional[str] = "neon-purple"

class MedicationUpdate(BaseModel):
    taken: Optional[bool] = None
    name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    time: Optional[str] = None
    color: Optional[str] = None

class MedicationListResponse(BaseModel):
    medications: List[Medication]
    message: str

class MedicationResponse(BaseModel):
    medication: Medication
    message: str