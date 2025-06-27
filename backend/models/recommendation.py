from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from database.connection import Base


class Recommendation(Base):
    __tablename__ = "recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Student and Session Information
    student_id = Column(Integer, nullable=False)  # Foreign key to students
    session_id = Column(String(255), nullable=False, index=True)
    
    # Recommendation Details
    program_id = Column(Integer, nullable=False)  # Foreign key to programs
    recommendation_type = Column(String(50), default="program")  # 'program', 'career', 'skill'
    
    # Scoring and Ranking
    match_score = Column(Float, nullable=False)  # 0-100 score
    confidence_score = Column(Float, nullable=False)  # 0-100 confidence
    ranking_position = Column(Integer, nullable=False)  # 1-based ranking
    
    # Recommendation Reasoning
    reasons = Column(JSON, nullable=True)  # Why this was recommended
    pros = Column(JSON, nullable=True)  # Advantages
    cons = Column(JSON, nullable=True)  # Potential challenges
    requirements_met = Column(JSON, nullable=True)  # Which requirements student meets
    requirements_missing = Column(JSON, nullable=True)  # What student needs to work on
    
    # Career Information
    career_prospects = Column(JSON, nullable=True)  # Related career paths
    employment_outlook = Column(String(50), nullable=True)  # Market outlook
    salary_expectations = Column(JSON, nullable=True)  # Expected salary ranges
    
    # Preparation Guidance
    preparation_tips = Column(JSON, nullable=True)  # How to prepare for this program
    recommended_subjects = Column(JSON, nullable=True)  # Subjects to focus on
    skill_gaps = Column(JSON, nullable=True)  # Skills to develop
    
    # AI-Generated Content
    personalized_advice = Column(Text, nullable=True)  # Gemini-generated advice
    study_guide_summary = Column(Text, nullable=True)  # Key preparation points
    success_pathway = Column(JSON, nullable=True)  # Step-by-step guidance
    
    # Alternative Options
    alternative_programs = Column(JSON, nullable=True)  # Similar programs
    fallback_options = Column(JSON, nullable=True)  # Backup choices
    
    # Metadata
    algorithm_version = Column(String(20), default="1.0")
    generation_time_ms = Column(Integer, nullable=True)
    agent_contributions = Column(JSON, nullable=True)  # Which agents contributed
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "session_id": self.session_id,
            "program_id": self.program_id,
            "recommendation_type": self.recommendation_type,
            "match_score": self.match_score,
            "confidence_score": self.confidence_score,
            "ranking_position": self.ranking_position,
            "reasons": self.reasons,
            "pros": self.pros,
            "cons": self.cons,
            "requirements_met": self.requirements_met,
            "requirements_missing": self.requirements_missing,
            "career_prospects": self.career_prospects,
            "employment_outlook": self.employment_outlook,
            "salary_expectations": self.salary_expectations,
            "preparation_tips": self.preparation_tips,
            "recommended_subjects": self.recommended_subjects,
            "skill_gaps": self.skill_gaps,
            "personalized_advice": self.personalized_advice,
            "study_guide_summary": self.study_guide_summary,
            "success_pathway": self.success_pathway,
            "alternative_programs": self.alternative_programs,
            "fallback_options": self.fallback_options,
            "algorithm_version": self.algorithm_version,
            "generation_time_ms": self.generation_time_ms,
            "agent_contributions": self.agent_contributions,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "is_active": self.is_active
        }


class RecommendationSession(Base):
    __tablename__ = "recommendation_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    student_id = Column(Integer, nullable=False)
    
    # Session Information
    request_data = Column(JSON, nullable=False)  # Original request
    response_data = Column(JSON, nullable=True)  # Final response
    
    # Processing Information
    total_recommendations = Column(Integer, default=0)
    processing_time_ms = Column(Integer, nullable=True)
    agents_involved = Column(JSON, nullable=True)  # List of agents that participated
    
    # Quality Metrics
    recommendation_quality_score = Column(Float, nullable=True)  # Overall quality
    user_feedback = Column(JSON, nullable=True)  # If user provides feedback
    
    # Status
    status = Column(String(50), default="processing")  # 'processing', 'completed', 'failed'
    error_message = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "session_id": self.session_id,
            "student_id": self.student_id,
            "request_data": self.request_data,
            "response_data": self.response_data,
            "total_recommendations": self.total_recommendations,
            "processing_time_ms": self.processing_time_ms,
            "agents_involved": self.agents_involved,
            "recommendation_quality_score": self.recommendation_quality_score,
            "user_feedback": self.user_feedback,
            "status": self.status,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class ScholarshipOpportunity(Base):
    __tablename__ = "scholarships"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_fr = Column(String(255), nullable=True)
    
    # Scholarship Information
    provider = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    description_fr = Column(Text, nullable=True)
    
    # Eligibility Criteria
    eligible_programs = Column(JSON, nullable=True)  # List of program codes
    eligible_countries = Column(JSON, nullable=True)  # For international scholarships
    min_academic_score = Column(Float, nullable=True)
    max_age = Column(Integer, nullable=True)
    gender_requirement = Column(String(20), nullable=True)  # 'male', 'female', 'any'
    
    # Financial Information
    award_amount_fcfa = Column(Integer, nullable=True)
    coverage_type = Column(String(50), nullable=True)  # 'full', 'partial', 'tuition_only'
    duration_years = Column(Integer, nullable=True)
    renewable = Column(Boolean, default=False)
    
    # Application Information
    application_deadline = Column(DateTime, nullable=True)
    application_url = Column(String(500), nullable=True)
    required_documents = Column(JSON, nullable=True)
    selection_criteria = Column(JSON, nullable=True)
    
    # Statistics
    annual_recipients = Column(Integer, nullable=True)
    success_rate = Column(Float, nullable=True)  # Percentage
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_fr": self.name_fr,
            "provider": self.provider,
            "description": self.description,
            "description_fr": self.description_fr,
            "eligible_programs": self.eligible_programs,
            "eligible_countries": self.eligible_countries,
            "min_academic_score": self.min_academic_score,
            "max_age": self.max_age,
            "gender_requirement": self.gender_requirement,
            "award_amount_fcfa": self.award_amount_fcfa,
            "coverage_type": self.coverage_type,
            "duration_years": self.duration_years,
            "renewable": self.renewable,
            "application_deadline": self.application_deadline.isoformat() if self.application_deadline else None,
            "application_url": self.application_url,
            "required_documents": self.required_documents,
            "selection_criteria": self.selection_criteria,
            "annual_recipients": self.annual_recipients,
            "success_rate": self.success_rate,
            "is_active": self.is_active
        }
