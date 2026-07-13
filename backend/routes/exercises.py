from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import ExerciseTemplate, ExerciseLog, Injury
from schemas import (
    ExerciseTemplateCreate, ExerciseTemplateResponse,
    ExerciseLogCreate, ExerciseLogResponse
)
from database import get_db

router = APIRouter()

# Exercise Templates
@router.post("/templates", response_model=ExerciseTemplateResponse)
def create_exercise_template(exercise: ExerciseTemplateCreate, db: Session = Depends(get_db)):
    """Create a new exercise template"""
    db_exercise = ExerciseTemplate(
        injury_type=exercise.injury_type,
        name=exercise.name,
        description=exercise.description,
        recommended_frequency=exercise.recommended_frequency,
        repetitions=exercise.repetitions,
        sets=exercise.sets,
        duration_minutes=exercise.duration_minutes,
        difficulty_level=exercise.difficulty_level
    )
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

@router.get("/templates/{injury_type}", response_model=List[ExerciseTemplateResponse])
def get_exercises_for_injury(injury_type: str, db: Session = Depends(get_db)):
    """Get exercise templates for a specific injury type"""
    exercises = db.query(ExerciseTemplate).filter(
        ExerciseTemplate.injury_type == injury_type
    ).all()
    return exercises

@router.get("/templates", response_model=List[ExerciseTemplateResponse])
def get_all_exercise_templates(db: Session = Depends(get_db)):
    """Get all exercise templates"""
    return db.query(ExerciseTemplate).all()

# Exercise Logs
@router.post("/logs/{injury_id}", response_model=ExerciseLogResponse)
def log_exercise(
    injury_id: int,
    user_id: int,
    exercise_log: ExerciseLogCreate,
    db: Session = Depends(get_db)
):
    """Log a completed exercise"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    exercise = db.query(ExerciseTemplate).filter(
        ExerciseTemplate.id == exercise_log.exercise_id
    ).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    db_log = ExerciseLog(
        user_id=user_id,
        injury_id=injury_id,
        exercise_id=exercise_log.exercise_id,
        pain_level=exercise_log.pain_level,
        difficulty=exercise_log.difficulty,
        notes=exercise_log.notes,
        completed=1
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/logs/{injury_id}", response_model=List[ExerciseLogResponse])
def get_exercise_logs(injury_id: int, db: Session = Depends(get_db)):
    """Get all exercise logs for an injury"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    logs = db.query(ExerciseLog).filter(
        ExerciseLog.injury_id == injury_id
    ).order_by(ExerciseLog.completed_at.desc()).all()
    return logs

@router.get("/logs/detail/{log_id}", response_model=ExerciseLogResponse)
def get_exercise_log(log_id: int, db: Session = Depends(get_db)):
    """Get specific exercise log"""
    log = db.query(ExerciseLog).filter(ExerciseLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Exercise log not found")
    return log

@router.delete("/logs/{log_id}")
def delete_exercise_log(log_id: int, db: Session = Depends(get_db)):
    """Delete an exercise log"""
    log = db.query(ExerciseLog).filter(ExerciseLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Exercise log not found")
    
    db.delete(log)
    db.commit()
    return {"message": "Exercise log deleted successfully"}
