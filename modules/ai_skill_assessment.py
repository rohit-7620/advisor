import json
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime
import sqlite3
import os

# Lazy loader for Gemini to avoid heavy import at startup
def _get_genai():
    try:
        import google.generativeai as _genai
        return _genai
    except Exception:
        return None

class AISkillAssessment:
    def __init__(self):
        self.db_path = 'career_advisor.db'
        self.assessment_questions = self._load_assessment_questions()
        self.skill_categories = self._load_skill_categories()
        self.assessment_sessions = {}
    
    def _load_assessment_questions(self) -> Dict[str, List[Dict]]:
        """Load comprehensive assessment questions for different skill categories"""
        return {
            'technical_skills': [
                {
                    'id': 'tech_001',
                    'question': 'How comfortable are you with programming concepts like variables, loops, and functions?',
                    'type': 'scale',
                    'options': ['Not familiar', 'Basic understanding', 'Comfortable', 'Very comfortable', 'Expert'],
                    'skill_mapping': {
                        'Python Programming': [0, 1, 2, 3, 4],
                        'JavaScript': [0, 1, 2, 3, 4],
                        'SQL': [0, 1, 2, 3, 4]
                    }
                },
                {
                    'id': 'tech_002',
                    'question': 'Have you worked with data analysis tools like Excel, Python pandas, or R?',
                    'type': 'multiple_choice',
                    'options': ['Never used', 'Basic Excel only', 'Advanced Excel', 'Python/R basics', 'Advanced Python/R'],
                    'skill_mapping': {
                        'Data Analysis': [0, 1, 2, 3, 4],
                        'Python Programming': [0, 0, 1, 3, 4]
                    }
                },
                {
                    'id': 'tech_003',
                    'question': 'What is your experience with machine learning and AI concepts?',
                    'type': 'multiple_choice',
                    'options': ['No experience', 'Heard about it', 'Basic understanding', 'Worked on projects', 'Expert level'],
                    'skill_mapping': {
                        'Machine Learning': [0, 1, 2, 3, 4],
                        'Data Analysis': [0, 0, 1, 2, 3]
                    }
                },
                {
                    'id': 'tech_004',
                    'question': 'How would you rate your database and SQL skills?',
                    'type': 'scale',
                    'options': ['No experience', 'Basic queries', 'Intermediate', 'Advanced', 'Expert'],
                    'skill_mapping': {
                        'SQL': [0, 1, 2, 3, 4],
                        'Data Analysis': [0, 1, 2, 3, 4]
                    }
                },
                {
                    'id': 'tech_005',
                    'question': 'Have you built any web applications or websites?',
                    'type': 'multiple_choice',
                    'options': ['Never', 'Static HTML/CSS', 'Dynamic with JavaScript', 'Full-stack applications', 'Complex web systems'],
                    'skill_mapping': {
                        'JavaScript': [0, 1, 2, 3, 4],
                        'Python Programming': [0, 0, 1, 2, 3]
                    }
                }
            ],
            'soft_skills': [
                {
                    'id': 'soft_001',
                    'question': 'How do you handle working in a team environment?',
                    'type': 'scale',
                    'options': ['Prefer working alone', 'Can work in teams', 'Enjoy collaboration', 'Natural team leader', 'Excellent team player'],
                    'skill_mapping': {
                        'Communication': [1, 2, 3, 4, 4],
                        'Leadership': [0, 1, 2, 3, 4],
                        'Problem Solving': [1, 2, 3, 3, 4]
                    }
                },
                {
                    'id': 'soft_002',
                    'question': 'When faced with a complex problem, what is your typical approach?',
                    'type': 'multiple_choice',
                    'options': ['Ask for help immediately', 'Break it into smaller parts', 'Research and analyze', 'Try different approaches', 'Systematic problem-solving'],
                    'skill_mapping': {
                        'Problem Solving': [1, 2, 3, 4, 4],
                        'Critical Thinking': [1, 2, 3, 4, 4]
                    }
                },
                {
                    'id': 'soft_003',
                    'question': 'How comfortable are you with presenting ideas to groups?',
                    'type': 'scale',
                    'options': ['Very uncomfortable', 'Somewhat uncomfortable', 'Neutral', 'Comfortable', 'Very comfortable'],
                    'skill_mapping': {
                        'Communication': [0, 1, 2, 3, 4],
                        'Leadership': [0, 1, 2, 3, 4]
                    }
                },
                {
                    'id': 'soft_004',
                    'question': 'How do you prioritize tasks when you have multiple deadlines?',
                    'type': 'multiple_choice',
                    'options': ['Work on whatever comes first', 'Ask manager for guidance', 'Use a simple list', 'Use project management tools', 'Strategic prioritization'],
                    'skill_mapping': {
                        'Project Management': [1, 2, 2, 3, 4],
                        'Critical Thinking': [1, 2, 2, 3, 4]
                    }
                },
                {
                    'id': 'soft_005',
                    'question': 'How do you handle feedback and criticism?',
                    'type': 'scale',
                    'options': ['Take it personally', 'Feel defensive', 'Listen but ignore', 'Use it to improve', 'Actively seek feedback'],
                    'skill_mapping': {
                        'Communication': [1, 1, 2, 3, 4],
                        'Leadership': [0, 1, 2, 3, 4]
                    }
                }
            ],
            'interests_and_goals': [
                {
                    'id': 'interest_001',
                    'question': 'What type of work environment do you prefer?',
                    'type': 'multiple_choice',
                    'options': ['Remote work', 'Office environment', 'Hybrid model', 'Field work', 'No preference'],
                    'category': 'work_preference'
                },
                {
                    'id': 'interest_002',
                    'question': 'What motivates you most in your career?',
                    'type': 'multiple_choice',
                    'options': ['High salary', 'Creative freedom', 'Helping others', 'Technical challenges', 'Leadership opportunities'],
                    'category': 'motivation'
                },
                {
                    'id': 'interest_003',
                    'question': 'Which industries interest you most? (Select all that apply)',
                    'type': 'checkbox',
                    'options': ['Technology', 'Healthcare', 'Finance', 'Education', 'Business', 'Research', 'Creative Arts'],
                    'category': 'industry_interest'
                },
                {
                    'id': 'interest_004',
                    'question': 'What is your ideal work-life balance?',
                    'type': 'multiple_choice',
                    'options': ['Work-focused (60+ hours/week)', 'Balanced (40-50 hours/week)', 'Flexible schedule', 'Part-time preferred', 'Freelance/contract'],
                    'category': 'work_life_balance'
                },
                {
                    'id': 'interest_005',
                    'question': 'Where do you see yourself in 5 years?',
                    'type': 'multiple_choice',
                    'options': ['Individual contributor', 'Team lead', 'Manager', 'Director/VP', 'Entrepreneur'],
                    'category': 'career_vision'
                }
            ],
            'experience_and_education': [
                {
                    'id': 'exp_001',
                    'question': 'What is your highest level of education?',
                    'type': 'multiple_choice',
                    'options': ['High School', 'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD'],
                    'category': 'education_level'
                },
                {
                    'id': 'exp_002',
                    'question': 'How many years of professional work experience do you have?',
                    'type': 'multiple_choice',
                    'options': ['No experience', 'Less than 1 year', '1-2 years', '3-5 years', '5+ years'],
                    'category': 'work_experience'
                },
                {
                    'id': 'exp_003',
                    'question': 'Have you completed any professional certifications or courses?',
                    'type': 'checkbox',
                    'options': ['None', 'Online courses', 'Professional certifications', 'Bootcamps', 'University courses'],
                    'category': 'certifications'
                },
                {
                    'id': 'exp_004',
                    'question': 'What type of projects have you worked on? (Select all that apply)',
                    'type': 'checkbox',
                    'options': ['Academic projects', 'Personal projects', 'Open source contributions', 'Freelance work', 'Internships', 'Full-time employment'],
                    'category': 'project_experience'
                }
            ]
        }
    
    def _load_skill_categories(self) -> Dict[str, Dict]:
        """Load skill categories with descriptions and weights"""
        return {
            'Technical Skills': {
                'description': 'Programming, tools, and technical competencies',
                'weight': 0.4,
                'skills': ['Python Programming', 'Machine Learning', 'Data Analysis', 'JavaScript', 'SQL']
            },
            'Soft Skills': {
                'description': 'Communication, leadership, and interpersonal skills',
                'weight': 0.3,
                'skills': ['Communication', 'Leadership', 'Problem Solving', 'Project Management', 'Critical Thinking']
            },
            'Domain Knowledge': {
                'description': 'Industry-specific knowledge and expertise',
                'weight': 0.2,
                'skills': ['Business Analysis', 'User Experience', 'System Design', 'Data Science']
            },
            'Learning Agility': {
                'description': 'Ability to learn and adapt to new technologies',
                'weight': 0.1,
                'skills': ['Continuous Learning', 'Adaptability', 'Innovation']
            }
        }
    
    def start_assessment(self, user_id: str = None) -> Dict[str, Any]:
        """Start a new assessment session"""
        if not user_id:
            user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = {
            'user_id': user_id,
            'start_time': datetime.now().isoformat(),
            'current_phase': 'technical_skills',
            'current_question': 0,
            'responses': {},
            'skill_scores': {},
            'completed_phases': [],
            'assessment_id': f"assessment_{user_id}_{int(datetime.now().timestamp())}"
        }
        
        self.assessment_sessions[user_id] = session
        
        return {
            'session_id': user_id,
            'assessment_id': session['assessment_id'],
            'current_phase': session['current_phase'],
            'total_phases': len(self.assessment_questions),
            'current_question': 0,
            'total_questions': len(self.assessment_questions[session['current_phase']]),
            'question': self._get_current_question(session),
            # Provide initial progress so the UI can render the progress bar safely
            'progress': self._calculate_progress(session)
        }
    
    def submit_answer(self, user_id: str, answer: Any) -> Dict[str, Any]:
        """Submit an answer and get the next question"""
        if user_id not in self.assessment_sessions:
            return {'error': 'Assessment session not found'}
        
        session = self.assessment_sessions[user_id]
        current_phase = session['current_phase']
        current_question = session['current_question']
        
        # Store the answer
        question_id = self.assessment_questions[current_phase][current_question]['id']
        session['responses'][question_id] = answer
        
        # Update skill scores based on answer
        self._update_skill_scores(session, current_phase, current_question, answer)
        
        # Optional AI coaching for this question
        ai_coaching = None
        api_key = os.getenv('GEMINI_API_KEY')
        genai = _get_genai()
        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                q = self.assessment_questions[current_phase][current_question]
                prompt = (
                    "You are a career coach. In one short paragraph (max 70 words), provide coaching for a "
                    "user who answered the following assessment item. Focus on how to improve and what to learn next.\n"
                    f"Question: {q['question']}\n"
                    f"User answer (index or list): {answer}\n"
                )
                resp = model.generate_content(prompt)
                if getattr(resp, 'text', '').strip():
                    ai_coaching = resp.text.strip()
            except Exception:
                ai_coaching = None

        # Move to next question
        session['current_question'] += 1
        
        # Check if phase is complete
        if session['current_question'] >= len(self.assessment_questions[current_phase]):
            session['completed_phases'].append(current_phase)
            session['current_question'] = 0
            
            # Move to next phase
            phases = list(self.assessment_questions.keys())
            current_phase_index = phases.index(current_phase)
            
            if current_phase_index + 1 < len(phases):
                session['current_phase'] = phases[current_phase_index + 1]
            else:
                # Assessment complete
                return self._complete_assessment(user_id)
        
        return {
            'session_id': user_id,
            'current_phase': session['current_phase'],
            'current_question': session['current_question'],
            'total_questions': len(self.assessment_questions[session['current_phase']]),
            'progress': self._calculate_progress(session),
            'question': self._get_current_question(session),
            'ai_coaching': ai_coaching
        }
    
    def _get_current_question(self, session: Dict) -> Dict[str, Any]:
        """Get the current question for the session"""
        current_phase = session['current_phase']
        current_question = session['current_question']
        
        if current_phase not in self.assessment_questions:
            return None
        
        questions = self.assessment_questions[current_phase]
        if current_question >= len(questions):
            return None
        
        question = questions[current_question].copy()
        question['phase'] = current_phase
        question['question_number'] = current_question + 1
        question['total_in_phase'] = len(questions)
        
        return question
    
    def _update_skill_scores(self, session: Dict, phase: str, question_index: int, answer: Any):
        """Update skill scores based on the answer"""
        question = self.assessment_questions[phase][question_index]
        skill_mapping = question.get('skill_mapping', {})
        
        for skill, score_mapping in skill_mapping.items():
            if skill not in session['skill_scores']:
                session['skill_scores'][skill] = 0
            
            # Determine score based on answer type
            if question['type'] == 'scale':
                score = answer if isinstance(answer, int) else 0
            elif question['type'] == 'multiple_choice':
                score = answer if isinstance(answer, int) else 0
            elif question['type'] == 'checkbox':
                # For checkbox, count number of selected options
                score = len(answer) if isinstance(answer, list) else 0
            else:
                score = 0
            
            # Map score to skill level
            if score < len(score_mapping):
                skill_score = score_mapping[score]
                session['skill_scores'][skill] += skill_score
    
    def _calculate_progress(self, session: Dict) -> Dict[str, Any]:
        """Calculate assessment progress"""
        total_questions = sum(len(questions) for questions in self.assessment_questions.values())
        answered_questions = len(session['responses'])
        
        return {
            'percentage': round((answered_questions / total_questions) * 100, 1),
            'answered_questions': answered_questions,
            'total_questions': total_questions,
            'completed_phases': len(session['completed_phases']),
            'total_phases': len(self.assessment_questions)
        }
    
    def _complete_assessment(self, user_id: str) -> Dict[str, Any]:
        """Complete the assessment and generate results"""
        session = self.assessment_sessions[user_id]
        session['end_time'] = datetime.now().isoformat()
        session['status'] = 'completed'
        
        # Calculate final skill scores
        final_scores = self._calculate_final_scores(session)
        
        # Generate assessment report
        assessment_report = self._generate_assessment_report(session, final_scores)
        
        # Save to database
        self._save_assessment_results(user_id, session, final_scores, assessment_report)
        
        # Optional AI refinement of recommendations
        api_key = os.getenv('GEMINI_API_KEY')
        genai = _get_genai()
        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = (
                    "Given the following skill scores and report, create 3 concise, actionable career development tips "
                    "(bulleted, <=12 words each).\n"
                    f"Scores: {final_scores}\nReport: {assessment_report}"
                )
                resp = model.generate_content(prompt)
                if getattr(resp, 'text', '').strip():
                    tips = [t.strip('-• ').strip() for t in resp.text.split('\n') if t.strip()]
                    tips = [t for t in tips if t]
                    if tips:
                        recs = self._generate_recommendations(final_scores, session)
                        recs.setdefault('ai_coaching_tips', tips[:5])
                        recommendations = recs
                    else:
                        recommendations = self._generate_recommendations(final_scores, session)
                else:
                    recommendations = self._generate_recommendations(final_scores, session)
            except Exception:
                recommendations = self._generate_recommendations(final_scores, session)
        else:
            recommendations = self._generate_recommendations(final_scores, session)

        return {
            'status': 'completed',
            'session_id': user_id,
            'assessment_id': session['assessment_id'],
            'final_scores': final_scores,
            'assessment_report': assessment_report,
            'recommendations': recommendations
        }
    
    def _calculate_final_scores(self, session: Dict) -> Dict[str, Any]:
        """Calculate final skill scores with normalization"""
        raw_scores = session['skill_scores']
        final_scores = {}
        
        # Normalize scores to 0-100 scale
        for skill, score in raw_scores.items():
            # Find max possible score for this skill
            max_possible = self._get_max_possible_score(skill)
            normalized_score = min(100, (score / max_possible) * 100) if max_possible > 0 else 0
            final_scores[skill] = round(normalized_score, 1)
        
        return final_scores
    
    def _get_max_possible_score(self, skill: str) -> int:
        """Get maximum possible score for a skill"""
        max_score = 0
        for phase_questions in self.assessment_questions.values():
            for question in phase_questions:
                skill_mapping = question.get('skill_mapping', {})
                if skill in skill_mapping:
                    max_score += max(skill_mapping[skill])
        return max_score
    
    def _generate_assessment_report(self, session: Dict, final_scores: Dict) -> Dict[str, Any]:
        """Generate comprehensive assessment report"""
        # Categorize skills
        skill_categories = {}
        for category, data in self.skill_categories.items():
            skill_categories[category] = {
                'description': data['description'],
                'weight': data['weight'],
                'skills': {},
                'average_score': 0
            }
            
            category_skills = data['skills']
            category_scores = []
            
            for skill in category_skills:
                if skill in final_scores:
                    skill_categories[category]['skills'][skill] = final_scores[skill]
                    category_scores.append(final_scores[skill])
            
            if category_scores:
                skill_categories[category]['average_score'] = round(sum(category_scores) / len(category_scores), 1)
        
        # Calculate overall score
        overall_score = 0
        total_weight = 0
        for category, data in skill_categories.items():
            if data['average_score'] > 0:
                overall_score += data['average_score'] * data['weight']
                total_weight += data['weight']
        
        overall_score = round(overall_score / total_weight, 1) if total_weight > 0 else 0
        
        # Identify strengths and weaknesses
        all_skills = [(skill, score) for skill, score in final_scores.items()]
        all_skills.sort(key=lambda x: x[1], reverse=True)
        
        strengths = [skill for skill, score in all_skills if score >= 70][:5]
        weaknesses = [skill for skill, score in all_skills if score < 40][:5]
        
        return {
            'overall_score': overall_score,
            'skill_categories': skill_categories,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'assessment_duration': self._calculate_duration(session['start_time'], session['end_time']),
            'total_questions_answered': len(session['responses']),
            'assessment_date': session['end_time']
        }
    
    def _generate_recommendations(self, final_scores: Dict, session: Dict) -> Dict[str, Any]:
        """Generate personalized recommendations based on assessment results"""
        recommendations = {
            'skill_development': [],
            'career_paths': [],
            'learning_resources': [],
            'next_steps': []
        }
        
        # Skill development recommendations
        for skill, score in final_scores.items():
            if score < 50:
                recommendations['skill_development'].append({
                    'skill': skill,
                    'current_level': self._get_skill_level(score),
                    'recommendation': f'Focus on developing {skill} - current level is {self._get_skill_level(score)}',
                    'priority': 'High' if score < 30 else 'Medium'
                })
        
        # Career path recommendations based on strengths
        strengths = [skill for skill, score in final_scores.items() if score >= 70]
        if 'Python Programming' in strengths and 'Data Analysis' in strengths:
            recommendations['career_paths'].append('Data Scientist')
        if 'Communication' in strengths and 'Leadership' in strengths:
            recommendations['career_paths'].append('Project Manager')
        if 'JavaScript' in strengths and 'Python Programming' in strengths:
            recommendations['career_paths'].append('Full Stack Developer')
        
        # Learning resources
        for skill in recommendations['skill_development'][:3]:  # Top 3 skills to develop
            recommendations['learning_resources'].append({
                'skill': skill['skill'],
                'resources': self._get_learning_resources(skill['skill'])
            })
        
        # Next steps
        recommendations['next_steps'] = [
            'Review your assessment results and identify top 3 skills to develop',
            'Create a learning plan for your priority skills',
            'Start with beginner-level courses for your weakest areas',
            'Practice skills through hands-on projects',
            'Consider getting certified in your strongest areas'
        ]
        
        return recommendations
    
    def _get_skill_level(self, score: float) -> str:
        """Convert numeric score to skill level"""
        if score >= 80:
            return 'Expert'
        elif score >= 60:
            return 'Advanced'
        elif score >= 40:
            return 'Intermediate'
        elif score >= 20:
            return 'Beginner'
        else:
            return 'Novice'
    
    def _get_learning_resources(self, skill: str) -> List[str]:
        """Get learning resources for a specific skill"""
        resources = {
            'Python Programming': [
                'Python.org official tutorial',
                'Coursera Python for Everybody',
                'NPTEL Python Programming course',
                'LeetCode Python practice problems'
            ],
            'Machine Learning': [
                'Andrew Ng\'s Machine Learning course',
                'NPTEL Machine Learning course',
                'Kaggle Learn modules',
                'Hands-on Machine Learning book'
            ],
            'Data Analysis': [
                'Google Data Analytics Certificate',
                'NPTEL Data Science course',
                'Pandas documentation and tutorials',
                'Tableau Public for visualization'
            ],
            'Communication': [
                'LinkedIn Learning Communication courses',
                'Toastmasters International',
                'NPTEL Professional Communication',
                'Practice presentation skills'
            ]
        }
        return resources.get(skill, ['General online courses and tutorials'])
    
    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate assessment duration"""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = end - start
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    def _save_assessment_results(self, user_id: str, session: Dict, final_scores: Dict, report: Dict):
        """Save assessment results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create assessment results table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessment_results (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                assessment_id TEXT,
                start_time TEXT,
                end_time TEXT,
                final_scores TEXT,
                assessment_report TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert assessment results
        cursor.execute('''
            INSERT INTO assessment_results 
            (user_id, assessment_id, start_time, end_time, final_scores, assessment_report)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            session['assessment_id'],
            session['start_time'],
            session['end_time'],
            json.dumps(final_scores),
            json.dumps(report)
        ))
        
        conn.commit()
        conn.close()
    
    def get_assessment_history(self, user_id: str) -> List[Dict]:
        """Get assessment history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT assessment_id, start_time, end_time, final_scores, assessment_report
            FROM assessment_results 
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for result in results:
            history.append({
                'assessment_id': result[0],
                'start_time': result[1],
                'end_time': result[2],
                'final_scores': json.loads(result[3]),
                'assessment_report': json.loads(result[4])
            })
        
        return history
    
    def get_skill_insights(self, user_id: str) -> Dict[str, Any]:
        """Get skill development insights for a user"""
        history = self.get_assessment_history(user_id)
        
        if not history:
            return {'message': 'No assessment history found'}
        
        # Compare latest assessment with previous ones
        latest = history[0]
        previous = history[1] if len(history) > 1 else None
        
        insights = {
            'latest_assessment': latest,
            'skill_progress': {},
            'improvement_areas': [],
            'strengths_maintained': []
        }
        
        if previous:
            latest_scores = latest['final_scores']
            previous_scores = previous['final_scores']
            
            for skill in latest_scores:
                if skill in previous_scores:
                    improvement = latest_scores[skill] - previous_scores[skill]
                    insights['skill_progress'][skill] = {
                        'previous_score': previous_scores[skill],
                        'current_score': latest_scores[skill],
                        'improvement': round(improvement, 1),
                        'trend': 'improving' if improvement > 0 else 'declining' if improvement < 0 else 'stable'
                    }
                    
                    if improvement > 10:
                        insights['improvement_areas'].append(skill)
                    elif latest_scores[skill] >= 70:
                        insights['strengths_maintained'].append(skill)
        
        return insights
