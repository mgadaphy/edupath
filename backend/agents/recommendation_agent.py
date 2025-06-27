from typing import Dict, Any, List, Tuple
import random
from datetime import datetime

from .base_agent import BaseAgent
from database.connection import SessionLocal
from models.recommendation import Recommendation, RecommendationSession


class RecommendationAgent(BaseAgent):
    """
    Core recommendation agent that synthesizes data from all other agents
    to generate personalized academic and career recommendations.
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description)
        self.db_session = None
        self.recommendation_weights = {
            "academic_fit": 0.35,      # How well student fits program requirements
            "career_prospects": 0.25,  # Job market demand and opportunities
            "salary_potential": 0.15,  # Expected earning potential
            "entrepreneurship": 0.10,  # Self-employment opportunities
            "personal_interest": 0.10, # Alignment with student interests
            "accessibility": 0.05      # Program accessibility (fees, location)
        }
    
    async def _initialize_resources(self):
        """Initialize database connection"""
        self.db_session = SessionLocal()
        self.logger.info("Database session initialized for RecommendationAgent")
    
    async def _cleanup_resources(self):
        """Cleanup database connection"""
        if self.db_session:
            self.db_session.close()
            self.db_session = None
    
    def get_required_fields(self) -> List[str]:
        return ["action"]
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process recommendation related requests"""
        action = request["action"]
        
        if action == "generate_recommendations":
            return await self._generate_recommendations(request)
        elif action == "rank_programs":
            return await self._rank_programs(request)
        elif action == "explain_recommendation":
            return await self._explain_recommendation(request)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def _generate_recommendations(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive recommendations for a student"""
        student_profile = request.get("student_profile", {})
        university_programs = request.get("university_programs", [])
        job_insights = request.get("job_insights", {})
        session_id = request.get("session_id")
        
        if not university_programs:
            return {
                "success": False,
                "error": "No university programs provided for analysis",
                "recommendations": []
            }
        
        # Generate recommendations for each program
        recommendations = []
        
        for i, program in enumerate(university_programs):
            recommendation = await self._analyze_program_recommendation(
                student_profile=student_profile,
                program=program,
                job_insights=job_insights,
                ranking_position=i + 1
            )
            
            if recommendation:
                recommendations.append(recommendation)
        
        # Sort recommendations by match score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        # Update ranking positions
        for i, rec in enumerate(recommendations):
            rec["ranking_position"] = i + 1
        
        # Store recommendations in database
        if session_id:
            await self._store_recommendations(session_id, student_profile, recommendations)
        
        # Take top 10 recommendations
        top_recommendations = recommendations[:10]
        
        return {
            "success": True,
            "recommendations": top_recommendations,
            "total_analyzed": len(university_programs),
            "total_recommended": len(top_recommendations)
        }
    
    async def _analyze_program_recommendation(
        self, 
        student_profile: Dict[str, Any], 
        program: Dict[str, Any], 
        job_insights: Dict[str, Any],
        ranking_position: int
    ) -> Dict[str, Any]:
        """Analyze a single program and generate detailed recommendation"""
        
        # Get program eligibility from university agent
        eligibility = program.get("eligibility", {})
        
        if not eligibility.get("eligible", False):
            # Skip ineligible programs
            return None
        
        # Calculate component scores
        scores = {
            "academic_fit": self._calculate_academic_fit_score(student_profile, program, eligibility),
            "career_prospects": self._calculate_career_prospects_score(program, job_insights),
            "salary_potential": self._calculate_salary_potential_score(program, job_insights),
            "entrepreneurship": self._calculate_entrepreneurship_score(program, job_insights),
            "personal_interest": self._calculate_personal_interest_score(student_profile, program),
            "accessibility": self._calculate_accessibility_score(student_profile, program)
        }
        
        # Calculate weighted match score
        match_score = sum(
            scores[component] * weight 
            for component, weight in self.recommendation_weights.items()
        )
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(scores, eligibility)
        
        # Generate recommendation reasoning
        reasoning = self._generate_recommendation_reasoning(scores, eligibility, program)
        
        # Get career information
        career_info = self._extract_career_information(program, job_insights)
        
        # Generate preparation guidance
        preparation = self._generate_preparation_guidance(student_profile, program, eligibility)
        
        recommendation = {
            "program_id": program.get("id"),
            "program_name": program.get("name"),
            "program_code": program.get("code"),
            "university_name": program.get("university", {}).get("name", "Unknown University"),
            "degree_type": program.get("degree_type"),
            "duration_years": program.get("duration_years"),
            "faculty": program.get("faculty"),
            "match_score": round(match_score, 2),
            "confidence_score": round(confidence_score, 2),
            "ranking_position": ranking_position,
            
            # Detailed scores
            "component_scores": scores,
            
            # Eligibility information
            "eligibility": eligibility,
            
            # Reasoning
            "reasons": reasoning["reasons"],
            "pros": reasoning["pros"],
            "cons": reasoning["cons"],
            "requirements_met": reasoning["requirements_met"],
            "requirements_missing": reasoning["requirements_missing"],
            
            # Career information
            "career_prospects": career_info["prospects"],
            "employment_outlook": career_info["outlook"],
            "salary_expectations": career_info["salary"],
            
            # Preparation guidance
            "preparation_tips": preparation["tips"],
            "recommended_subjects": preparation["subjects"],
            "skill_gaps": preparation["skills"],
            
            # Alternative options
            "alternative_programs": [],  # To be filled by other analysis
            "fallback_options": []       # To be filled by other analysis
        }
        
        return recommendation
    
    def _calculate_academic_fit_score(
        self, 
        student_profile: Dict[str, Any], 
        program: Dict[str, Any], 
        eligibility: Dict[str, Any]
    ) -> float:
        """Calculate how well student fits academically"""
        base_score = eligibility.get("score", 0)
        
        # Bonus for exceeding requirements
        if eligibility.get("eligible", False) and not eligibility.get("missing_requirements"):
            base_score += 20
        
        # Subject alignment bonus
        required_subjects = program.get("required_subjects", [])
        if required_subjects:
            student_subjects = set()
            if student_profile.get("ol_results"):
                student_subjects.update(student_profile["ol_results"].keys())
            if student_profile.get("al_results"):
                student_subjects.update(student_profile["al_results"].keys())
            if student_profile.get("bac_results"):
                student_subjects.update(student_profile["bac_results"].keys())
            
            subject_match_ratio = len(set(required_subjects) & student_subjects) / len(required_subjects)
            base_score += subject_match_ratio * 15
        
        return min(100, base_score)
    
    def _calculate_career_prospects_score(
        self, 
        program: Dict[str, Any], 
        job_insights: Dict[str, Any]
    ) -> float:
        """Calculate career prospects score based on job market"""
        program_id = program.get("id")
        career_outlook = job_insights.get("career_outlook", {}).get(str(program_id), {})
        
        base_score = 50  # Default medium score
        
        # Demand level scoring
        demand_level = career_outlook.get("average_demand", "medium")
        demand_scores = {"low": 25, "medium": 50, "high": 75, "very_high": 100}
        base_score = demand_scores.get(demand_level, 50)
        
        # Growth potential bonus
        growth_potential = career_outlook.get("growth_potential", "stable")
        if growth_potential == "growing":
            base_score += 20
        elif growth_potential == "declining":
            base_score -= 20
        
        # Employment rate bonus (if available)
        employment_rate = program.get("employment_rate")
        if employment_rate:
            if employment_rate >= 80:
                base_score += 15
            elif employment_rate >= 60:
                base_score += 10
            else:
                base_score -= 10
        
        return min(100, max(0, base_score))
    
    def _calculate_salary_potential_score(
        self, 
        program: Dict[str, Any], 
        job_insights: Dict[str, Any]
    ) -> float:
        """Calculate salary potential score"""
        salary_expectations = job_insights.get("salary_expectations", {})
        program_salaries = salary_expectations.get("program_salaries", {})
        program_id = str(program.get("id", ""))
        
        if program_id in program_salaries:
            salary_data = program_salaries[program_id]
            # Score based on mid-career salary
            mid_salary = salary_data.get("mid", 500000)
            
            if mid_salary >= 1200000:
                return 100
            elif mid_salary >= 800000:
                return 80
            elif mid_salary >= 500000:
                return 60
            elif mid_salary >= 300000:
                return 40
            else:
                return 20
        
        # Use program's own salary data if available
        avg_salary = program.get("average_starting_salary")
        if avg_salary:
            if avg_salary >= 800000:
                return 90
            elif avg_salary >= 500000:
                return 70
            elif avg_salary >= 300000:
                return 50
            else:
                return 30
        
        return 50  # Default score
    
    def _calculate_entrepreneurship_score(
        self, 
        program: Dict[str, Any], 
        job_insights: Dict[str, Any]
    ) -> float:
        """Calculate entrepreneurship potential score"""
        program_id = program.get("id")
        career_outlook = job_insights.get("career_outlook", {}).get(str(program_id), {})
        
        entrepreneurship_score = career_outlook.get("entrepreneurship_score", 50)
        
        # Bonus for programs with high business potential
        career_prospects = program.get("career_prospects", [])
        business_keywords = ["entrepreneur", "business", "manager", "consultant", "analyst"]
        
        business_alignment = sum(
            1 for prospect in career_prospects 
            for keyword in business_keywords 
            if keyword.lower() in prospect.lower()
        )
        
        if business_alignment > 0:
            entrepreneurship_score += business_alignment * 10
        
        return min(100, entrepreneurship_score)
    
    def _calculate_personal_interest_score(
        self, 
        student_profile: Dict[str, Any], 
        program: Dict[str, Any]
    ) -> float:
        """Calculate alignment with student interests"""
        interests = student_profile.get("interests", [])
        career_preferences = student_profile.get("career_preferences", [])
        
        if not interests and not career_preferences:
            return 50  # Neutral score if no preferences
        
        score = 50
        
        # Match with program name and description
        program_text = f"{program.get('name', '')} {program.get('description', '')}".lower()
        
        # Check interest alignment
        for interest in interests:
            if interest.lower() in program_text:
                score += 15
        
        # Check career preference alignment
        career_prospects = program.get("career_prospects", [])
        for preference in career_preferences:
            for prospect in career_prospects:
                if preference.lower() in prospect.lower():
                    score += 20
                    break
        
        return min(100, score)
    
    def _calculate_accessibility_score(
        self, 
        student_profile: Dict[str, Any], 
        program: Dict[str, Any]
    ) -> float:
        """Calculate program accessibility (cost, location, etc.)"""
        score = 70  # Base accessibility score
        
        # Cost consideration
        tuition_fee = program.get("tuition_fee_fcfa", 0)
        if tuition_fee:
            if tuition_fee <= 50000:
                score += 20  # Very affordable
            elif tuition_fee <= 100000:
                score += 10  # Affordable
            elif tuition_fee <= 200000:
                score += 0   # Moderate
            else:
                score -= 15  # Expensive
        
        # Location preference
        location_preferences = student_profile.get("location_preferences", [])
        university = program.get("university", {})
        university_region = university.get("region", "")
        
        if location_preferences and university_region:
            if any(pref.lower() in university_region.lower() for pref in location_preferences):
                score += 15
        
        # Language compatibility
        language_pref = student_profile.get("language_preference", "en")
        program_language = program.get("language_instruction", "bilingual")
        
        if program_language == "bilingual" or language_pref in program_language:
            score += 10
        
        # Competitive program penalty
        if program.get("is_competitive", False):
            score -= 10
        
        # Entrance exam penalty
        if program.get("entrance_exam_required", False):
            score -= 10
        
        return min(100, max(0, score))
    
    def _calculate_confidence_score(
        self, 
        scores: Dict[str, float], 
        eligibility: Dict[str, Any]
    ) -> float:
        """Calculate confidence in the recommendation"""
        # Base confidence from eligibility
        if eligibility.get("eligible", False):
            if not eligibility.get("missing_requirements"):
                base_confidence = 80
            else:
                base_confidence = 60
        else:
            base_confidence = 30
        
        # Variance in scores - lower variance means higher confidence
        score_values = list(scores.values())
        if score_values:
            avg_score = sum(score_values) / len(score_values)
            variance = sum((score - avg_score) ** 2 for score in score_values) / len(score_values)
            
            # Lower variance increases confidence
            variance_penalty = min(20, variance / 100)
            base_confidence -= variance_penalty
        
        # High scores increase confidence
        high_score_bonus = sum(1 for score in score_values if score >= 80) * 5
        base_confidence += high_score_bonus
        
        return min(100, max(10, base_confidence))
    
    def _generate_recommendation_reasoning(
        self, 
        scores: Dict[str, float], 
        eligibility: Dict[str, Any], 
        program: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate human-readable reasoning for the recommendation"""
        reasons = []
        pros = []
        cons = []
        requirements_met = eligibility.get("match_reasons", [])
        requirements_missing = eligibility.get("missing_requirements", [])
        
        # Academic fit reasons
        if scores["academic_fit"] >= 80:
            reasons.append("Excellent academic fit based on your grades and subjects")
            pros.append("You meet or exceed all academic requirements")
        elif scores["academic_fit"] >= 60:
            reasons.append("Good academic match with your current qualifications")
        else:
            cons.append("Academic requirements may be challenging to meet")
        
        # Career prospects reasons
        if scores["career_prospects"] >= 80:
            reasons.append("Outstanding career opportunities in this field")
            pros.append("High demand for graduates in the job market")
        elif scores["career_prospects"] >= 60:
            reasons.append("Good employment prospects after graduation")
        else:
            cons.append("Limited job opportunities in this field")
        
        # Salary potential reasons
        if scores["salary_potential"] >= 80:
            pros.append("High earning potential throughout your career")
        elif scores["salary_potential"] >= 60:
            pros.append("Good salary expectations for graduates")
        else:
            cons.append("Below-average salary expectations")
        
        # Entrepreneurship reasons
        if scores["entrepreneurship"] >= 70:
            reasons.append("Great potential for starting your own business")
            pros.append("Skills gained are valuable for entrepreneurship")
        
        # Personal interest alignment
        if scores["personal_interest"] >= 70:
            reasons.append("Aligns well with your interests and career goals")
            pros.append("You're likely to enjoy studying and working in this field")
        
        # Accessibility considerations
        if scores["accessibility"] >= 70:
            pros.append("Accessible program with reasonable requirements")
        else:
            cons.append("May have accessibility challenges (cost, location, or competition)")
        
        # Program-specific pros and cons
        if program.get("is_competitive"):
            cons.append("Highly competitive admission process")
        
        if program.get("entrance_exam_required"):
            cons.append("Requires entrance examination")
        
        tuition_fee = program.get("tuition_fee_fcfa", 0)
        if tuition_fee <= 50000:
            pros.append("Very affordable tuition fees")
        elif tuition_fee >= 200000:
            cons.append("High tuition fees")
        
        return {
            "reasons": reasons,
            "pros": pros,
            "cons": cons,
            "requirements_met": requirements_met,
            "requirements_missing": requirements_missing
        }
    
    def _extract_career_information(
        self, 
        program: Dict[str, Any], 
        job_insights: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Extract and format career information"""
        program_id = str(program.get("id", ""))
        career_outlook = job_insights.get("career_outlook", {}).get(program_id, {})
        salary_expectations = job_insights.get("salary_expectations", {})
        
        career_prospects = program.get("career_prospects", [])
        
        # Employment outlook
        demand_level = career_outlook.get("average_demand", "medium")
        growth_potential = career_outlook.get("growth_potential", "stable")
        
        outlook_map = {
            ("very_high", "growing"): "Excellent",
            ("high", "growing"): "Very Good",
            ("medium", "growing"): "Good",
            ("very_high", "stable"): "Very Good",
            ("high", "stable"): "Good",
            ("medium", "stable"): "Fair",
            ("low", "stable"): "Limited",
            ("low", "declining"): "Poor"
        }
        
        employment_outlook = outlook_map.get((demand_level, growth_potential), "Fair")
        
        # Salary information
        program_salaries = salary_expectations.get("program_salaries", {}).get(program_id, {})
        
        return {
            "prospects": career_prospects,
            "outlook": employment_outlook,
            "salary": program_salaries
        }
    
    def _generate_preparation_guidance(
        self, 
        student_profile: Dict[str, Any], 
        program: Dict[str, Any], 
        eligibility: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Generate preparation guidance for the student"""
        tips = []
        subjects = []
        skills = []
        
        # Academic preparation
        missing_requirements = eligibility.get("missing_requirements", [])
        for requirement in missing_requirements:
            if "points" in requirement.lower():
                tips.append("Focus on improving grades in core subjects")
            elif "subject" in requirement.lower():
                subject = requirement.split(": ")[-1] if ": " in requirement else requirement
                subjects.append(subject)
        
        # Subject recommendations
        required_subjects = program.get("required_subjects", [])
        subjects.extend(required_subjects)
        
        # General preparation tips
        if program.get("is_competitive"):
            tips.append("Prepare thoroughly for competitive entrance exams")
            tips.append("Consider taking preparatory courses")
        
        if program.get("entrance_exam_required"):
            tips.append("Practice past entrance exam questions")
            tips.append("Join study groups for exam preparation")
        
        # Skill development
        career_prospects = program.get("career_prospects", [])
        for prospect in career_prospects:
            if "software" in prospect.lower() or "computer" in prospect.lower():
                skills.extend(["Programming", "Problem Solving", "Computer Skills"])
            elif "business" in prospect.lower() or "manager" in prospect.lower():
                skills.extend(["Leadership", "Communication", "Business Analysis"])
            elif "engineer" in prospect.lower():
                skills.extend(["Technical Skills", "Mathematics", "Design Thinking"])
        
        # Remove duplicates
        subjects = list(set(subjects))
        skills = list(set(skills))
        
        return {
            "tips": tips,
            "subjects": subjects,
            "skills": skills
        }
    
    async def _store_recommendations(
        self, 
        session_id: str, 
        student_profile: Dict[str, Any], 
        recommendations: List[Dict[str, Any]]
    ):
        """Store recommendations in database"""
        try:
            # Create recommendation session
            session = RecommendationSession(
                session_id=session_id,
                student_id=student_profile.get("id", 0),
                request_data={"student_profile": student_profile},
                total_recommendations=len(recommendations),
                status="completed"
            )
            
            self.db_session.add(session)
            
            # Store individual recommendations
            for rec_data in recommendations:
                recommendation = Recommendation(
                    student_id=student_profile.get("id", 0),
                    session_id=session_id,
                    program_id=rec_data["program_id"],
                    match_score=rec_data["match_score"],
                    confidence_score=rec_data["confidence_score"],
                    ranking_position=rec_data["ranking_position"],
                    reasons=rec_data["reasons"],
                    pros=rec_data["pros"],
                    cons=rec_data["cons"],
                    requirements_met=rec_data["requirements_met"],
                    requirements_missing=rec_data["requirements_missing"],
                    career_prospects=rec_data["career_prospects"],
                    employment_outlook=rec_data["employment_outlook"],
                    salary_expectations=rec_data["salary_expectations"],
                    preparation_tips=rec_data["preparation_tips"],
                    recommended_subjects=rec_data["recommended_subjects"],
                    skill_gaps=rec_data["skill_gaps"]
                )
                
                self.db_session.add(recommendation)
            
            self.db_session.commit()
            self.logger.info(f"Stored {len(recommendations)} recommendations for session {session_id}")
            
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Failed to store recommendations: {e}")
    
    async def _rank_programs(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Rank programs based on criteria"""
        # Implementation for program ranking
        return {"success": True, "message": "Program ranking not implemented yet"}
    
    async def _explain_recommendation(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Provide detailed explanation for a specific recommendation"""
        # Implementation for recommendation explanation
        return {"success": True, "message": "Recommendation explanation not implemented yet"}
