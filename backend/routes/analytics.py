from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Injury, ProgressMetric
from schemas import ProgressMetricCreate, ProgressMetricResponse, RecoveryPredictionResponse
from database import get_db
from services.prediction import PredictionService
from typing import List

router = APIRouter()

# Progress Metrics
@router.post("/metrics/{injury_id}", response_model=ProgressMetricResponse)
def create_progress_metric(
    injury_id: int,
    metric: ProgressMetricCreate,
    db: Session = Depends(get_db)
):
    """Log a progress metric for recovery tracking"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    db_metric = ProgressMetric(
        injury_id=injury_id,
        metric_date=metric.metric_date,
        mobility_score=metric.mobility_score,
        pain_score=metric.pain_score,
        exercises_completed=metric.exercises_completed,
        range_of_motion=metric.range_of_motion,
        swelling_level=metric.swelling_level,
        notes=metric.notes
    )
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/metrics/{injury_id}", response_model=List[ProgressMetricResponse])
def get_progress_metrics(injury_id: int, db: Session = Depends(get_db)):
    """Get all progress metrics for an injury"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    metrics = db.query(ProgressMetric).filter(
        ProgressMetric.injury_id == injury_id
    ).order_by(ProgressMetric.metric_date).all()
    return metrics

# Predictions & Analytics
@router.get("/predict/{injury_id}", response_model=RecoveryPredictionResponse)
def predict_recovery(injury_id: int, db: Session = Depends(get_db)):
    """Get recovery prediction for an injury"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    prediction = PredictionService.predict_recovery_date(db, injury_id)
    if not prediction:
        raise HTTPException(status_code=400, detail="Insufficient data for prediction")
    
    return {
        "injury_id": injury_id,
        **prediction
    }

@router.get("/injury-analytics/{injury_id}")
def get_injury_analytics(injury_id: int, db: Session = Depends(get_db)):
    """Get comprehensive analytics for an injury"""
    injury = db.query(Injury).filter(Injury.id == injury_id).first()
    if not injury:
        raise HTTPException(status_code=404, detail="Injury not found")
    
    analytics = PredictionService.get_injury_analytics(db, injury_id)
    if not analytics:
        raise HTTPException(status_code=400, detail="Insufficient data for analytics")
    
    return analytics

@router.get("/similar-injury-stats/{injury_type}")
def get_similar_injury_stats(injury_type: str):
    """Get recovery statistics for similar injury types"""
    stats = PredictionService.get_similar_injury_stats(injury_type)
    return {
        "injury_type": injury_type,
        "avg_recovery_weeks": stats["avg_weeks"],
        "avg_adherence_rate": stats["avg_adherence"]
    }
