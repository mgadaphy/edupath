from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any, Optional

router = APIRouter()


@router.get("/status")
async def get_agents_status(app_request: Request):
    """Get status of all agents in the system"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            return {
                "orchestrator_initialized": False,
                "error": "Orchestrator not available",
                "agents": {}
            }
        
        status = await orchestrator.get_agent_status()
        return status
    
    except Exception as e:
        return {
            "orchestrator_initialized": False,
            "error": str(e),
            "agents": {}
        }


@router.get("/status/{agent_id}")
async def get_agent_status(agent_id: str, app_request: Request):
    """Get status of a specific agent"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        status = await orchestrator.get_agent_status(agent_id)
        
        if "error" in status:
            raise HTTPException(status_code=404, detail=status["error"])
        
        return status
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get agent status: {str(e)}")


@router.get("/sessions")
async def get_active_sessions(app_request: Request):
    """Get list of active recommendation sessions"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            return {
                "active_sessions": [],
                "total_count": 0
            }
        
        # Get session information from orchestrator
        sessions = []
        for session_id, session_data in orchestrator.active_sessions.items():
            sessions.append({
                "session_id": session_id,
                "status": session_data.get("status", "unknown"),
                "start_time": session_data.get("start_time"),
                "current_step": session_data.get("current_step", "unknown"),
                "agents_involved": session_data.get("agents_involved", [])
            })
        
        return {
            "active_sessions": sessions,
            "total_count": len(sessions)
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "active_sessions": [],
            "total_count": 0
        }


@router.get("/sessions/{session_id}")
async def get_session_status(session_id: str, app_request: Request):
    """Get detailed status of a specific session"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        status = await orchestrator.get_session_status(session_id)
        
        if "error" in status:
            raise HTTPException(status_code=404, detail=status["error"])
        
        return status
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get session status: {str(e)}")


@router.get("/metrics")
async def get_system_metrics(app_request: Request):
    """Get comprehensive system metrics"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            return {
                "system_status": "offline",
                "metrics": {}
            }
        
        status = await orchestrator.get_agent_status()
        
        # Aggregate metrics
        total_requests = 0
        total_successes = 0
        total_failures = 0
        avg_response_times = []
        
        for agent_id, agent_data in status.get("agents", {}).items():
            metrics = agent_data.get("performance_metrics", {})
            total_requests += metrics.get("total_requests", 0)
            total_successes += metrics.get("successful_requests", 0)
            total_failures += metrics.get("failed_requests", 0)
            
            if metrics.get("average_response_time"):
                avg_response_times.append(metrics["average_response_time"])
        
        overall_avg_response_time = sum(avg_response_times) / len(avg_response_times) if avg_response_times else 0
        success_rate = (total_successes / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "system_status": "online" if status.get("orchestrator_initialized") else "offline",
            "metrics": {
                "total_requests": total_requests,
                "successful_requests": total_successes,
                "failed_requests": total_failures,
                "success_rate_percent": round(success_rate, 2),
                "average_response_time_seconds": round(overall_avg_response_time, 3),
                "active_sessions": status.get("active_sessions", 0),
                "total_agents": status.get("total_agents", 0)
            },
            "agent_details": status.get("agents", {})
        }
    
    except Exception as e:
        return {
            "system_status": "error",
            "error": str(e),
            "metrics": {}
        }


@router.post("/agents/{agent_id}/test")
async def test_agent(agent_id: str, test_data: Optional[Dict[str, Any]] = None, app_request: Request = None):
    """Test a specific agent with sample data"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        if agent_id not in orchestrator.agents:
            raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found")
        
        agent = orchestrator.agents[agent_id]
        
        # Default test requests for each agent
        default_test_data = {
            "student_profile": {
                "action": "validate_grades",
                "exam_system": "gce",
                "results": {"Mathematics": "A", "Physics": "B", "Chemistry": "A"},
                "level": "ol"
            },
            "university": {
                "action": "get_universities",
                "filters": {}
            },
            "job_market": {
                "action": "get_sector_insights",
                "filters": {}
            },
            "recommendation": {
                "action": "rank_programs",
                "programs": [],
                "student_profile": {}
            },
            "gemini": {
                "action": "generate_study_guide",
                "program": {"name": "Computer Science"},
                "language": "en"
            }
        }
        
        test_request = test_data or default_test_data.get(agent_id, {"action": "test"})
        
        response = await agent.handle_request(test_request)
        
        return {
            "agent_id": agent_id,
            "test_request": test_request,
            "test_response": response,
            "test_passed": response.get("success", True) if "success" in response else True
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent test failed: {str(e)}")


@router.get("/logs/{agent_id}")
async def get_agent_logs(agent_id: str, limit: int = 100, app_request: Request = None):
    """Get recent logs for a specific agent"""
    try:
        # In a real implementation, this would fetch logs from a logging system
        # For now, return a placeholder response
        return {
            "agent_id": agent_id,
            "logs": [
                {
                    "timestamp": "2025-01-26T16:01:03Z",
                    "level": "INFO",
                    "message": f"Agent {agent_id} processed request successfully"
                },
                {
                    "timestamp": "2025-01-26T16:01:02Z",
                    "level": "INFO",
                    "message": f"Agent {agent_id} initialized"
                }
            ],
            "total_logs": 2,
            "limit": limit
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get logs: {str(e)}")


@router.post("/restart")
async def restart_agents(app_request: Request):
    """Restart all agents (for admin use)"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        if not orchestrator:
            raise HTTPException(status_code=503, detail="Orchestrator not available")
        
        # In a real implementation, this would properly restart the agents
        # For now, return a status message
        return {
            "message": "Agent restart initiated",
            "status": "in_progress",
            "timestamp": "2025-01-26T16:01:03Z"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restart agents: {str(e)}")


@router.get("/config")
async def get_system_config():
    """Get system configuration and settings"""
    try:
        from core.config import settings
        
        # Return non-sensitive configuration
        return {
            "app_name": settings.app_name,
            "app_version": settings.app_version,
            "debug": settings.debug,
            "supported_exam_systems": ["gce", "french"],
            "supported_languages": ["en", "fr"],
            "gemini_enabled": bool(settings.gemini_api_key),
            "database_configured": bool(settings.database_url),
            "redis_configured": bool(settings.redis_url),
            "neo4j_configured": bool(settings.neo4j_uri)
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "config": {}
        }


@router.get("/health")
async def agents_health_check(app_request: Request):
    """Health check for agents system"""
    try:
        orchestrator = getattr(app_request.app.state, 'orchestrator', None)
        healthy = orchestrator is not None and orchestrator.is_initialized
        
        return {
            "service": "agents",
            "status": "healthy" if healthy else "unhealthy",
            "orchestrator_initialized": healthy,
            "timestamp": "2025-01-26T16:01:03Z"
        }
    
    except Exception as e:
        return {
            "service": "agents",
            "status": "error",
            "error": str(e),
            "timestamp": "2025-01-26T16:01:03Z"
        }
