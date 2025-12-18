"""
Advanced Mock Interview Module using Gemini AI
Complete interview simulation with real-time evaluation and feedback
"""

import google.generativeai as genai
import os
from typing import Dict, List, Any, Optional
import json
import time
from datetime import datetime
import sqlite3

class AdvancedMockInterview:
    def __init__(self):
        # Configure Gemini API with dedicated interview key
        api_key = os.getenv('GEMINI_INTERVIEW_API_KEY', 'AIzaSyDkmPptCKymWWQaMr05esvLCpaxyTDR2es')
        genai.configure(api_key=api_key)
        
        # Use Gemini 2.5 Flash model
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Generation config optimized for interviews
        self.generation_config = {
            'temperature': 0.8,  # Higher for more natural conversation
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 4096,
        }
        
        # Safety settings
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        # Interview session storage
        self.active_sessions = {}
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database for storing interview sessions"""
        conn = sqlite3.connect('career_advisor.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT,
                difficulty TEXT,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                total_score REAL,
                feedback TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interview_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                question_number INTEGER,
                question TEXT,
                answer TEXT,
                score REAL,
                feedback TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES interview_sessions(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def start_interview_session(self, user_id: str, role: str, difficulty: str = 'medium') -> Dict[str, Any]:
        """
        Start a new mock interview session
        
        Args:
            user_id: Unique user identifier
            role: Job role for interview (e.g., "Software Engineer")
            difficulty: easy, medium, or hard
        
        Returns:
            Dictionary with session info and first question
        """
        try:
            # Create session ID
            session_id = f"{user_id}_{int(time.time())}"
            
            # Store session in database
            conn = sqlite3.connect('career_advisor.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO interview_sessions (user_id, role, difficulty, started_at)
                VALUES (?, ?, ?, ?)
            ''', (user_id, role, difficulty, datetime.now()))
            db_session_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            # Initialize session data
            self.active_sessions[session_id] = {
                'db_session_id': db_session_id,
                'user_id': user_id,
                'role': role,
                'difficulty': difficulty,
                'question_number': 0,
                'questions': [],
                'answers': [],
                'scores': [],
                'started_at': datetime.now().isoformat()
            }
            
            # Generate first question
            first_question = self._generate_interview_question(session_id, 1)
            
            return {
                'success': True,
                'session_id': session_id,
                'message': f'Mock interview started for {role} position',
                'first_question': first_question
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _generate_interview_question(self, session_id: str, question_number: int) -> Dict[str, Any]:
        """Generate a dynamic interview question based on context"""
        
        session = self.active_sessions.get(session_id)
        if not session:
            return {'error': 'Session not found'}
        
        role = session['role']
        difficulty = session['difficulty']
        previous_questions = session['questions']
        
        # Build context from previous questions
        context = ""
        if previous_questions:
            context = f"\nPrevious questions asked: {', '.join([q['question'][:50] + '...' for q in previous_questions[-3:]])}"
        
        prompt = f"""
        You are conducting a professional job interview for the position of {role}.
        This is question #{question_number} at {difficulty} difficulty level.
        {context}
        
        Generate a unique, relevant interview question that:
        1. Tests practical knowledge and problem-solving skills
        2. Is appropriate for the {difficulty} difficulty level
        3. Is different from previously asked questions
        4. Relates to real-world scenarios in {role} position
        
        Provide the response in JSON format with:
        {{
            "question": "The interview question",
            "type": "technical/behavioral/situational",
            "key_points": ["point1", "point2", "point3"],
            "evaluation_criteria": ["criteria1", "criteria2"],
            "hints": ["hint1", "hint2"],
            "time_limit": 120
        }}
        
        Make it conversational and professional.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Parse JSON from response
            result_text = response.text
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            question_data = json.loads(result_text)
            question_data['question_number'] = question_number
            
            # Store question in session
            session['questions'].append(question_data)
            session['question_number'] = question_number
            
            return {
                'success': True,
                'question_data': question_data
            }
        
        except Exception as e:
            # Fallback question if API fails
            fallback_question = self._get_fallback_question(role, difficulty, question_number)
            session['questions'].append(fallback_question)
            return {
                'success': True,
                'question_data': fallback_question,
                'note': 'Using fallback question'
            }
    
    def submit_answer(self, session_id: str, answer: str) -> Dict[str, Any]:
        """
        Submit answer for current question and get evaluation
        
        Args:
            session_id: Active session ID
            answer: User's answer to the question
        
        Returns:
            Evaluation results and next question (if any)
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return {'success': False, 'error': 'Session not found'}
        
        try:
            current_question = session['questions'][-1]
            question_number = session['question_number']
            
            # Evaluate the answer
            evaluation = self._evaluate_answer(
                question=current_question['question'],
                answer=answer,
                role=session['role'],
                key_points=current_question.get('key_points', []),
                evaluation_criteria=current_question.get('evaluation_criteria', [])
            )
            
            # Store answer and evaluation
            session['answers'].append(answer)
            session['scores'].append(evaluation.get('score', 0))
            
            # Save to database
            self._save_question_answer(
                session['db_session_id'],
                question_number,
                current_question['question'],
                answer,
                evaluation.get('score', 0),
                json.dumps(evaluation)
            )
            
            # Decide if interview should continue
            total_questions = 5  # Standard interview has 5 questions
            should_continue = question_number < total_questions
            
            response = {
                'success': True,
                'evaluation': evaluation,
                'question_number': question_number,
                'total_questions': total_questions
            }
            
            if should_continue:
                # Generate next question
                next_question = self._generate_interview_question(session_id, question_number + 1)
                response['next_question'] = next_question
                response['interview_continues'] = True
            else:
                # Interview complete, generate final report
                final_report = self._generate_final_report(session_id)
                response['interview_complete'] = True
                response['final_report'] = final_report
                
                # Update database
                self._complete_interview_session(session_id)
            
            return response
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _evaluate_answer(self, question: str, answer: str, role: str, 
                        key_points: List[str], evaluation_criteria: List[str]) -> Dict[str, Any]:
        """Evaluate interview answer with detailed feedback"""
        
        prompt = f"""
        You are an expert interviewer evaluating a candidate's answer for a {role} position.
        
        Question: {question}
        Candidate's Answer: {answer}
        
        Key Points Expected: {', '.join(key_points)}
        Evaluation Criteria: {', '.join(evaluation_criteria)}
        
        Provide a comprehensive evaluation in JSON format:
        {{
            "score": 8.5,
            "out_of": 10,
            "rating": "Excellent/Good/Average/Poor",
            "strengths": ["strength1", "strength2"],
            "weaknesses": ["weakness1", "weakness2"],
            "missing_points": ["missing1", "missing2"],
            "communication_quality": {{
                "clarity": 8,
                "structure": 7,
                "confidence": 8
            }},
            "technical_accuracy": 8,
            "detailed_feedback": "Paragraph explaining the evaluation",
            "improvement_suggestions": ["suggestion1", "suggestion2"],
            "sample_improved_answer": "A better version of the answer",
            "interviewer_follow_up": "What the interviewer might ask next"
        }}
        
        Be constructive, specific, and professional.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            result_text = response.text
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            evaluation = json.loads(result_text)
            return evaluation
        
        except Exception as e:
            # Fallback evaluation
            return {
                'score': 5.0,
                'out_of': 10,
                'rating': 'Average',
                'detailed_feedback': 'Answer received. Please provide more details for better evaluation.',
                'error': str(e)
            }
    
    def _generate_final_report(self, session_id: str) -> Dict[str, Any]:
        """Generate comprehensive interview report"""
        
        session = self.active_sessions.get(session_id)
        if not session:
            return {'error': 'Session not found'}
        
        # Calculate overall statistics
        total_score = sum(session['scores']) / len(session['scores']) if session['scores'] else 0
        
        prompt = f"""
        Generate a comprehensive interview performance report for a {session['role']} candidate.
        
        Interview Details:
        - Role: {session['role']}
        - Difficulty: {session['difficulty']}
        - Questions Asked: {len(session['questions'])}
        - Average Score: {total_score:.1f}/10
        
        Individual Question Scores: {', '.join([f"{s:.1f}" for s in session['scores']])}
        
        Provide a detailed report in JSON format:
        {{
            "overall_score": {total_score},
            "performance_rating": "Excellent/Good/Average/Needs Improvement",
            "strengths": ["strength1", "strength2", "strength3"],
            "areas_for_improvement": ["area1", "area2", "area3"],
            "key_highlights": ["highlight1", "highlight2"],
            "concerns": ["concern1", "concern2"],
            "category_scores": {{
                "technical_knowledge": 7.5,
                "problem_solving": 8.0,
                "communication": 7.0,
                "confidence": 8.5
            }},
            "recommendation": "Strong Hire/Hire/Maybe/No Hire",
            "next_steps": ["step1", "step2", "step3"],
            "preparation_tips": ["tip1", "tip2", "tip3"],
            "estimated_readiness": "85%",
            "detailed_summary": "Comprehensive paragraph about overall performance"
        }}
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            result_text = response.text
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            report = json.loads(result_text)
            report['total_questions'] = len(session['questions'])
            report['date'] = session['started_at']
            
            return report
        
        except Exception as e:
            return {
                'overall_score': total_score,
                'performance_rating': 'Average',
                'error': str(e)
            }
    
    def get_interview_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get interview history for a user"""
        try:
            conn = sqlite3.connect('career_advisor.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, role, difficulty, started_at, completed_at, total_score
                FROM interview_sessions
                WHERE user_id = ?
                ORDER BY started_at DESC
                LIMIT 10
            ''', (user_id,))
            
            sessions = []
            for row in cursor.fetchall():
                sessions.append({
                    'session_id': row[0],
                    'role': row[1],
                    'difficulty': row[2],
                    'started_at': row[3],
                    'completed_at': row[4],
                    'total_score': row[5]
                })
            
            conn.close()
            return sessions
        
        except Exception as e:
            return []
    
    def get_session_details(self, session_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific session"""
        
        # Check active sessions first
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]
        
        # Check database for completed sessions
        try:
            # Try to extract db_session_id from session_id format
            parts = session_id.split('_')
            if len(parts) >= 2:
                user_id = parts[0]
                timestamp = parts[1]
                
                conn = sqlite3.connect('career_advisor.db')
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, role, difficulty, started_at, completed_at, total_score, feedback
                    FROM interview_sessions
                    WHERE user_id = ?
                    ORDER BY started_at DESC
                    LIMIT 1
                ''', (user_id,))
                
                row = cursor.fetchone()
                if row:
                    session_data = {
                        'db_session_id': row[0],
                        'role': row[1],
                        'difficulty': row[2],
                        'started_at': row[3],
                        'completed_at': row[4],
                        'total_score': row[5],
                        'feedback': json.loads(row[6]) if row[6] else {}
                    }
                    
                    # Get questions and answers
                    cursor.execute('''
                        SELECT question_number, question, answer, score, feedback
                        FROM interview_questions
                        WHERE session_id = ?
                        ORDER BY question_number
                    ''', (row[0],))
                    
                    questions = []
                    for q_row in cursor.fetchall():
                        questions.append({
                            'question_number': q_row[0],
                            'question': q_row[1],
                            'answer': q_row[2],
                            'score': q_row[3],
                            'feedback': json.loads(q_row[4]) if q_row[4] else {}
                        })
                    
                    session_data['questions'] = questions
                    conn.close()
                    return session_data
                
                conn.close()
        except Exception as e:
            pass
        
        return {'error': 'Session not found'}
    
    def _save_question_answer(self, session_id: int, question_number: int, 
                              question: str, answer: str, score: float, feedback: str):
        """Save question and answer to database"""
        try:
            conn = sqlite3.connect('career_advisor.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO interview_questions 
                (session_id, question_number, question, answer, score, feedback, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (session_id, question_number, question, answer, score, feedback, datetime.now()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving question: {e}")
    
    def _complete_interview_session(self, session_id: str):
        """Mark interview session as complete"""
        session = self.active_sessions.get(session_id)
        if not session:
            return
        
        try:
            total_score = sum(session['scores']) / len(session['scores']) if session['scores'] else 0
            
            conn = sqlite3.connect('career_advisor.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE interview_sessions
                SET completed_at = ?, total_score = ?
                WHERE id = ?
            ''', (datetime.now(), total_score, session['db_session_id']))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error completing session: {e}")
    
    def _get_fallback_question(self, role: str, difficulty: str, question_number: int) -> Dict[str, Any]:
        """Provide fallback questions if API fails"""
        
        fallback_questions = {
            'Software Engineer': [
                {
                    'question': 'Can you explain the difference between a process and a thread? When would you use one over the other?',
                    'type': 'technical',
                    'key_points': ['Process isolation', 'Thread memory sharing', 'Context switching', 'Use cases'],
                    'evaluation_criteria': ['Technical accuracy', 'Practical examples', 'Understanding of concepts']
                },
                {
                    'question': 'Describe a challenging bug you encountered and how you debugged it.',
                    'type': 'behavioral',
                    'key_points': ['Problem description', 'Debugging approach', 'Resolution', 'Lessons learned'],
                    'evaluation_criteria': ['Problem-solving', 'Communication', 'Technical depth']
                }
            ]
        }
        
        questions = fallback_questions.get(role, fallback_questions['Software Engineer'])
        selected = questions[question_number % len(questions)]
        selected['question_number'] = question_number
        return selected
    
    def test_api_connection(self) -> Dict[str, Any]:
        """Test if Gemini API is working correctly"""
        try:
            test_prompt = "Say 'API is working' if you receive this message."
            response = self.model.generate_content(
                test_prompt,
                generation_config={'temperature': 0.1, 'max_output_tokens': 100}
            )
            
            return {
                'success': True,
                'message': 'API connection successful',
                'response': response.text,
                'api_key': os.getenv('GEMINI_INTERVIEW_API_KEY', 'Not set')[:20] + '...'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'api_key_configured': os.getenv('GEMINI_INTERVIEW_API_KEY') is not None
            }
