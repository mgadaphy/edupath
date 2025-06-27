import asyncio
import logging
import time
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime

from .base_agent import BaseAgent
from .student_profile_agent import StudentProfileAgent
from .university_agent import UniversityAgent
from .job_market_agent import JobMarketAgent
from .recommendation_agent import RecommendationAgent
from .gemini_agent import GeminiAgent


class AgentOrchestrator:
    """
    Central orchestrator that manages all agents and coordinates their interactions
    to generate comprehensive recommendations for students.
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.is_initialized = False
        self.logger = logging.getLogger("orchestrator")
        self.active_sessions: Dict[str, Dict] = {}
        
    async def initialize(self):
        """Initialize all agents in the system"""
        self.logger.info("🎼 Initializing Agent Orchestrator...")
        
        try:
            # Initialize all agents
            self.agents = {
                "student_profile": StudentProfileAgent(
                    agent_id="student_profile",
                    name="Student Profile Agent",
                    description="Manages student data validation and storage"
                ),
                "university": UniversityAgent(
                    agent_id="university",
                    name="University Program Agent", 
                    description="Manages university data and admission requirements"
                ),
                "job_market": JobMarketAgent(
                    agent_id="job_market",
                    name="Job Market Insights Agent",
                    description="Analyzes career trends and employment opportunities"
                ),
                "recommendation": RecommendationAgent(
                    agent_id="recommendation",
                    name="Personalized Recommendation Agent",
                    description="Core recommendation engine with knowledge graph"
                ),
                "gemini": GeminiAgent(
                    agent_id="gemini",
                    name="Generative AI Module",
                    description="Google Gemini integration for personalized content"
                )
            }
            
            # Initialize each agent
            for agent_id, agent in self.agents.items():
                success = await agent.initialize()
                if not success:
                    raise RuntimeError(f"Failed to initialize agent: {agent_id}")
                self.logger.info(f"✅ {agent.name} initialized successfully")
            
            self.is_initialized = True
            self.logger.info("🎉 All agents initialized successfully!")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize orchestrator: {e}")
            raise
    
    async def process_student_recommendation_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point for processing student recommendation requests.
        Coordinates multiple agents to generate comprehensive recommendations.
        """
        if not self.is_initialized:
            raise RuntimeError("Orchestrator is not initialized")
        
        session_id = str(uuid.uuid4())
        start_time = time.time()
        
        self.logger.info(f"🚀 Processing recommendation request {session_id}")
        
        try:
            # Create session tracking
            self.active_sessions[session_id] = {
                "start_time": start_time,
                "status": "processing",
                "agents_involved": [],
                "current_step": "initialization"
            }
            
            # Step 1: Process and validate student profile
            self.logger.info("👤 Step 1: Processing student profile...")
            self.active_sessions[session_id]["current_step"] = "student_profile"
            self.active_sessions[session_id]["agents_involved"].append("student_profile")
            
            student_response = await self.agents["student_profile"].handle_request({
                "action": "process_profile",
                "student_data": request.get("student_data", {}),
                "session_id": session_id
            })
            
            if not student_response.get("success", True):
                raise RuntimeError(f"Student profile processing failed: {student_response.get('error')}")
            
            student_profile = student_response["student_profile"]
            
            # Step 2: Get relevant university programs
            self.logger.info("🏫 Step 2: Fetching university programs...")
            self.active_sessions[session_id]["current_step"] = "university_programs"
            self.active_sessions[session_id]["agents_involved"].append("university")
            
            university_response = await self.agents["university"].handle_request({
                "action": "get_matching_programs",
                "student_profile": student_profile,
                "filters": request.get("filters", {}),
                "session_id": session_id
            })
            
            if not university_response.get("success", True):
                self.logger.warning(f"University program fetching had issues: {university_response.get('error')}")
                university_programs = []
            else:
                university_programs = university_response.get("programs", [])
            
            # Step 3: Get job market insights
            self.logger.info("💼 Step 3: Analyzing job market...")
            self.active_sessions[session_id]["current_step"] = "job_market"
            self.active_sessions[session_id]["agents_involved"].append("job_market")
            
            job_market_response = await self.agents["job_market"].handle_request({
                "action": "analyze_opportunities",
                "student_profile": student_profile,
                "programs": university_programs,
                "session_id": session_id
            })
            
            if not job_market_response.get("success", True):
                self.logger.warning(f"Job market analysis had issues: {job_market_response.get('error')}")
                job_insights = {}
            else:
                job_insights = job_market_response.get("insights", {})
            
            # Step 4: Generate core recommendations
            self.logger.info("🎯 Step 4: Generating recommendations...")
            self.active_sessions[session_id]["current_step"] = "recommendations"
            self.active_sessions[session_id]["agents_involved"].append("recommendation")
            
            recommendation_response = await self.agents["recommendation"].handle_request({
                "action": "generate_recommendations",
                "student_profile": student_profile,
                "university_programs": university_programs,
                "job_insights": job_insights,
                "session_id": session_id
            })
            
            if not recommendation_response.get("success", True):
                raise RuntimeError(f"Recommendation generation failed: {recommendation_response.get('error')}")
            
            recommendations = recommendation_response["recommendations"]
            
            # Step 5: Enhance with AI-generated content
            self.logger.info("🤖 Step 5: Enhancing with AI content...")
            self.active_sessions[session_id]["current_step"] = "ai_enhancement"
            self.active_sessions[session_id]["agents_involved"].append("gemini")
            
            gemini_response = await self.agents["gemini"].handle_request({
                "action": "enhance_recommendations",
                "student_profile": student_profile,
                "recommendations": recommendations,
                "language": request.get("language", "en"),
                "session_id": session_id
            })
            
            if gemini_response.get("success", True):
                enhanced_content = gemini_response.get("enhanced_content", {})
                # Merge enhanced content into recommendations
                for i, rec in enumerate(recommendations):
                    if i < len(enhanced_content.get("recommendations", [])):
                        rec.update(enhanced_content["recommendations"][i])
            else:
                self.logger.warning("AI enhancement failed, proceeding without enhanced content")
            
            # Step 6: Finalize response
            processing_time = time.time() - start_time
            self.active_sessions[session_id]["status"] = "completed"
            self.active_sessions[session_id]["processing_time"] = processing_time
            
            final_response = {
                "success": True,
                "session_id": session_id,
                "student_profile": student_profile,
                "recommendations": recommendations,
                "job_insights": job_insights,
                "metadata": {
                    "processing_time_ms": int(processing_time * 1000),
                    "total_recommendations": len(recommendations),
                    "agents_involved": self.active_sessions[session_id]["agents_involved"],
                    "timestamp": datetime.now().isoformat(),
                    "algorithm_version": "1.0"
                }
            }
            
            # Add enhanced content if available
            if 'enhanced_content' in locals():
                final_response["enhanced_content"] = enhanced_content
            
            self.logger.info(f"✅ Request {session_id} completed in {processing_time:.2f}s")
            return final_response
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.active_sessions[session_id]["status"] = "failed"
            self.active_sessions[session_id]["error"] = str(e)
            
            self.logger.error(f"❌ Request {session_id} failed after {processing_time:.2f}s: {e}")
            
            return {
                "success": False,
                "session_id": session_id,
                "error": str(e),
                "metadata": {
                    "processing_time_ms": int(processing_time * 1000),
                    "agents_involved": self.active_sessions[session_id]["agents_involved"],
                    "failed_step": self.active_sessions[session_id].get("current_step"),
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        finally:
            # Clean up session after some time
            asyncio.create_task(self._cleanup_session(session_id, delay=300))  # 5 minutes
    
    async def get_agent_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Get status of specific agent or all agents"""
        if agent_id:
            if agent_id not in self.agents:
                return {"error": f"Agent {agent_id} not found"}
            return self.agents[agent_id].get_status()
        
        return {
            "orchestrator_initialized": self.is_initialized,
            "total_agents": len(self.agents),
            "active_sessions": len(self.active_sessions),
            "agents": {agent_id: agent.get_status() for agent_id, agent in self.agents.items()}
        }
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get status of specific session"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        return self.active_sessions[session_id].copy()
    
    async def _cleanup_session(self, session_id: str, delay: int = 0):
        """Clean up session data after delay"""
        if delay > 0:
            await asyncio.sleep(delay)
        
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            self.logger.debug(f"🧹 Cleaned up session {session_id}")
    
    async def cleanup(self):
        """Cleanup all agents and resources"""
        self.logger.info("🧹 Cleaning up Agent Orchestrator...")
        
        for agent_id, agent in self.agents.items():
            try:
                await agent.cleanup()
                self.logger.info(f"✅ {agent.name} cleaned up")
            except Exception as e:
                self.logger.error(f"❌ Failed to cleanup {agent.name}: {e}")
        
        self.agents.clear()
        self.active_sessions.clear()
        self.is_initialized = False
        self.logger.info("✅ Orchestrator cleanup completed")
