import sys
import os

# Add the shared directory to the Python path
# Add the parent directory to the Python path to allow imports from shared
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI, HTTPException, Query, Depends, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from models import Doctor, DoctorCreate, DoctorUpdate, DoctorListResponse, DoctorResponse
from geolocation import geo_service
from database import get_db
from shared.models import Doctor as DoctorModel

# Load environment variables
load_dotenv()

app = FastAPI(title="Doctor Recommendation Service", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API Router
router = APIRouter()

# Routes
@router.get("/doctor/nearby", response_model=DoctorListResponse)
async def get_nearby_doctors_endpoint(
    lat: float = Query(..., description="User latitude"),
    lng: float = Query(..., description="User longitude"),
    max_distance: float = Query(50.0, description="Maximum distance in kilometers"),
    db: Session = Depends(get_db)
):
    """
    Get nearby doctors based on user location
    """
    try:
        # Fetch all doctors from database
        db_doctors = db.query(DoctorModel).all()
        
        # Convert to dict format for processing
        doctors = [
            {
                "doctor_id": d.doctor_id,
                "name": d.name,
                "specialization": d.specialization,
                "address": d.address,
                "latitude": float(d.latitude) if d.latitude else 0.0,
                "longitude": float(d.longitude) if d.longitude else 0.0,
                "rating": float(d.rating) if d.rating else 0.0,
                "contact": d.contact
            }
            for d in db_doctors
        ]
        
        # Get nearby doctors
        nearby_doctors = geo_service.find_nearby_doctors(doctors, lat, lng, max_distance)
        
        # Convert to Doctor objects
        doctor_objects = [
            Doctor(
                doctor_id=d["doctor_id"],
                name=d["name"],
                specialization=d["specialization"],
                address=d["address"],
                latitude=d["latitude"],
                longitude=d["longitude"],
                rating=d["rating"],
                contact=d["contact"],
                distance=d.get("distance")
            )
            for d in nearby_doctors
        ]
        
        return DoctorListResponse(
            doctors=doctor_objects,
            message=f"Found {len(doctor_objects)} doctors within {max_distance}km"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doctors: {str(e)}")

@router.get("/doctor/specialists", response_model=DoctorListResponse)
async def get_specialist_doctors(
    specialization: str = Query(..., description="Specialization to search for"),
    lat: float = Query(None, description="User latitude (optional)"),
    lng: float = Query(None, description="User longitude (optional)"),
    db: Session = Depends(get_db)
):
    """
    Get doctors by specialization
    """
    try:
        # Fetch doctors by specialization from database
        db_doctors = db.query(DoctorModel).filter(DoctorModel.specialization.ilike(f"%{specialization}%")).all()
        
        # Convert to dict format for processing
        doctors = [
            {
                "doctor_id": d.doctor_id,
                "name": d.name,
                "specialization": d.specialization,
                "address": d.address,
                "latitude": float(d.latitude) if d.latitude else 0.0,
                "longitude": float(d.longitude) if d.longitude else 0.0,
                "rating": float(d.rating) if d.rating else 0.0,
                "contact": d.contact
            }
            for d in db_doctors
        ]
        
        # If location provided, calculate distances
        if lat is not None and lng is not None:
            for doctor in doctors:
                distance = geo_service.calculate_distance(
                    lat, lng, 
                    doctor["latitude"], doctor["longitude"]
                )
                doctor["distance"] = round(distance, 2)
            
            # Sort by distance
            doctors.sort(key=lambda x: x.get("distance", float('inf')))
        
        # Convert to Doctor objects
        doctor_objects = [
            Doctor(
                doctor_id=d["doctor_id"],
                name=d["name"],
                specialization=d["specialization"],
                address=d["address"],
                latitude=d["latitude"],
                longitude=d["longitude"],
                rating=d["rating"],
                contact=d["contact"],
                distance=d.get("distance")
            )
            for d in doctors
        ]
        
        return DoctorListResponse(
            doctors=doctor_objects,
            message=f"Found {len(doctor_objects)} {specialization} specialists"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch specialists: {str(e)}")

@router.get("/doctor/{doctor_id}", response_model=DoctorResponse)
async def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Get a specific doctor by ID
    """
    try:
        # Fetch doctor from database
        db_doctor = db.query(DoctorModel).filter(DoctorModel.doctor_id == doctor_id).first()
        if not db_doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        # Convert to Doctor object
        doctor = Doctor(
            doctor_id=db_doctor.doctor_id,
            name=db_doctor.name,
            specialization=db_doctor.specialization,
            address=db_doctor.address,
            latitude=float(db_doctor.latitude) if db_doctor.latitude else 0.0,
            longitude=float(db_doctor.longitude) if db_doctor.longitude else 0.0,
            rating=float(db_doctor.rating) if db_doctor.rating else 0.0,
            contact=db_doctor.contact
        )
        
        return DoctorResponse(
            doctor=doctor,
            message="Doctor retrieved successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch doctor: {str(e)}")

@router.post("/doctor", response_model=DoctorResponse)
async def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    """
    Create a new doctor
    """
    try:
        # Create new doctor in database
        db_doctor = DoctorModel(
            name=doctor.name,
            specialization=doctor.specialization,
            address=doctor.address,
            latitude=doctor.latitude,
            longitude=doctor.longitude,
            rating=doctor.rating,
            contact=doctor.contact
        )
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        
        # Convert to Doctor object
        new_doctor = Doctor(
            doctor_id=db_doctor.doctor_id,
            name=db_doctor.name,
            specialization=db_doctor.specialization,
            address=db_doctor.address,
            latitude=float(db_doctor.latitude) if db_doctor.latitude else 0.0,
            longitude=float(db_doctor.longitude) if db_doctor.longitude else 0.0,
            rating=float(db_doctor.rating) if db_doctor.rating else 0.0,
            contact=db_doctor.contact
        )
        
        return DoctorResponse(
            doctor=new_doctor,
            message="Doctor created successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create doctor: {str(e)}")

@router.put("/doctor/{doctor_id}", response_model=DoctorResponse)
async def update_doctor(doctor_id: int, doctor_update: DoctorUpdate, db: Session = Depends(get_db)):
    """
    Update a doctor
    """
    try:
        # Fetch doctor from database
        db_doctor = db.query(DoctorModel).filter(DoctorModel.doctor_id == doctor_id).first()
        if not db_doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        # Update doctor fields
        if doctor_update.name is not None:
            db_doctor.name = doctor_update.name
        if doctor_update.specialization is not None:
            db_doctor.specialization = doctor_update.specialization
        if doctor_update.address is not None:
            db_doctor.address = doctor_update.address
        if doctor_update.latitude is not None:
            db_doctor.latitude = doctor_update.latitude
        if doctor_update.longitude is not None:
            db_doctor.longitude = doctor_update.longitude
        if doctor_update.rating is not None:
            db_doctor.rating = doctor_update.rating
        if doctor_update.contact is not None:
            db_doctor.contact = doctor_update.contact
        
        db.commit()
        db.refresh(db_doctor)
        
        # Convert to Doctor object
        updated_doctor = Doctor(
            doctor_id=db_doctor.doctor_id,
            name=db_doctor.name,
            specialization=db_doctor.specialization,
            address=db_doctor.address,
            latitude=float(db_doctor.latitude) if db_doctor.latitude else 0.0,
            longitude=float(db_doctor.longitude) if db_doctor.longitude else 0.0,
            rating=float(db_doctor.rating) if db_doctor.rating else 0.0,
            contact=db_doctor.contact
        )
        
        return DoctorResponse(
            doctor=updated_doctor,
            message="Doctor updated successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update doctor: {str(e)}")

@router.delete("/doctor/{doctor_id}", response_model=dict)
async def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """
    Delete a doctor
    """
    try:
        # Fetch doctor from database
        db_doctor = db.query(DoctorModel).filter(DoctorModel.doctor_id == doctor_id).first()
        if not db_doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        
        # Delete doctor
        db.delete(db_doctor)
        db.commit()
        
        return {"message": f"Doctor {doctor_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete doctor: {str(e)}")

@router.post("/notes", response_model=dict)
async def create_session_note(note_data: dict):
    """
    Create a new therapy session note
    """
    try:
        from shared.therapy_notes import therapy_notes_service, SessionNote
        
        # Create note
        note = SessionNote(**note_data)
        created_note = therapy_notes_service.create_note(note)
        
        return {
            "note": created_note.dict(),
            "message": "Session note created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create session note: {str(e)}")

@router.get("/notes/client/{client_id}", response_model=dict)
async def get_client_notes(client_id: int):
    """
    Get all notes for a client
    """
    try:
        from shared.therapy_notes import therapy_notes_service
        
        notes = therapy_notes_service.get_client_notes(client_id)
        
        return {
            "notes": [note.dict() for note in notes],
            "count": len(notes)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch client notes: {str(e)}")

@router.get("/notes/summary/{client_id}", response_model=dict)
async def get_client_summary(client_id: int):
    """
    Get therapy summary for a client
    """
    try:
        from shared.therapy_notes import therapy_notes_service
        
        summary = therapy_notes_service.get_session_summary(client_id)
        
        return {
            "summary": summary.dict(),
            "message": "Summary generated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

# Medication Routes
from models import Medication, MedicationCreate, MedicationUpdate, MedicationListResponse, MedicationResponse
from shared.models import Medication as MedicationModel

@router.get("/medications/user/{user_id}", response_model=MedicationListResponse)
async def get_user_medications(user_id: int, db: Session = Depends(get_db)):
    """
    Get all medications for a specific user
    """
    try:
        db_meds = db.query(MedicationModel).filter(MedicationModel.user_id == user_id).all()
        
        medications = [
            Medication(
                med_id=m.med_id,
                user_id=m.user_id,
                name=m.name,
                dosage=m.dosage,
                frequency=m.frequency,
                time=m.time,
                taken=bool(m.taken),
                color=m.color
            ) for m in db_meds
        ]
        
        return MedicationListResponse(
            medications=medications,
            message=f"Found {len(medications)} medications"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch medications: {str(e)}")

@router.post("/medications", response_model=MedicationResponse)
async def create_medication(medication: MedicationCreate, db: Session = Depends(get_db)):
    """
    Add a new medication
    """
    try:
        db_med = MedicationModel(
            user_id=medication.user_id,
            name=medication.name,
            dosage=medication.dosage,
            frequency=medication.frequency,
            time=medication.time,
            taken=0,
            color=medication.color
        )
        db.add(db_med)
        db.commit()
        db.refresh(db_med)
        
        new_med = Medication(
            med_id=db_med.med_id,
            user_id=db_med.user_id,
            name=db_med.name,
            dosage=db_med.dosage,
            frequency=db_med.frequency,
            time=db_med.time,
            taken=bool(db_med.taken),
            color=db_med.color
        )
        
        return MedicationResponse(
            medication=new_med,
            message="Medication added successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add medication: {str(e)}")

@router.put("/medications/{med_id}", response_model=MedicationResponse)
async def update_medication(med_id: int, med_update: MedicationUpdate, db: Session = Depends(get_db)):
    """
    Update a medication (e.g., mark as taken)
    """
    try:
        db_med = db.query(MedicationModel).filter(MedicationModel.med_id == med_id).first()
        if not db_med:
            raise HTTPException(status_code=404, detail="Medication not found")
        
        if med_update.taken is not None:
            db_med.taken = 1 if med_update.taken else 0
        if med_update.name is not None:
            db_med.name = med_update.name
        if med_update.dosage is not None:
            db_med.dosage = med_update.dosage
        if med_update.frequency is not None:
            db_med.frequency = med_update.frequency
        if med_update.time is not None:
            db_med.time = med_update.time
        if med_update.color is not None:
            db_med.color = med_update.color
            
        db.commit()
        db.refresh(db_med)
        
        updated_med = Medication(
            med_id=db_med.med_id,
            user_id=db_med.user_id,
            name=db_med.name,
            dosage=db_med.dosage,
            frequency=db_med.frequency,
            time=db_med.time,
            taken=bool(db_med.taken),
            color=db_med.color
        )
        
        return MedicationResponse(
            medication=updated_med,
            message="Medication updated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update medication: {str(e)}")

@router.delete("/medications/{med_id}", response_model=dict)
async def delete_medication(med_id: int, db: Session = Depends(get_db)):
    """
    Delete a medication
    """
    try:
        db_med = db.query(MedicationModel).filter(MedicationModel.med_id == med_id).first()
        if not db_med:
            raise HTTPException(status_code=404, detail="Medication not found")
            
        db.delete(db_med)
        db.commit()
        
        return {"message": "Medication deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete medication: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Doctor Recommendation Service is running"}

# Include the router with prefix
app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)