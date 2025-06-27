from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import uuid

router = APIRouter()


class StudentProfileRequest(BaseModel):
    session_id: str
    exam_system: str = Field(..., pattern="^(gce|french)$", description="Educational system: 'gce' or 'french'")
    name: Optional[str] = None
    email: Optional[str] = None
    language_preference: str = "en"
    
    # Academic results
    ol_results: Optional[Dict[str, str]] = None  # O-Level results for GCE
    al_results: Optional[Dict[str, str]] = None  # A-Level results for GCE
    bepc_results: Optional[Dict[str, float]] = None  # BEPC results for French
    bac_results: Optional[Dict[str, float]] = None  # Baccalauréat results for French
    
    # Preferences
    interests: Optional[List[str]] = None
    career_preferences: Optional[List[str]] = None
    location_preferences: Optional[List[str]] = None


class GradeValidationRequest(BaseModel):
    exam_system: str = Field(..., pattern="^(gce|french)$")
    results: Dict[str, Any]
    level: Optional[str] = None  # For GCE: "ol" or "al"


class StudentProfileResponse(BaseModel):
    success: bool
    student_profile: Optional[Dict[str, Any]] = None
    session_id: str
    profile_completed: bool
    message: str


@router.post("/profile", response_model=StudentProfileResponse)
async def create_or_update_profile(request: StudentProfileRequest, app_request: Request):
    """Create or update student profile"""
    try:
        # Get the orchestrator from the app state
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Recommendation service not available")
        
        # Get the student profile agent
        student_agent = orchestrator.agents.get("student_profile")
        if not student_agent:
            raise HTTPException(status_code=503, detail="Student profile service not available")
        
        # Process the profile request
        response = await student_agent.handle_request({
            "action": "process_profile",
            "student_data": request.dict(exclude_unset=True),
            "session_id": request.session_id
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=400, detail=response.get("error", "Profile processing failed"))
        
        return StudentProfileResponse(
            success=True,
            student_profile=response["student_profile"],
            session_id=response["session_id"],
            profile_completed=response["profile_completed"],
            message="Profile processed successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process profile: {str(e)}")


@router.get("/profile/{session_id}")
async def get_profile(session_id: str, app_request: Request):
    """Get student profile by session ID"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        student_agent = orchestrator.agents.get("student_profile")
        if not student_agent:
            raise HTTPException(status_code=503, detail="Student profile service not available")
        
        response = await student_agent.handle_request({
            "action": "get_profile",
            "session_id": session_id
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=404, detail=response.get("error", "Profile not found"))
        
        return {
            "success": True,
            "student_profile": response["student_profile"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")


@router.post("/validate-grades")
async def validate_grades(request: GradeValidationRequest, app_request: Request):
    """Validate grade format and calculate points/averages"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        student_agent = orchestrator.agents.get("student_profile")
        if not student_agent:
            raise HTTPException(status_code=503, detail="Student profile service not available")
        
        response = await student_agent.handle_request({
            "action": "validate_grades",
            "exam_system": request.exam_system,
            "results": request.results,
            "level": request.level
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=400, detail=response.get("error", "Grade validation failed"))
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Grade validation failed: {str(e)}")


@router.post("/calculate-points")
async def calculate_points(request: GradeValidationRequest, app_request: Request):
    """Calculate points or average for given results"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        student_agent = orchestrator.agents.get("student_profile")
        if not student_agent:
            raise HTTPException(status_code=503, detail="Student profile service not available")
        
        response = await student_agent.handle_request({
            "action": "calculate_points",
            "exam_system": request.exam_system,
            "results": request.results,
            "level": request.level
        })
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Point calculation failed: {str(e)}")


@router.get("/exam-systems")
async def get_exam_systems():
    """Get information about supported exam systems"""
    return {
        "exam_systems": [
            {
                "code": "gce",
                "name": "GCE (General Certificate of Education)",
                "levels": [
                    {
                        "code": "ol",
                        "name": "Ordinary Level",
                        "grade_scale": ["A", "B", "C", "D", "E", "F"],
                        "points": {"A": 3, "B": 2, "C": 1, "D": 0, "E": 0, "F": 0}
                    },
                    {
                        "code": "al",
                        "name": "Advanced Level", 
                        "grade_scale": ["A", "B", "C", "D", "E", "O", "F"],
                        "points": {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "O": 0, "F": 0}
                    }
                ],
                "subjects": [
                    "English Language", "French", "Mathematics", "Physics", "Chemistry",
                    "Biology", "Geography", "History", "Literature", "Economics",
                    "Computer Science", "Further Mathematics", "Government", "Commerce"
                ]
            },
            {
                "code": "french",
                "name": "French Educational System",
                "levels": [
                    {
                        "code": "bepc",
                        "name": "BEPC (Brevet d'Études du Premier Cycle)",
                        "grade_scale": "0-20",
                        "pass_mark": 10
                    },
                    {
                        "code": "bac",
                        "name": "Baccalauréat",
                        "grade_scale": "0-20",
                        "pass_mark": 10
                    }
                ],
                "subjects": [
                    "Français", "Anglais", "Mathématiques", "Physique", "Chimie",
                    "Sciences de la Vie et de la Terre", "Histoire", "Géographie",
                    "Philosophie", "Économie", "Informatique", "Arts"
                ]
            }
        ]
    }


@router.get("/interests")
async def get_interest_options():
    """Get predefined interest options for students"""
    return {
        "interests": [
            "Science & Technology",
            "Medicine & Health",
            "Business & Economics", 
            "Engineering",
            "Arts & Creative",
            "Education",
            "Law & Government",
            "Agriculture",
            "Environmental Science",
            "Mathematics",
            "Computer Science",
            "Social Sciences",
            "Languages",
            "Sports & Recreation",
            "Media & Communication"
        ]
    }


@router.get("/career-preferences")
async def get_career_options():
    """Get predefined career preference options"""
    return {
        "career_preferences": [
            "Software Developer",
            "Medical Doctor", 
            "Engineer",
            "Teacher",
            "Lawyer",
            "Business Manager",
            "Entrepreneur",
            "Researcher",
            "Consultant",
            "Government Worker",
            "NGO Worker",
            "Farmer/Agriculturalist",
            "Artist/Creative",
            "Journalist",
            "Nurse",
            "Pharmacist",
            "Architect",
            "Accountant",
            "Marketing Specialist",
            "Data Analyst"
        ]
    }


@router.get("/health")
async def students_health_check():
    """Health check for students service"""
    return {
        "service": "students",
        "status": "healthy",
        "timestamp": "2025-01-26T16:01:03Z"
    }
