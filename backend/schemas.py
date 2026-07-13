from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Exercise Template Schemas
class ExerciseTemplateCreate(BaseModel):
    injury_type: str
    name: str
    description: str
    recommended_frequency: str
    repetitions: int
    sets: int
    duration_minutes: int
    difficulty_level: str

class ExerciseTemplateResponse(BaseModel):
    id: int
    injury_type: str
    name: str
    description: str
    recommended_frequency: str
    repetitions: int
    sets: int
    duration_minutes: int
    difficulty_level: str
    
    class Config:
        from_attributes = True

# Injury Schemas
class InjuryCreate(BaseModel):
    injury_type: str
    severity: int
    description: str
    start_date: date
    expected_recovery_weeks: Optional[int] = None

class InjuryUpdate(BaseModel):
    severity: Optional[int] = None
    description: Optional[str] = None

class InjuryResponse(BaseModel):
    id: int
    user_id: int
    injury_type: str
    severity: int
    description: str
    start_date: date
    expected_recovery_weeks: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Exercise Log Schemas
class ExerciseLogCreate(BaseModel):
    exercise_id: int
    pain_level: int
    difficulty: Optional[int] = None
    notes: Optional[str] = None

class ExerciseLogResponse(BaseModel):
    id: int
    user_id: int
    injury_id: int
    exercise_id: int
    completed_at: datetime
    pain_level: int
    difficulty: Optional[int]
    notes: Optional[str]
    completed: int
    
    class Config:
        from_attributes = True

# Progress Metric Schemas
class ProgressMetricCreate(BaseModel):
    metric_date: date
    mobility_score: Optional[int] = None
    pain_score: int
    exercises_completed: int
    range_of_motion: Optional[str] = None
    swelling_level: Optional[int] = None
    notes: Optional[str] = None

class ProgressMetricResponse(BaseModel):
    id: int
    injury_id: int
    metric_date: date
    mobility_score: Optional[int]
    pain_score: int
    exercises_completed: int
    range_of_motion: Optional[str]
    swelling_level: Optional[int]
    notes: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Analytics Schemas
class RecoveryPredictionResponse(BaseModel):
    injury_id: int
    estimated_recovery_date: date
    confidence_percentage: float
    days_until_recovery: int
    current_progress_percentage: float

class InjuryAnalyticsResponse(BaseModel):
    injury_id: int
    avg_pain_trend: List[float]
    avg_mobility_trend: List[float]
    exercise_adherence_rate: float
    best_performing_exercises: List[dict]
    recommended_next_steps: List[str]
