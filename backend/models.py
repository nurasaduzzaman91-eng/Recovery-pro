from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, Float
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    injuries = relationship("Injury", back_populates="user", cascade="all, delete-orphan")
    exercise_logs = relationship("ExerciseLog", back_populates="user", cascade="all, delete-orphan")

class Injury(Base):
    __tablename__ = "injuries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    injury_type = Column(String, index=True, nullable=False)  # e.g., "ACL tear", "Shoulder dislocation"
    severity = Column(Integer, nullable=False)  # 1-10
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    expected_recovery_weeks = Column(Integer)  # Doctor's estimate
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="injuries")
    exercise_logs = relationship("ExerciseLog", back_populates="injury", cascade="all, delete-orphan")
    progress_metrics = relationship("ProgressMetric", back_populates="injury", cascade="all, delete-orphan")

class ExerciseTemplate(Base):
    __tablename__ = "exercise_templates"
    
    id = Column(Integer, primary_key=True, index=True)
    injury_type = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    recommended_frequency = Column(String)  # e.g., "3x per week"
    repetitions = Column(Integer)
    sets = Column(Integer)
    duration_minutes = Column(Integer)
    difficulty_level = Column(String)  # beginner, intermediate, advanced
    created_at = Column(DateTime, default=datetime.utcnow)
    
    exercise_logs = relationship("ExerciseLog", back_populates="exercise")

class ExerciseLog(Base):
    __tablename__ = "exercise_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    injury_id = Column(Integer, ForeignKey("injuries.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise_templates.id"), nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    pain_level = Column(Integer, nullable=False)  # 1-10
    difficulty = Column(Integer)  # 1-10
    notes = Column(Text)
    completed = Column(Integer, default=1)  # 0 or 1
    
    user = relationship("User", back_populates="exercise_logs")
    injury = relationship("Injury", back_populates="exercise_logs")
    exercise = relationship("ExerciseTemplate", back_populates="exercise_logs")

class ProgressMetric(Base):
    __tablename__ = "progress_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    injury_id = Column(Integer, ForeignKey("injuries.id"), nullable=False)
    metric_date = Column(Date, nullable=False)
    mobility_score = Column(Integer)  # 0-100
    pain_score = Column(Integer)  # 1-10
    exercises_completed = Column(Integer)  # Count of exercises done that day
    range_of_motion = Column(String)  # e.g., "30 degrees"
    swelling_level = Column(Integer)  # 1-10
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    injury = relationship("Injury", back_populates="progress_metrics")
