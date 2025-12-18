"""
Advanced Gemini AI Engine for Career Advisor
Hackathon-Ready Features with Multi-Modal AI Capabilities
"""

import google.generativeai as genai
import os
from typing import Dict, List, Any, Optional
import json
import time
from datetime import datetime

class GeminiAIEngine:
    def __init__(self):
        # Configure Gemini API with primary key
        self.primary_api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyCfmKyKhKk58OaXkoWsTgXnqW2kMhlxnVQ')
        # Secondary key for evaluation to avoid quota issues
        self.evaluation_api_key = os.getenv('GEMINI_INTERVIEW_API_KEY', 'AIzaSyA6MDcUHhzuEP4_6NFPI9d8abVeTjKhq3U')
        
        genai.configure(api_key=self.primary_api_key)
        
        # Use Gemini 2.5 Flash model
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.vision_model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Generation config for optimal outputs
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192,
        }
        
        # Safety settings
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
    
    def generate_ats_optimized_resume(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate ATS-optimized resume with industry-specific keywords
        """
        prompt = f"""
        You are an expert resume writer specializing in ATS (Applicant Tracking System) optimization.
        
        User Profile:
        - Name: {user_data.get('name', 'Professional')}
        - Target Role: {user_data.get('target_role', 'Software Engineer')}
        - Experience: {user_data.get('experience', [])}
        - Skills: {user_data.get('skills', [])}
        - Education: {user_data.get('education', '')}
        - Achievements: {user_data.get('achievements', [])}
        
        Create a comprehensive, ATS-optimized resume that includes:
        1. Powerful professional summary (50-75 words) with relevant keywords
        2. Optimized work experience with quantifiable achievements (use STAR method)
        3. Technical skills section organized by categories
        4. Education with relevant coursework and GPA (if >3.5)
        5. Key projects with impact metrics
        6. Certifications and awards
        7. ATS-friendly formatting keywords
        
        Return the response as a JSON object with sections: summary, experience, skills, education, projects, certifications, ats_keywords.
        Make it compelling for both ATS systems and human recruiters.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Parse JSON from response
            resume_text = response.text
            # Extract JSON if wrapped in markdown code blocks
            if '```json' in resume_text:
                resume_text = resume_text.split('```json')[1].split('```')[0].strip()
            elif '```' in resume_text:
                resume_text = resume_text.split('```')[1].split('```')[0].strip()
            
            resume_data = json.loads(resume_text)
            
            return {
                'success': True,
                'resume': resume_data,
                'ats_score': self._calculate_ats_score(resume_data),
                'optimization_tips': self._get_optimization_tips(resume_data)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fallback_resume': self._generate_fallback_resume(user_data)
            }
    
    def generate_personalized_cover_letter(self, user_data: Dict[str, Any], job_description: str) -> str:
        """
        Generate personalized cover letter matching job description
        """
        prompt = f"""
        Create a compelling cover letter for the following job application.
        
        Candidate Profile:
        - Name: {user_data.get('name', 'Candidate')}
        - Experience: {user_data.get('experience_years', 0)} years
        - Key Skills: {', '.join(user_data.get('skills', []))}
        - Recent Role: {user_data.get('current_role', 'Professional')}
        
        Job Description:
        {job_description}
        
        Write a professional cover letter that:
        1. Opens with a strong hook referencing the company/role
        2. Highlights 2-3 key achievements matching job requirements
        3. Shows enthusiasm and cultural fit
        4. Includes specific examples of relevant experience
        5. Closes with a clear call to action
        
        Keep it concise (250-350 words), professional, and personalized.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.text
        except Exception as e:
            return f"Error generating cover letter: {str(e)}"
    
    def analyze_linkedin_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze LinkedIn profile and provide optimization recommendations
        """
        prompt = f"""
        Analyze this LinkedIn profile and provide detailed recommendations for improvement.
        
        Profile Data:
        - Headline: {profile_data.get('headline', '')}
        - About: {profile_data.get('about', '')}
        - Experience: {json.dumps(profile_data.get('experience', []))}
        - Skills: {', '.join(profile_data.get('skills', []))}
        
        Provide a comprehensive analysis including:
        1. Overall profile strength score (0-100)
        2. Headline optimization suggestions
        3. About section improvements
        4. Experience bullet point enhancements
        5. Skills endorsement strategy
        6. Content posting recommendations
        7. Networking tips
        
        Return as JSON with sections: score, headline_tips, about_tips, experience_tips, skills_strategy, content_ideas, networking_tips.
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
            
            return json.loads(result_text)
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def conduct_mock_interview(self, role: str, difficulty: str, question_number: int) -> Dict[str, Any]:
        """
        Generate dynamic interview questions with follow-ups
        """
        prompt = f"""
        You are an expert interviewer for a {role} position.
        Generate interview question #{question_number} at {difficulty} difficulty level.
        
        Create a comprehensive interview question that tests practical knowledge and problem-solving.
        
        Return ONLY valid JSON with this exact structure:
        {{
            "question": "The actual interview question here",
            "evaluation_criteria": "What you're looking for in the answer",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "mistakes": ["Common mistake 1", "Common mistake 2"],
            "sample_answer": "Example of a strong answer",
            "follow_ups": ["Follow-up question 1", "Follow-up question 2"]
        }}
        
        Make sure the question is specific, relevant to {role}, and at {difficulty} level.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            result_text = response.text.strip()
            
            # Extract JSON from markdown code blocks
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            # Parse JSON
            interview_data = json.loads(result_text)
            
            # Validate required fields
            if 'question' not in interview_data or not interview_data['question']:
                interview_data['question'] = f"Describe your experience with {role} responsibilities and provide a specific example of a challenge you overcame."
            
            if 'evaluation_criteria' not in interview_data:
                interview_data['evaluation_criteria'] = "Looking for specific examples, problem-solving approach, and outcome"
            
            if 'key_points' not in interview_data:
                interview_data['key_points'] = ["Specific situation", "Your actions", "Measurable results"]
            
            return interview_data
        
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Raw response: {result_text[:500]}")
            # Return fallback question
            return {
                'question': f"Tell me about a challenging project you worked on as a {role}. What was the problem, how did you approach it, and what was the outcome?",
                'evaluation_criteria': "Looking for problem-solving skills, technical depth, and measurable impact",
                'key_points': ["Clear problem statement", "Your specific approach and actions", "Quantifiable results and learnings"],
                'mistakes': ["Being too vague", "Not mentioning specific technologies", "Focusing only on team achievements without personal contribution"],
                'sample_answer': "I worked on a system that had performance issues. I profiled the code, identified bottlenecks, implemented caching, and reduced response time by 60%.",
                'follow_ups': ["What would you do differently?", "How did you measure success?"]
            }
        except Exception as e:
            # Handle quota errors and other exceptions
            if '429' in str(e) or 'quota' in str(e).lower():
                print(f"API Quota exceeded. Using fallback question.")
            else:
                print(f"Mock interview generation error: {e}")
            
            # Always return a valid dictionary
            return {
                'question': f"Tell me about a challenging project you worked on as a {role}. What was the problem, how did you approach it, and what was the outcome?",
                'evaluation_criteria': "Looking for problem-solving skills, technical depth, and measurable impact",
                'key_points': ["Clear problem statement", "Your specific approach and actions", "Quantifiable results and learnings"],
                'mistakes': ["Being too vague", "Not mentioning specific technologies", "Focusing only on team achievements without personal contribution"],
                'sample_answer': "I worked on a system that had performance issues. I profiled the code, identified bottlenecks, implemented caching, and reduced response time by 60%.",
                'follow_ups': ["What would you do differently?", "How did you measure success?"]
            }
    
    def evaluate_interview_answer(self, question: str, answer: str, role: str) -> Dict[str, Any]:
        """
        Evaluate interview answer with detailed feedback using secondary API key
        """
        prompt = f"""
        You are an expert interviewer evaluating a candidate's answer for a {role} position.
        
        Question: {question}
        Candidate's Answer: {answer}
        
        Provide comprehensive feedback including:
        1. Overall score (0-10)
        2. Strengths in the answer
        3. Areas for improvement
        4. Missing key points
        5. Communication quality assessment
        6. Specific suggestions for better answer
        7. Example of improved response
        
        Return as JSON with: score, strengths, improvements, missing_points, communication_score, suggestions, improved_answer.
        """
        
        try:
            # Use secondary API key for evaluation to avoid quota issues
            genai.configure(api_key=self.evaluation_api_key)
            evaluation_model = genai.GenerativeModel('models/gemini-2.5-flash')
            
            response = evaluation_model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            # Switch back to primary API key
            genai.configure(api_key=self.primary_api_key)
            
            result_text = response.text
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0].strip()
            
            return json.loads(result_text)
        except Exception as e:
            return {'error': str(e)}
    
    def predict_career_trajectory(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict 5-year career trajectory with multiple paths
        """
        prompt = f"""
        Analyze this professional profile and predict realistic career trajectories.
        
        Current Profile:
        - Current Role: {user_profile.get('current_role', '')}
        - Experience: {user_profile.get('experience_years', 0)} years
        - Skills: {', '.join(user_profile.get('skills', []))}
        - Industry: {user_profile.get('industry', '')}
        - Education: {user_profile.get('education', '')}
        - Goals: {user_profile.get('career_goals', '')}
        
        Provide 3 realistic career paths for the next 5 years:
        1. Conservative path (steady growth)
        2. Ambitious path (fast-track)
        3. Pivot path (career change)
        
        For each path, include:
        - Year-by-year role progression
        - Skills to develop each year
        - Expected salary ranges (in INR)
        - Key milestones
        - Probability of success (%)
        - Action items for each transition
        
        Return as JSON with paths: conservative, ambitious, pivot. Each with yearly_progression, skills_timeline, salary_progression, milestones, success_probability, action_plan.
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
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Career trajectory error: {e}")
            # Return structured fallback data
            return {
                'conservative': {
                    'yearly_progression': {
                        'Year 1': f"Continue as {user_profile.get('current_role', 'current role')} with skill enhancement",
                        'Year 2': 'Senior position with team responsibilities',
                        'Year 3': 'Lead position with project management',
                        'Year 4': 'Manager role overseeing multiple projects',
                        'Year 5': 'Senior manager or director level'
                    },
                    'success_probability': '75-85%',
                    'salary_progression': 'Steady 10-15% annual growth'
                },
                'ambitious': {
                    'yearly_progression': {
                        'Year 1': 'Rapid skill acquisition and high-impact projects',
                        'Year 2': 'Senior role with leadership responsibilities',
                        'Year 3': 'Manager or technical lead position',
                        'Year 4': 'Senior manager or principal engineer',
                        'Year 5': 'Director or VP level'
                    },
                    'success_probability': '50-60%',
                    'salary_progression': '20-30% annual growth with strategic moves'
                },
                'pivot': {
                    'yearly_progression': {
                        'Year 1': 'Skill transition and certification in new domain',
                        'Year 2': 'Entry to mid-level role in new field',
                        'Year 3': 'Establishing expertise in new domain',
                        'Year 4': 'Senior position in new career path',
                        'Year 5': 'Leadership role in new industry'
                    },
                    'success_probability': '40-55%',
                    'salary_progression': 'Initial dip, then 15-20% recovery growth'
                }
            }
    
    def analyze_skill_gaps(self, current_skills: List[str], target_role: str) -> Dict[str, Any]:
        """
        Comprehensive skill gap analysis with learning recommendations
        """
        prompt = f"""
        Perform a detailed skill gap analysis.
        
        Current Skills: {', '.join(current_skills)}
        Target Role: {target_role}
        
        Provide:
        1. Required skills for target role (categorized: must-have, good-to-have, nice-to-have)
        2. Skill gap analysis with priority levels (Critical, High, Medium, Low)
        3. Learning timeline (realistic timeframes for each skill)
        4. Recommended learning resources (online courses, certifications, books)
        5. Practice projects for each skill
        6. Industry demand for each skill (trending up/stable/declining)
        7. Salary impact of each skill
        
        Return as JSON with: required_skills, skill_gaps, learning_timeline, resources, projects, market_demand, salary_impact.
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
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Skill gap analysis error: {e}")
            # Return structured fallback data
            return {
                'required_skills': {
                    'Must-Have': ['Machine Learning Fundamentals', 'Deep Learning', 'Python Programming', 'Statistical Analysis', 'Data Preprocessing'],
                    'Good-to-Have': ['TensorFlow/PyTorch', 'Natural Language Processing', 'Computer Vision', 'Cloud Computing (AWS/GCP)', 'MLOps'],
                    'Nice-to-Have': ['Reinforcement Learning', 'Edge AI', 'Model Optimization', 'Research Paper Implementation']
                },
                'skill_gaps': {
                    'Critical Priority': ['Machine Learning Algorithms', 'Deep Neural Networks', 'Model Training & Evaluation'],
                    'High Priority': ['TensorFlow/PyTorch Frameworks', 'NLP Techniques', 'Computer Vision'],
                    'Medium Priority': ['Cloud ML Deployment', 'MLOps Practices', 'Advanced Statistics']
                },
                'learning_timeline': {
                    'Month 1-2': 'Machine Learning Fundamentals & Python for ML',
                    'Month 3-4': 'Deep Learning & Neural Networks',
                    'Month 5-6': 'Specialized Areas (NLP/Computer Vision)',
                    'Month 7-9': 'Framework Mastery (TensorFlow/PyTorch)',
                    'Month 10-12': 'Real Projects & Portfolio Building'
                },
                'resources': [
                    'Andrew Ng\'s Machine Learning Course (Coursera)',
                    'Deep Learning Specialization (deeplearning.ai)',
                    'Fast.ai Practical Deep Learning',
                    'Kaggle Competitions for Practice',
                    'Google ML Crash Course',
                    'PyTorch/TensorFlow Official Tutorials'
                ]
            }
    
    def generate_salary_negotiation_strategy(self, user_data: Dict[str, Any], job_offer: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized salary negotiation strategy
        """
        prompt = f"""
        Create a detailed salary negotiation strategy.
        
        Candidate Profile:
        - Current Salary: ₹{user_data.get('current_salary', 0)}
        - Experience: {user_data.get('experience_years', 0)} years
        - Skills: {', '.join(user_data.get('skills', []))}
        - Location: {user_data.get('location', 'India')}
        
        Job Offer:
        - Offered Salary: ₹{job_offer.get('offered_salary', 0)}
        - Role: {job_offer.get('role', '')}
        - Company: {job_offer.get('company', '')}
        
        Provide:
        1. Market salary range for this role (percentile breakdown)
        2. Your position in the market (where you stand)
        3. Negotiation leverage points (skills, experience, demand)
        4. Counter-offer recommendation (specific number)
        5. Negotiation script (word-for-word dialogue)
        6. Alternative benefits to negotiate (if salary is fixed)
        7. Red flags to watch for
        8. When to walk away
        
        Return as JSON with: market_range, your_position, leverage_points, counter_offer, negotiation_script, alternative_benefits, red_flags, walk_away_threshold.
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
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Salary negotiation error: {e}")
            # Return structured fallback data
            try:
                offered = int(job_offer.get('offered_salary', 700000))
            except (ValueError, TypeError):
                offered = 700000
            
            return {
                'market_range': {
                    '25th Percentile': f'₹{int(offered * 0.85):,}',
                    '50th Percentile (Median)': f'₹{offered:,}',
                    '75th Percentile': f'₹{int(offered * 1.15):,}',
                    '90th Percentile': f'₹{int(offered * 1.30):,}'
                },
                'your_position': 'Based on your experience and skills, you are positioned around the 60th percentile',
                'counter_offer': f'₹{int(offered * 1.12):,} (12% higher than offer)',
                'negotiation_script': '''Thank you for the offer. I'm very excited about this opportunity. Based on my research and considering my experience and skills in [key skills], I was expecting a range of ₹[counter_offer]. Would there be flexibility to meet somewhere in this range?\n\nI'm particularly valuable because of my expertise in [specific skill] and track record of [specific achievement]. I believe this would bring significant value to your team.''',
                'alternative_benefits': [
                    'Sign-on bonus (₹50,000-₹100,000)',
                    'Performance bonus structure',
                    'Stock options or equity',
                    'Additional paid leave days',
                    'Learning & development budget',
                    'Remote work flexibility',
                    'Earlier salary review (6 months vs 12 months)'
                ],
                'red_flags': ['Unwillingness to negotiate at all', 'Unclear job responsibilities', 'High employee turnover mentioned'],
                'walk_away_threshold': f'If final offer is below ₹{int(offered * 0.95):,} with no additional benefits'
            }
    
    def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """
        Deep analysis of job description with matching strategy
        """
        prompt = f"""
        Analyze this job description comprehensively.
        
        Job Description:
        {job_description}
        
        Extract and analyze:
        1. Required skills (technical and soft skills)
        2. Hidden requirements (reading between the lines)
        3. Company culture indicators
        4. Red flags or concerns
        5. Keywords for ATS optimization
        6. Estimated salary range (in INR)
        7. Career growth potential
        8. Work-life balance indicators
        9. Remote work compatibility score
        10. Application tips specific to this role
        
        Return as JSON with: required_skills, hidden_requirements, culture_indicators, red_flags, ats_keywords, salary_range, growth_potential, work_life_balance, remote_score, application_tips.
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
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Job description analysis error: {e}")
            # Return structured fallback data
            return {
                'required_skills': {
                    'Technical Skills': ['Programming', 'Problem Solving', 'System Design', 'Database Management'],
                    'Soft Skills': ['Communication', 'Teamwork', 'Leadership', 'Time Management']
                },
                'hidden_requirements': [
                    'Self-starter who can work independently',
                    'Ability to learn new technologies quickly',
                    'Experience with agile methodologies',
                    'Strong attention to detail'
                ],
                'culture_indicators': [
                    'Fast-paced environment',
                    'Collaborative team structure',
                    'Innovation-focused',
                    'Results-driven approach'
                ],
                'red_flags': [
                    'Check for unrealistic expectations',
                    'Verify work-life balance policies',
                    'Research company reviews online'
                ],
                'ats_keywords': ['experience', 'development', 'technical', 'project', 'team', 'skills'],
                'salary_range': '₹6,00,000 - ₹12,00,000 per annum (based on experience)',
                'growth_potential': 'Good opportunities for advancement with skill development',
                'work_life_balance': 'Standard - verify during interview',
                'remote_score': '7/10 - Hybrid work likely available',
                'application_tips': [
                    'Highlight relevant project experience',
                    'Use keywords from job description in your resume',
                    'Prepare specific examples of problem-solving',
                    'Research the company thoroughly before interview',
                    'Quantify your achievements with metrics'
                ]
            }
    
    def generate_personalized_learning_path(self, user_profile: Dict[str, Any], goal: str) -> Dict[str, Any]:
        """
        Create personalized learning roadmap with weekly milestones
        """
        prompt = f"""
        Create a comprehensive, personalized learning path.
        
        Current Profile:
        - Current Skills: {', '.join(user_profile.get('skills', []))}
        - Learning Style: {user_profile.get('learning_style', 'balanced')}
        - Time Available: {user_profile.get('hours_per_week', 10)} hours/week
        - Budget: ₹{user_profile.get('budget', 10000)}
        
        Goal: {goal}
        
        Create a detailed learning roadmap including:
        1. Learning phases (Foundation → Intermediate → Advanced → Expert)
        2. Week-by-week curriculum (specific topics)
        3. Recommended resources (courses, books, videos) with costs
        4. Practice projects for each phase
        5. Milestones and assessments
        6. Time estimates for each phase
        7. Total cost breakdown
        8. Success metrics
        
        Return as JSON with: phases, weekly_curriculum, resources, projects, milestones, time_estimates, cost_breakdown, success_metrics.
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
            
            return json.loads(result_text)
        except Exception as e:
            print(f"Learning path generation error: {e}")
            # Return comprehensive fallback learning path
            goal = goal if goal else "Target Role"
            return {
                'phases': {
                    'Foundation (Weeks 1-4)': {
                        'topics': ['Core fundamentals', 'Basic concepts', 'Programming basics', 'Problem-solving'],
                        'duration': '4 weeks'
                    },
                    'Intermediate (Weeks 5-12)': {
                        'topics': ['Advanced concepts', 'Practical applications', 'Framework learning', 'Project work'],
                        'duration': '8 weeks'
                    },
                    'Advanced (Weeks 13-20)': {
                        'topics': ['Specialized skills', 'Real-world projects', 'Industry best practices', 'Performance optimization'],
                        'duration': '8 weeks'
                    },
                    'Expert (Weeks 21-24)': {
                        'topics': ['Master-level projects', 'System design', 'Production deployment', 'Portfolio building'],
                        'duration': '4 weeks'
                    }
                },
                'weekly_curriculum': {
                    'Week 1-2': 'Introduction and basic setup - Learn fundamentals',
                    'Week 3-4': 'Core concepts mastery',
                    'Week 5-8': 'Framework and tools learning',
                    'Week 9-12': 'Building small projects',
                    'Week 13-16': 'Advanced topics and specialization',
                    'Week 17-20': 'Real-world project development',
                    'Week 21-24': 'Portfolio and final projects'
                },
                'recommended_resources': [
                    {
                        'name': 'Online Platform Course (e.g., Coursera, Udemy)',
                        'type': 'Online Course',
                        'cost': '₹2,000 - ₹5,000',
                        'duration': '8-12 weeks'
                    },
                    {
                        'name': 'Specialization Certificate',
                        'type': 'Certification',
                        'cost': '₹10,000 - ₹20,000',
                        'duration': '3-6 months'
                    },
                    {
                        'name': 'Technical Books (3-5 recommended)',
                        'type': 'Books',
                        'cost': '₹3,000 - ₹5,000',
                        'duration': 'Self-paced'
                    },
                    {
                        'name': 'Practice Platform Subscription',
                        'type': 'Platform',
                        'cost': '₹1,000 - ₹3,000/month',
                        'duration': '6 months'
                    }
                ],
                'practice_projects': [
                    'Project 1: Beginner-level application to understand basics',
                    'Project 2: Intermediate project with database integration',
                    'Project 3: Full-stack application with authentication',
                    'Project 4: Advanced project with real-world use case',
                    'Project 5: Portfolio-worthy capstone project'
                ],
                'milestones': [
                    'Month 1: Complete fundamentals and build first project',
                    'Month 2: Master intermediate concepts with 2 projects',
                    'Month 3: Learn advanced topics and frameworks',
                    'Month 4: Build 2 real-world projects',
                    'Month 5: Specialize and optimize skills',
                    'Month 6: Complete portfolio and prepare for job applications'
                ],
                'estimated_time': '24 weeks (6 months)',
                'total_budget': f"₹{int(user_profile.get('budget', 100000)):,}",
                'success_metrics': [
                    'Complete all weekly assignments',
                    'Build 5 portfolio projects',
                    'Contribute to 2 open-source projects',
                    'Achieve certification',
                    'Land first job/project in target role'
                ],
                'tips': [
                    'Practice coding daily for consistency',
                    'Join online communities for support',
                    'Build projects while learning',
                    'Document your learning journey',
                    'Network with professionals in the field'
                ]
            }
    
    def generate_industry_insights(self, industry: str) -> Dict[str, Any]:
        """
        Generate real-time industry insights and trends
        """
        prompt = f"""
        Provide comprehensive insights for the {industry} industry in 2025.
        
        Include:
        1. Top 10 trending technologies/skills
        2. Emerging job roles (next 2-3 years)
        3. Skills becoming obsolete
        4. Salary trends (growth rates)
        5. Top hiring companies
        6. Remote work trends
        7. Industry challenges and opportunities
        8. Geographic hotspots (best cities for this industry)
        9. Startup vs Corporate comparison
        10. Future outlook (5-year prediction)
        
        Return as JSON with all sections.
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
            
            return json.loads(result_text)
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_ats_score(self, resume_data: Dict) -> int:
        """Calculate ATS optimization score"""
        score = 0
        
        # Check for key sections
        if 'summary' in resume_data and len(resume_data['summary']) > 50:
            score += 20
        if 'skills' in resume_data:
            score += 25
        if 'experience' in resume_data:
            score += 25
        if 'ats_keywords' in resume_data and len(resume_data.get('ats_keywords', [])) > 10:
            score += 30
        
        return min(score, 100)
    
    def _get_optimization_tips(self, resume_data: Dict) -> List[str]:
        """Get resume optimization tips"""
        tips = []
        
        if 'summary' not in resume_data or len(resume_data.get('summary', '')) < 50:
            tips.append("Add a compelling professional summary (50-75 words)")
        
        if 'ats_keywords' not in resume_data or len(resume_data.get('ats_keywords', [])) < 15:
            tips.append("Include more industry-specific keywords for ATS")
        
        if 'projects' not in resume_data:
            tips.append("Add relevant projects with impact metrics")
        
        return tips
    
    def _generate_fallback_resume(self, user_data: Dict) -> Dict:
        """Generate basic fallback resume if AI fails"""
        return {
            'summary': f"Experienced {user_data.get('target_role', 'professional')} with strong technical skills.",
            'skills': user_data.get('skills', []),
            'experience': user_data.get('experience', []),
            'education': user_data.get('education', '')
        }
