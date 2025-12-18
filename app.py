from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
import time
from dotenv import load_dotenv
from modules.skill_mapping import SkillMappingEngine
from modules.job_market_analysis import JobMarketAnalyzer
from modules.career_recommender import CareerRecommender
from modules.learning_planner import LearningPlanGenerator
from modules.resume_prep import ResumePreparation
from modules.ai_skill_assessment import AISkillAssessment
from modules.ai_interview_prep import AIInterviewPreparation
from modules.gemini_ai_engine import GeminiAIEngine
from modules.advanced_mock_interview import AdvancedMockInterview
import sqlite3

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize AI modules
skill_mapper = SkillMappingEngine()
job_analyzer = JobMarketAnalyzer()
career_recommender = CareerRecommender()
learning_planner = LearningPlanGenerator()
resume_prep = ResumePreparation()
ai_assessment = AISkillAssessment()
ai_interview = AIInterviewPreparation()
gemini_engine = GeminiAIEngine()  # Advanced Gemini AI Engine
mock_interview = AdvancedMockInterview()  # Advanced Mock Interview Module

@app.route('/')
def index():
    """Hackathon Edition - Advanced Gemini Features (Main Page)"""
    return render_template('index_gemini.html')

@app.route('/gemini')
def gemini_features():
    """Hackathon Edition - Advanced Gemini Features"""
    return render_template('index_gemini.html')

@app.route('/old')
def old_index():
    """Old basic interface"""
    return render_template('index.html')

