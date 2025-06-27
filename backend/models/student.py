from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, Text
from sqlalchemy.sql import func
from database.connection import Base


class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    
    # Personal Information
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    language_preference = Column(String(10), default="en")  # 'en' or 'fr'
    
    # Educational System
    exam_system = Column(String(20), nullable=False)  # 'gce' or 'french'
    
    # Academic Information (stored as JSON for flexibility)
    ol_results = Column(JSON, nullable=True)  # For GCE O-Level results
    al_results = Column(JSON, nullable=True)  # For GCE A-Level results
    bepc_results = Column(JSON, nullable=True)  # For French BEPC results
    bac_results = Column(JSON, nullable=True)  # For French Baccalauréat results
    
    # Calculated Scores
    ol_points = Column(Integer, nullable=True)
    al_points = Column(Integer, nullable=True)
    french_average = Column(Integer, nullable=True)  # Out of 20
    
    # Interests and Preferences
    interests = Column(JSON, nullable=True)  # Areas of interest
    career_preferences = Column(JSON, nullable=True)
    location_preferences = Column(JSON, nullable=True)  # Preferred regions/cities
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())
    
    # Status
    is_active = Column(Boolean, default=True)
    profile_completed = Column(Boolean, default=False)
    
    def calculate_gce_points(self):
        """Calculate total points for GCE system"""
        from core.config import settings
        
        total_points = 0
        
        # O-Level points
        if self.ol_results:
            for subject, grade in self.ol_results.items():
                total_points += settings.gce_ol_grades.get(grade, 0)
        
        # A-Level points (weighted more heavily)
        if self.al_results:
            for subject, grade in self.al_results.items():
                total_points += settings.gce_al_grades.get(grade, 0) * 2
        
        return total_points
    
    def calculate_french_average(self):
        """Calculate average for French system"""
        if self.bac_results:
            scores = [score for score in self.bac_results.values() if isinstance(score, (int, float))]
            return sum(scores) / len(scores) if scores else 0
        return 0
    
    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "name": self.name,
            "email": self.email,
            "language_preference": self.language_preference,
            "exam_system": self.exam_system,
            "ol_results": self.ol_results,
            "al_results": self.al_results,
            "bepc_results": self.bepc_results,
            "bac_results": self.bac_results,
            "ol_points": self.ol_points,
            "al_points": self.al_points,
            "french_average": self.french_average,
            "interests": self.interests,
            "career_preferences": self.career_preferences,
            "location_preferences": self.location_preferences,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "profile_completed": self.profile_completed
        }
