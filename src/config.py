import os
from typing import Dict, List

class Config:
    # Security settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")
    
    # CORS settings
    CORS_HEADERS = 'Content-Type'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Participant limits
    MIN_PARTICIPANTS = 10  # Minimum for statistical significance
    MAX_PARTICIPANTS = 10000  # Maximum for performance constraints
    
    # Scoring weights and thresholds (matching frontend)
    DIMENSION_WEIGHTS: Dict[str, float] = {
        "Accuracy": 0.25,
        "Clarity": 0.20,
        "Depth": 0.20, 
        "Ethics": 0.20,
        "Engagement": 0.15
    }
    
    SCORE_THRESHOLDS: Dict[str, float] = {
        "excellent": 4.5,
        "good": 3.5,
        "acceptable": 2.5,
        "poor": 1.5
    }
    
    # Validate configuration
    @classmethod
    def validate(cls) -> None:
        """Validate configuration settings"""
        # Validate dimension weights sum to 1.0
        if not abs(sum(cls.DIMENSION_WEIGHTS.values()) - 1.0) < 0.0001:
            raise ValueError("Dimension weights must sum to 1.0")
            
        # Validate participant limits
        if cls.MIN_PARTICIPANTS < 1:
            raise ValueError("MIN_PARTICIPANTS must be positive")
        if cls.MAX_PARTICIPANTS < cls.MIN_PARTICIPANTS:
            raise ValueError("MAX_PARTICIPANTS must be greater than MIN_PARTICIPANTS")

# Validate config on import
Config.validate()