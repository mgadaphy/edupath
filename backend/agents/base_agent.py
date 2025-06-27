from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import asyncio
import logging
import time
import json
from datetime import datetime


class BaseAgent(ABC):
    """Base class for all agents in the EduPath multi-agent system"""
    
    def __init__(self, agent_id: str, name: str, description: str):
        self.agent_id = agent_id
        self.name = name
        self.description = description
        self.is_initialized = False
        self.performance_metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "last_activity": None
        }
        self.logger = logging.getLogger(f"agent.{agent_id}")
        
    async def initialize(self) -> bool:
        """Initialize the agent with required resources"""
        try:
            await self._initialize_resources()
            self.is_initialized = True
            self.logger.info(f"Agent {self.name} initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize agent {self.name}: {e}")
            return False
    
    @abstractmethod
    async def _initialize_resources(self):
        """Initialize agent-specific resources (databases, APIs, etc.)"""
        pass
    
    @abstractmethod
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request and return response"""
        pass
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle request with error handling and metrics collection"""
        if not self.is_initialized:
            raise RuntimeError(f"Agent {self.name} is not initialized")
        
        start_time = time.time()
        self.performance_metrics["total_requests"] += 1
        
        try:
            # Validate request
            self._validate_request(request)
            
            # Process request
            response = await self.process_request(request)
            
            # Record success
            self.performance_metrics["successful_requests"] += 1
            self.performance_metrics["last_activity"] = datetime.now().isoformat()
            
            # Update response time
            response_time = time.time() - start_time
            self._update_response_time(response_time)
            
            # Add metadata to response
            response["_metadata"] = {
                "agent_id": self.agent_id,
                "agent_name": self.name,
                "processing_time_ms": int(response_time * 1000),
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"Request processed successfully in {response_time:.3f}s")
            return response
            
        except Exception as e:
            self.performance_metrics["failed_requests"] += 1
            self.logger.error(f"Request processing failed: {e}")
            
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id,
                "agent_name": self.name,
                "_metadata": {
                    "processing_time_ms": int((time.time() - start_time) * 1000),
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    def _validate_request(self, request: Dict[str, Any]):
        """Validate incoming request format"""
        if not isinstance(request, dict):
            raise ValueError("Request must be a dictionary")
        
        required_fields = self.get_required_fields()
        for field in required_fields:
            if field not in request:
                raise ValueError(f"Missing required field: {field}")
    
    def get_required_fields(self) -> List[str]:
        """Return list of required fields for this agent"""
        return []
    
    def _update_response_time(self, response_time: float):
        """Update average response time"""
        current_avg = self.performance_metrics["average_response_time"]
        total_requests = self.performance_metrics["successful_requests"]
        
        if total_requests == 1:
            self.performance_metrics["average_response_time"] = response_time
        else:
            self.performance_metrics["average_response_time"] = (
                (current_avg * (total_requests - 1) + response_time) / total_requests
            )
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and metrics"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "is_initialized": self.is_initialized,
            "performance_metrics": self.performance_metrics.copy()
        }
    
    async def cleanup(self):
        """Cleanup agent resources"""
        try:
            await self._cleanup_resources()
            self.is_initialized = False
            self.logger.info(f"Agent {self.name} cleaned up successfully")
        except Exception as e:
            self.logger.error(f"Failed to cleanup agent {self.name}: {e}")
    
    async def _cleanup_resources(self):
        """Cleanup agent-specific resources"""
        pass


class LLMAgent(BaseAgent):
    """Base class for agents that use Large Language Models"""
    
    def __init__(self, agent_id: str, name: str, description: str, model_config: Optional[Dict] = None):
        super().__init__(agent_id, name, description)
        self.model_config = model_config or {}
        self.llm_client = None
    
    async def _initialize_resources(self):
        """Initialize LLM resources"""
        # Initialize Google Gemini client if API key is available
        try:
            import google.generativeai as genai
            from core.config import settings
            
            if settings.gemini_api_key:
                genai.configure(api_key=settings.gemini_api_key)
                self.llm_client = genai.GenerativeModel('gemini-pro')
                self.logger.info("Gemini LLM client initialized")
            else:
                self.logger.warning("No Gemini API key provided, LLM features disabled")
        except ImportError:
            self.logger.warning("Google Generative AI library not available")
        except Exception as e:
            self.logger.error(f"Failed to initialize LLM client: {e}")
    
    async def generate_content(self, prompt: str, **kwargs) -> Optional[str]:
        """Generate content using LLM"""
        if not self.llm_client:
            return None
        
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.llm_client.generate_content(prompt)
            )
            return response.text
        except Exception as e:
            self.logger.error(f"LLM content generation failed: {e}")
            return None
    
    async def _cleanup_resources(self):
        """Cleanup LLM resources"""
        self.llm_client = None
