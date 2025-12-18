import sqlite3
import json
from typing import Dict, List, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SkillMappingEngine:
    def __init__(self):
        self.db_path = 'career_advisor.db'
        self.vectorizer = TfidfVectorizer()
        self.skill_vectors = None
        self.skill_names = []
        self._load_skills()
    
    def _load_skills(self):
        """Load skills from database and create vector representations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, description FROM skills')
        skills_data = cursor.fetchall()
        
        self.skill_names = [skill[0] for skill in skills_data]
        skill_descriptions = [f"{skill[0]} {skill[1]}" for skill in skills_data]
        
        if skill_descriptions:
            self.skill_vectors = self.vectorizer.fit_transform(skill_descriptions)
        
        conn.close()
    
    def get_available_skills(self) -> List[Dict[str, str]]:
        """Get all available skills from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, category, description FROM skills ORDER BY category, name')
        skills = cursor.fetchall()
        
        result = []
        for skill in skills:
            result.append({
                'name': skill[0],
                'category': skill[1],
                'description': skill[2]
            })
        
        conn.close()
        return result
    
    def analyze_skills(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze student skills and identify strengths, gaps, and recommendations
        """
        student_skills = student_data.get('skills', [])
        interests = student_data.get('interests', [])
        education = student_data.get('education', '')
        experience = student_data.get('experience', '')
        
        # Get all available skills
        available_skills = self.get_available_skills()
        all_skill_names = [skill['name'] for skill in available_skills]
        
        # Categorize skills
        technical_skills = [skill for skill in available_skills if skill['category'] == 'Technical']
        soft_skills = [skill for skill in available_skills if skill['category'] == 'Soft Skills']
        
        # Find skill matches and gaps
        matched_skills = []
        skill_gaps = []
        
        for skill in available_skills:
            skill_name = skill['name']
            if skill_name in student_skills:
                matched_skills.append(skill)
            else:
                skill_gaps.append(skill)
        
        # Calculate skill strength score
        skill_strength = len(matched_skills) / len(available_skills) * 100
        
        # Find similar skills based on interests
        recommended_skills = self._recommend_skills(student_skills, interests, available_skills)
        
        # Analyze skill distribution
        technical_matches = [s for s in matched_skills if s['category'] == 'Technical']
        soft_matches = [s for s in matched_skills if s['category'] == 'Soft Skills']
        
        return {
            'matched_skills': matched_skills,
            'skill_gaps': skill_gaps[:10],  # Top 10 gaps
            'skill_strength_score': round(skill_strength, 2),
            'technical_skills_count': len(technical_matches),
            'soft_skills_count': len(soft_matches),
            'recommended_skills': recommended_skills,
            'skill_distribution': {
                'technical': len(technical_matches),
                'soft_skills': len(soft_matches),
                'total_available': len(available_skills)
            },
            'strengths': self._identify_strengths(matched_skills),
            'improvement_areas': self._identify_improvement_areas(skill_gaps, interests)
        }
    
    def _recommend_skills(self, current_skills: List[str], interests: List[str], 
                         available_skills: List[Dict]) -> List[Dict]:
        """Recommend skills based on current skills and interests"""
        if not current_skills and not interests:
            return available_skills[:5]  # Return top 5 if no input
        
        # Create a combined text for similarity matching
        combined_text = ' '.join(current_skills + interests)
        
        if not self.skill_vectors is None and combined_text.strip():
            # Vectorize the combined input
            input_vector = self.vectorizer.transform([combined_text])
            
            # Calculate similarities
            similarities = cosine_similarity(input_vector, self.skill_vectors)[0]
            
            # Get top similar skills
            skill_indices = np.argsort(similarities)[::-1]
            recommended = []
            
            for idx in skill_indices:
                if similarities[idx] > 0.1:  # Threshold for relevance
                    skill = available_skills[idx]
                    if skill['name'] not in current_skills:
                        recommended.append({
                            'skill': skill,
                            'similarity_score': round(similarities[idx], 3)
                        })
                        if len(recommended) >= 10:
                            break
            
            return recommended
        
        return available_skills[:5]
    
    def _identify_strengths(self, matched_skills: List[Dict]) -> List[str]:
        """Identify key strengths from matched skills"""
        if not matched_skills:
            return ["No skills assessed yet"]
        
        # Group by category
        technical_count = len([s for s in matched_skills if s['category'] == 'Technical'])
        soft_count = len([s for s in matched_skills if s['category'] == 'Soft Skills'])
        
        strengths = []
        if technical_count > 0:
            strengths.append(f"Strong technical foundation ({technical_count} skills)")
        if soft_count > 0:
            strengths.append(f"Good soft skills development ({soft_count} skills)")
        
        # Add specific skill strengths
        skill_names = [s['name'] for s in matched_skills]
        if 'Python Programming' in skill_names:
            strengths.append("Programming expertise")
        if 'Machine Learning' in skill_names:
            strengths.append("AI/ML knowledge")
        if 'Project Management' in skill_names:
            strengths.append("Leadership capabilities")
        
        return strengths if strengths else ["Building skill foundation"]
    
    def _identify_improvement_areas(self, skill_gaps: List[Dict], interests: List[str]) -> List[str]:
        """Identify key areas for improvement"""
        if not skill_gaps:
            return ["All core skills covered"]
        
        # Prioritize based on interests
        improvement_areas = []
        
        # Check for critical missing skills
        critical_skills = ['Communication', 'Problem Solving', 'Critical Thinking']
        missing_critical = [skill for skill in skill_gaps if skill['name'] in critical_skills]
        
        if missing_critical:
            improvement_areas.append("Essential soft skills development")
        
        # Check for technical gaps
        technical_gaps = [skill for skill in skill_gaps if skill['category'] == 'Technical']
        if technical_gaps:
            improvement_areas.append("Technical skill expansion")
        
        # Interest-based recommendations
        if 'Technology' in interests or 'Programming' in interests:
            tech_skills = [s for s in skill_gaps if s['category'] == 'Technical']
            if tech_skills:
                improvement_areas.append("Programming and technical skills")
        
        return improvement_areas if improvement_areas else ["General skill development"]

