from typing import Dict, Any, List
from sqlalchemy.orm import Session

from .base_agent import BaseAgent
from database.connection import SessionLocal
from models.job_market import JobSector, Skill, CareerPath


class JobMarketAgent(BaseAgent):
    """
    Agent responsible for analyzing job market trends, career opportunities,
    and matching them with student profiles and academic programs.
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description)
        self.db_session = None
    
    async def _initialize_resources(self):
        """Initialize database connection and ensure sample data exists"""
        self.db_session = SessionLocal()
        await self._ensure_sample_data()
        self.logger.info("Database session initialized for JobMarketAgent")
    
    async def _cleanup_resources(self):
        """Cleanup database connection"""
        if self.db_session:
            self.db_session.close()
            self.db_session = None
    
    def get_required_fields(self) -> List[str]:
        return ["action"]
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process job market related requests"""
        action = request["action"]
        
        if action == "analyze_opportunities":
            return await self._analyze_opportunities(request)
        elif action == "get_career_paths":
            return await self._get_career_paths(request)
        elif action == "get_skills_demand":
            return await self._get_skills_demand(request)
        elif action == "get_sector_insights":
            return await self._get_sector_insights(request)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def _analyze_opportunities(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze job market opportunities for student and programs"""
        student_profile = request.get("student_profile", {})
        programs = request.get("programs", [])
        session_id = request.get("session_id")
        
        insights = {
            "career_outlook": {},
            "skill_recommendations": [],
            "sector_analysis": [],
            "entrepreneurship_opportunities": [],
            "government_priorities": [],
            "salary_expectations": {}
        }
        
        # Analyze career prospects for each program
        program_careers = {}
        for program in programs:
            career_prospects = program.get("career_prospects", [])
            program_id = program.get("id")
            
            if career_prospects:
                program_careers[program_id] = await self._analyze_program_careers(career_prospects)
        
        insights["career_outlook"] = program_careers
        
        # Get general market insights
        insights["sector_analysis"] = await self._get_high_demand_sectors()
        insights["skill_recommendations"] = await self._get_trending_skills()
        insights["entrepreneurship_opportunities"] = await self._get_entrepreneurship_opportunities()
        insights["government_priorities"] = await self._get_government_priority_sectors()
        
        # Calculate salary expectations
        insights["salary_expectations"] = await self._calculate_salary_expectations(programs)
        
        return {
            "success": True,
            "insights": insights,
            "analysis_timestamp": "2025-01-26T16:01:03Z"
        }
    
    async def _analyze_program_careers(self, career_prospects: List[str]) -> Dict[str, Any]:
        """Analyze specific career prospects for a program"""
        career_analysis = {
            "prospects": [],
            "average_demand": "medium",
            "growth_potential": "stable",
            "entrepreneurship_score": 50
        }
        
        total_demand_score = 0
        total_growth_score = 0
        total_entrepreneurship = 0
        analyzed_count = 0
        
        for career_name in career_prospects:
            # Find matching career paths
            career_path = self.db_session.query(CareerPath).filter(
                CareerPath.name.ilike(f"%{career_name}%")
            ).first()
            
            if career_path:
                career_data = career_path.to_dict()
                
                # Get related sector information
                sector = self.db_session.query(JobSector).filter(
                    JobSector.id == career_path.sector_id
                ).first()
                
                if sector:
                    career_data["sector"] = sector.to_dict()
                    
                    # Calculate scores
                    demand_scores = {"low": 25, "medium": 50, "high": 75, "very_high": 100}
                    total_demand_score += demand_scores.get(sector.demand_level, 50)
                    
                    if sector.growth_rate:
                        total_growth_score += min(100, max(0, sector.growth_rate * 10 + 50))
                    else:
                        total_growth_score += 50
                    
                    total_entrepreneurship += sector.entrepreneurship_score
                    analyzed_count += 1
                
                career_analysis["prospects"].append(career_data)
        
        # Calculate averages
        if analyzed_count > 0:
            avg_demand = total_demand_score / analyzed_count
            avg_growth = total_growth_score / analyzed_count
            avg_entrepreneurship = total_entrepreneurship / analyzed_count
            
            # Convert to categorical values
            if avg_demand >= 80:
                career_analysis["average_demand"] = "very_high"
            elif avg_demand >= 65:
                career_analysis["average_demand"] = "high"
            elif avg_demand >= 35:
                career_analysis["average_demand"] = "medium"
            else:
                career_analysis["average_demand"] = "low"
            
            if avg_growth >= 70:
                career_analysis["growth_potential"] = "growing"
            elif avg_growth >= 30:
                career_analysis["growth_potential"] = "stable"
            else:
                career_analysis["growth_potential"] = "declining"
            
            career_analysis["entrepreneurship_score"] = int(avg_entrepreneurship)
        
        return career_analysis
    
    async def _get_high_demand_sectors(self) -> List[Dict[str, Any]]:
        """Get sectors with high demand"""
        sectors = self.db_session.query(JobSector).filter(
            JobSector.demand_level.in_(["high", "very_high"]),
            JobSector.is_active == True
        ).order_by(JobSector.growth_rate.desc()).limit(5).all()
        
        return [sector.to_dict() for sector in sectors]
    
    async def _get_trending_skills(self) -> List[Dict[str, Any]]:
        """Get skills that are trending or in high demand"""
        skills = self.db_session.query(Skill).filter(
            Skill.trend.in_(["growing", "emerging"]),
            Skill.demand_level.in_(["high", "very_high"]),
            Skill.is_active == True
        ).order_by(Skill.salary_impact.desc()).limit(10).all()
        
        return [skill.to_dict() for skill in skills]
    
    async def _get_entrepreneurship_opportunities(self) -> List[Dict[str, Any]]:
        """Get sectors with high entrepreneurship potential"""
        sectors = self.db_session.query(JobSector).filter(
            JobSector.entrepreneurship_score >= 70,
            JobSector.is_active == True
        ).order_by(JobSector.entrepreneurship_score.desc()).limit(5).all()
        
        opportunities = []
        for sector in sectors:
            sector_data = sector.to_dict()
            sector_data["startup_recommendations"] = self._get_startup_recommendations(sector)
            opportunities.append(sector_data)
        
        return opportunities
    
    def _get_startup_recommendations(self, sector: JobSector) -> List[str]:
        """Get startup recommendations for a sector"""
        recommendations = []
        
        if sector.startup_capital_required:
            capital_levels = sector.startup_capital_required
            if capital_levels.get("low"):
                recommendations.append("Consider low-capital digital services")
            if capital_levels.get("medium"):
                recommendations.append("Explore medium-investment manufacturing")
            if capital_levels.get("high"):
                recommendations.append("Plan for high-capital infrastructure projects")
        
        if sector.entrepreneurship_score >= 80:
            recommendations.append("Excellent entrepreneurship potential - consider business incubators")
        
        return recommendations
    
    async def _get_government_priority_sectors(self) -> List[Dict[str, Any]]:
        """Get sectors prioritized by government"""
        sectors = self.db_session.query(JobSector).filter(
            JobSector.government_priority == True,
            JobSector.is_active == True
        ).order_by(JobSector.contribution_to_gdp.desc()).all()
        
        return [sector.to_dict() for sector in sectors]
    
    async def _calculate_salary_expectations(self, programs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate salary expectations for programs"""
        salary_data = {
            "program_salaries": {},
            "sector_averages": {},
            "overall_range": {"min": 150000, "max": 2000000}  # FCFA
        }
        
        # Get sector salary averages
        sectors = self.db_session.query(JobSector).filter(
            JobSector.average_salary_range.isnot(None),
            JobSector.is_active == True
        ).all()
        
        for sector in sectors:
            if sector.average_salary_range:
                salary_data["sector_averages"][sector.name] = sector.average_salary_range
        
        # Calculate program-specific salary expectations
        for program in programs:
            career_prospects = program.get("career_prospects", [])
            if career_prospects:
                program_salary = self._estimate_program_salary(career_prospects)
                salary_data["program_salaries"][program.get("id")] = program_salary
        
        return salary_data
    
    def _estimate_program_salary(self, career_prospects: List[str]) -> Dict[str, int]:
        """Estimate salary range for a program based on career prospects"""
        # Default salary ranges by career type (in FCFA)
        salary_estimates = {
            "Software Developer": {"entry": 300000, "mid": 800000, "senior": 1500000},
            "Engineer": {"entry": 350000, "mid": 900000, "senior": 1800000},
            "Medical Doctor": {"entry": 500000, "mid": 1200000, "senior": 2500000},
            "Business Manager": {"entry": 250000, "mid": 700000, "senior": 1500000},
            "Teacher": {"entry": 150000, "mid": 300000, "senior": 600000},
            "Lawyer": {"entry": 300000, "mid": 800000, "senior": 2000000}
        }
        
        # Find matching careers and calculate average
        total_entry = 0
        total_mid = 0
        total_senior = 0
        match_count = 0
        
        for career in career_prospects:
            for key, salary_range in salary_estimates.items():
                if key.lower() in career.lower():
                    total_entry += salary_range["entry"]
                    total_mid += salary_range["mid"]
                    total_senior += salary_range["senior"]
                    match_count += 1
                    break
        
        if match_count > 0:
            return {
                "entry": int(total_entry / match_count),
                "mid": int(total_mid / match_count),
                "senior": int(total_senior / match_count)
            }
        else:
            # Default range
            return {"entry": 200000, "mid": 500000, "senior": 1000000}
    
    async def _get_career_paths(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get career paths with optional filtering"""
        filters = request.get("filters", {})
        
        query = self.db_session.query(CareerPath).filter(CareerPath.is_active == True)
        
        if filters.get("sector_id"):
            query = query.filter(CareerPath.sector_id == filters["sector_id"])
        
        career_paths = query.all()
        
        return {
            "success": True,
            "career_paths": [path.to_dict() for path in career_paths],
            "total_found": len(career_paths)
        }
    
    async def _get_skills_demand(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get skills demand analysis"""
        filters = request.get("filters", {})
        
        query = self.db_session.query(Skill).filter(Skill.is_active == True)
        
        if filters.get("category"):
            query = query.filter(Skill.category == filters["category"])
        
        if filters.get("trend"):
            query = query.filter(Skill.trend == filters["trend"])
        
        skills = query.order_by(Skill.salary_impact.desc()).all()
        
        return {
            "success": True,
            "skills": [skill.to_dict() for skill in skills],
            "total_found": len(skills)
        }
    
    async def _get_sector_insights(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed sector insights"""
        sector_id = request.get("sector_id")
        
        if sector_id:
            sector = self.db_session.query(JobSector).filter(
                JobSector.id == sector_id,
                JobSector.is_active == True
            ).first()
            
            if not sector:
                return {"success": False, "error": "Sector not found"}
            
            return {
                "success": True,
                "sector": sector.to_dict()
            }
        else:
            sectors = self.db_session.query(JobSector).filter(
                JobSector.is_active == True
            ).all()
            
            return {
                "success": True,
                "sectors": [sector.to_dict() for sector in sectors],
                "total_found": len(sectors)
            }
    
    async def _ensure_sample_data(self):
        """Ensure sample job market data exists in database"""
        # Check if sample data already exists
        if self.db_session.query(JobSector).count() > 0:
            return
        
        # Create sample job sectors
        job_sectors = [
            {
                "name": "Information Technology",
                "name_fr": "Technologies de l'Information",
                "description": "Software development, IT services, and digital innovation",
                "description_fr": "Développement logiciel, services IT et innovation numérique",
                "growth_rate": 8.5,
                "employment_size": 50000,
                "demand_level": "very_high",
                "skill_shortage": True,
                "contribution_to_gdp": 3.2,
                "average_salary_range": {"min": 300000, "max": 1500000},
                "entrepreneurship_score": 85,
                "startup_capital_required": {"low": True, "medium": True, "high": False},
                "related_programs": ["UY1_CS_BSC"],
                "required_skills": ["Programming", "Problem Solving", "Database Management"],
                "government_priority": True,
                "development_programs": ["Digital Cameroon 2020", "Tech Hubs Initiative"]
            },
            {
                "name": "Healthcare",
                "name_fr": "Santé",
                "description": "Medical services, pharmaceuticals, and health technology",
                "description_fr": "Services médicaux, pharmaceutiques et technologie de santé",
                "growth_rate": 6.2,
                "employment_size": 120000,
                "demand_level": "very_high",
                "skill_shortage": True,
                "contribution_to_gdp": 5.8,
                "average_salary_range": {"min": 400000, "max": 2500000},
                "entrepreneurship_score": 65,
                "startup_capital_required": {"low": False, "medium": True, "high": True},
                "related_programs": ["UY1_MED_MD"],
                "required_skills": ["Medical Knowledge", "Patient Care", "Diagnostics"],
                "government_priority": True,
                "development_programs": ["Universal Health Coverage", "Telemedicine Initiative"]
            },
            {
                "name": "Agriculture & Agribusiness",
                "name_fr": "Agriculture et Agrobusiness",
                "description": "Modern farming, food processing, and agricultural technology",
                "description_fr": "Agriculture moderne, transformation alimentaire et technologie agricole",
                "growth_rate": 4.8,
                "employment_size": 800000,
                "demand_level": "high",
                "skill_shortage": False,
                "contribution_to_gdp": 18.5,
                "average_salary_range": {"min": 150000, "max": 800000},
                "entrepreneurship_score": 90,
                "startup_capital_required": {"low": True, "medium": True, "high": True},
                "related_programs": [],
                "required_skills": ["Agricultural Science", "Business Management", "Marketing"],
                "government_priority": True,
                "development_programs": ["Agriculture Modernization", "Rural Development"]
            },
            {
                "name": "Manufacturing",
                "name_fr": "Industrie Manufacturière",
                "description": "Industrial production, textiles, and manufacturing processes",
                "description_fr": "Production industrielle, textiles et processus de fabrication",
                "growth_rate": 3.5,
                "employment_size": 200000,
                "demand_level": "medium",
                "skill_shortage": False,
                "contribution_to_gdp": 12.3,
                "average_salary_range": {"min": 180000, "max": 600000},
                "entrepreneurship_score": 70,
                "startup_capital_required": {"low": False, "medium": True, "high": True},
                "related_programs": ["UB_ENG_BSC"],
                "required_skills": ["Technical Skills", "Quality Control", "Operations Management"],
                "government_priority": False,
                "development_programs": ["Industrial Development Plan"]
            }
        ]
        
        # Insert job sectors
        for sector_data in job_sectors:
            sector = JobSector(**sector_data)
            self.db_session.add(sector)
        
        self.db_session.commit()
        
        # Create sample skills
        skills = [
            {
                "name": "Python Programming",
                "name_fr": "Programmation Python",
                "category": "technical",
                "description": "Programming in Python language for various applications",
                "demand_level": "very_high",
                "trend": "growing",
                "difficulty_level": "intermediate",
                "learning_time_months": 6,
                "certification_available": True,
                "salary_impact": 25.0,
                "freelance_potential": True,
                "remote_work_compatible": True,
                "related_sectors": [1],  # IT sector
                "tools_technologies": ["Django", "Flask", "NumPy", "Pandas"]
            },
            {
                "name": "Digital Marketing",
                "name_fr": "Marketing Numérique",
                "category": "creative",
                "description": "Online marketing strategies and digital advertising",
                "demand_level": "high",
                "trend": "growing",
                "difficulty_level": "beginner",
                "learning_time_months": 3,
                "certification_available": True,
                "salary_impact": 15.0,
                "freelance_potential": True,
                "remote_work_compatible": True,
                "related_sectors": [1, 3],  # IT and Agriculture
                "tools_technologies": ["Google Analytics", "Facebook Ads", "SEO Tools"]
            },
            {
                "name": "Project Management",
                "name_fr": "Gestion de Projet",
                "category": "soft",
                "description": "Planning, executing, and managing projects effectively",
                "demand_level": "high",
                "trend": "stable",
                "difficulty_level": "intermediate",
                "learning_time_months": 4,
                "certification_available": True,
                "salary_impact": 20.0,
                "freelance_potential": False,
                "remote_work_compatible": True,
                "related_sectors": [1, 4],  # IT and Manufacturing
                "tools_technologies": ["MS Project", "Asana", "Trello"]
            }
        ]
        
        # Insert skills
        for skill_data in skills:
            skill = Skill(**skill_data)
            self.db_session.add(skill)
        
        self.db_session.commit()
        
        # Create sample career paths
        career_paths = [
            {
                "name": "Software Developer",
                "name_fr": "Développeur Logiciel",
                "description": "Design and develop software applications",
                "sector_id": 1,  # IT sector
                "entry_level_positions": ["Junior Developer", "Programmer Trainee"],
                "mid_level_positions": ["Software Developer", "Full Stack Developer"],
                "senior_level_positions": ["Senior Developer", "Tech Lead", "Software Architect"],
                "required_education": ["Bachelor in Computer Science", "Software Engineering"],
                "required_skills": ["Programming", "Problem Solving", "Debugging"],
                "preferred_skills": ["Cloud Computing", "Mobile Development", "AI/ML"],
                "entry_salary_range": {"min": 300000, "max": 500000},
                "mid_salary_range": {"min": 600000, "max": 1000000},
                "senior_salary_range": {"min": 1200000, "max": 2000000},
                "job_availability": "high",
                "work_life_balance": 70,
                "stress_level": 60,
                "creativity_required": 80,
                "travel_required": False
            },
            {
                "name": "Medical Doctor",
                "name_fr": "Médecin",
                "description": "Diagnose and treat patients, provide medical care",
                "sector_id": 2,  # Healthcare sector
                "entry_level_positions": ["Intern Doctor", "Resident"],
                "mid_level_positions": ["General Practitioner", "Specialist"],
                "senior_level_positions": ["Consultant", "Department Head", "Medical Director"],
                "required_education": ["Doctor of Medicine"],
                "required_skills": ["Medical Knowledge", "Patient Care", "Diagnostics"],
                "preferred_skills": ["Surgical Skills", "Research", "Leadership"],
                "entry_salary_range": {"min": 500000, "max": 800000},
                "mid_salary_range": {"min": 1000000, "max": 1800000},
                "senior_salary_range": {"min": 2000000, "max": 3500000},
                "job_availability": "very_high",
                "work_life_balance": 40,
                "stress_level": 90,
                "creativity_required": 60,
                "travel_required": False
            }
        ]
        
        # Insert career paths
        for path_data in career_paths:
            career_path = CareerPath(**path_data)
            self.db_session.add(career_path)
        
        self.db_session.commit()
        self.logger.info("Sample job market data created successfully")
