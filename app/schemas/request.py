"""
Request schemas for the API.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator


class PersonalityFeatures(BaseModel):
    """Features for personality prediction."""
    
    time_spent_alone: Optional[float] = Field(
        None, 
        ge=0, 
        le=11, 
        description="Hours spent alone per day (0-11)"
    )
    stage_fear: Optional[str] = Field(
        None, 
        description="Stage fear (Yes/No)"
    )
    social_event_attendance: Optional[float] = Field(
        None, 
        ge=0, 
        le=10, 
        description="Social event attendance frequency (0-10)"
    )
    going_outside: Optional[float] = Field(
        None, 
        ge=0, 
        le=10, 
        description="Going outside frequency (0-10)"
    )
    drained_after_socializing: Optional[str] = Field(
        None, 
        description="Drained after socializing (Yes/No)"
    )
    friends_circle_size: Optional[float] = Field(
        None, 
        ge=0, 
        le=15, 
        description="Number of friends in circle (0-15)"
    )
    post_frequency: Optional[float] = Field(
        None, 
        ge=0, 
        le=10, 
        description="Social media posting frequency (0-10)"
    )
    
    @field_validator('stage_fear', 'drained_after_socializing')
    def validate_yes_no(cls, v):
        """Validate Yes/No fields."""
        if v is not None and v.lower() not in ['yes', 'no']:
            raise ValueError('Must be either "Yes" or "No"')
        return v.title() if v else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with proper field names."""
        return {
            'Time_spent_Alone': self.time_spent_alone,
            'Stage_fear': self.stage_fear,
            'Social_event_attendance': self.social_event_attendance,
            'Going_outside': self.going_outside,
            'Drained_after_socializing': self.drained_after_socializing,
            'Friends_circle_size': self.friends_circle_size,
            'Post_frequency': self.post_frequency
        }


class SinglePredictionRequest(BaseModel):
    """Request for single prediction."""
    
    features: PersonalityFeatures = Field(
        ..., 
        description="Features for personality prediction"
    )


class BatchPredictionRequest(BaseModel):
    """Request for batch prediction."""
    
    features: List[PersonalityFeatures] = Field(
        ..., 
        description="List of features for batch personality prediction",
        min_length=1,
        max_length=100
    )