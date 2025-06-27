from fastapi import APIRouter, HTTPException, Request, Query
from typing import Dict, Any, List, Optional

router = APIRouter()


@router.get("/")
async def get_universities(
    region: Optional[str] = Query(None, description="Filter by region"),
    type: Optional[str] = Query(None, description="Filter by university type"),
    language: Optional[str] = Query(None, description="Filter by language of instruction"),
    app_request: Request = None
):
    """Get list of universities with optional filtering"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            raise HTTPException(status_code=503, detail="University service not available")
        
        filters = {}
        if region:
            filters["region"] = region
        if type:
            filters["type"] = type
        if language:
            filters["language"] = language
        
        response = await university_agent.handle_request({
            "action": "get_universities",
            "filters": filters
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=500, detail=response.get("error", "Failed to get universities"))
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get universities: {str(e)}")


@router.get("/{university_id}")
async def get_university(university_id: int, app_request: Request):
    """Get specific university details"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            raise HTTPException(status_code=503, detail="University service not available")
        
        response = await university_agent.handle_request({
            "action": "get_universities",
            "filters": {"university_id": university_id}
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=500, detail=response.get("error", "Failed to get university"))
        
        universities = response.get("universities", [])
        if not universities:
            raise HTTPException(status_code=404, detail="University not found")
        
        return {
            "success": True,
            "university": universities[0]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get university: {str(e)}")


@router.get("/programs")
async def get_programs(
    university_id: Optional[int] = Query(None, description="Filter by university"),
    degree_type: Optional[str] = Query(None, description="Filter by degree type"),
    faculty: Optional[str] = Query(None, description="Filter by faculty"),
    app_request: Request = None
):
    """Get list of programs with optional filtering"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            raise HTTPException(status_code=503, detail="University service not available")
        
        filters = {}
        if university_id:
            filters["university_id"] = university_id
        if degree_type:
            filters["degree_type"] = degree_type
        if faculty:
            filters["faculty"] = faculty
        
        response = await university_agent.handle_request({
            "action": "get_programs",
            "filters": filters
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=500, detail=response.get("error", "Failed to get programs"))
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get programs: {str(e)}")


@router.get("/programs/{program_id}")
async def get_program(program_id: int, app_request: Request):
    """Get specific program details"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            raise HTTPException(status_code=503, detail="University service not available")
        
        response = await university_agent.handle_request({
            "action": "get_programs",
            "filters": {"program_id": program_id}
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=500, detail=response.get("error", "Failed to get program"))
        
        programs = response.get("programs", [])
        if not programs:
            raise HTTPException(status_code=404, detail="Program not found")
        
        return {
            "success": True,
            "program": programs[0]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get program: {str(e)}")


@router.get("/{university_id}/programs")
async def get_university_programs(
    university_id: int,
    degree_type: Optional[str] = Query(None, description="Filter by degree type"),
    faculty: Optional[str] = Query(None, description="Filter by faculty"),
    app_request: Request = None
):
    """Get programs offered by a specific university"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            raise HTTPException(status_code=503, detail="University service not available")
        
        filters = {"university_id": university_id}
        if degree_type:
            filters["degree_type"] = degree_type
        if faculty:
            filters["faculty"] = faculty
        
        response = await university_agent.handle_request({
            "action": "get_programs",
            "filters": filters
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=500, detail=response.get("error", "Failed to get programs"))
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get university programs: {str(e)}")


@router.get("/search/programs")
async def search_programs(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results"),
    app_request: Request = None
):
    """Search programs by name, description, or keywords"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Service not available")
        
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            raise HTTPException(status_code=503, detail="University service not available")
        
        # Get all programs first (in a real implementation, this would be a proper search)
        response = await university_agent.handle_request({
            "action": "get_programs",
            "filters": {}
        })
        
        if not response.get("success", True):
            raise HTTPException(status_code=500, detail=response.get("error", "Search failed"))
        
        programs = response.get("programs", [])
        
        # Simple text search (in production, use proper search engine)
        search_query = q.lower()
        filtered_programs = []
        
        for program in programs:
            program_text = f"{program.get('name', '')} {program.get('description', '')} {program.get('faculty', '')}".lower()
            if search_query in program_text:
                filtered_programs.append(program)
            
            if len(filtered_programs) >= limit:
                break
        
        return {
            "success": True,
            "query": q,
            "programs": filtered_programs,
            "total_found": len(filtered_programs)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/filters/options")
async def get_filter_options(app_request: Request):
    """Get available filter options for universities and programs"""
    try:
        return {
            "regions": [
                "Centre", "Littoral", "West", "North West", "South West",
                "Adamawa", "East", "Far North", "North", "South"
            ],
            "university_types": [
                {"code": "public", "name": "Public"},
                {"code": "private", "name": "Private"},
                {"code": "international", "name": "International"}
            ],
            "languages": [
                {"code": "english", "name": "English"},
                {"code": "french", "name": "French"},
                {"code": "bilingual", "name": "Bilingual"}
            ],
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
                "Faculty of Agriculture and Veterinary Medicine",
                "Faculty of Information and Communication Technology"
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get filter options: {str(e)}")


@router.get("/statistics")
async def get_university_statistics(app_request: Request):
    """Get university and program statistics"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            return {
                "total_universities": 0,
                "total_programs": 0,
                "by_region": {},
                "by_type": {}
            }
        
        university_agent = orchestrator.agents.get("university")
        if not university_agent:
            return {
                "total_universities": 0,
                "total_programs": 0,
                "by_region": {},
                "by_type": {}
            }
        
        # Get universities
        uni_response = await university_agent.handle_request({
            "action": "get_universities",
            "filters": {}
        })
        
        # Get programs
        prog_response = await university_agent.handle_request({
            "action": "get_programs",
            "filters": {}
        })
        
        universities = uni_response.get("universities", []) if uni_response.get("success") else []
        programs = prog_response.get("programs", []) if prog_response.get("success") else []
        
        # Calculate statistics
        by_region = {}
        by_type = {}
        
        for uni in universities:
            region = uni.get("region", "Unknown")
            uni_type = uni.get("type", "Unknown")
            
            by_region[region] = by_region.get(region, 0) + 1
            by_type[uni_type] = by_type.get(uni_type, 0) + 1
        
        return {
            "total_universities": len(universities),
            "total_programs": len(programs),
            "by_region": by_region,
            "by_type": by_type,
            "last_updated": "2025-01-26T16:01:03Z"
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "total_universities": 0,
            "total_programs": 0,
            "by_region": {},
            "by_type": {}
        }


@router.get("/health")
async def universities_health_check():
    """Health check for universities service"""
    return {
        "service": "universities",
        "status": "healthy",
        "timestamp": "2025-01-26T16:01:03Z"
    }
