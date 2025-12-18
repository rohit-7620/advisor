"""
Vercel Serverless Function for CareerNexus API
This module imports and wraps the Flask app routes for serverless deployment
"""
import os
import sys
from pathlib import Path

# Add parent directory to path to import modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Import AI modules
from modules.gemini_ai_engine import (
    generate_ats_resume,
    generate_cover_letter,
    optimize_linkedin_profile,
    conduct_mock_interview,
    evaluate_interview_answer,
    predict_career_trajectory,
    analyze_skill_gaps,
    generate_salary_negotiation_strategy,
    analyze_job_description,
    generate_personalized_learning_path
)

app = Flask(__name__)
CORS(app)

@app.route('/api/gemini/ats-resume', methods=['POST'])
def ats_resume():
    try:
        data = request.json
        result = generate_ats_resume(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            target_role=data.get('target_role'),
            years_experience=data.get('years_experience'),
            skills=data.get('skills', []),
            education=data.get('education'),
            experience=data.get('experience'),
            achievements=data.get('achievements')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/cover-letter', methods=['POST'])
def cover_letter():
    try:
        data = request.json
        result = generate_cover_letter(
            user_profile=data.get('user_profile', {}),
            job_details=data.get('job_details', {})
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/linkedin-optimizer', methods=['POST'])
def linkedin_optimizer():
    try:
        data = request.json
        result = optimize_linkedin_profile(
            current_profile=data.get('current_profile', {}),
            target_role=data.get('target_role', ''),
            industry=data.get('industry', '')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/mock-interview', methods=['POST'])
def mock_interview():
    try:
        data = request.json
        result = conduct_mock_interview(
            role=data.get('role'),
            difficulty=data.get('difficulty', 'medium')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/evaluate-answer', methods=['POST'])
def evaluate_answer():
    try:
        data = request.json
        result = evaluate_interview_answer(
            question=data.get('question'),
            answer=data.get('answer'),
            role=data.get('role')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/career-trajectory', methods=['POST'])
def career_trajectory():
    try:
        data = request.json
        result = predict_career_trajectory(
            user_profile=data.get('user_profile', {})
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/skill-gap', methods=['POST'])
def skill_gap():
    try:
        data = request.json
        result = analyze_skill_gaps(
            user_profile=data.get('user_profile', {}),
            target_role=data.get('target_role', '')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/salary-negotiation', methods=['POST'])
def salary_negotiation():
    try:
        data = request.json
        result = generate_salary_negotiation_strategy(
            user_profile=data.get('user_profile', {}),
            job_offer=data.get('job_offer', {})
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/job-analysis', methods=['POST'])
def job_analysis():
    try:
        data = request.json
        result = analyze_job_description(
            job_description=data.get('job_description', ''),
            user_skills=data.get('user_skills', [])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gemini/learning-path', methods=['POST'])
def learning_path():
    try:
        data = request.json
        result = generate_personalized_learning_path(
            user_profile=data.get('user_profile', {}),
            target_skills=data.get('target_skills', [])
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel handler
def handler(request):
    """Vercel serverless function handler"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()
