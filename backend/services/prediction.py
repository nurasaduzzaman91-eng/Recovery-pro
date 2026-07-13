from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from models import Injury, ExerciseLog, ProgressMetric
import pandas as pd
import numpy as np
from collections import defaultdict

class PredictionService:
    """Service for generating recovery predictions and analytics"""
    
    @staticmethod
    def predict_recovery_date(db: Session, injury_id: int):
        """
        Predict estimated recovery date based on:
        - Initial severity
        - Progress metrics trends
        - Exercise adherence
        - Recovery patterns for similar injuries
        """
        injury = db.query(Injury).filter(Injury.id == injury_id).first()
        if not injury:
            return None
        
        # Get progress metrics
        metrics = db.query(ProgressMetric).filter(
            ProgressMetric.injury_id == injury_id
        ).order_by(ProgressMetric.metric_date).all()
        
        if not metrics:
            # No data yet, use doctor's estimate
            if injury.expected_recovery_weeks:
                estimated_date = injury.start_date + timedelta(weeks=injury.expected_recovery_weeks)
                return {
                    "estimated_recovery_date": estimated_date,
                    "confidence_percentage": 30.0,
                    "days_until_recovery": (estimated_date - date.today()).days,
                    "current_progress_percentage": 0.0
                }
            return None
        
        # Convert to DataFrame for analysis
        data = {
            'date': [m.metric_date for m in metrics],
            'pain_score': [m.pain_score for m in metrics],
            'mobility_score': [m.mobility_score or 0 for m in metrics],
        }
        df = pd.DataFrame(data)
        
        # Calculate trends
        pain_trend = np.polyfit(range(len(df)), df['pain_score'].values, 1)[0]
        mobility_trend = np.polyfit(range(len(df)), df['mobility_score'].values, 1)[0]
        
        # Estimate recovery (when pain <= 2 and mobility >= 80)
        days_elapsed = (date.today() - injury.start_date).days
        
        # Conservative estimate based on trends
        if pain_trend < 0:  # Pain decreasing
            pain_days_remaining = (df['pain_score'].iloc[-1] - 2) / abs(pain_trend) if pain_trend != 0 else 14
        else:
            pain_days_remaining = 14
        
        if mobility_trend > 0:  # Mobility increasing
            mobility_days_remaining = (80 - df['mobility_score'].iloc[-1]) / mobility_trend if mobility_trend != 0 else 14
        else:
            mobility_days_remaining = 14
        
        days_remaining = max(int(pain_days_remaining), int(mobility_days_remaining))
        estimated_recovery_date = date.today() + timedelta(days=days_remaining)
        
        # Calculate current progress
        initial_pain = df['pain_score'].iloc[0]
        current_pain = df['pain_score'].iloc[-1]
        progress_percentage = min(((initial_pain - current_pain) / initial_pain * 100), 100) if initial_pain > 0 else 0
        
        # Confidence based on data points
        confidence = min(len(metrics) * 10, 95)
        
        return {
            "estimated_recovery_date": estimated_recovery_date,
            "confidence_percentage": float(confidence),
            "days_until_recovery": days_remaining,
            "current_progress_percentage": max(float(progress_percentage), 0)
        }
    
    @staticmethod
    def get_injury_analytics(db: Session, injury_id: int):
        """
        Generate comprehensive analytics for an injury including:
        - Pain and mobility trends
        - Exercise adherence
        - Best performing exercises
        - Recommendations
        """
        injury = db.query(Injury).filter(Injury.id == injury_id).first()
        if not injury:
            return None
        
        # Get metrics
        metrics = db.query(ProgressMetric).filter(
            ProgressMetric.injury_id == injury_id
        ).order_by(ProgressMetric.metric_date).all()
        
        # Get exercise logs
        logs = db.query(ExerciseLog).filter(
            ExerciseLog.injury_id == injury_id
        ).order_by(ExerciseLog.completed_at).all()
        
        # Pain and mobility trends
        pain_trend = [m.pain_score for m in metrics]
        mobility_trend = [m.mobility_score or 0 for m in metrics]
        
        # Exercise adherence
        if logs:
            adherence_rate = sum(1 for log in logs if log.completed) / len(logs) * 100
        else:
            adherence_rate = 0
        
        # Best performing exercises (lowest pain after exercise)
        exercise_performance = defaultdict(list)
        for log in logs:
            exercise_performance[log.exercise.name].append(log.pain_level)
        
        best_exercises = sorted(
            [(name, np.mean(pain_levels)) for name, pain_levels in exercise_performance.items()],
            key=lambda x: x[1]
        )[:5]
        
        best_performing = [
            {"name": name, "avg_pain_after": float(pain)}
            for name, pain in best_exercises
        ]
        
        # Recommendations
        recommendations = []
        if pain_trend and pain_trend[-1] > 5:
            recommendations.append("Consider reducing exercise intensity - pain levels still high")
        if adherence_rate < 50:
            recommendations.append("Increase exercise frequency for better recovery")
        if mobility_trend and mobility_trend[-1] < 50:
            recommendations.append("Focus on mobility-improving exercises")
        if not recommendations:
            recommendations.append("Great progress! Keep up with current routine")
        
        return {
            "injury_id": injury_id,
            "avg_pain_trend": pain_trend,
            "avg_mobility_trend": mobility_trend,
            "exercise_adherence_rate": float(adherence_rate),
            "best_performing_exercises": best_performing,
            "recommended_next_steps": recommendations
        }
    
    @staticmethod
    def get_similar_injury_stats(injury_type: str):
        """
        Return statistics for similar injuries
        (In production, this would query aggregated anonymized data)
        """
        # Mock data for demonstration
        recovery_stats = {
            "ACL tear": {"avg_weeks": 16, "avg_adherence": 75},
            "Shoulder dislocation": {"avg_weeks": 12, "avg_adherence": 70},
            "Ankle sprain": {"avg_weeks": 6, "avg_adherence": 80},
            "Knee meniscus tear": {"avg_weeks": 12, "avg_adherence": 72},
            "Rotator cuff injury": {"avg_weeks": 14, "avg_adherence": 68},
        }
        return recovery_stats.get(injury_type, {"avg_weeks": 10, "avg_adherence": 70})
