from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from database.connection import Base


class JobSector(Base):
    __tablename__ = "job_sectors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    name_fr = Column(String(255), nullable=True)
    
    # Sector Information
    description = Column(Text, nullable=True)
    description_fr = Column(Text, nullable=True)
    growth_rate = Column(Float, nullable=True)  # Annual growth percentage
    employment_size = Column(Integer, nullable=True)  # Number of people employed
    
    # Market Demand
    demand_level = Column(String(20), default="medium")  # 'low', 'medium', 'high', 'very_high'
    skill_shortage = Column(Boolean, default=False)
    
    # Economic Impact
    contribution_to_gdp = Column(Float, nullable=True)  # Percentage contribution
    average_salary_range = Column(JSON, nullable=True)  # {"min": 150000, "max": 500000}
    
    # Entrepreneurship Potential
    entrepreneurship_score = Column(Integer, default=50)  # 0-100 scale
    startup_capital_required = Column(JSON, nullable=True)  # Different levels
    
    # Related Programs and Skills
    related_programs = Column(JSON, nullable=True)  # List of program codes
    required_skills = Column(JSON, nullable=True)  # List of skills
    
    # Government Priorities
    government_priority = Column(Boolean, default=False)
    development_programs = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_fr": self.name_fr,
            "description": self.description,
            "description_fr": self.description_fr,
            "growth_rate": self.growth_rate,
            "employment_size": self.employment_size,
            "demand_level": self.demand_level,
            "skill_shortage": self.skill_shortage,
            "contribution_to_gdp": self.contribution_to_gdp,
            "average_salary_range": self.average_salary_range,
            "entrepreneurship_score": self.entrepreneurship_score,
            "startup_capital_required": self.startup_capital_required,
            "related_programs": self.related_programs,
            "required_skills": self.required_skills,
            "government_priority": self.government_priority,
            "development_programs": self.development_programs,
            "is_active": self.is_active
        }


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    name_fr = Column(String(255), nullable=True)
    
    # Skill Information
    category = Column(String(100), nullable=False)  # 'technical', 'soft', 'analytical', 'creative'
    description = Column(Text, nullable=True)
    description_fr = Column(Text, nullable=True)
    
    # Market Demand
    demand_level = Column(String(20), default="medium")
    trend = Column(String(20), default="stable")  # 'declining', 'stable', 'growing', 'emerging'
    
    # Learning Information
    difficulty_level = Column(String(20), default="medium")  # 'beginner', 'intermediate', 'advanced'
    learning_time_months = Column(Integer, nullable=True)
    certification_available = Column(Boolean, default=False)
    
    # Economic Value
    salary_impact = Column(Float, nullable=True)  # Percentage increase in salary
    freelance_potential = Column(Boolean, default=False)
    remote_work_compatible = Column(Boolean, default=False)
    
    # Related Information
    related_sectors = Column(JSON, nullable=True)  # List of sector IDs
    prerequisite_skills = Column(JSON, nullable=True)  # List of skill names
    tools_technologies = Column(JSON, nullable=True)  # Associated tools/tech
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_fr": self.name_fr,
            "category": self.category,
            "description": self.description,
            "description_fr": self.description_fr,
            "demand_level": self.demand_level,
            "trend": self.trend,
            "difficulty_level": self.difficulty_level,
            "learning_time_months": self.learning_time_months,
            "certification_available": self.certification_available,
            "salary_impact": self.salary_impact,
            "freelance_potential": self.freelance_potential,
            "remote_work_compatible": self.remote_work_compatible,
            "related_sectors": self.related_sectors,
            "prerequisite_skills": self.prerequisite_skills,
            "tools_technologies": self.tools_technologies,
            "is_active": self.is_active
        }


class CareerPath(Base):
    __tablename__ = "career_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    name_fr = Column(String(255), nullable=True)
    
    # Career Information
    description = Column(Text, nullable=True)
    description_fr = Column(Text, nullable=True)
    sector_id = Column(Integer, nullable=False)  # Foreign key to job_sectors
    
    # Career Progression
    entry_level_positions = Column(JSON, nullable=True)
    mid_level_positions = Column(JSON, nullable=True)
    senior_level_positions = Column(JSON, nullable=True)
    
    # Requirements
    required_education = Column(JSON, nullable=True)  # Minimum degree requirements
    required_skills = Column(JSON, nullable=True)  # Essential skills
    preferred_skills = Column(JSON, nullable=True)  # Nice-to-have skills
    
    # Economic Information
    entry_salary_range = Column(JSON, nullable=True)
    mid_salary_range = Column(JSON, nullable=True)
    senior_salary_range = Column(JSON, nullable=True)
    job_availability = Column(String(20), default="medium")
    
    # Career Attributes
    work_life_balance = Column(Integer, default=50)  # 0-100 scale
    stress_level = Column(Integer, default=50)  # 0-100 scale
    creativity_required = Column(Integer, default=50)  # 0-100 scale
    travel_required = Column(Boolean, default=False)
    
    # Success Factors
    success_stories = Column(JSON, nullable=True)  # Alumni examples
    challenges = Column(JSON, nullable=True)  # Common challenges
    tips_for_success = Column(JSON, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "name_fr": self.name_fr,
            "description": self.description,
            "description_fr": self.description_fr,
            "sector_id": self.sector_id,
            "entry_level_positions": self.entry_level_positions,
            "mid_level_positions": self.mid_level_positions,
            "senior_level_positions": self.senior_level_positions,
            "required_education": self.required_education,
            "required_skills": self.required_skills,
            "preferred_skills": self.preferred_skills,
            "entry_salary_range": self.entry_salary_range,
            "mid_salary_range": self.mid_salary_range,
            "senior_salary_range": self.senior_salary_range,
            "job_availability": self.job_availability,
            "work_life_balance": self.work_life_balance,
            "stress_level": self.stress_level,
            "creativity_required": self.creativity_required,
            "travel_required": self.travel_required,
            "success_stories": self.success_stories,
            "challenges": self.challenges,
            "tips_for_success": self.tips_for_success,
            "is_active": self.is_active
        }
