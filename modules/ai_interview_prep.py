import json
import random
from typing import Dict, List, Any
from datetime import datetime
import sqlite3
import os
import requests

# Lazy loader for Gemini to avoid heavy import at startup
def _get_genai():
    try:
        import google.generativeai as _genai
        return _genai
    except Exception:
        return None

class AIInterviewPreparation:
    def __init__(self):
        self.db_path = 'career_advisor.db'
        self.interview_questions = self._load_interview_questions()
        self.interview_sessions = {}
        self.feedback_criteria = self._load_feedback_criteria()
    
    def _load_interview_questions(self) -> Dict[str, List[Dict]]:
        """Load comprehensive interview questions for different types of interviews"""
        return {
            'technical': {
                'python': [
                    {
                        'id': 'py_001',
                        'question': 'Explain the difference between a list and a tuple in Python.',
                        'difficulty': 'beginner',
                        'category': 'Data Structures',
                        'expected_keywords': ['mutable', 'immutable', 'performance', 'memory'],
                        'sample_answer': 'Lists are mutable sequences that can be modified after creation, while tuples are immutable sequences that cannot be changed. Lists use more memory and are slower for iteration, while tuples are more memory-efficient and faster.'
                    },
                    {
                        'id': 'py_002',
                        'question': 'What is the difference between == and is in Python?',
                        'difficulty': 'intermediate',
                        'category': 'Operators',
                        'expected_keywords': ['equality', 'identity', 'object', 'value'],
                        'sample_answer': '== compares the values of two objects, while is compares the identity (memory location) of two objects. == checks if values are equal, is checks if they are the same object.'
                    },
                    {
                        'id': 'py_003',
                        'question': 'Explain list comprehensions and provide an example.',
                        'difficulty': 'intermediate',
                        'category': 'Python Features',
                        'expected_keywords': ['comprehension', 'syntax', 'efficiency', 'readable'],
                        'sample_answer': 'List comprehensions provide a concise way to create lists. Example: [x**2 for x in range(10) if x % 2 == 0] creates a list of squares of even numbers from 0 to 9.'
                    }
                ],
                'data_science': [
                    {
                        'id': 'ds_001',
                        'question': 'What is the difference between supervised and unsupervised learning?',
                        'difficulty': 'beginner',
                        'category': 'Machine Learning',
                        'expected_keywords': ['labeled', 'unlabeled', 'training', 'prediction'],
                        'sample_answer': 'Supervised learning uses labeled training data to learn a mapping from inputs to outputs, while unsupervised learning finds patterns in data without labeled examples.'
                    },
                    {
                        'id': 'ds_002',
                        'question': 'Explain overfitting and how to prevent it.',
                        'difficulty': 'intermediate',
                        'category': 'Model Performance',
                        'expected_keywords': ['overfitting', 'generalization', 'validation', 'regularization'],
                        'sample_answer': 'Overfitting occurs when a model learns the training data too well and performs poorly on new data. Prevention methods include cross-validation, regularization, and early stopping.'
                    }
                ],
                'general': [
                    {
                        'id': 'gen_001',
                        'question': 'How would you approach debugging a complex system?',
                        'difficulty': 'intermediate',
                        'category': 'Problem Solving',
                        'expected_keywords': ['systematic', 'logs', 'reproduction', 'isolation'],
                        'sample_answer': 'I would start by reproducing the issue, check logs, isolate the problem area, use debugging tools, and test fixes systematically.'
                    }
                ]
            },
            'behavioral': [
                {
                    'id': 'beh_001',
                    'question': 'Tell me about a time when you had to work with a difficult team member.',
                    'difficulty': 'intermediate',
                    'category': 'Teamwork',
                    'expected_keywords': ['communication', 'conflict resolution', 'collaboration', 'understanding'],
                    'sample_answer': 'I once worked with a colleague who had different communication styles. I focused on understanding their perspective, improved my communication approach, and found common ground to work effectively together.'
                },
                {
                    'id': 'beh_002',
                    'question': 'Describe a situation where you had to learn a new technology quickly.',
                    'difficulty': 'intermediate',
                    'category': 'Learning Agility',
                    'expected_keywords': ['learning', 'adaptability', 'resources', 'application'],
                    'sample_answer': 'When I needed to learn React for a project, I used online tutorials, documentation, and built a small project to practice. I also sought help from experienced developers and applied the knowledge immediately.'
                },
                {
                    'id': 'beh_003',
                    'question': 'Give me an example of a time when you failed and what you learned from it.',
                    'difficulty': 'intermediate',
                    'category': 'Resilience',
                    'expected_keywords': ['failure', 'learning', 'improvement', 'growth'],
                    'sample_answer': 'I once missed a project deadline due to poor time estimation. I learned to break down tasks better, add buffer time, and communicate early when facing challenges.'
                }
            ],
            'system_design': [
                {
                    'id': 'sys_001',
                    'question': 'Design a URL shortener like bit.ly',
                    'difficulty': 'advanced',
                    'category': 'System Design',
                    'expected_keywords': ['scalability', 'database', 'caching', 'load balancing'],
                    'sample_answer': 'I would use a hash function to generate short URLs, store mappings in a database, implement caching for frequently accessed URLs, and use load balancers for scalability.'
                },
                {
                    'id': 'sys_002',
                    'question': 'How would you design a chat application?',
                    'difficulty': 'advanced',
                    'category': 'System Design',
                    'expected_keywords': ['real-time', 'websockets', 'database', 'scalability'],
                    'sample_answer': 'I would use WebSockets for real-time communication, a message queue for reliability, a database for message persistence, and implement proper authentication and authorization.'
                }
            ]
        }
    
    def _load_feedback_criteria(self) -> Dict[str, List[str]]:
        """Load feedback criteria for different types of questions"""
        return {
            'technical': [
                'Technical accuracy and depth of knowledge',
                'Problem-solving approach and methodology',
                'Code quality and best practices',
                'Communication of technical concepts',
                'Handling of edge cases and error scenarios'
            ],
            'behavioral': [
                'Use of STAR method (Situation, Task, Action, Result)',
                'Relevance of example to the question',
                'Demonstration of key competencies',
                'Clarity and structure of response',
                'Learning and growth mindset'
            ],
            'system_design': [
                'System architecture and design principles',
                'Scalability and performance considerations',
                'Trade-offs and decision rationale',
                'Knowledge of relevant technologies',
                'Communication of complex systems'
            ]
        }
    
    def start_mock_interview(self, user_id: str, interview_type: str, difficulty: str = 'intermediate') -> Dict[str, Any]:
        """Start a new mock interview session"""
        if not user_id:
            user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Select questions based on type and difficulty
        questions = self._select_questions(interview_type, difficulty)
        
        session = {
            'user_id': user_id,
            'interview_type': interview_type,
            'difficulty': difficulty,
            'start_time': datetime.now().isoformat(),
            'questions': questions,
            'current_question': 0,
            'answers': {},
            'feedback': {},
            'session_id': f"interview_{user_id}_{int(datetime.now().timestamp())}"
        }
        
        self.interview_sessions[user_id] = session
        
        return {
            'session_id': user_id,
            'user_id': user_id,
            'interview_id': session['session_id'],
            'id': session['session_id'],
            'interview_type': interview_type,
            'difficulty': difficulty,
            'total_questions': len(questions),
            'current_question': 0,
            'question': questions[0] if questions else None,
            'questions': questions
        }
    
    def _select_questions(self, interview_type: str, difficulty: str) -> List[Dict]:
        """Select appropriate questions based on type and difficulty"""
        all_questions = []
        
        if interview_type == 'technical':
            # Mix of technical questions
            for category, questions in self.interview_questions['technical'].items():
                filtered_questions = [q for q in questions if q['difficulty'] == difficulty]
                all_questions.extend(filtered_questions[:2])  # Max 2 per category
        elif interview_type == 'behavioral':
            all_questions = [q for q in self.interview_questions['behavioral'] if q['difficulty'] == difficulty]
        elif interview_type == 'system_design':
            all_questions = [q for q in self.interview_questions['system_design'] if q['difficulty'] == difficulty]
        elif interview_type == 'mixed':
            # Mix all types
            for category, questions in self.interview_questions.items():
                if isinstance(questions, list):
                    filtered_questions = [q for q in questions if q['difficulty'] == difficulty]
                    all_questions.extend(filtered_questions[:1])  # Max 1 per category
                elif isinstance(questions, dict):
                    for subcategory, subquestions in questions.items():
                        filtered_questions = [q for q in subquestions if q['difficulty'] == difficulty]
                        all_questions.extend(filtered_questions[:1])  # Max 1 per subcategory
        
        # Shuffle and limit to 5 questions
        random.shuffle(all_questions)
        return all_questions[:5]
    
    def submit_answer(self, user_id: str, answer: str) -> Dict[str, Any]:
        """Submit an answer and get feedback"""
        if user_id not in self.interview_sessions:
            return {'error': 'Interview session not found'}
        
        session = self.interview_sessions[user_id]
        current_question_index = session['current_question']
        
        if current_question_index >= len(session['questions']):
            return {'error': 'No more questions in this interview'}
        
        current_question = session['questions'][current_question_index]
        
        # Store the answer
        session['answers'][current_question['id']] = {
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        }
        
        # Generate baseline feedback
        feedback = self._generate_feedback(current_question, answer, session['interview_type'])

        # Optionally enrich with Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        genai = _get_genai()
        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = (
                    "You are an interview coach. Score 0-100 and give 2 strengths and 2 improvements, "
                    "with one concise recommendation line. Use JSON with keys: score, strengths, improvements, recommendation.\n"
                    f"Question: {current_question['question']}\nAnswer: {answer}"
                )
                resp = model.generate_content(prompt)
                if getattr(resp, 'text', '').strip():
                    import json as _json
                    try:
                        j = _json.loads(resp.text)
                        if isinstance(j, dict):
                            if 'score' in j:
                                feedback['overall_score'] = max(feedback['overall_score'], j['score'])
                            if 'strengths' in j:
                                feedback['strengths'] = list(set(feedback.get('strengths', []) + j['strengths']))
                            if 'improvements' in j:
                                feedback['areas_for_improvement'] = list(set(feedback.get('areas_for_improvement', []) + j['improvements']))
                            if 'recommendation' in j:
                                feedback.setdefault('suggestions', []).append(j['recommendation'])
                    except Exception:
                        pass
            except Exception:
                pass

        # Optionally enrich with Perplexity
        pplx_key = os.getenv('PPLX_API_KEY')
        if pplx_key:
            try:
                headers = {
                    'Authorization': f'Bearer {pplx_key}',
                    'Content-Type': 'application/json'
                }
                payload = {
                    'model': 'sonar-small-online',
                    'messages': [
                        {'role': 'system', 'content': 'You are a concise interview coach.'},
                        {'role': 'user', 'content': f"Give one tip (<=16 words) to improve this answer to: {current_question['question']}\nAnswer: {answer}"}
                    ]
                }
                r = requests.post('https://api.perplexity.ai/chat/completions', headers=headers, json=payload, timeout=12)
                if r.status_code == 200:
                    data = r.json()
                    tip = data.get('choices', [{}])[0].get('message', {}).get('content')
                    if tip:
                        feedback.setdefault('suggestions', []).append(tip.strip())
            except Exception:
                pass
        session['feedback'][current_question['id']] = feedback
        
        # Move to next question
        session['current_question'] += 1
        
        # Check if interview is complete
        if session['current_question'] >= len(session['questions']):
            return self._complete_interview(user_id)
        
        # Return next question
        next_question = session['questions'][session['current_question']]
        
        return {
            'session_id': user_id,
            'current_question': session['current_question'],
            'total_questions': len(session['questions']),
            'progress': (session['current_question'] / len(session['questions'])) * 100,
            'question': next_question,
            'feedback': feedback
        }
    
    def _generate_feedback(self, question: Dict, answer: str, interview_type: str) -> Dict[str, Any]:
        """Generate AI-powered feedback for the answer"""
        feedback = {
            'overall_score': 0,
            'strengths': [],
            'areas_for_improvement': [],
            'detailed_feedback': '',
            'suggestions': [],
            'keyword_analysis': {},
            'sample_answer': question.get('sample_answer', '')
        }
        
        # Analyze answer based on question type
        if interview_type == 'technical':
            feedback = self._analyze_technical_answer(question, answer, feedback)
        elif interview_type == 'behavioral':
            feedback = self._analyze_behavioral_answer(question, answer, feedback)
        elif interview_type == 'system_design':
            feedback = self._analyze_system_design_answer(question, answer, feedback)
        
        return feedback
    
    def _analyze_technical_answer(self, question: Dict, answer: str, feedback: Dict) -> Dict[str, Any]:
        """Analyze technical interview answer"""
        answer_lower = answer.lower()
        expected_keywords = question.get('expected_keywords', [])
        
        # Check for expected keywords
        found_keywords = [keyword for keyword in expected_keywords if keyword.lower() in answer_lower]
        keyword_score = (len(found_keywords) / len(expected_keywords)) * 100 if expected_keywords else 0
        
        # Analyze answer length and structure
        word_count = len(answer.split())
        structure_score = min(100, word_count * 2) if word_count > 20 else word_count * 3
        
        # Calculate overall score
        overall_score = (keyword_score * 0.6 + structure_score * 0.4)
        feedback['overall_score'] = round(overall_score, 1)
        
        # Generate strengths
        if keyword_score > 70:
            feedback['strengths'].append('Good technical knowledge demonstrated')
        if word_count > 30:
            feedback['strengths'].append('Comprehensive answer provided')
        if found_keywords:
            feedback['strengths'].append(f'Covered key concepts: {", ".join(found_keywords)}')
        
        # Generate areas for improvement
        if keyword_score < 50:
            feedback['areas_for_improvement'].append('Include more technical details and specific concepts')
        if word_count < 20:
            feedback['areas_for_improvement'].append('Provide more detailed explanation')
        
        missing_keywords = [kw for kw in expected_keywords if kw.lower() not in answer_lower]
        if missing_keywords:
            feedback['areas_for_improvement'].append(f'Consider mentioning: {", ".join(missing_keywords)}')
        
        # Generate suggestions
        feedback['suggestions'] = [
            'Practice explaining technical concepts clearly',
            'Use specific examples to illustrate your points',
            'Structure your answer with clear beginning, middle, and end'
        ]
        
        feedback['keyword_analysis'] = {
            'expected_keywords': expected_keywords,
            'found_keywords': found_keywords,
            'missing_keywords': missing_keywords,
            'keyword_coverage': round(keyword_score, 1)
        }
        
        return feedback
    
    def _analyze_behavioral_answer(self, question: Dict, answer: str, feedback: Dict) -> Dict[str, Any]:
        """Analyze behavioral interview answer"""
        answer_lower = answer.lower()
        expected_keywords = question.get('expected_keywords', [])
        
        # Check for STAR method components
        star_components = {
            'situation': any(word in answer_lower for word in ['situation', 'when', 'time', 'once']),
            'task': any(word in answer_lower for word in ['task', 'goal', 'objective', 'needed']),
            'action': any(word in answer_lower for word in ['action', 'did', 'took', 'implemented']),
            'result': any(word in answer_lower for word in ['result', 'outcome', 'achieved', 'learned'])
        }
        
        star_score = (sum(star_components.values()) / len(star_components)) * 100
        
        # Check for expected keywords
        found_keywords = [keyword for keyword in expected_keywords if keyword.lower() in answer_lower]
        keyword_score = (len(found_keywords) / len(expected_keywords)) * 100 if expected_keywords else 0
        
        # Calculate overall score
        overall_score = (star_score * 0.6 + keyword_score * 0.4)
        feedback['overall_score'] = round(overall_score, 1)
        
        # Generate strengths
        if star_score > 70:
            feedback['strengths'].append('Good use of STAR method structure')
        if keyword_score > 60:
            feedback['strengths'].append('Demonstrated relevant competencies')
        if len(answer.split()) > 50:
            feedback['strengths'].append('Provided detailed example')
        
        # Generate areas for improvement
        if star_score < 50:
            feedback['areas_for_improvement'].append('Use STAR method: Situation, Task, Action, Result')
        if keyword_score < 40:
            feedback['areas_for_improvement'].append('Focus more on the specific competencies asked about')
        
        # Generate suggestions
        feedback['suggestions'] = [
            'Practice the STAR method for behavioral questions',
            'Prepare specific examples for common behavioral scenarios',
            'Quantify your achievements with numbers when possible'
        ]
        
        feedback['keyword_analysis'] = {
            'star_components': star_components,
            'star_score': round(star_score, 1),
            'expected_keywords': expected_keywords,
            'found_keywords': found_keywords
        }
        
        return feedback
    
    def _analyze_system_design_answer(self, question: Dict, answer: str, feedback: Dict) -> Dict[str, Any]:
        """Analyze system design interview answer"""
        answer_lower = answer.lower()
        expected_keywords = question.get('expected_keywords', [])
        
        # Check for system design concepts
        design_concepts = {
            'scalability': any(word in answer_lower for word in ['scale', 'scalable', 'load', 'traffic']),
            'database': any(word in answer_lower for word in ['database', 'db', 'storage', 'persistence']),
            'caching': any(word in answer_lower for word in ['cache', 'caching', 'redis', 'memcached']),
            'load_balancing': any(word in answer_lower for word in ['load balancer', 'distribute', 'multiple servers']),
            'security': any(word in answer_lower for word in ['security', 'auth', 'encryption', 'secure'])
        }
        
        concept_score = (sum(design_concepts.values()) / len(design_concepts)) * 100
        
        # Check for expected keywords
        found_keywords = [keyword for keyword in expected_keywords if keyword.lower() in answer_lower]
        keyword_score = (len(found_keywords) / len(expected_keywords)) * 100 if expected_keywords else 0
        
        # Calculate overall score
        overall_score = (concept_score * 0.6 + keyword_score * 0.4)
        feedback['overall_score'] = round(overall_score, 1)
        
        # Generate strengths
        if concept_score > 70:
            feedback['strengths'].append('Good understanding of system design principles')
        if keyword_score > 60:
            feedback['strengths'].append('Covered relevant technical concepts')
        if len(answer.split()) > 100:
            feedback['strengths'].append('Comprehensive system design approach')
        
        # Generate areas for improvement
        if concept_score < 50:
            feedback['areas_for_improvement'].append('Consider scalability, performance, and reliability aspects')
        if keyword_score < 40:
            feedback['areas_for_improvement'].append('Include more specific technical components')
        
        # Generate suggestions
        feedback['suggestions'] = [
            'Start with high-level architecture and drill down to details',
            'Consider scalability, performance, and reliability from the beginning',
            'Discuss trade-offs and alternatives for your design choices'
        ]
        
        feedback['keyword_analysis'] = {
            'design_concepts': design_concepts,
            'concept_score': round(concept_score, 1),
            'expected_keywords': expected_keywords,
            'found_keywords': found_keywords
        }
        
        return feedback
    
    def _complete_interview(self, user_id: str) -> Dict[str, Any]:
        """Complete the interview and generate final report"""
        session = self.interview_sessions[user_id]
        session['end_time'] = datetime.now().isoformat()
        session['status'] = 'completed'
        
        # Calculate overall performance
        feedback_scores = [feedback['overall_score'] for feedback in session['feedback'].values()]
        overall_score = sum(feedback_scores) / len(feedback_scores) if feedback_scores else 0
        
        # Generate final report
        final_report = self._generate_final_report(session, overall_score)

        # Optional Gemini summary paragraph
        api_key = os.getenv('GEMINI_API_KEY')
        genai = _get_genai()
        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = (
                    "Summarize this mock interview performance in one short paragraph (<=70 words) "
                    "with an encouraging tone.\n"
                    f"Report: {final_report}"
                )
                resp = model.generate_content(prompt)
                if getattr(resp, 'text', '').strip():
                    final_report['ai_summary'] = resp.text.strip()
            except Exception:
                pass
        
        # Save to database
        self._save_interview_results(user_id, session, final_report)
        
        return {
            'status': 'completed',
            'session_id': user_id,
            'interview_id': session['session_id'],
            'overall_score': round(overall_score, 1),
            'final_report': final_report,
            'recommendations': self._generate_recommendations(session, overall_score)
        }
    
    def _generate_final_report(self, session: Dict, overall_score: float) -> Dict[str, Any]:
        """Generate comprehensive final interview report"""
        return {
            'interview_summary': {
                'type': session['interview_type'],
                'difficulty': session['difficulty'],
                'total_questions': len(session['questions']),
                'overall_score': round(overall_score, 1),
                'duration': self._calculate_duration(session['start_time'], session['end_time'])
            },
            'performance_breakdown': {
                'question_scores': [
                    {
                        'question_id': qid,
                        'question': session['questions'][i]['question'],
                        'score': session['feedback'][qid]['overall_score'],
                        'category': session['questions'][i].get('category', 'General')
                    }
                    for i, qid in enumerate(session['answers'].keys())
                ],
                'average_score_by_category': self._calculate_category_scores(session)
            },
            'strengths': self._consolidate_strengths(session),
            'areas_for_improvement': self._consolidate_improvements(session),
            'detailed_feedback': self._consolidate_detailed_feedback(session)
        }
    
    def _generate_recommendations(self, session: Dict, overall_score: float) -> Dict[str, Any]:
        """Generate personalized recommendations based on performance"""
        recommendations = {
            'immediate_actions': [],
            'study_resources': [],
            'practice_suggestions': [],
            'next_steps': []
        }
        
        if overall_score < 60:
            recommendations['immediate_actions'] = [
                'Focus on fundamental concepts in your field',
                'Practice explaining technical concepts clearly',
                'Prepare specific examples for behavioral questions'
            ]
        elif overall_score < 80:
            recommendations['immediate_actions'] = [
                'Continue practicing with more challenging questions',
                'Work on structuring your answers better',
                'Prepare more detailed examples'
            ]
        else:
            recommendations['immediate_actions'] = [
                'Great job! Continue practicing to maintain your skills',
                'Consider helping others practice interviews',
                'Focus on advanced topics and edge cases'
            ]
        
        # Add study resources based on interview type
        if session['interview_type'] == 'technical':
            recommendations['study_resources'] = [
                'LeetCode for coding practice',
                'System Design Interview book',
                'Technical interview preparation courses'
            ]
        elif session['interview_type'] == 'behavioral':
            recommendations['study_resources'] = [
                'STAR method practice guides',
                'Behavioral interview question banks',
                'Leadership and teamwork resources'
            ]
        
        recommendations['practice_suggestions'] = [
            'Practice with a timer to improve time management',
            'Record yourself answering questions',
            'Get feedback from peers or mentors'
        ]
        
        recommendations['next_steps'] = [
            'Schedule regular mock interview sessions',
            'Focus on your weakest areas identified in this session',
            'Practice with different question types and difficulties'
        ]
        
        return recommendations
    
    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate interview duration"""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = end - start
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutes"
    
    def _calculate_category_scores(self, session: Dict) -> Dict[str, float]:
        """Calculate average scores by category"""
        category_scores = {}
        
        for i, question in enumerate(session['questions']):
            category = question.get('category', 'General')
            question_id = question['id']
            
            if question_id in session['feedback']:
                score = session['feedback'][question_id]['overall_score']
                
                if category not in category_scores:
                    category_scores[category] = []
                category_scores[category].append(score)
        
        # Calculate averages
        for category in category_scores:
            category_scores[category] = round(
                sum(category_scores[category]) / len(category_scores[category]), 1
            )
        
        return category_scores
    
    def _consolidate_strengths(self, session: Dict) -> List[str]:
        """Consolidate strengths from all feedback"""
        all_strengths = []
        
        for feedback in session['feedback'].values():
            all_strengths.extend(feedback.get('strengths', []))
        
        # Count and return most common strengths
        strength_counts = {}
        for strength in all_strengths:
            strength_counts[strength] = strength_counts.get(strength, 0) + 1
        
        return sorted(strength_counts.keys(), key=lambda x: strength_counts[x], reverse=True)[:5]
    
    def _consolidate_improvements(self, session: Dict) -> List[str]:
        """Consolidate improvement areas from all feedback"""
        all_improvements = []
        
        for feedback in session['feedback'].values():
            all_improvements.extend(feedback.get('areas_for_improvement', []))
        
        # Count and return most common improvements
        improvement_counts = {}
        for improvement in all_improvements:
            improvement_counts[improvement] = improvement_counts.get(improvement, 0) + 1
        
        return sorted(improvement_counts.keys(), key=lambda x: improvement_counts[x], reverse=True)[:5]
    
    def _consolidate_detailed_feedback(self, session: Dict) -> List[Dict]:
        """Consolidate detailed feedback for each question"""
        detailed_feedback = []
        
        for i, question in enumerate(session['questions']):
            question_id = question['id']
            if question_id in session['feedback']:
                feedback = session['feedback'][question_id]
                detailed_feedback.append({
                    'question_number': i + 1,
                    'question': question['question'],
                    'category': question.get('category', 'General'),
                    'score': feedback['overall_score'],
                    'strengths': feedback.get('strengths', []),
                    'improvements': feedback.get('areas_for_improvement', []),
                    'suggestions': feedback.get('suggestions', [])
                })
        
        return detailed_feedback
    
    def _save_interview_results(self, user_id: str, session: Dict, final_report: Dict):
        """Save interview results to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create interview results table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_results (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                interview_id TEXT,
                interview_type TEXT,
                difficulty TEXT,
                start_time TEXT,
                end_time TEXT,
                overall_score REAL,
                session_data TEXT,
                final_report TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert interview results
        cursor.execute('''
            INSERT INTO interview_results 
            (user_id, interview_id, interview_type, difficulty, start_time, end_time, overall_score, session_data, final_report)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            session['session_id'],
            session['interview_type'],
            session['difficulty'],
            session['start_time'],
            session['end_time'],
            final_report['interview_summary']['overall_score'],
            json.dumps(session),
            json.dumps(final_report)
        ))
        
        conn.commit()
        conn.close()
    
    def get_interview_history(self, user_id: str) -> List[Dict]:
        """Get interview history for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT interview_id, interview_type, difficulty, start_time, end_time, overall_score, final_report
            FROM interview_results 
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        history = []
        for result in results:
            history.append({
                'interview_id': result[0],
                'interview_type': result[1],
                'difficulty': result[2],
                'start_time': result[3],
                'end_time': result[4],
                'overall_score': result[5],
                'final_report': json.loads(result[6])
            })
        
        return history
    
    def get_interview_insights(self, user_id: str) -> Dict[str, Any]:
        """Get interview performance insights for a user"""
        history = self.get_interview_history(user_id)
        
        if not history:
            return {'message': 'No interview history found'}
        
        # Calculate performance trends
        scores = [interview['overall_score'] for interview in history]
        avg_score = sum(scores) / len(scores)
        
        # Performance by interview type
        type_scores = {}
        for interview in history:
            interview_type = interview['interview_type']
            if interview_type not in type_scores:
                type_scores[interview_type] = []
            type_scores[interview_type].append(interview['overall_score'])
        
        for interview_type in type_scores:
            type_scores[interview_type] = round(
                sum(type_scores[interview_type]) / len(type_scores[interview_type]), 1
            )
        
        return {
            'total_interviews': len(history),
            'average_score': round(avg_score, 1),
            'best_score': max(scores),
            'latest_score': scores[0],
            'performance_by_type': type_scores,
            'improvement_trend': 'Improving' if len(scores) > 1 and scores[0] > scores[-1] else 'Stable',
            'recommended_focus': self._get_recommended_focus(type_scores)
        }
    
    def _get_recommended_focus(self, type_scores: Dict[str, float]) -> str:
        """Get recommended focus area based on performance"""
        if not type_scores:
            return 'Start with technical interviews'
        
        lowest_type = min(type_scores.keys(), key=lambda x: type_scores[x])
        lowest_score = type_scores[lowest_type]
        
        if lowest_score < 60:
            return f'Focus on improving {lowest_type} interview skills'
        elif lowest_score < 80:
            return f'Continue practicing {lowest_type} interviews'
        else:
            return 'Great performance! Consider advanced interview preparation'
