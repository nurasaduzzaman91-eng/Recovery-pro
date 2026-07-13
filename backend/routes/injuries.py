from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Injury, User
from schemas import InjuryCreate, InjuryResponse, InjuryUpdate
from database import get_db

router = APIRouter()

@router.post("/{user_id}", response_model=InjuryResponse)
def create_injury(user_id: int, injury: InjuryCreate, db: Session = Depends(get_db)):
    """Create a new injury record"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_injury = Injury(
        user_id=user_id,
        injury_type=injury.injury_type,
        severity=injury.severity,
        description=injury.description,
        start_date=injury.start_date,
        expected_recovery_weeks=injury.expected_recovery_weeks
    )
    db.add(db_injury)
    db.commit()
    db.refresh(db_injury)
    return db_injury

@router.get("/{user_id}", response_model=List[InjuryResponse])
def get_user_injuries(user_id: int, db: Session = Depends(get_db)):
    """Get all injuries for a user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    injuries = db.query(Injury).filter(Injury.user_id == user_id).all()
    return injuries

@router.get("/detail/{injury_id}", response_model=InjuryResponse)
def get_injury(injury_id: int, db: Session = Depends(get_db)):
    """Get specific injury details"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    return injury

@router.put("/{injury_id}", response_model=InjuryResponse)
def update_injury(injury_id: int, injury_update: InjuryUpdate, db: Session = Depends(get_db)):
    """Update injury details"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    if injury_update.severity is not None:
        injury.severity = injury_update.severity
    if injury_update.description is not None:
        injury.description = injury_update.description
    
    db.commit()
    db.refresh(injury)
    return injury

@router.delete("/{injury_id}")
def delete_injury(injury_id: int, db: Session = Depends(get_db)):
    """Delete an injury record"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    db.delete(injury)
    db.commit()
    return {"message": "Injury deleted successfully"}
