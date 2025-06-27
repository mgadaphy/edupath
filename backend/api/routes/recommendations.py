from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

router = APIRouter()


class RecommendationRequest(BaseModel):
    session_id: str
    language: str = "en"
    filters: Optional[Dict[str, Any]] = None
    max_recommendations: int = Field(default=10, ge=1, le=20)


class RecommendationResponse(BaseModel):
    success: bool
    session_id: str
    recommendations: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    enhanced_content: Optional[Dict[str, Any]] = None


@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendations(request: RecommendationRequest, app_request: Request):
    """Generate personalized recommendations for a student"""
    try:
        # Get the orchestrator from the app state
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Recommendation service not available")
        
        # First, get the student profile
        student_agent = orchestrator.agents.get("student_profile")
        if not student_agent:
            raise HTTPException(status_code=503, detail="Student profile service not available")
        
        profile_response = await student_agent.handle_request({
            "action": "get_profile",
            "session_id": request.session_id
        })
        
        if not profile_response.get("success", True):
            raise HTTPException(status_code=404, detail="Student profile not found. Please create a profile first.")
        
        student_profile = profile_response["student_profile"]
        
        if not student_profile.get("profile_completed", False):
            raise HTTPException(
                status_code=400, 
                detail="Student profile is incomplete. Please provide academic results to get recommendations."
            )
        
        # Generate comprehensive recommendations using the orchestrator
        recommendation_request = {
            "student_data": student_profile,
            "filters": request.filters or {},
            "language": request.language,
            "max_recommendations": request.max_recommendations
        }
        
        response = await orchestrator.process_student_recommendation_request(recommendation_request)
        
        if not response.get("success", False):
            raise HTTPException(
                status_code=500, 
                detail=response.get("error", "Failed to generate recommendations")
            )
        
        # Limit recommendations to requested amount
        recommendations = response.get("recommendations", [])[:request.max_recommendations]
        
        return RecommendationResponse(
            success=True,
            session_id=request.session_id,
            recommendations=recommendations,
            metadata=response.get("metadata", {}),
            enhanced_content=response.get("enhanced_content")
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")


@router.get("/session/{session_id}")
async def get_recommendations_by_session(session_id: str, app_request: Request):
    """Get previously generated recommendations for a session"""
    try:
        # This would typically fetch from database
        # For now, we'll return a message indicating this feature
        return {
            "success": True,
            "session_id": session_id,
            "message": "Recommendation history feature coming soon",
            "recommendations": []
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")


@router.get("/program/{program_id}/eligibility")
async def check_program_eligibility(program_id: int, session_id: str, app_request: Request):
    """Check eligibility for a specific program"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        # Get student profile
        student_agent = orchestrator.agents.get("student_profile")
        if not student_agent:
            raise HTTPException(status_code=503, detail="Student profile service not available")
        
        profile_response = await student_agent.handle_request({
            "action": "get_profile",
            "session_id": session_id
        })
        
        if not profile_response.get("success", True):
            raise HTTPException(status_code=404, detail="Student profile not found")
        
        # Check program eligibility
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            raise HTTPException(status_code=503, detail="University service not available")
        
        eligibility_response = await university_agent.handle_request({
            "action": "check_eligibility",
            "program_id": program_id,
            "student_profile": profile_response["student_profile"]
        })
        
        return eligibility_response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check eligibility: {str(e)}")


@router.post("/explain/{recommendation_id}")
async def explain_recommendation(recommendation_id: int, app_request: Request):
    """Get detailed explanation for a specific recommendation"""
    try:
        # This would typically fetch the recommendation from database and provide detailed explanation
        return {
            "success": True,
            "recommendation_id": recommendation_id,
            "explanation": {
                "reasoning": "This recommendation is based on your academic performance, career interests, and job market analysis.",
                "strengths": ["Good academic fit", "Strong career prospects", "Aligns with interests"],
                "considerations": ["Competitive admission", "Higher tuition fees"],
                "next_steps": ["Prepare application documents", "Study for entrance exam", "Research scholarship opportunities"]
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to explain recommendation: {str(e)}")


class FeedbackRequest(BaseModel):
    session_id: str
    recommendation_id: int
    rating: int = Field(..., ge=1, le=5)
    feedback: Optional[str] = None

@router.post("/feedback")
async def submit_recommendation_feedback(
    feedback_request: FeedbackRequest,
    app_request: Request = None
):
    """Submit feedback on a recommendation"""
    try:
        feedback_data = {
            "session_id": feedback_request.session_id,
            "recommendation_id": feedback_request.recommendation_id,
            "rating": feedback_request.rating,
            "feedback": feedback_request.feedback,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # In a real application, you would store this in a database
        # For now, we'll just log it
        print(f"Feedback received: {feedback_data}")
        
        return {
            "success": True,
            "message": "Thank you for your feedback!",
            "session_id": feedback_request.session_id,
            "recommendation_id": feedback_request.recommendation_id
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")


@router.get("/filters")
async def get_recommendation_filters():
    """Get available filters for recommendations"""
    return {
        "filters": {
            "degree_types": [
                {"code": "bachelor", "name": "Bachelor's Degree"},
                {"code": "master", "name": "Master's Degree"},
                {"code": "doctorate", "name": "Doctorate/PhD"},
                {"code": "diploma", "name": "Diploma/Certificate"}
            ],
            "faculties": [
                "Faculty of Science",
                "Faculty of Medicine and Biomedical Sciences",
                "Faculty of Engineering and Technology",
                "Faculty of Economics and Management",
                "Faculty of Arts, Letters and Social Sciences",
                "Faculty of Education",
                "Faculty of Law and Political Science",
                "Faculty of Agriculture and Veterinary Medicine"
            ],
            "regions": [
                "Centre", "Littoral", "West", "North West", "South West",
                "Adamawa", "East", "Far North", "North", "South"
            ],
            "university_types": [
                {"code": "public", "name": "Public Universities"},
                {"code": "private", "name": "Private Universities"},
                {"code": "international", "name": "International Universities"}
            ],
            "languages": [
                {"code": "english", "name": "English"},
                {"code": "french", "name": "French"},
                {"code": "bilingual", "name": "Bilingual"}
            ]
        }
    }


@router.get("/statistics")
async def get_recommendation_statistics(app_request: Request):
    """Get recommendation system statistics"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            return {
                "total_recommendations": 0,
                "active_sessions": 0,
                "agent_status": "offline"
            }
        
        status = await orchestrator.get_agent_status()
        
        return {
            "total_recommendations": 0,  # Would be fetched from database
            "active_sessions": status.get("active_sessions", 0),
            "agent_status": "online" if status.get("orchestrator_initialized") else "offline",
            "agents": {
                agent_id: agent_data.get("performance_metrics", {}).get("total_requests", 0)
                for agent_id, agent_data in status.get("agents", {}).items()
            }
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "total_recommendations": 0,
            "active_sessions": 0,
            "agent_status": "error"
        }


@router.get("/health")
async def recommendations_health_check():
    """Health check for recommendations service"""
    return {
        "service": "recommendations",
        "status": "healthy",
        "timestamp": "2025-01-26T16:01:03Z"
    }
