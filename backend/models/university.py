from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from database.connection import Base


class University(Base):
    __tablename__ = "universities"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    
    # Basic Information
    name = Column(String(255), nullable=False)
    name_fr = Column(String(255), nullable=True)  # French name
    type = Column(String(50), nullable=False)  # 'public', 'private', 'international'
    
    # Location
    city = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    
    # Contact Information
    website = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    
    # Academic Information
    language_instruction = Column(String(20), default="bilingual")  # 'english', 'french', 'bilingual'
    established_year = Column(Integer, nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "name_fr": self.name_fr,
            "type": self.type,
            "city": self.city,
            "region": self.region,
            "address": self.address,
            "website": self.website,
            "email": self.email,
            "phone": self.phone,
            "language_instruction": self.language_instruction,
            "established_year": self.established_year,
            "is_active": self.is_active
        }


class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, index=True, nullable=False)
    
    # Basic Information
    name = Column(String(255), nullable=False)
    name_fr = Column(String(255), nullable=True)
    degree_type = Column(String(50), nullable=False)  # 'bachelor', 'master', 'doctorate', 'diploma'
    duration_years = Column(Integer, nullable=False)
    
    # University Relationship
    university_id = Column(Integer, nullable=False)
    faculty = Column(String(255), nullable=False)
    department = Column(String(255), nullable=True)
    
    # Academic Requirements
    admission_requirements = Column(JSON, nullable=False)  # Complex requirements structure
    minimum_ol_points = Column(Integer, nullable=True)
    minimum_al_points = Column(Integer, nullable=True)
    minimum_french_average = Column(Float, nullable=True)
    required_subjects = Column(JSON, nullable=True)  # List of required subjects
    
    # Program Details
    description = Column(Text, nullable=True)
    description_fr = Column(Text, nullable=True)
    curriculum_outline = Column(JSON, nullable=True)
    career_prospects = Column(JSON, nullable=True)
    
    # Financial Information
    tuition_fee_fcfa = Column(Integer, nullable=True)
    registration_fee_fcfa = Column(Integer, nullable=True)
    other_fees = Column(JSON, nullable=True)
    
    # Competitive Information
    is_competitive = Column(Boolean, default=False)
    entrance_exam_required = Column(Boolean, default=False)
    entrance_exam_details = Column(JSON, nullable=True)
    annual_intake = Column(Integer, nullable=True)
    
    # Language and Delivery
    language_instruction = Column(String(20), default="bilingual")
    delivery_mode = Column(String(20), default="full_time")  # 'full_time', 'part_time', 'distance'
    
    # Employment Statistics
    employment_rate = Column(Float, nullable=True)  # Percentage
    average_starting_salary = Column(Integer, nullable=True)  # In FCFA
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    last_updated_source = Column(String(255), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "name_fr": self.name_fr,
            "degree_type": self.degree_type,
            "duration_years": self.duration_years,
            "university_id": self.university_id,
            "faculty": self.faculty,
            "department": self.department,
            "admission_requirements": self.admission_requirements,
            "minimum_ol_points": self.minimum_ol_points,
            "minimum_al_points": self.minimum_al_points,
            "minimum_french_average": self.minimum_french_average,
            "required_subjects": self.required_subjects,
            "description": self.description,
            "description_fr": self.description_fr,
            "curriculum_outline": self.curriculum_outline,
            "career_prospects": self.career_prospects,
            "tuition_fee_fcfa": self.tuition_fee_fcfa,
            "registration_fee_fcfa": self.registration_fee_fcfa,
            "other_fees": self.other_fees,
            "is_competitive": self.is_competitive,
            "entrance_exam_required": self.entrance_exam_required,
            "entrance_exam_details": self.entrance_exam_details,
            "annual_intake": self.annual_intake,
            "language_instruction": self.language_instruction,
            "delivery_mode": self.delivery_mode,
            "employment_rate": self.employment_rate,
            "average_starting_salary": self.average_starting_salary,
            "is_active": self.is_active
        }
    
    def check_eligibility(self, student_profile):
        """Check if student meets program admission requirements"""
        from models.student import Student
        
        eligibility = {
            "eligible": False,
            "score": 0,
            "missing_requirements": [],
            "recommendations": []
        }
        
        if student_profile.exam_system == "gce":
            # Check GCE requirements
            ol_points = student_profile.calculate_gce_points()
            
            if self.minimum_ol_points and ol_points < self.minimum_ol_points:
                eligibility["missing_requirements"].append(f"Minimum O-Level points: {self.minimum_ol_points}")
            
            if self.minimum_al_points and student_profile.al_points and student_profile.al_points < self.minimum_al_points:
                eligibility["missing_requirements"].append(f"Minimum A-Level points: {self.minimum_al_points}")
            
        elif student_profile.exam_system == "french":
            # Check French system requirements
            avg = student_profile.calculate_french_average()
            
            if self.minimum_french_average and avg < self.minimum_french_average:
                eligibility["missing_requirements"].append(f"Minimum average: {self.minimum_french_average}/20")
        
        # Check required subjects
        if self.required_subjects:
            student_subjects = set()
            if student_profile.ol_results:
                student_subjects.update(student_profile.ol_results.keys())
            if student_profile.al_results:
                student_subjects.update(student_profile.al_results.keys())
            if student_profile.bac_results:
                student_subjects.update(student_profile.bac_results.keys())
            
            for required_subject in self.required_subjects:
                if required_subject not in student_subjects:
                    eligibility["missing_requirements"].append(f"Required subject: {required_subject}")
        
        # Calculate eligibility score
        if not eligibility["missing_requirements"]:
            eligibility["eligible"] = True
            eligibility["score"] = 85  # Base score for eligible programs
        else:
            eligibility["score"] = max(0, 50 - len(eligibility["missing_requirements"]) * 10)
        
        return eligibility
