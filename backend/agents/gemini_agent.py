from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime

from .base_agent import LLMAgent
from database.connection import get_redis


class GeminiAgent(LLMAgent):
    """
    Agent responsible for enhancing recommendations with AI-generated content
    using Google Gemini for personalized study guides, career advice, and content generation.
    """
    
    def __init__(self, agent_id: str, name: str, description: str):
        super().__init__(agent_id, name, description)
        self.redis_client = None
        self.cache_ttl = 3600  # 1 hour cache TTL
    
    async def _initialize_resources(self):
        """Initialize Gemini client and Redis cache"""
        await super()._initialize_resources()
        self.redis_client = await get_redis()
        self.logger.info("Gemini agent resources initialized")
    
    async def _cleanup_resources(self):
        """Cleanup resources"""
        await super()._cleanup_resources()
        self.redis_client = None
    
    def get_required_fields(self) -> List[str]:
        return ["action"]
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process Gemini-related requests"""
        action = request["action"]
        
        if action == "enhance_recommendations":
            return await self._enhance_recommendations(request)
        elif action == "generate_study_guide":
            return await self._generate_study_guide(request)
        elif action == "generate_career_advice":
            return await self._generate_career_advice(request)
        elif action == "generate_mock_interview":
            return await self._generate_mock_interview(request)
        elif action == "generate_preparation_plan":
            return await self._generate_preparation_plan(request)
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def _enhance_recommendations(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance recommendations with AI-generated content"""
        student_profile = request.get("student_profile", {})
        recommendations = request.get("recommendations", [])
        language = request.get("language", "en")
        session_id = request.get("session_id")
        
        if not self.llm_client:
            # Return without enhancement if Gemini is not available
            return {
                "success": True,
                "enhanced_content": {
                    "general_advice": "Focus on your strengths and interests when choosing your academic path.",
                    "recommendations": []
                },
                "note": "AI enhancement not available - using fallback content"
            }
        
        enhanced_content = {
            "general_advice": "",
            "study_tips": [],
            "career_planning": "",
            "recommendations": []
        }
        
        try:
            # Generate general advice for the student
            general_advice = await self._generate_general_advice(student_profile, language)
            enhanced_content["general_advice"] = general_advice
            
            # Generate study tips
            study_tips = await self._generate_study_tips(student_profile, language)
            enhanced_content["study_tips"] = study_tips
            
            # Generate career planning advice
            career_planning = await self._generate_career_planning_advice(student_profile, language)
            enhanced_content["career_planning"] = career_planning
            
            # Enhance top 3 recommendations with detailed content
            for i, recommendation in enumerate(recommendations[:3]):
                enhanced_rec = await self._enhance_single_recommendation(
                    recommendation, student_profile, language
                )
                enhanced_content["recommendations"].append(enhanced_rec)
            
            return {
                "success": True,
                "enhanced_content": enhanced_content
            }
            
        except Exception as e:
            self.logger.error(f"Enhancement failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "enhanced_content": enhanced_content  # Return partial content
            }
    
    async def _generate_general_advice(self, student_profile: Dict[str, Any], language: str) -> str:
        """Generate general advice for the student"""
        cache_key = f"general_advice:{self._hash_profile(student_profile)}:{language}"
        
        # Check cache first
        cached_content = await self._get_cached_content(cache_key)
        if cached_content:
            return cached_content
        
        # Prepare context
        exam_system = student_profile.get("exam_system", "unknown")
        interests = student_profile.get("interests", [])
        career_prefs = student_profile.get("career_preferences", [])
        
        if language == "fr":
            prompt = f"""
            En tant que conseiller éducatif expert au Cameroun, donnez des conseils personnalisés à un étudiant avec le profil suivant:
            
            Système d'examen: {exam_system}
            Intérêts: {', '.join(interests) if interests else 'Non spécifiés'}
            Préférences de carrière: {', '.join(career_prefs) if career_prefs else 'Non spécifiées'}
            
            Donnez des conseils encourageants et pratiques en 2-3 paragraphes sur:
            1. Comment tirer parti de leurs forces académiques
            2. L'importance de l'exploration de carrière
            3. Des conseils spécifiques au contexte camerounais
            
            Répondez en français, soyez positif et motivant.
            """
        else:
            prompt = f"""
            As an expert educational counselor in Cameroon, provide personalized advice for a student with this profile:
            
            Exam system: {exam_system}
            Interests: {', '.join(interests) if interests else 'Not specified'}
            Career preferences: {', '.join(career_prefs) if career_prefs else 'Not specified'}
            
            Provide encouraging and practical advice in 2-3 paragraphs covering:
            1. How to leverage their academic strengths
            2. The importance of career exploration
            3. Specific advice for the Cameroonian context
            
            Be positive and motivating in your response.
            """
        
        content = await self.generate_content(prompt)
        if content:
            await self._cache_content(cache_key, content)
            return content
        
        # Fallback content
        if language == "fr":
            return "Votre parcours éducatif est unique. Concentrez-vous sur vos forces et explorez les opportunités qui correspondent à vos intérêts. Le Cameroun offre de nombreuses possibilités pour les étudiants motivés."
        else:
            return "Your educational journey is unique. Focus on your strengths and explore opportunities that align with your interests. Cameroon offers many possibilities for motivated students."
    
    async def _generate_study_tips(self, student_profile: Dict[str, Any], language: str) -> List[str]:
        """Generate study tips for the student"""
        cache_key = f"study_tips:{self._hash_profile(student_profile)}:{language}"
        
        cached_content = await self._get_cached_content(cache_key)
        if cached_content:
            return json.loads(cached_content)
        
        exam_system = student_profile.get("exam_system", "unknown")
        
        if language == "fr":
            prompt = f"""
            Donnez 5 conseils d'étude spécifiques pour un étudiant camerounais utilisant le système {exam_system}.
            
            Formatez votre réponse comme une liste JSON de 5 conseils pratiques et actionables.
            Exemple: ["Conseil 1", "Conseil 2", "Conseil 3", "Conseil 4", "Conseil 5"]
            
            Concentrez-vous sur des stratégies d'étude efficaces, la gestion du temps, et la préparation aux examens.
            """
        else:
            prompt = f"""
            Provide 5 specific study tips for a Cameroonian student using the {exam_system} system.
            
            Format your response as a JSON list of 5 practical and actionable tips.
            Example: ["Tip 1", "Tip 2", "Tip 3", "Tip 4", "Tip 5"]
            
            Focus on effective study strategies, time management, and exam preparation.
            """
        
        content = await self.generate_content(prompt)
        if content:
            try:
                # Extract JSON from content
                import re
                json_match = re.search(r'\[.*\]', content, re.DOTALL)
                if json_match:
                    tips = json.loads(json_match.group())
                    await self._cache_content(cache_key, json.dumps(tips))
                    return tips
            except:
                pass
        
        # Fallback tips
        if language == "fr":
            return [
                "Créez un calendrier d'étude régulier",
                "Formez des groupes d'étude avec vos camarades",
                "Pratiquez avec des examens passés",
                "Demandez de l'aide à vos professeurs",
                "Prenez des pauses régulières pendant l'étude"
            ]
        else:
            return [
                "Create a regular study schedule",
                "Form study groups with classmates",
                "Practice with past exam papers",
                "Seek help from your teachers",
                "Take regular breaks while studying"
            ]
    
    async def _generate_career_planning_advice(self, student_profile: Dict[str, Any], language: str) -> str:
        """Generate career planning advice"""
        cache_key = f"career_planning:{self._hash_profile(student_profile)}:{language}"
        
        cached_content = await self._get_cached_content(cache_key)
        if cached_content:
            return cached_content
        
        interests = student_profile.get("interests", [])
        career_prefs = student_profile.get("career_preferences", [])
        
        if language == "fr":
            prompt = f"""
            En tant que conseiller en carrière au Cameroun, donnez des conseils de planification de carrière pour un étudiant avec:
            
            Intérêts: {', '.join(interests) if interests else 'Non spécifiés'}
            Préférences de carrière: {', '.join(career_prefs) if career_prefs else 'Non spécifiées'}
            
            Donnez des conseils pratiques en 2-3 paragraphes sur:
            1. Comment explorer les options de carrière
            2. L'importance du réseautage et de l'expérience pratique
            3. Les opportunités spécifiques au marché du travail camerounais
            
            Soyez pratique et orienté vers l'action.
            """
        else:
            prompt = f"""
            As a career counselor in Cameroon, provide career planning advice for a student with:
            
            Interests: {', '.join(interests) if interests else 'Not specified'}
            Career preferences: {', '.join(career_prefs) if career_prefs else 'Not specified'}
            
            Provide practical advice in 2-3 paragraphs covering:
            1. How to explore career options
            2. The importance of networking and practical experience
            3. Specific opportunities in the Cameroonian job market
            
            Be practical and action-oriented.
            """
        
        content = await self.generate_content(prompt)
        if content:
            await self._cache_content(cache_key, content)
            return content
        
        # Fallback content
        if language == "fr":
            return "Explorez activement différentes carrières à travers des stages, du bénévolat et des conversations avec des professionnels. Construisez votre réseau et acquérez une expérience pratique dès maintenant."
        else:
            return "Actively explore different careers through internships, volunteering, and conversations with professionals. Build your network and gain practical experience early."
    
    async def _enhance_single_recommendation(
        self, 
        recommendation: Dict[str, Any], 
        student_profile: Dict[str, Any], 
        language: str
    ) -> Dict[str, Any]:
        """Enhance a single recommendation with detailed content"""
        program_name = recommendation.get("program_name", "Unknown Program")
        university_name = recommendation.get("university_name", "Unknown University")
        
        cache_key = f"recommendation:{program_name}:{self._hash_profile(student_profile)}:{language}"
        
        cached_content = await self._get_cached_content(cache_key)
        if cached_content:
            try:
                return json.loads(cached_content)
            except:
                pass
        
        enhanced = {
            "personalized_advice": "",
            "study_guide_summary": "",
            "success_tips": [],
            "preparation_checklist": []
        }
        
        try:
            # Generate personalized advice
            if language == "fr":
                advice_prompt = f"""
                Donnez des conseils personnalisés pour un étudiant camerounais considérant {program_name} à {university_name}.
                
                Rédigez un paragraphe motivant et informatif expliquant pourquoi ce programme pourrait être un bon choix et comment réussir.
                Soyez spécifique au contexte camerounais et encourageant.
                """
            else:
                advice_prompt = f"""
                Provide personalized advice for a Cameroonian student considering {program_name} at {university_name}.
                
                Write a motivating and informative paragraph explaining why this program might be a good choice and how to succeed.
                Be specific to the Cameroonian context and encouraging.
                """
            
            advice = await self.generate_content(advice_prompt)
            if advice:
                enhanced["personalized_advice"] = advice.strip()
            
            # Generate study guide summary
            if language == "fr":
                study_prompt = f"""
                Créez un résumé de guide d'étude pour préparer {program_name}.
                
                Donnez 3-4 points clés sur ce qu'il faut étudier et comment se préparer efficacement.
                Soyez concis et pratique.
                """
            else:
                study_prompt = f"""
                Create a study guide summary for preparing for {program_name}.
                
                Provide 3-4 key points on what to study and how to prepare effectively.
                Be concise and practical.
                """
            
            study_guide = await self.generate_content(study_prompt)
            if study_guide:
                enhanced["study_guide_summary"] = study_guide.strip()
            
            # Cache the enhanced content
            await self._cache_content(cache_key, json.dumps(enhanced))
            
        except Exception as e:
            self.logger.error(f"Failed to enhance recommendation {program_name}: {e}")
        
        # Add fallback content if generation failed
        if not enhanced["personalized_advice"]:
            if language == "fr":
                enhanced["personalized_advice"] = f"Ce programme à {university_name} offre d'excellentes opportunités. Concentrez-vous sur vos points forts académiques et préparez-vous soigneusement."
            else:
                enhanced["personalized_advice"] = f"This program at {university_name} offers excellent opportunities. Focus on your academic strengths and prepare thoroughly."
        
        if not enhanced["study_guide_summary"]:
            if language == "fr":
                enhanced["study_guide_summary"] = "Révisez les matières principales, pratiquez les examens passés, et développez les compétences pertinentes pour ce domaine."
            else:
                enhanced["study_guide_summary"] = "Review core subjects, practice past exams, and develop relevant skills for this field."
        
        return enhanced
    
    async def _generate_study_guide(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed study guide for a specific program"""
        program = request.get("program", {})
        student_profile = request.get("student_profile", {})
        language = request.get("language", "en")
        
        if not self.llm_client:
            return {
                "success": False,
                "error": "Gemini service not available"
            }
        
        program_name = program.get("name", "Unknown Program")
        
        try:
            if language == "fr":
                prompt = f"""
                Créez un guide d'étude détaillé pour {program_name} au Cameroun.
                
                Incluez:
                1. Matières principales à maîtriser
                2. Ressources d'étude recommandées
                3. Calendrier de préparation (3-6 mois)
                4. Conseils d'examen spécifiques
                5. Compétences pratiques à développer
                
                Soyez détaillé et pratique.
                """
            else:
                prompt = f"""
                Create a detailed study guide for {program_name} in Cameroon.
                
                Include:
                1. Core subjects to master
                2. Recommended study resources
                3. Preparation timeline (3-6 months)
                4. Specific exam tips
                5. Practical skills to develop
                
                Be detailed and practical.
                """
            
            content = await self.generate_content(prompt)
            
            return {
                "success": True,
                "study_guide": content or "Study guide could not be generated at this time."
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _generate_career_advice(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized career advice"""
        # Implementation for career advice generation
        return {"success": True, "message": "Career advice generation not fully implemented"}
    
    async def _generate_mock_interview(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock interview questions and tips"""
        # Implementation for mock interview generation
        return {"success": True, "message": "Mock interview generation not fully implemented"}
    
    async def _generate_preparation_plan(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a comprehensive preparation plan"""
        # Implementation for preparation plan generation
        return {"success": True, "message": "Preparation plan generation not fully implemented"}
    
    def _hash_profile(self, student_profile: Dict[str, Any]) -> str:
        """Create a hash for caching based on student profile"""
        import hashlib
        
        # Use key profile elements for hashing
        cache_elements = {
            "exam_system": student_profile.get("exam_system", ""),
            "interests": sorted(student_profile.get("interests", [])),
            "career_preferences": sorted(student_profile.get("career_preferences", []))
        }
        
        cache_string = json.dumps(cache_elements, sort_keys=True)
        return hashlib.md5(cache_string.encode()).hexdigest()[:12]
    
    async def _get_cached_content(self, cache_key: str) -> Optional[str]:
        """Get content from Redis cache"""
        if not self.redis_client:
            return None
        
        try:
            content = await self.redis_client.get(f"gemini:{cache_key}")
            return content
        except Exception:
            return None
    
    async def _cache_content(self, cache_key: str, content: str):
        """Store content in Redis cache"""
        if not self.redis_client:
            return
        
        try:
            await self.redis_client.setex(
                f"gemini:{cache_key}", 
                self.cache_ttl, 
                content
            )
        except Exception as e:
            self.logger.warning(f"Failed to cache content: {e}")
