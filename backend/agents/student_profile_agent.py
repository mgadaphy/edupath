from typing import Dict, Any, List
import uuid
from sqlalchemy.orm import Session

from .base_agent import BaseAgent
from database.connection import get_db, SessionLocal
from models.student import Student
from core.config import settings


class StudentProfileAgent(BaseAgent):
    """
    Agent responsible for processing, validating, and storing student academic data
    and personal preferences for both GCE and French educational systems.
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description)
        self.db_session = None
    
    async def _initialize_resources(self):
        """Initialize database connection"""
        self.db_session = SessionLocal()
        self.logger.info("Database session initialized for StudentProfileAgent")
    
    async def _cleanup_resources(self):
        """Cleanup database connection"""
        if self.db_session:
            self.db_session.close()
            self.db_session = None
    
    def get_required_fields(self) -> List[str]:
        return ["action"]
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process student profile related requests"""
        action = request["action"]
        
        if action == "process_profile":
            return await self._process_student_profile(request)
        elif action == "validate_grades":
            return await self._validate_grades(request)
        elif action == "calculate_points":
            return await self._calculate_points(request)
        elif action == "get_profile":
            return await self._get_student_profile(request)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def _process_student_profile(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process and store complete student profile"""
        student_data = request.get("student_data", {})
        session_id = request.get("session_id", str(uuid.uuid4()))
        
        # Validate required fields
        if "exam_system" not in student_data:
            raise ValueError("Exam system is required (gce or french)")
        
        exam_system = student_data["exam_system"].lower()
        if exam_system not in ["gce", "french"]:
            raise ValueError("Exam system must be 'gce' or 'french'")
        
        # Check if student already exists by session_id
        existing_student = self.db_session.query(Student).filter(
            Student.session_id == session_id
        ).first()
        
        if existing_student:
            student = existing_student
            # Update existing profile
            for key, value in student_data.items():
                if hasattr(student, key):
                    setattr(student, key, value)
        else:
            # Create new student profile
            student = Student(
                session_id=session_id,
                exam_system=exam_system,
                language_preference=student_data.get("language_preference", "en")
            )
            
            # Set basic information
            if "name" in student_data:
                student.name = student_data["name"]
            if "email" in student_data:
                student.email = student_data["email"]
            if "interests" in student_data:
                student.interests = student_data["interests"]
            if "career_preferences" in student_data:
                student.career_preferences = student_data["career_preferences"]
            if "location_preferences" in student_data:
                student.location_preferences = student_data["location_preferences"]
        
        # Process academic results based on exam system
        if exam_system == "gce":
            await self._process_gce_results(student, student_data)
        else:  # french
            await self._process_french_results(student, student_data)
        
        # Save to database
        if not existing_student:
            self.db_session.add(student)
        
        try:
            self.db_session.commit()
            self.db_session.refresh(student)
        except Exception as e:
            self.db_session.rollback()
            raise RuntimeError(f"Failed to save student profile: {e}")
        
        # Mark profile as completed if sufficient data
        if self._is_profile_complete(student):
            student.profile_completed = True
            self.db_session.commit()
        
        return {
            "success": True,
            "student_profile": student.to_dict(),
            "session_id": session_id,
            "profile_completed": student.profile_completed
        }
    
    async def _process_gce_results(self, student: Student, student_data: Dict[str, Any]):
        """Process GCE O-Level and A-Level results"""
        # Process O-Level results
        if "ol_results" in student_data:
            ol_results = student_data["ol_results"]
            validated_ol = self._validate_gce_grades(ol_results, level="ol")
            student.ol_results = validated_ol
            student.ol_points = self._calculate_gce_points(validated_ol, level="ol")
        
        # Process A-Level results
        if "al_results" in student_data:
            al_results = student_data["al_results"]
            validated_al = self._validate_gce_grades(al_results, level="al")
            student.al_results = validated_al
            student.al_points = self._calculate_gce_points(validated_al, level="al")
    
    async def _process_french_results(self, student: Student, student_data: Dict[str, Any]):
        """Process French system BEPC and Baccalauréat results"""
        # Process BEPC results
        if "bepc_results" in student_data:
            bepc_results = student_data["bepc_results"]
            validated_bepc = self._validate_french_grades(bepc_results)
            student.bepc_results = validated_bepc
        
        # Process Baccalauréat results
        if "bac_results" in student_data:
            bac_results = student_data["bac_results"]
            validated_bac = self._validate_french_grades(bac_results)
            student.bac_results = validated_bac
            student.french_average = self._calculate_french_average(validated_bac)
    
    def _validate_gce_grades(self, results: Dict[str, str], level: str) -> Dict[str, str]:
        """Validate GCE grade format and subjects"""
        valid_grades = set(settings.gce_ol_grades.keys()) if level == "ol" else set(settings.gce_al_grades.keys())
        valid_subjects = set(settings.gce_subjects)
        
        validated = {}
        for subject, grade in results.items():
            if subject not in valid_subjects:
                self.logger.warning(f"Unknown GCE subject: {subject}")
            
            grade = grade.upper()
            if grade not in valid_grades:
                raise ValueError(f"Invalid GCE {level.upper()} grade '{grade}' for subject '{subject}'")
            
            validated[subject] = grade
        
        return validated
    
    def _validate_french_grades(self, results: Dict[str, float]) -> Dict[str, float]:
        """Validate French system grade format and subjects"""
        valid_subjects = set(settings.french_subjects)
        
        validated = {}
        for subject, grade in results.items():
            if subject not in valid_subjects:
                self.logger.warning(f"Unknown French subject: {subject}")
            
            if not isinstance(grade, (int, float)):
                raise ValueError(f"French grade must be numeric for subject '{subject}'")
            
            if not (0 <= grade <= 20):
                raise ValueError(f"French grade must be between 0 and 20 for subject '{subject}'")
            
            validated[subject] = float(grade)
        
        return validated
    
    def _calculate_gce_points(self, results: Dict[str, str], level: str) -> int:
        """Calculate total points for GCE results"""
        grade_scale = settings.gce_ol_grades if level == "ol" else settings.gce_al_grades
        
        total_points = 0
        for subject, grade in results.items():
            points = grade_scale.get(grade, 0)
            total_points += points
        
        return total_points
    
    def _calculate_french_average(self, results: Dict[str, float]) -> float:
        """Calculate average for French system results"""
        if not results:
            return 0.0
        
        return sum(results.values()) / len(results)
    
    def _is_profile_complete(self, student: Student) -> bool:
        """Check if student profile has sufficient data for recommendations"""
        if student.exam_system == "gce":
            return bool(student.ol_results) or bool(student.al_results)
        else:  # french
            return bool(student.bepc_results) or bool(student.bac_results)
    
    async def _validate_grades(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Validate grade data without saving"""
        exam_system = request.get("exam_system", "").lower()
        results = request.get("results", {})
        level = request.get("level", "")
        
        try:
            if exam_system == "gce":
                validated = self._validate_gce_grades(results, level)
                points = self._calculate_gce_points(validated, level)
                return {
                    "success": True,
                    "validated_results": validated,
                    "points": points
                }
            elif exam_system == "french":
                validated = self._validate_french_grades(results)
                average = self._calculate_french_average(validated)
                return {
                    "success": True,
                    "validated_results": validated,
                    "average": average
                }
            else:
                raise ValueError("Invalid exam system")
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _calculate_points(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate points/average for given results"""
        exam_system = request.get("exam_system", "").lower()
        results = request.get("results", {})
        level = request.get("level", "")
        
        try:
            if exam_system == "gce":
                points = self._calculate_gce_points(results, level)
                return {"success": True, "points": points}
            elif exam_system == "french":
                average = self._calculate_french_average(results)
                return {"success": True, "average": average}
            else:
                raise ValueError("Invalid exam system")
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _get_student_profile(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve student profile by session ID"""
        session_id = request.get("session_id")
        if not session_id:
            raise ValueError("Session ID is required")
        
        student = self.db_session.query(Student).filter(
            Student.session_id == session_id
        ).first()
        
        if not student:
            return {
                "success": False,
                "error": "Student profile not found"
            }
        
        return {
            "success": True,
            "student_profile": student.to_dict()
        }