@app.route('/mock-interview')
def mock_interview_demo():
    """Advanced Mock Interview Demo Page"""
    return render_template('mock_interview_demo.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_student():
    try:
        data = request.json
        student_data = {
            'skills': data.get('skills', []),
            'interests': data.get('interests', []),
            'education': data.get('education', ''),
            'experience': data.get('experience', ''),
            'goals': data.get('goals', '')
        }
        
        # Step 1: Skill Mapping
        skill_analysis = skill_mapper.analyze_skills(student_data)
        
        # Step 2: Job Market Analysis
        market_analysis = job_analyzer.analyze_market(skill_analysis)
        
        # Step 3: Career Recommendations
        career_recommendations = career_recommender.get_recommendations(
            skill_analysis, market_analysis, student_data
        )
        
        # Step 4: Learning Plan
        learning_plan = learning_planner.generate_plan(
            skill_analysis, career_recommendations, student_data
        )
        
        # Step 5: Resume & Interview Prep
        resume_guidance = resume_prep.prepare_guidance(
            student_data, career_recommendations, skill_analysis
        )
        
        return jsonify({
            'success': True,
            'skill_analysis': skill_analysis,
            'market_analysis': market_analysis,
            'career_recommendations': career_recommendations,
            'learning_plan': learning_plan,
            'resume_guidance': resume_guidance
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get available skills from the database"""
    return jsonify(skill_mapper.get_available_skills())

@app.route('/api/industries', methods=['GET'])
def get_industries():
    """Get available industries for interest selection"""
    return jsonify(job_analyzer.get_available_industries())

def init_database():
    """Initialize SQLite database with sample data"""
    conn = sqlite3.connect('career_advisor.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            category TEXT,
            description TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS careers (
            id INTEGER PRIMARY KEY,
            title TEXT,
            industry TEXT,
            required_skills TEXT,
            salary_range TEXT,
            growth_rate REAL,
            description TEXT
        )
    ''')
    
    # Insert sample data
    sample_skills = [
        ('Python Programming', 'Technical', 'Programming language for data science and web development'),
        ('Machine Learning', 'Technical', 'AI/ML algorithms and model development'),
        ('Data Analysis', 'Technical', 'Statistical analysis and data visualization'),
        ('Project Management', 'Soft Skills', 'Leading teams and managing projects'),
        ('Communication', 'Soft Skills', 'Verbal and written communication skills'),
        ('Problem Solving', 'Soft Skills', 'Analytical thinking and creative solutions'),
        ('JavaScript', 'Technical', 'Web development and frontend programming'),
        ('SQL', 'Technical', 'Database management and querying'),
        ('Leadership', 'Soft Skills', 'Team leadership and management'),
        ('Critical Thinking', 'Soft Skills', 'Logical analysis and evaluation')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO skills (name, category, description) VALUES (?, ?, ?)', sample_skills)
    
    sample_careers = [
        ('Data Scientist', 'Technology', 'Python Programming,Machine Learning,Data Analysis,Statistics', '₹8,00,000 - ₹15,00,000', 15.0, 'Analyze complex data to help organizations make decisions'),
        ('Software Engineer', 'Technology', 'Python Programming,JavaScript,SQL,Problem Solving', '₹7,00,000 - ₹13,00,000', 12.0, 'Design and develop software applications'),
        ('Product Manager', 'Technology', 'Project Management,Communication,Leadership,Critical Thinking', '₹9,00,000 - ₹16,00,000', 8.0, 'Lead product development and strategy'),
        ('Data Analyst', 'Technology', 'Data Analysis,SQL,Python Programming,Communication', '₹6,00,000 - ₹10,00,000', 10.0, 'Interpret data and turn it into information'),
        ('Machine Learning Engineer', 'Technology', 'Machine Learning,Python Programming,Data Analysis,Problem Solving', '₹8,50,000 - ₹14,00,000', 20.0, 'Build and deploy ML models in production')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO careers (title, industry, required_skills, salary_range, growth_rate, description) VALUES (?, ?, ?, ?, ?, ?)', sample_careers)
    
    conn.commit()
    conn.close()

# AI Skill Assessment Routes
@app.route('/api/assessment/start', methods=['POST'])
def start_assessment():
    try:
        data = request.json
        user_id = data.get('user_id')
        result = ai_assessment.start_assessment(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessment/submit', methods=['POST'])
def submit_assessment():
    try:
        data = request.json
        user_id = data.get('user_id')
        answer = data.get('answer')
        result = ai_assessment.submit_answer(user_id, answer)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessment/history/<user_id>', methods=['GET'])
def get_assessment_history(user_id):
    try:
        history = ai_assessment.get_assessment_history(user_id)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assessment/insights/<user_id>', methods=['GET'])
def get_assessment_insights(user_id):
    try:
        insights = ai_assessment.get_skill_insights(user_id)
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# AI Interview Preparation Routes
@app.route('/api/interview/start', methods=['POST'])
def start_interview():
    try:
        data = request.json
        user_id = data.get('user_id')
        interview_type = data.get('interview_type', 'technical')
        difficulty = data.get('difficulty', 'intermediate')
        result = ai_interview.start_mock_interview(user_id, interview_type, difficulty)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interview/submit', methods=['POST'])
def submit_interview():
    try:
        data = request.json
        user_id = data.get('user_id')
        answer = data.get('answer')
        result = ai_interview.submit_answer(user_id, answer)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interview/history/<user_id>', methods=['GET'])
def get_interview_history(user_id):
    try:
        history = ai_interview.get_interview_history(user_id)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interview/insights/<user_id>', methods=['GET'])
def get_interview_insights(user_id):
    try:
        insights = ai_interview.get_interview_insights(user_id)
        return jsonify(insights)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Resume Generation Route
@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.json
        resume_data = {
            'personal_info': data.get('personal_info', {}),
            'experience': data.get('experience', []),
            'education': data.get('education', []),
            'skills': data.get('skills', {}),
            'use_ai': data.get('use_ai', False)
        }
        
        # Generate resume content
        resume_content = resume_prep.generate_resume_content(resume_data)
        
        # Generate PDF
        pdf_filename = resume_prep.generate_pdf_resume(resume_content, resume_data['personal_info'].get('full_name', 'Resume'))
        
        # Extract just the filename from the full path
        filename_only = os.path.basename(pdf_filename)
        
        return jsonify({
            'success': True,
            'resume_content': resume_content,
            'download_url': f'/downloads/{filename_only}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    try:
        from flask import send_file
        import os
        file_path = os.path.join('downloads', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ADVANCED GEMINI AI FEATURES ====================

@app.route('/api/gemini/ats-resume', methods=['POST'])
def generate_ats_resume():
    """Generate ATS-optimized resume using Gemini AI"""
    try:
        data = request.json
        result = gemini_engine.generate_ats_optimized_resume(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate personalized cover letter"""
    try:
        data = request.json
        user_data = data.get('user_data', {})
        job_description = data.get('job_description', '')
        
        cover_letter = gemini_engine.generate_personalized_cover_letter(user_data, job_description)
        return jsonify({'success': True, 'cover_letter': cover_letter})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/linkedin-analysis', methods=['POST'])
def analyze_linkedin():
    """Analyze and optimize LinkedIn profile"""
    try:
        data = request.json
        print(f"Received LinkedIn data: {data}")
        analysis = gemini_engine.analyze_linkedin_profile(data)
        print(f"Analysis result: {type(analysis)}")
        
        # Ensure analysis is a dict
        if isinstance(analysis, str):
            return jsonify({'success': True, 'analysis': {'message': analysis}})
        elif isinstance(analysis, dict):
            return jsonify({'success': True, 'analysis': analysis})
        else:
            return jsonify({'success': True, 'analysis': {'result': str(analysis)}})
    except Exception as e:
        print(f"LinkedIn analysis error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e), 'details': 'Check server logs for more information'}), 500

@app.route('/api/gemini/mock-interview', methods=['POST'])
def mock_interview():
    """Generate mock interview questions"""
    try:
        data = request.json
        role = data.get('role', 'Software Engineer')
        difficulty = data.get('difficulty', 'medium')
        question_number = data.get('question_number', 1)
        
        print(f"Generating interview for role: {role}, difficulty: {difficulty}")
        
        interview_data = gemini_engine.conduct_mock_interview(role, difficulty, question_number)
        
        print(f"Interview data generated: {interview_data}")
        
        # Check if interview_data is None or has error
        if interview_data is None:
            return jsonify({'success': False, 'error': 'Failed to generate interview question'}), 500
        if 'error' in interview_data:
            return jsonify({'success': False, 'error': interview_data['error']}), 500
        
        # Ensure required fields exist
        if 'question' not in interview_data:
            interview_data['question'] = 'Could not generate question. Please try again.'
        
        return jsonify({'success': True, 'interview': interview_data})
    except Exception as e:
        print(f"Mock interview error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/evaluate-answer', methods=['POST'])
def evaluate_answer():
    """Evaluate interview answer with AI feedback"""
    try:
        data = request.json
        question = data.get('question', '')
        answer = data.get('answer', '')
        role = data.get('role', 'Software Engineer')
        
        evaluation = gemini_engine.evaluate_interview_answer(question, answer, role)
        return jsonify({'success': True, 'evaluation': evaluation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/career-trajectory', methods=['POST'])
def predict_career_trajectory():
    """Predict 5-year career trajectory"""
    try:
        data = request.json
        trajectory = gemini_engine.predict_career_trajectory(data)
        return jsonify({'success': True, 'trajectory': trajectory})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/skill-gaps', methods=['POST'])
def analyze_skill_gaps():
    """Analyze skill gaps with learning recommendations"""
    try:
        data = request.json
        current_skills = data.get('current_skills', [])
        target_role = data.get('target_role', 'Software Engineer')
        
        gap_analysis = gemini_engine.analyze_skill_gaps(current_skills, target_role)
        return jsonify({'success': True, 'analysis': gap_analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/salary-negotiation', methods=['POST'])
def salary_negotiation():
    """Generate salary negotiation strategy"""
    try:
        data = request.json
        user_data = data.get('user_data', {})
        job_offer = data.get('job_offer', {})
        
        strategy = gemini_engine.generate_salary_negotiation_strategy(user_data, job_offer)
        return jsonify({'success': True, 'strategy': strategy})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/job-analysis', methods=['POST'])
def analyze_job():
    """Deep analysis of job description"""
    try:
        data = request.json
        job_description = data.get('job_description', '')
        
        analysis = gemini_engine.analyze_job_description(job_description)
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/learning-path', methods=['POST'])
def create_learning_path():
    """Generate personalized learning roadmap"""
    try:
        data = request.json
        user_profile = data.get('user_profile', {})
        goal = data.get('goal', 'Become a Full Stack Developer')
        
        learning_path = gemini_engine.generate_personalized_learning_path(user_profile, goal)
        return jsonify({'success': True, 'learning_path': learning_path})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/gemini/industry-insights', methods=['POST'])
def industry_insights():
    """Get real-time industry insights"""
    try:
        data = request.json
        industry = data.get('industry', 'Technology')
        
        insights = gemini_engine.generate_industry_insights(industry)
        return jsonify({'success': True, 'insights': insights})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== END GEMINI AI FEATURES ====================

# ==================== ADVANCED MOCK INTERVIEW FEATURES ====================

@app.route('/api/interview/test-connection', methods=['GET'])
def test_interview_api():
    """Test if interview API is working"""
    try:
        result = mock_interview.test_api_connection()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/interview/start-session', methods=['POST'])
def start_interview_session():
    """Start a new mock interview session"""
    try:
        data = request.json
        user_id = data.get('user_id', 'user_' + str(int(time.time())))
        role = data.get('role', 'Software Engineer')
        difficulty = data.get('difficulty', 'medium')
        
        result = mock_interview.start_interview_session(user_id, role, difficulty)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/interview/submit-answer', methods=['POST'])
def submit_interview_answer():
    """Submit answer to current interview question"""
    try:
        data = request.json
        session_id = data.get('session_id')
        answer = data.get('answer')
        
        if not session_id or not answer:
            return jsonify({'success': False, 'error': 'Missing session_id or answer'}), 400
        
        result = mock_interview.submit_answer(session_id, answer)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/interview/history/<user_id>', methods=['GET'])
def get_interview_history_route(user_id):
    """Get interview history for a user"""
    try:
        history = mock_interview.get_interview_history(user_id)
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/interview/session/<session_id>', methods=['GET'])
def get_session_details_route(session_id):
    """Get details of a specific interview session"""
    try:
        details = mock_interview.get_session_details(session_id)
        return jsonify({'success': True, 'session': details})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== END ADVANCED MOCK INTERVIEW FEATURES ====================

if __name__ == '__main__':
    # Initialize database
    init_database()
    print("\n" + "="*70)
    print("🚀 AI Career Advisor - Hackathon Edition")
    print("="*70)
    print("✨ Features:")
    print("   • ATS-Optimized Resume Generation")
    print("   • Personalized Cover Letters")
    print("   • LinkedIn Profile Optimization")
    print("   • AI Mock Interviews with Real-time Feedback")
    print("   • 5-Year Career Trajectory Prediction")
    print("   • Skill Gap Analysis & Learning Paths")
    print("   • Salary Negotiation Strategies")
    print("   • Job Description Deep Analysis")
    print("   • Industry Insights & Trends")
    print("="*70)
    print("🌐 Server running at: http://localhost:5000")
    print("📊 Powered by: Gemini AI 1.5 Pro")
    print("="*70 + "\n")
    app.run(debug=False, host='0.0.0.0', port=5000)
