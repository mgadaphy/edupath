from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from .base_agent import BaseAgent
from database.connection import SessionLocal
from models.university import University, Program
from models.student import Student


class UniversityAgent(BaseAgent):
    """
    Agent responsible for managing university data, admission requirements,
    and matching students with appropriate programs.
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description)
        self.db_session = None
    
    async def _initialize_resources(self):
        """Initialize database connection and ensure sample data exists"""
        self.db_session = SessionLocal()
        await self._ensure_sample_data()
        self.logger.info("Database session initialized for UniversityAgent")
    
    async def _cleanup_resources(self):
        """Cleanup database connection"""
        if self.db_session:
            self.db_session.close()
            self.db_session = None
    
    def get_required_fields(self) -> List[str]:
        return ["action"]
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process university-related requests"""
        action = request["action"]
        
        if action == "get_matching_programs":
            return await self._get_matching_programs(request)
        elif action == "get_universities":
            return await self._get_universities(request)
        elif action == "get_programs":
            return await self._get_programs(request)
        elif action == "check_eligibility":
            return await self._check_program_eligibility(request)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def _get_matching_programs(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get programs that match student profile and preferences"""
        student_profile = request.get("student_profile", {})
        filters = request.get("filters", {})
        session_id = request.get("session_id")
        
        # Get all active programs
        query = self.db_session.query(Program).filter(Program.is_active == True)
        
        # Apply filters
        if filters.get("program_type"):
            query = query.filter(Program.degree_type == filters["program_type"])
        
        if filters.get("university_id"):
            query = query.filter(Program.university_id == filters["university_id"])
        
        if filters.get("faculty"):
            query = query.filter(Program.faculty.ilike(f"%{filters['faculty']}%"))
        
        programs = query.all()
        
        # Evaluate each program for the student
        matched_programs = []
        for program in programs:
            eligibility = self._evaluate_program_eligibility(program, student_profile)
            
            program_data = program.to_dict()
            program_data["eligibility"] = eligibility
            
            # Get university information
            university = self.db_session.query(University).filter(
                University.id == program.university_id
            ).first()
            
            if university:
                program_data["university"] = university.to_dict()
            
            matched_programs.append(program_data)
        
        # Sort by eligibility score and match
        matched_programs.sort(key=lambda x: (
            x["eligibility"]["eligible"],
            x["eligibility"]["score"]
        ), reverse=True)
        
        return {
            "success": True,
            "programs": matched_programs[:20],  # Top 20 matches
            "total_found": len(matched_programs),
            "filters_applied": filters
        }
    
    def _evaluate_program_eligibility(self, program: Program, student_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate how well a student matches a program"""
        eligibility = {
            "eligible": False,
            "score": 0,
            "match_reasons": [],
            "missing_requirements": [],
            "recommendations": []
        }
        
        exam_system = student_profile.get("exam_system", "")
        
        if exam_system == "gce":
            return self._evaluate_gce_eligibility(program, student_profile, eligibility)
        elif exam_system == "french":
            return self._evaluate_french_eligibility(program, student_profile, eligibility)
        else:
            eligibility["missing_requirements"].append("Valid exam system required")
            return eligibility
    
    def _evaluate_gce_eligibility(self, program: Program, student_profile: Dict[str, Any], eligibility: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate GCE student eligibility for program"""
        ol_results = student_profile.get("ol_results", {})
        al_results = student_profile.get("al_results", {})
        ol_points = student_profile.get("ol_points", 0)
        al_points = student_profile.get("al_points", 0)
        
        # Check minimum O-Level requirements
        if program.minimum_ol_points:
            if ol_points >= program.minimum_ol_points:
                eligibility["match_reasons"].append(f"Meets O-Level requirement ({ol_points}/{program.minimum_ol_points} points)")
                eligibility["score"] += 20
            else:
                eligibility["missing_requirements"].append(f"Need {program.minimum_ol_points - ol_points} more O-Level points")
                eligibility["score"] = max(0, eligibility["score"] - 10)
        
        # Check minimum A-Level requirements
        if program.minimum_al_points:
            if al_points >= program.minimum_al_points:
                eligibility["match_reasons"].append(f"Meets A-Level requirement ({al_points}/{program.minimum_al_points} points)")
                eligibility["score"] += 30
            else:
                eligibility["missing_requirements"].append(f"Need {program.minimum_al_points - al_points} more A-Level points")
                eligibility["score"] = max(0, eligibility["score"] - 20)
        
        # Check required subjects
        if program.required_subjects:
            student_subjects = set(ol_results.keys()) | set(al_results.keys())
            missing_subjects = []
            
            for required_subject in program.required_subjects:
                if required_subject not in student_subjects:
                    missing_subjects.append(required_subject)
                else:
                    eligibility["score"] += 10
            
            if missing_subjects:
                eligibility["missing_requirements"].extend([f"Required subject: {subj}" for subj in missing_subjects])
            else:
                eligibility["match_reasons"].append("All required subjects completed")
        
        # Check for competitive programs
        if program.is_competitive:
            if al_points > 0:
                eligibility["score"] += 15
                eligibility["match_reasons"].append("Has A-Level results for competitive program")
            else:
                eligibility["recommendations"].append("Consider completing A-Levels for better chances")
        
        # Determine final eligibility
        if not eligibility["missing_requirements"]:
            eligibility["eligible"] = True
            eligibility["score"] = min(100, eligibility["score"] + 25)  # Bonus for full eligibility
        elif len(eligibility["missing_requirements"]) <= 2:
            eligibility["eligible"] = True  # Conditionally eligible
            eligibility["score"] = min(75, eligibility["score"])
        
        # Subject match bonus
        if program.required_subjects:
            match_count = len(set(program.required_subjects) & student_subjects)
            subject_bonus = (match_count / len(program.required_subjects)) * 20
            eligibility["score"] += subject_bonus
        
        return eligibility
    
    def _evaluate_french_eligibility(self, program: Program, student_profile: Dict[str, Any], eligibility: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate French system student eligibility for program"""
        bepc_results = student_profile.get("bepc_results", {})
        bac_results = student_profile.get("bac_results", {})
        french_average = student_profile.get("french_average", 0)
        
        # Check minimum average requirements
        if program.minimum_french_average:
            if french_average >= program.minimum_french_average:
                eligibility["match_reasons"].append(f"Meets average requirement ({french_average:.1f}/{program.minimum_french_average})")
                eligibility["score"] += 40
            else:
                deficit = program.minimum_french_average - french_average
                eligibility["missing_requirements"].append(f"Need {deficit:.1f} points higher average")
                eligibility["score"] = max(0, eligibility["score"] - 20)
        
        # Check required subjects
        if program.required_subjects:
            student_subjects = set(bepc_results.keys()) | set(bac_results.keys())
            missing_subjects = []
            
            for required_subject in program.required_subjects:
                if required_subject not in student_subjects:
                    missing_subjects.append(required_subject)
                else:
                    eligibility["score"] += 10
            
            if missing_subjects:
                eligibility["missing_requirements"].extend([f"Required subject: {subj}" for subj in missing_subjects])
            else:
                eligibility["match_reasons"].append("All required subjects completed")
        
        # Baccalauréat bonus
        if bac_results:
            eligibility["score"] += 20
            eligibility["match_reasons"].append("Has Baccalauréat qualification")
        elif bepc_results:
            eligibility["score"] += 10
            eligibility["match_reasons"].append("Has BEPC qualification")
        
        # Determine final eligibility
        if not eligibility["missing_requirements"]:
            eligibility["eligible"] = True
            eligibility["score"] = min(100, eligibility["score"] + 25)
        elif len(eligibility["missing_requirements"]) <= 2:
            eligibility["eligible"] = True
            eligibility["score"] = min(75, eligibility["score"])
        
        return eligibility
    
    async def _get_universities(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get list of universities with optional filtering"""
        filters = request.get("filters", {})
        
        query = self.db_session.query(University).filter(University.is_active == True)
        
        if filters.get("region"):
            query = query.filter(University.region.ilike(f"%{filters['region']}%"))
        
        if filters.get("type"):
            query = query.filter(University.type == filters["type"])
        
        if filters.get("language"):
            query = query.filter(University.language_instruction.ilike(f"%{filters['language']}%"))
        
        universities = query.all()
        
        return {
            "success": True,
            "universities": [uni.to_dict() for uni in universities],
            "total_found": len(universities)
        }
    
    async def _get_programs(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get list of programs with optional filtering"""
        filters = request.get("filters", {})
        
        query = self.db_session.query(Program).filter(Program.is_active == True)
        
        if filters.get("university_id"):
            query = query.filter(Program.university_id == filters["university_id"])
        
        if filters.get("degree_type"):
            query = query.filter(Program.degree_type == filters["degree_type"])
        
        if filters.get("faculty"):
            query = query.filter(Program.faculty.ilike(f"%{filters['faculty']}%"))
        
        programs = query.all()
        
        return {
            "success": True,
            "programs": [prog.to_dict() for prog in programs],
            "total_found": len(programs)
        }
    
    async def _check_program_eligibility(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check specific program eligibility for student"""
        program_id = request.get("program_id")
        student_profile = request.get("student_profile", {})
        
        if not program_id:
            raise ValueError("Program ID is required")
        
        program = self.db_session.query(Program).filter(
            Program.id == program_id,
            Program.is_active == True
        ).first()
        
        if not program:
            return {
                "success": False,
                "error": "Program not found"
            }
        
        eligibility = self._evaluate_program_eligibility(program, student_profile)
        
        return {
            "success": True,
            "program": program.to_dict(),
            "eligibility": eligibility
        }
    
    async def _ensure_sample_data(self):
        """Ensure sample universities and programs exist in database"""
        # Check if sample data already exists
        if self.db_session.query(University).count() > 0:
            return
        
        # Create sample universities
        universities = [
            {
                "code": "UY1",
                "name": "University of Yaoundé I",
                "name_fr": "Université de Yaoundé I",
                "type": "public",
                "city": "Yaoundé",
                "region": "Centre",
                "website": "https://www.uy1.uninet.cm",
                "language_instruction": "bilingual",
                "established_year": 1962
            },
            {
                "code": "UDS",
                "name": "University of Douala",
                "name_fr": "Université de Douala",
                "type": "public",
                "city": "Douala",
                "region": "Littoral",
                "website": "https://www.univ-douala.com",
                "language_instruction": "bilingual",
                "established_year": 1977
            },
            {
                "code": "UB",
                "name": "University of Bamenda",
                "name_fr": "Université de Bamenda",
                "type": "public",
                "city": "Bamenda",
                "region": "North West",
                "website": "https://www.uniba.cm",
                "language_instruction": "english",
                "established_year": 2011
            }
        ]
        
        # Insert universities
        for uni_data in universities:
            university = University(**uni_data)
            self.db_session.add(university)
        
        self.db_session.commit()
        
        # Create sample programs
        programs = [
            # University of Yaoundé I programs
            {
                "code": "UY1_CS_BSC",
                "name": "Bachelor of Science in Computer Science",
                "name_fr": "Licence en Informatique",
                "degree_type": "bachelor",
                "duration_years": 3,
                "university_id": 1,
                "faculty": "Faculty of Science",
                "department": "Computer Science",
                "admission_requirements": {
                    "gce_ol_min": 9,
                    "gce_al_min": 6,
                    "french_min": 12.0
                },
                "minimum_ol_points": 9,
                "minimum_al_points": 6,
                "minimum_french_average": 12.0,
                "required_subjects": ["Mathematics", "Physics", "Chemistry"],
                "description": "A comprehensive program in computer science covering programming, algorithms, and system design.",
                "career_prospects": ["Software Developer", "System Analyst", "IT Consultant"],
                "tuition_fee_fcfa": 50000,
                "language_instruction": "bilingual"
            },
            {
                "code": "UY1_MED_MD",
                "name": "Doctor of Medicine",
                "name_fr": "Doctorat en Médecine",
                "degree_type": "doctorate",
                "duration_years": 7,
                "university_id": 1,
                "faculty": "Faculty of Medicine and Biomedical Sciences",
                "department": "Medicine",
                "admission_requirements": {
                    "gce_al_min": 12,
                    "french_min": 15.0
                },
                "minimum_al_points": 12,
                "minimum_french_average": 15.0,
                "required_subjects": ["Biology", "Chemistry", "Physics", "Mathematics"],
                "description": "Medical degree program preparing students for medical practice.",
                "career_prospects": ["Medical Doctor", "Surgeon", "Medical Researcher"],
                "tuition_fee_fcfa": 200000,
                "is_competitive": True,
                "entrance_exam_required": True,
                "language_instruction": "bilingual"
            },
            # University of Douala programs
            {
                "code": "UDS_BUS_BSC",
                "name": "Bachelor of Science in Business Administration",
                "name_fr": "Licence en Administration des Affaires",
                "degree_type": "bachelor",
                "duration_years": 3,
                "university_id": 2,
                "faculty": "Faculty of Economics and Management",
                "department": "Business Administration",
                "admission_requirements": {
                    "gce_ol_min": 6,
                    "gce_al_min": 4,
                    "french_min": 10.0
                },
                "minimum_ol_points": 6,
                "minimum_al_points": 4,
                "minimum_french_average": 10.0,
                "required_subjects": ["Mathematics", "Economics"],
                "description": "Business administration program focusing on management and entrepreneurship.",
                "career_prospects": ["Business Manager", "Entrepreneur", "Financial Analyst"],
                "tuition_fee_fcfa": 75000,
                "language_instruction": "bilingual"
            },
            # University of Bamenda programs
            {
                "code": "UB_ENG_BSC",
                "name": "Bachelor of Engineering",
                "name_fr": "Licence en Ingénierie",
                "degree_type": "bachelor",
                "duration_years": 4,
                "university_id": 3,
                "faculty": "Faculty of Engineering and Technology",
                "department": "Engineering",
                "admission_requirements": {
                    "gce_al_min": 8
                },
                "minimum_al_points": 8,
                "required_subjects": ["Mathematics", "Physics", "Chemistry"],
                "description": "Engineering program with specializations in various engineering disciplines.",
                "career_prospects": ["Engineer", "Technical Consultant", "Project Manager"],
                "tuition_fee_fcfa": 100000,
                "language_instruction": "english"
            }
        ]
        
        # Insert programs
        for prog_data in programs:
            program = Program(**prog_data)
            self.db_session.add(program)
        
        self.db_session.commit()
        self.logger.info("Sample university and program data created successfully")
