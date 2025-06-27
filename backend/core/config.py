from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "EduPath"
    app_version: str = "1.0.0"
    debug: bool = Field(default=True, env="DEBUG")
    
    # Database
    database_url: str = Field(
        default="postgresql://edupath_user:edupath_password@localhost:5432/edupath",
        env="DATABASE_URL"
    )
    
    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379",
        env="REDIS_URL"
    )
    
    # Neo4j
    neo4j_uri: str = Field(
        default="bolt://localhost:7687",
        env="NEO4J_URI"
    )
    neo4j_user: str = Field(default="neo4j", env="NEO4J_USER")
    neo4j_password: str = Field(default="edupath_password", env="NEO4J_PASSWORD")
    
    # Google Gemini API
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    
    # Security
    secret_key: str = Field(
        default="edupath-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Cameroon Education Systems
    gce_subjects: list = [
        "English Language", "French", "Mathematics", "Physics", "Chemistry",
        "Biology", "Geography", "History", "Literature", "Economics",
        "Computer Science", "Further Mathematics", "Government", "Commerce"
    ]
    
    french_subjects: list = [
        "Français", "Anglais", "Mathématiques", "Physique", "Chimie",
        "Sciences de la Vie et de la Terre", "Histoire", "Géographie",
        "Philosophie", "Économie", "Informatique", "Arts"
    ]
    
    # Grade scales
    gce_ol_grades: dict = {"A": 3, "B": 2, "C": 1, "D": 0, "E": 0, "F": 0}
    gce_al_grades: dict = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "O": 0, "F": 0}
    french_grade_scale: tuple = (0, 20)  # Out of 20
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
