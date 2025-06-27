from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
from contextlib import asynccontextmanager

from core.config import settings
from api.routes import auth, students, recommendations, universities, agents
from database.connection import init_db
from agents.orchestrator import AgentOrchestrator


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting EduPath Application...")
    await init_db()
    
    # Initialize the agent orchestrator
    app.state.orchestrator = AgentOrchestrator()
    await app.state.orchestrator.initialize()
    
    print("✅ EduPath Application started successfully!")
    yield
    
    # Shutdown
    print("🛑 Shutting down EduPath Application...")
    if hasattr(app.state, 'orchestrator'):
        await app.state.orchestrator.cleanup()
    print("✅ Cleanup completed!")


app = FastAPI(
    title="EduPath API",
    description="AI-Powered Educational Guidance System for Cameroonian Students",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(students.router, prefix="/api/v1/students", tags=["Students"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(universities.router, prefix="/api/v1/universities", tags=["Universities"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to EduPath - Your Guide to Academic and Career Success in Cameroon",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Multi-agent AI recommendation system",
            "GCE and French educational system support",
            "University program matching",
            "Career path guidance",
            "AI-powered content generation"
        ]
    }


@app.get("/health")
async def health_check():
    try:
        # Check if orchestrator is initialized
        orchestrator = getattr(app.state, 'orchestrator', None)
        agent_status = "operational" if orchestrator else "not_initialized"
        
        return {
            "status": "healthy",
            "agents": agent_status,
            "database": "connected",
            "timestamp": "2025-01-26T16:01:03Z"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
