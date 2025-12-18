import json
from typing import Dict, List, Any
from datetime import datetime
import random
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
import requests

# Lazy-load Gemini to avoid heavy import delays at startup
def _get_genai():
    try:
        import google.generativeai as _genai
        return _genai
    except Exception:
        return None

class ResumePreparation:
    def __init__(self):
        self.resume_templates = self._load_resume_templates()
        self.interview_questions = self._load_interview_questions()
        self.skill_keywords = self._load_skill_keywords()
    
    def _load_resume_templates(self) -> Dict[str, Dict]:
        """Load comprehensive resume templates for different career paths"""
        return {
            'Data Scientist': {
                'template_name': 'Data Science Professional',
                'sections': {
                    'summary': 'Passionate data scientist with expertise in machine learning, statistical analysis, and data visualization. Proven track record of delivering actionable insights from complex datasets and driving business growth through data-driven solutions.',
                    'technical_skills': [
                        'Programming: Python, R, SQL, JavaScript',
                        'Machine Learning: Scikit-learn, TensorFlow, PyTorch, XGBoost',
                        'Data Visualization: Matplotlib, Seaborn, Plotly, Tableau, Power BI',
                        'Statistical Analysis: Hypothesis Testing, A/B Testing, Regression Analysis',
                        'Big Data Tools: Hadoop, Spark, Apache Kafka, Airflow',
                        'Cloud Platforms: AWS, Azure, Google Cloud Platform',
                        'Databases: PostgreSQL, MongoDB, Redis, Elasticsearch'
                    ],
                    'experience_format': '''Data Scientist | TechCorp Solutions | Jan 2022 - Present
• Developed ML models that improved customer retention by 25% and increased revenue by ₹50L
• Analyzed 10M+ customer records using Python and SQL, identifying key behavioral patterns
• Created interactive dashboards using Tableau, reducing reporting time by 60%
• Collaborated with cross-functional teams to implement data-driven decision making
• Mentored 3 junior data scientists and conducted technical training sessions

Junior Data Analyst | DataInsights Pvt Ltd | Jun 2020 - Dec 2021
• Performed statistical analysis on sales data, leading to 15% improvement in forecasting accuracy
• Built automated ETL pipelines using Python and Apache Airflow
• Created monthly business intelligence reports for senior management''',
                    'education_format': 'Master of Science in Data Science | IIT Delhi | 2018-2020\nBachelor of Technology in Computer Science | NIT Surat | 2014-2018',
                    'projects_format': '''Machine Learning Sales Prediction Model | GitHub: github.com/username/sales-prediction
• Built end-to-end ML pipeline using Python, Scikit-learn, and XGBoost
• Achieved 92% accuracy on test dataset with 15% improvement over baseline
• Deployed model using Flask API and Docker containerization
• Technologies: Python, Pandas, Scikit-learn, XGBoost, Flask, Docker

Real-time Data Analytics Dashboard | GitHub: github.com/username/dashboard
• Created interactive dashboard using Python, Plotly, and Streamlit
• Processed real-time data from multiple sources using Apache Kafka
• Reduced data processing time by 40% through optimization
• Technologies: Python, Streamlit, Plotly, Apache Kafka, PostgreSQL'''
                }
            },
            'Software Engineer': {
                'template_name': 'Software Engineering Professional',
                'sections': {
                    'summary': 'Experienced software engineer with expertise in full-stack development, cloud technologies, and agile methodologies. Proven track record of building scalable applications and leading technical teams to deliver high-quality software solutions.',
                    'technical_skills': [
                        'Programming Languages: Python, JavaScript, Java, C++, TypeScript',
                        'Frontend: React, Angular, Vue.js, HTML5, CSS3, Bootstrap',
                        'Backend: Node.js, Django, Flask, Spring Boot, Express.js',
                        'Database Management: PostgreSQL, MongoDB, Redis, MySQL',
                        'Cloud Platforms: AWS, Azure, Google Cloud Platform',
                        'DevOps: Docker, Kubernetes, Jenkins, GitLab CI/CD',
                        'Version Control: Git, GitHub, GitLab, Bitbucket'
                    ],
                    'experience_format': '''Senior Software Engineer | TechStart India | Mar 2021 - Present
• Led development of microservices architecture serving 100K+ users daily
• Implemented CI/CD pipelines reducing deployment time by 70%
• Mentored 4 junior developers and conducted code reviews
• Optimized database queries resulting in 50% faster response times
• Technologies: Python, React, AWS, Docker, PostgreSQL

Software Engineer | InnovateTech Solutions | Jun 2019 - Feb 2021
• Developed full-stack web applications using React and Node.js
• Collaborated with product managers to define technical requirements
• Implemented automated testing increasing code coverage to 85%
• Built RESTful APIs handling 10K+ requests per minute
• Technologies: JavaScript, React, Node.js, MongoDB, AWS''',
                    'education_format': 'Bachelor of Technology in Computer Science | IIT Bombay | 2015-2019\nCertified AWS Solutions Architect | Amazon Web Services | 2020',
                    'projects_format': '''E-commerce Platform | GitHub: github.com/username/ecommerce-platform
• Built full-stack e-commerce application with React frontend and Node.js backend
• Implemented payment gateway integration with Razorpay
• Achieved 99.9% uptime with load balancing and auto-scaling
• Technologies: React, Node.js, MongoDB, AWS, Razorpay, Docker

Real-time Chat Application | GitHub: github.com/username/chat-app
• Developed real-time messaging app using Socket.io and React
• Implemented end-to-end encryption for secure communication
• Supports 1000+ concurrent users with Redis caching
• Technologies: React, Socket.io, Node.js, Redis, MongoDB'''
                }
            },
            'Product Manager': {
                'template_name': 'Product Management Professional',
                'sections': {
                    'summary': 'Strategic product manager with experience in product development, market analysis, and cross-functional team leadership. Strong analytical skills and customer-focused approach.',
                    'technical_skills': [
                        'Product Strategy & Roadmapping',
                        'Data Analysis & Market Research',
                        'Agile/Scrum Methodologies',
                        'Project Management Tools (Jira, Asana)',
                        'User Experience Design'
                    ],
                    'experience_format': 'Product Manager | Company | Date\n• Led product development from concept to launch\n• Analyzed market trends and user feedback\n• Coordinated with engineering and design teams',
                    'education_format': 'Degree in Business/Engineering/Related Field',
                    'projects_format': 'Product Launch | Results\n• Launched new feature that increased user engagement by 30%\n• Conducted user research and A/B testing'
                }
            }
        }
    
    def _load_interview_questions(self) -> Dict[str, List[Dict]]:
        """Load comprehensive interview questions by career and skill level"""
        return {
            'Data Scientist': [
                {
                    'question': 'Explain the difference between supervised and unsupervised learning with real-world examples.',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': 'Supervised learning uses labeled data to train models for predictions. Example: Email spam detection using labeled emails. Unsupervised learning finds hidden patterns without labels. Example: Customer segmentation based on purchasing behavior.',
                    'follow_up': 'How would you choose between supervised and unsupervised learning for a new project?',
                    'key_points': ['Clear problem definition', 'Data availability', 'Business objectives', 'Evaluation metrics']
                },
                {
                    'question': 'How would you handle missing data in a dataset? Walk me through your approach.',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': '1) Analyze missing data patterns (MCAR, MAR, MNAR), 2) Visualize missing data distribution, 3) Choose method: deletion for <5% missing, imputation for 5-30%, advanced modeling for >30%, 4) Validate approach with cross-validation.',
                    'follow_up': 'What if 40% of your target variable is missing?',
                    'key_points': ['Data analysis', 'Pattern identification', 'Method selection', 'Validation']
                },
                {
                    'question': 'Describe a challenging data science project you worked on. What was the problem and how did you solve it?',
                    'category': 'Behavioral',
                    'difficulty': 'Medium',
                    'sample_answer': 'I worked on predicting customer churn for a telecom company. The data was highly imbalanced (5% churn rate). I used SMOTE for oversampling, feature engineering, and ensemble methods (Random Forest + XGBoost). Achieved 85% precision and 78% recall.',
                    'follow_up': 'How did you measure success and what would you do differently?',
                    'key_points': ['Problem definition', 'Data challenges', 'Solution approach', 'Results and learnings']
                },
                {
                    'question': 'How do you ensure your machine learning model is not overfitting?',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': 'Use cross-validation, regularization techniques (L1/L2), early stopping, dropout for neural networks, and proper train/validation/test splits. Monitor learning curves and validation metrics.',
                    'follow_up': 'What if your model is underfitting instead?',
                    'key_points': ['Cross-validation', 'Regularization', 'Model complexity', 'Data quality']
                },
                {
                    'question': 'Explain the bias-variance tradeoff in machine learning.',
                    'category': 'Technical',
                    'difficulty': 'Hard',
                    'sample_answer': 'Bias is error from oversimplifying assumptions, variance is error from sensitivity to small fluctuations. High bias = underfitting, high variance = overfitting. Goal is to minimize total error by balancing both.',
                    'follow_up': 'How do you diagnose bias vs variance problems?',
                    'key_points': ['Error decomposition', 'Model complexity', 'Training vs validation error', 'Diagnostic techniques']
                }
            ],
            'Software Engineer': [
                {
                    'question': 'Explain the difference between REST and GraphQL APIs with examples.',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': 'REST uses HTTP methods (GET, POST, PUT, DELETE) with fixed endpoints returning complete resources. GraphQL uses a single endpoint with queries to fetch exactly needed data. REST: GET /users/1, GraphQL: query { user(id: 1) { name, email } }',
                    'follow_up': 'When would you choose GraphQL over REST?',
                    'key_points': ['Data fetching efficiency', 'Client requirements', 'Caching strategies', 'API evolution']
                },
                {
                    'question': 'How do you ensure code quality in a team environment? Walk me through your process.',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': '1) Code reviews for all PRs, 2) Automated testing (unit, integration, e2e), 3) CI/CD pipelines with quality gates, 4) Coding standards and linting, 5) Pair programming for complex features, 6) Regular refactoring sessions.',
                    'follow_up': 'How do you handle disagreements in code reviews?',
                    'key_points': ['Code reviews', 'Automated testing', 'CI/CD', 'Standards and guidelines']
                },
                {
                    'question': 'Describe a time when you had to debug a complex production issue. How did you approach it?',
                    'category': 'Behavioral',
                    'difficulty': 'Medium',
                    'sample_answer': 'We had a memory leak causing server crashes. I used profiling tools to identify the issue, analyzed heap dumps, and found a circular reference in our caching layer. Fixed it by implementing proper cleanup and added monitoring to prevent future occurrences.',
                    'follow_up': 'What preventive measures did you implement?',
                    'key_points': ['Problem identification', 'Debugging approach', 'Solution implementation', 'Prevention strategies']
                },
                {
                    'question': 'Explain microservices architecture and its benefits and challenges.',
                    'category': 'Technical',
                    'difficulty': 'Hard',
                    'sample_answer': 'Microservices break applications into small, independent services. Benefits: scalability, technology diversity, fault isolation. Challenges: distributed complexity, data consistency, network latency, service discovery.',
                    'follow_up': 'How do you handle data consistency in microservices?',
                    'key_points': ['Service independence', 'Scalability', 'Fault tolerance', 'Distributed challenges']
                },
                {
                    'question': 'How do you handle database migrations in a production environment?',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': 'Use backward-compatible migrations, blue-green deployments, feature flags, rollback plans, and test migrations on staging. For large changes, use gradual rollout with monitoring.',
                    'follow_up': 'What if a migration fails halfway through?',
                    'key_points': ['Backward compatibility', 'Rollback strategies', 'Testing', 'Monitoring']
                }
            ],
            'Product Manager': [
                {
                    'question': 'How do you prioritize features for a product roadmap?',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': 'I use frameworks like RICE (Reach, Impact, Confidence, Effort) or MoSCoW (Must have, Should have, Could have, Won\'t have) considering user value, business impact, and technical feasibility.',
                    'follow_up': 'How do you handle conflicting stakeholder priorities?'
                },
                {
                    'question': 'Describe your approach to user research.',
                    'category': 'Technical',
                    'difficulty': 'Medium',
                    'sample_answer': 'I combine quantitative data (analytics, surveys) with qualitative research (interviews, usability testing) to understand user needs and validate product decisions.',
                    'follow_up': 'How do you ensure research findings are actionable?'
                },
                {
                    'question': 'Tell me about a product that failed and what you learned.',
                    'category': 'Behavioral',
                    'difficulty': 'Medium',
                    'sample_answer': 'A feature I launched had low adoption because I didn\'t validate the user need properly. I learned the importance of user research and iterative validation.',
                    'follow_up': 'How did this change your approach to product development?'
                }
            ]
        }
    
    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        """Load ATS-friendly keywords for different skills"""
        return {
            'Python Programming': [
                'Python', 'Pandas', 'NumPy', 'Scikit-learn', 'Django', 'Flask',
                'Data Analysis', 'Machine Learning', 'Automation', 'API Development'
            ],
            'Machine Learning': [
                'Machine Learning', 'Deep Learning', 'Neural Networks', 'TensorFlow',
                'PyTorch', 'Model Training', 'Feature Engineering', 'Predictive Analytics'
            ],
            'Data Analysis': [
                'Data Analysis', 'SQL', 'Statistics', 'Data Visualization',
                'Business Intelligence', 'ETL', 'Data Mining', 'Statistical Modeling'
            ],
            'Project Management': [
                'Project Management', 'Agile', 'Scrum', 'Stakeholder Management',
                'Risk Management', 'Budget Planning', 'Team Leadership', 'Timeline Management'
            ],
            'Communication': [
                'Communication', 'Presentation Skills', 'Technical Writing',
                'Cross-functional Collaboration', 'Client Relations', 'Public Speaking'
            ]
        }
    
    def prepare_guidance(self, student_data: Dict, career_recommendations: Dict, 
                        skill_analysis: Dict) -> Dict[str, Any]:
        """
        Generate comprehensive resume and interview preparation guidance
        """
        top_careers = career_recommendations.get('top_careers', [])
        if not top_careers:
            return {'error': 'No career recommendations available for resume preparation'}
        
        # Get best career match
        best_career = top_careers[0]
        career_title = best_career['title']
        
        # Generate resume guidance
        resume_guidance = self._generate_resume_guidance(student_data, best_career, skill_analysis)
        
        # Generate interview preparation
        interview_prep = self._generate_interview_preparation(career_title, skill_analysis)
        
        # Generate portfolio recommendations
        portfolio_recommendations = self._generate_portfolio_recommendations(
            student_data, best_career, skill_analysis
        )
        
        # Generate networking guidance
        networking_guidance = self._generate_networking_guidance(career_title, best_career)
        
        # Generate interactive resume builder
        resume_builder = self._generate_resume_builder(student_data, best_career, skill_analysis)
        
        # Generate downloadable templates
        downloadable_templates = self._generate_downloadable_templates(career_title)
        
        # Generate ATS optimization tools
        ats_optimization = self._generate_ats_optimization_tools(career_title, skill_analysis)
        
        return {
            'resume_guidance': resume_guidance,
            'interview_preparation': interview_prep,
            'portfolio_recommendations': portfolio_recommendations,
            'networking_guidance': networking_guidance,
            'application_strategy': self._generate_application_strategy(best_career),
            'skill_optimization': self._optimize_skills_for_ats(skill_analysis, career_title),
            'resume_builder': resume_builder,
            'downloadable_templates': downloadable_templates,
            'ats_optimization': ats_optimization
        }
    
    def _generate_resume_guidance(self, student_data: Dict, career: Dict, 
                                 skill_analysis: Dict) -> Dict[str, Any]:
        """Generate comprehensive personalized resume guidance"""
        career_title = career['title']
        template = self.resume_templates.get(career_title, self.resume_templates['Software Engineer'])
        
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        return {
            'template_recommendation': template,
            'customized_sections': self._customize_resume_sections(template, student_data, skill_names),
            'ats_optimization': self._optimize_for_ats(career_title, skill_names),
            'formatting_tips': [
                'Use a clean, professional layout with consistent formatting',
                'Include relevant keywords from job descriptions naturally',
                'Quantify achievements with specific numbers and percentages',
                'Keep resume to 1-2 pages maximum (1 page for <5 years experience)',
                'Use strong action verbs to start bullet points (Led, Developed, Implemented)',
                'Use standard section headers (Experience, Education, Skills, Projects)',
                'Choose professional fonts like Arial, Calibri, or Times New Roman',
                'Maintain consistent spacing and alignment throughout',
                'Use bullet points for easy scanning by recruiters',
                'Include a professional summary tailored to the target role'
            ],
            'common_mistakes': [
                'Including irrelevant personal information (age, marital status, photo)',
                'Using unprofessional email addresses (funny123@email.com)',
                'Including outdated or irrelevant skills and technologies',
                'Having inconsistent formatting and font sizes',
                'Making spelling or grammar errors',
                'Using generic objective statements instead of professional summaries',
                'Including every job instead of relevant experience',
                'Using passive voice instead of active voice',
                'Not tailoring resume for specific job applications',
                'Including references directly on the resume'
            ],
            'tailoring_advice': self._generate_tailoring_advice(career, skill_names),
            'resume_sections': self._generate_resume_sections_guide(),
            'action_verbs': self._get_powerful_action_verbs(),
            'quantification_examples': self._get_quantification_examples(career_title),
            'keywords_by_section': self._get_keywords_by_section(career_title, skill_names)
        }
    
    def _customize_resume_sections(self, template: Dict, student_data: Dict, 
                                  skills: List[str]) -> Dict[str, str]:
        """Customize resume sections based on student data"""
        education = student_data.get('education', '')
        experience = student_data.get('experience', '')
        
        customized = template['sections'].copy()
        
        # Customize summary
        if skills:
            skill_highlights = ', '.join(skills[:3])
            customized['summary'] = f"Recent graduate with strong foundation in {skill_highlights}. {customized['summary']}"
        
        # Customize education
        if education:
            customized['education_format'] = f"{education} | {customized['education_format']}"
        
        # Customize experience
        if experience:
            customized['experience_format'] = f"{experience}\n{customized['experience_format']}"
        
        return customized
    
    def _optimize_for_ats(self, career_title: str, skills: List[str]) -> Dict[str, Any]:
        """Optimize resume for Applicant Tracking Systems"""
        relevant_keywords = []
        
        for skill in skills:
            keywords = self.skill_keywords.get(skill, [])
            relevant_keywords.extend(keywords)
        
        return {
            'recommended_keywords': list(set(relevant_keywords))[:15],
            'keyword_density_tips': [
                'Include keywords naturally in job descriptions',
                'Use variations of important keywords',
                'Include both technical and soft skills',
                'Match keywords from job postings'
            ],
            'ats_friendly_format': [
                'Use standard section headers (Experience, Education, Skills)',
                'Avoid graphics, tables, or complex formatting',
                'Use simple fonts like Arial or Calibri',
                'Save as .docx or .pdf format'
            ]
        }
    
    def _generate_tailoring_advice(self, career: Dict, skills: List[str]) -> List[str]:
        """Generate advice for tailoring resume to specific career"""
        advice = []
        
        # Industry-specific advice
        industry = career.get('industry', '')
        if industry == 'Technology':
            advice.append('Emphasize technical projects and coding experience')
            advice.append('Include GitHub profile and portfolio links')
        elif industry == 'Healthcare':
            advice.append('Highlight any healthcare-related experience or coursework')
            advice.append('Emphasize analytical and problem-solving skills')
        
        # Skill-based advice
        if 'Python Programming' in skills:
            advice.append('Include specific Python projects and libraries used')
        if 'Machine Learning' in skills:
            advice.append('Highlight ML projects and model performance metrics')
        if 'Communication' in skills:
            advice.append('Include examples of presentations or written work')
        
        # General advice
        advice.append(f"Research {career['title']} job descriptions for specific keywords")
        advice.append('Quantify achievements with numbers and percentages')
        
        return advice
    
    def _generate_interview_preparation(self, career_title: str, skill_analysis: Dict) -> Dict[str, Any]:
        """Generate interview preparation guidance"""
        questions = self.interview_questions.get(career_title, self.interview_questions['Software Engineer'])
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        return {
            'technical_questions': [q for q in questions if q['category'] == 'Technical'],
            'behavioral_questions': [q for q in questions if q['category'] == 'Behavioral'],
            'skill_specific_questions': self._generate_skill_specific_questions(skill_names),
            'preparation_tips': [
                'Practice explaining technical concepts in simple terms',
                'Prepare STAR method examples for behavioral questions',
                'Research the company and role thoroughly',
                'Practice coding problems if applicable',
                'Prepare thoughtful questions to ask the interviewer'
            ],
            'mock_interview_schedule': self._create_mock_interview_schedule(),
            'common_mistakes': [
                'Not preparing specific examples',
                'Being too technical or too vague',
                'Not asking questions about the role',
                'Arriving unprepared or late',
                'Not following up after the interview'
            ]
        }
    
    def _generate_skill_specific_questions(self, skills: List[str]) -> List[Dict]:
        """Generate questions specific to user's skills"""
        skill_questions = []
        
        for skill in skills[:5]:  # Top 5 skills
            if skill == 'Python Programming':
                skill_questions.append({
                    'question': 'How do you handle exceptions in Python?',
                    'skill': skill,
                    'difficulty': 'Medium',
                    'sample_answer': 'I use try-except blocks to handle exceptions gracefully and provide meaningful error messages.'
                })
            elif skill == 'Machine Learning':
                skill_questions.append({
                    'question': 'Explain overfitting and how to prevent it.',
                    'skill': skill,
                    'difficulty': 'Medium',
                    'sample_answer': 'Overfitting occurs when a model learns training data too well. I prevent it using cross-validation, regularization, and proper train/test splits.'
                })
            elif skill == 'Data Analysis':
                skill_questions.append({
                    'question': 'How do you ensure data quality in your analysis?',
                    'skill': skill,
                    'difficulty': 'Medium',
                    'sample_answer': 'I check for missing values, outliers, duplicates, and data consistency before analysis.'
                })
        
        return skill_questions
    
    def _create_mock_interview_schedule(self) -> List[Dict[str, str]]:
        """Create a comprehensive mock interview preparation schedule"""
        return [
            {
                'week': 'Week 1',
                'focus': 'Technical Foundation',
                'activities': [
                    'Review core technical concepts and fundamentals',
                    'Practice coding problems on LeetCode/HackerRank',
                    'Study system design basics and common patterns',
                    'Prepare technical project explanations'
                ],
                'time_commitment': '2-3 hours daily',
                'resources': ['LeetCode', 'System Design Primer', 'Technical blogs']
            },
            {
                'week': 'Week 2',
                'focus': 'Behavioral & Situational Questions',
                'activities': [
                    'Prepare STAR method examples for common scenarios',
                    'Practice storytelling and communication skills',
                    'Research company culture and values',
                    'Prepare questions to ask the interviewer'
                ],
                'time_commitment': '1-2 hours daily',
                'resources': ['STAR method guide', 'Company research', 'Behavioral question bank']
            },
            {
                'week': 'Week 3',
                'focus': 'Mock Interviews & Practice',
                'activities': [
                    'Conduct mock interviews with friends/mentors',
                    'Practice with online platforms (Pramp, InterviewBit)',
                    'Record and review your practice sessions',
                    'Focus on areas that need improvement'
                ],
                'time_commitment': '2-3 hours daily',
                'resources': ['Pramp', 'InterviewBit', 'Mock interview partners']
            },
            {
                'week': 'Week 4',
                'focus': 'Final Preparation & Polish',
                'activities': [
                    'Review company-specific information and recent news',
                    'Practice elevator pitch and self-introduction',
                    'Prepare for different interview formats (panel, technical, HR)',
                    'Final mock interviews and feedback sessions'
                ],
                'time_commitment': '1-2 hours daily',
                'resources': ['Company website', 'Recent news', 'Final practice sessions']
            }
        ]
    
    def _generate_portfolio_recommendations(self, student_data: Dict, career: Dict, 
                                          skill_analysis: Dict) -> Dict[str, Any]:
        """Generate portfolio recommendations"""
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        return {
            'portfolio_projects': self._suggest_portfolio_projects(skill_names, career),
            'github_optimization': [
                'Write clear README files for each project',
                'Include live demos or screenshots',
                'Use consistent commit messages',
                'Organize repositories by project type',
                'Pin your best projects to your profile'
            ],
            'showcase_strategies': [
                'Create a personal website to showcase projects',
                'Write technical blog posts about your projects',
                'Participate in open source contributions',
                'Create video demonstrations of your work',
                'Document your learning journey'
            ],
            'project_categories': self._categorize_projects(skill_names)
        }
    
    def _suggest_portfolio_projects(self, skills: List[str], career: Dict) -> List[Dict[str, str]]:
        """Suggest specific portfolio projects based on skills and career"""
        projects = []
        career_title = career['title']
        
        if 'Python Programming' in skills:
            if career_title == 'Data Scientist':
                projects.append({
                    'title': 'Data Analysis Dashboard',
                    'description': 'Interactive dashboard analyzing sales data with visualizations',
                    'technologies': 'Python, Pandas, Matplotlib, Streamlit',
                    'github_template': 'https://github.com/example/data-dashboard'
                })
            else:
                projects.append({
                    'title': 'Web Application',
                    'description': 'Full-stack web app with user authentication and database',
                    'technologies': 'Python, Flask, SQLite, HTML/CSS',
                    'github_template': 'https://github.com/example/web-app'
                })
        
        if 'Machine Learning' in skills:
            projects.append({
                'title': 'ML Prediction Model',
                'description': 'Machine learning model predicting house prices',
                'technologies': 'Python, Scikit-learn, Pandas, Jupyter',
                'github_template': 'https://github.com/example/ml-prediction'
            })
        
        return projects
    
    def _categorize_projects(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize projects by type"""
        categories = {
            'Data Science': [],
            'Web Development': [],
            'Machine Learning': [],
            'Automation': []
        }
        
        if 'Data Analysis' in skills or 'Python Programming' in skills:
            categories['Data Science'].append('Data visualization projects')
            categories['Data Science'].append('Statistical analysis projects')
        
        if 'Python Programming' in skills:
            categories['Web Development'].append('Web applications')
            categories['Automation'].append('Scripts and automation tools')
        
        if 'Machine Learning' in skills:
            categories['Machine Learning'].append('Prediction models')
            categories['Machine Learning'].append('Classification projects')
        
        return {k: v for k, v in categories.items() if v}
    
    def _generate_networking_guidance(self, career_title: str, career: Dict) -> Dict[str, Any]:
        """Generate networking guidance"""
        industry = career.get('industry', '')
        
        return {
            'networking_strategies': [
                'Join professional associations in your field',
                'Attend industry conferences and meetups',
                'Connect with professionals on LinkedIn',
                'Participate in online communities and forums',
                'Reach out to alumni from your school'
            ],
            'linkedin_optimization': [
                'Write a compelling headline highlighting your skills',
                'Include a professional summary with keywords',
                'Add relevant skills and get endorsements',
                'Share industry-related content regularly',
                'Connect with professionals in your target field'
            ],
            'industry_specific_networking': self._get_industry_networking_tips(industry),
            'elevator_pitch': self._create_elevator_pitch(career_title, career),
            'follow_up_strategies': [
                'Send thank you notes after networking events',
                'Share relevant articles with new connections',
                'Offer to help others with their projects',
                'Maintain regular but not excessive contact',
                'Provide value before asking for favors'
            ]
        }
    
    def _get_industry_networking_tips(self, industry: str) -> List[str]:
        """Get industry-specific networking tips"""
        tips = {
            'Technology': [
                'Join GitHub and contribute to open source projects',
                'Attend hackathons and coding meetups',
                'Participate in Stack Overflow discussions',
                'Follow tech blogs and share insights'
            ],
            'Healthcare': [
                'Join healthcare professional associations',
                'Attend medical technology conferences',
                'Connect with healthcare data professionals',
                'Follow healthcare innovation trends'
            ],
            'Finance': [
                'Join financial professional groups',
                'Attend fintech conferences',
                'Connect with financial analysts',
                'Follow market trends and regulations'
            ]
        }
        return tips.get(industry, ['Join general professional groups in your field'])
    
    def _create_elevator_pitch(self, career_title: str, career: Dict) -> str:
        """Create a personalized elevator pitch"""
        industry = career.get('industry', '')
        return f"Hi, I'm a recent graduate passionate about {industry} and excited about {career_title} opportunities. I have strong skills in data analysis and problem-solving, and I'm looking to contribute to innovative projects in the {industry} space. I'd love to learn more about your experience in this field."
    
    def _generate_application_strategy(self, career: Dict) -> Dict[str, Any]:
        """Generate job application strategy"""
        career_title = career['title']
        industry = career.get('industry', '')
        
        return {
            'target_companies': self._suggest_target_companies(industry),
            'application_timeline': [
                'Week 1-2: Research companies and roles',
                'Week 3-4: Customize resume and cover letters',
                'Week 5-6: Submit applications (5-10 per week)',
                'Week 7-8: Follow up and prepare for interviews'
            ],
            'job_search_platforms': [
                'LinkedIn Jobs',
                'Indeed',
                'Glassdoor',
                'Company career pages',
                'Professional association job boards'
            ],
            'application_tracking': [
                'Create a spreadsheet to track applications',
                'Set up job alerts for relevant positions',
                'Follow companies on social media',
                'Network with employees at target companies'
            ],
            'success_metrics': [
                'Apply to 20-30 relevant positions',
                'Maintain 10% response rate',
                'Schedule 3-5 interviews per month',
                'Receive 1-2 job offers'
            ]
        }
    
    def _suggest_target_companies(self, industry: str) -> List[str]:
        """Suggest target companies by industry"""
        companies = {
            'Technology': [
                'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta',
                'Netflix', 'Uber', 'Airbnb', 'Spotify', 'Salesforce'
            ],
            'Healthcare': [
                'Johnson & Johnson', 'Pfizer', 'Merck', 'Abbott',
                'Medtronic', 'Bristol Myers Squibb', 'Eli Lilly'
            ],
            'Finance': [
                'JPMorgan Chase', 'Bank of America', 'Wells Fargo',
                'Goldman Sachs', 'Morgan Stanley', 'Citigroup'
            ]
        }
        return companies.get(industry, ['Research companies in your target industry'])
    
    def _optimize_skills_for_ats(self, skill_analysis: Dict, career_title: str) -> Dict[str, Any]:
        """Optimize skills presentation for ATS systems"""
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        return {
            'ats_optimized_skills': self._create_ats_skill_list(skill_names, career_title),
            'skill_grouping': self._group_skills_by_category(skill_names),
            'keyword_variations': self._generate_skill_variations(skill_names),
            'skill_prioritization': self._prioritize_skills_for_career(skill_names, career_title)
        }
    
    def _create_ats_skill_list(self, skills: List[str], career_title: str) -> List[str]:
        """Create ATS-optimized skill list"""
        ats_skills = []
        
        for skill in skills:
            keywords = self.skill_keywords.get(skill, [skill])
            ats_skills.extend(keywords)
        
        # Add career-specific keywords
        career_keywords = {
            'Data Scientist': ['Statistics', 'Data Mining', 'Big Data', 'Analytics'],
            'Software Engineer': ['Software Development', 'Programming', 'Code Review', 'Testing'],
            'Product Manager': ['Product Strategy', 'Market Research', 'User Experience', 'Agile']
        }
        
        ats_skills.extend(career_keywords.get(career_title, []))
        
        return list(set(ats_skills))[:20]  # Top 20 skills
    
    def _group_skills_by_category(self, skills: List[str]) -> Dict[str, List[str]]:
        """Group skills by category for better organization"""
        categories = {
            'Programming Languages': [],
            'Tools & Technologies': [],
            'Soft Skills': [],
            'Domain Knowledge': []
        }
        
        for skill in skills:
            if 'Programming' in skill or skill in ['Python', 'JavaScript', 'SQL']:
                categories['Programming Languages'].append(skill)
            elif skill in ['Machine Learning', 'Data Analysis']:
                categories['Tools & Technologies'].append(skill)
            elif skill in ['Communication', 'Leadership', 'Problem Solving']:
                categories['Soft Skills'].append(skill)
            else:
                categories['Domain Knowledge'].append(skill)
        
        return {k: v for k, v in categories.items() if v}
    
    def _generate_skill_variations(self, skills: List[str]) -> Dict[str, List[str]]:
        """Generate keyword variations for skills"""
        variations = {}
        
        for skill in skills:
            skill_variations = [skill]
            if skill == 'Python Programming':
                skill_variations.extend(['Python', 'Python Development', 'Python Scripting'])
            elif skill == 'Machine Learning':
                skill_variations.extend(['ML', 'Artificial Intelligence', 'Predictive Modeling'])
            elif skill == 'Data Analysis':
                skill_variations.extend(['Data Analytics', 'Statistical Analysis', 'Data Science'])
            
            variations[skill] = skill_variations
        
        return variations
    
    def _prioritize_skills_for_career(self, skills: List[str], career_title: str) -> List[Dict[str, Any]]:
        """Prioritize skills based on career relevance"""
        priority_skills = []
        
        # Define skill priorities for different careers
        career_priorities = {
            'Data Scientist': ['Machine Learning', 'Data Analysis', 'Python Programming', 'Statistics'],
            'Software Engineer': ['Python Programming', 'JavaScript', 'SQL', 'Problem Solving'],
            'Product Manager': ['Communication', 'Project Management', 'Critical Thinking', 'Leadership']
        }
        
        required_skills = career_priorities.get(career_title, skills)
        
        for skill in skills:
            priority = 'High' if skill in required_skills else 'Medium'
            priority_skills.append({
                'skill': skill,
                'priority': priority,
                'career_relevance': 'Critical' if skill in required_skills else 'Important'
            })
        
        return sorted(priority_skills, key=lambda x: 0 if x['priority'] == 'High' else 1)
    
    def _generate_resume_sections_guide(self) -> Dict[str, List[str]]:
        """Generate comprehensive resume sections guide"""
        return {
            'header': [
                'Full name (larger font, bold)',
                'Professional email address',
                'Phone number with country code',
                'LinkedIn profile URL',
                'GitHub profile URL (for technical roles)',
                'Location (city, state)',
                'Portfolio website (if applicable)'
            ],
            'professional_summary': [
                '2-3 sentences highlighting key qualifications',
                'Years of experience and expertise areas',
                'Key achievements or unique value proposition',
                'Career objective or target role',
                'Tailor to specific job requirements'
            ],
            'experience': [
                'List in reverse chronological order (most recent first)',
                'Include: Job title, Company name, Location, Dates',
                'Use 3-5 bullet points per role',
                'Start each bullet with strong action verb',
                'Quantify achievements with numbers and percentages',
                'Focus on results and impact, not just responsibilities'
            ],
            'education': [
                'Degree, Major, University name, Graduation year',
                'GPA (if 3.5+ and recent graduate)',
                'Relevant coursework (for recent graduates)',
                'Academic honors or achievements',
                'Certifications and professional development'
            ],
            'skills': [
                'Group by category (Technical, Soft Skills, Tools)',
                'List most relevant skills first',
                'Include proficiency levels if applicable',
                'Use keywords from job descriptions',
                'Keep it concise and relevant'
            ],
            'projects': [
                'Project name and brief description',
                'Technologies and tools used',
                'Key achievements and results',
                'GitHub or demo links',
                'Team size and your role (if applicable)'
            ]
        }
    
    def _get_powerful_action_verbs(self) -> Dict[str, List[str]]:
        """Get powerful action verbs for different categories"""
        return {
            'leadership': ['Led', 'Managed', 'Directed', 'Oversaw', 'Coordinated', 'Supervised', 'Mentored'],
            'achievement': ['Achieved', 'Accomplished', 'Delivered', 'Exceeded', 'Improved', 'Increased', 'Reduced'],
            'creation': ['Created', 'Developed', 'Designed', 'Built', 'Implemented', 'Established', 'Launched'],
            'analysis': ['Analyzed', 'Evaluated', 'Assessed', 'Researched', 'Investigated', 'Identified', 'Diagnosed'],
            'collaboration': ['Collaborated', 'Partnered', 'Worked with', 'Coordinated', 'Facilitated', 'Supported'],
            'technical': ['Programmed', 'Coded', 'Debugged', 'Optimized', 'Automated', 'Integrated', 'Deployed']
        }
    
    def _get_quantification_examples(self, career_title: str) -> List[str]:
        """Get quantification examples for specific career"""
        examples = {
            'Data Scientist': [
                'Improved model accuracy by 25% using feature engineering',
                'Reduced data processing time by 40% through optimization',
                'Analyzed 10M+ customer records to identify key patterns',
                'Increased revenue by ₹50L through predictive analytics',
                'Led team of 3 data scientists on ML project'
            ],
            'Software Engineer': [
                'Developed application serving 100K+ daily users',
                'Reduced page load time by 60% through optimization',
                'Implemented CI/CD pipeline reducing deployment time by 70%',
                'Increased code coverage to 85% through automated testing',
                'Led migration of legacy system to microservices architecture'
            ],
            'Product Manager': [
                'Launched feature increasing user engagement by 30%',
                'Led cross-functional team of 8 members',
                'Increased conversion rate by 15% through A/B testing',
                'Reduced customer churn by 20% through product improvements',
                'Managed product roadmap for ₹2Cr revenue stream'
            ]
        }
        return examples.get(career_title, [
            'Quantify your achievements with specific numbers',
            'Include percentages, timeframes, and scale',
            'Show impact on business metrics',
            'Highlight team size and leadership experience'
        ])
    
    def _get_keywords_by_section(self, career_title: str, skills: List[str]) -> Dict[str, List[str]]:
        """Get relevant keywords for each resume section"""
        base_keywords = {
            'summary': ['Experienced', 'Passionate', 'Results-driven', 'Innovative', 'Collaborative'],
            'experience': ['Led', 'Developed', 'Implemented', 'Optimized', 'Delivered', 'Managed'],
            'skills': skills + ['Problem-solving', 'Communication', 'Teamwork', 'Leadership'],
            'projects': ['Built', 'Created', 'Designed', 'Deployed', 'Optimized', 'Analyzed']
        }
        
        career_specific = {
            'Data Scientist': {
                'summary': ['Machine Learning', 'Data Analysis', 'Predictive Modeling', 'Statistical Analysis'],
                'experience': ['ML Models', 'Data Pipeline', 'Feature Engineering', 'Model Deployment'],
                'skills': ['Python', 'R', 'SQL', 'TensorFlow', 'Scikit-learn', 'Pandas', 'NumPy'],
                'projects': ['Classification', 'Regression', 'Clustering', 'Deep Learning', 'NLP']
            },
            'Software Engineer': {
                'summary': ['Full-stack Development', 'Software Engineering', 'System Design', 'Agile'],
                'experience': ['API Development', 'Database Design', 'Code Review', 'Testing', 'Deployment'],
                'skills': ['JavaScript', 'Python', 'Java', 'React', 'Node.js', 'AWS', 'Docker'],
                'projects': ['Web Application', 'Mobile App', 'API', 'Microservices', 'Cloud']
            }
        }
        
        career_keywords = career_specific.get(career_title, {})
        
        # Merge base keywords with career-specific keywords
        result = {}
        for section in base_keywords:
            result[section] = base_keywords[section] + career_keywords.get(section, [])
        
        return result
    
    def _generate_resume_builder(self, student_data: Dict, career: Dict, skill_analysis: Dict) -> Dict[str, Any]:
        """Generate interactive resume builder with real-time suggestions"""
        career_title = career['title']
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        return {
            'resume_sections': {
                'header': {
                    'title': 'Contact Information',
                    'fields': [
                        {'name': 'full_name', 'label': 'Full Name', 'type': 'text', 'required': True, 'placeholder': 'John Doe'},
                        {'name': 'email', 'label': 'Email', 'type': 'email', 'required': True, 'placeholder': 'john.doe@email.com'},
                        {'name': 'phone', 'label': 'Phone', 'type': 'tel', 'required': True, 'placeholder': '+91 98765 43210'},
                        {'name': 'linkedin', 'label': 'LinkedIn URL', 'type': 'url', 'required': False, 'placeholder': 'https://linkedin.com/in/johndoe'},
                        {'name': 'github', 'label': 'GitHub URL', 'type': 'url', 'required': False, 'placeholder': 'https://github.com/johndoe'},
                        {'name': 'location', 'label': 'Location', 'type': 'text', 'required': True, 'placeholder': 'Mumbai, Maharashtra'},
                        {'name': 'portfolio', 'label': 'Portfolio Website', 'type': 'url', 'required': False, 'placeholder': 'https://johndoe.dev'}
                    ]
                },
                'summary': {
                    'title': 'Professional Summary',
                    'fields': [
                        {'name': 'summary', 'label': 'Summary', 'type': 'textarea', 'required': True, 
                         'placeholder': 'Write a 2-3 sentence summary highlighting your key qualifications...',
                         'max_length': 200, 'suggestions': self._get_summary_suggestions(career_title, skill_names)}
                    ]
                },
                'experience': {
                    'title': 'Work Experience',
                    'fields': [
                        {'name': 'job_title', 'label': 'Job Title', 'type': 'text', 'required': True},
                        {'name': 'company', 'label': 'Company', 'type': 'text', 'required': True},
                        {'name': 'location', 'label': 'Location', 'type': 'text', 'required': True},
                        {'name': 'start_date', 'label': 'Start Date', 'type': 'month', 'required': True},
                        {'name': 'end_date', 'label': 'End Date', 'type': 'month', 'required': False},
                        {'name': 'current', 'label': 'Currently Working', 'type': 'checkbox', 'required': False},
                        {'name': 'achievements', 'label': 'Key Achievements', 'type': 'textarea', 'required': True,
                         'placeholder': 'List 3-5 key achievements with quantifiable results...',
                         'suggestions': self._get_achievement_suggestions(career_title)}
                    ]
                },
                'education': {
                    'title': 'Education',
                    'fields': [
                        {'name': 'degree', 'label': 'Degree', 'type': 'text', 'required': True},
                        {'name': 'major', 'label': 'Major/Field', 'type': 'text', 'required': True},
                        {'name': 'university', 'label': 'University', 'type': 'text', 'required': True},
                        {'name': 'graduation_year', 'label': 'Graduation Year', 'type': 'number', 'required': True},
                        {'name': 'gpa', 'label': 'GPA (if 3.5+)', 'type': 'number', 'required': False, 'step': 0.01},
                        {'name': 'achievements', 'label': 'Academic Achievements', 'type': 'textarea', 'required': False}
                    ]
                },
                'skills': {
                    'title': 'Skills',
                    'fields': [
                        {'name': 'technical_skills', 'label': 'Technical Skills', 'type': 'tags', 'required': True,
                         'suggestions': skill_names + self._get_technical_skills_suggestions(career_title)},
                        {'name': 'soft_skills', 'label': 'Soft Skills', 'type': 'tags', 'required': True,
                         'suggestions': ['Communication', 'Leadership', 'Problem Solving', 'Teamwork', 'Time Management']},
                        {'name': 'tools', 'label': 'Tools & Technologies', 'type': 'tags', 'required': True,
                         'suggestions': self._get_tools_suggestions(career_title)}
                    ]
                },
                'projects': {
                    'title': 'Projects',
                    'fields': [
                        {'name': 'project_name', 'label': 'Project Name', 'type': 'text', 'required': True},
                        {'name': 'description', 'label': 'Description', 'type': 'textarea', 'required': True},
                        {'name': 'technologies', 'label': 'Technologies Used', 'type': 'tags', 'required': True},
                        {'name': 'github_url', 'label': 'GitHub URL', 'type': 'url', 'required': False},
                        {'name': 'live_url', 'label': 'Live Demo URL', 'type': 'url', 'required': False},
                        {'name': 'achievements', 'label': 'Key Achievements', 'type': 'textarea', 'required': True}
                    ]
                }
            },
            'real_time_suggestions': {
                'keyword_optimization': self._get_keyword_suggestions(career_title),
                'action_verbs': self._get_action_verb_suggestions(),
                'quantification_tips': self._get_quantification_tips(career_title),
                'ats_score': self._calculate_ats_score(student_data, career_title)
            },
            'preview_options': {
                'templates': ['Modern', 'Classic', 'Creative', 'Minimalist'],
                'formats': ['PDF', 'Word', 'HTML'],
                'color_schemes': ['Professional Blue', 'Elegant Black', 'Modern Green', 'Corporate Gray']
            }
        }
    
    def _generate_downloadable_templates(self, career_title: str) -> Dict[str, Any]:
        """Generate downloadable resume templates"""
        return {
            'templates': [
                {
                    'name': 'Modern Professional',
                    'description': 'Clean, modern design perfect for tech roles',
                    'file_format': 'PDF',
                    'preview_url': '/templates/modern_professional_preview.png',
                    'download_url': '/downloads/modern_professional_template.pdf',
                    'suitable_for': ['Data Scientist', 'Software Engineer', 'Product Manager'],
                    'features': ['ATS-friendly', 'Color-coded sections', 'Professional typography']
                },
                {
                    'name': 'Classic Executive',
                    'description': 'Traditional format ideal for senior positions',
                    'file_format': 'PDF',
                    'preview_url': '/templates/classic_executive_preview.png',
                    'download_url': '/downloads/classic_executive_template.pdf',
                    'suitable_for': ['Product Manager', 'Senior Software Engineer'],
                    'features': ['Conservative design', 'Emphasis on experience', 'Professional layout']
                },
                {
                    'name': 'Creative Portfolio',
                    'description': 'Eye-catching design for creative and design roles',
                    'file_format': 'PDF',
                    'preview_url': '/templates/creative_portfolio_preview.png',
                    'download_url': '/downloads/creative_portfolio_template.pdf',
                    'suitable_for': ['UX Designer', 'Frontend Developer'],
                    'features': ['Visual elements', 'Portfolio integration', 'Creative layout']
                },
                {
                    'name': 'Minimalist Clean',
                    'description': 'Simple, clean design focusing on content',
                    'file_format': 'PDF',
                    'preview_url': '/templates/minimalist_clean_preview.png',
                    'download_url': '/downloads/minimalist_clean_template.pdf',
                    'suitable_for': ['All roles'],
                    'features': ['Maximum readability', 'ATS-optimized', 'Print-friendly']
                }
            ],
            'customization_options': {
                'colors': ['Blue', 'Black', 'Green', 'Purple', 'Red'],
                'fonts': ['Arial', 'Calibri', 'Times New Roman', 'Helvetica', 'Georgia'],
                'layouts': ['Single Column', 'Two Column', 'Hybrid'],
                'sections': ['All', 'Experience Focus', 'Skills Focus', 'Education Focus']
            }
        }
    
    def _generate_ats_optimization_tools(self, career_title: str, skill_analysis: Dict) -> Dict[str, Any]:
        """Generate ATS optimization tools and analysis"""
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        return {
            'keyword_analyzer': {
                'title': 'Keyword Analysis Tool',
                'description': 'Analyze your resume for ATS optimization',
                'features': [
                    'Keyword density analysis',
                    'Missing keyword suggestions',
                    'Keyword placement recommendations',
                    'Industry-specific keyword matching'
                ],
                'analysis_criteria': {
                    'keyword_density': '2-3% for primary keywords',
                    'keyword_placement': 'First 1/3 of resume',
                    'keyword_variations': 'Include synonyms and variations',
                    'industry_keywords': 'Match job description keywords'
                }
            },
            'format_checker': {
                'title': 'Format Compatibility Checker',
                'description': 'Ensure your resume is ATS-compatible',
                'checks': [
                    'File format compatibility (PDF vs Word)',
                    'Font usage and readability',
                    'Section header standardization',
                    'Bullet point formatting',
                    'Table and graphic compatibility',
                    'Contact information placement'
                ],
                'recommendations': [
                    'Use standard section headers',
                    'Avoid graphics and tables',
                    'Use simple fonts (Arial, Calibri)',
                    'Save as .docx for maximum compatibility',
                    'Use standard bullet points'
                ]
            },
            'content_optimizer': {
                'title': 'Content Optimization Suggestions',
                'description': 'Improve resume content for better ATS performance',
                'suggestions': self._get_content_optimization_suggestions(career_title, skill_names),
                'score_breakdown': {
                    'keyword_match': 0,
                    'format_compatibility': 0,
                    'content_quality': 0,
                    'overall_score': 0
                }
            },
            'job_matching': {
                'title': 'Job Description Matching',
                'description': 'Compare your resume against job requirements',
                'features': [
                    'Upload job description for analysis',
                    'Keyword matching percentage',
                    'Missing requirements identification',
                    'Tailoring suggestions',
                    'Compatibility score'
                ]
            }
        }
    
    def _get_summary_suggestions(self, career_title: str, skills: List[str]) -> List[str]:
        """Get personalized summary suggestions"""
        suggestions = {
            'Data Scientist': [
                f"Passionate data scientist with expertise in {', '.join(skills[:3])} and proven track record of delivering actionable insights from complex datasets.",
                f"Results-driven data scientist specializing in machine learning and statistical analysis, with experience in {', '.join(skills[:2])}.",
                f"Experienced data scientist with strong background in {', '.join(skills[:3])}, committed to driving business growth through data-driven solutions."
            ],
            'Software Engineer': [
                f"Skilled software engineer with expertise in {', '.join(skills[:3])} and experience building scalable applications.",
                f"Passionate full-stack developer specializing in {', '.join(skills[:2])}, with a track record of delivering high-quality software solutions.",
                f"Experienced software engineer with strong background in {', '.join(skills[:3])}, committed to writing clean, efficient code."
            ]
        }
        return suggestions.get(career_title, [
            f"Experienced professional with expertise in {', '.join(skills[:3])} and proven track record of success.",
            f"Results-driven individual with strong background in {', '.join(skills[:2])} and commitment to excellence."
        ])
    
    def _get_achievement_suggestions(self, career_title: str) -> List[str]:
        """Get achievement suggestions for specific careers"""
        suggestions = {
            'Data Scientist': [
                "Improved model accuracy by 25% using advanced feature engineering techniques",
                "Reduced data processing time by 40% through optimization and parallel processing",
                "Analyzed 10M+ customer records to identify key behavioral patterns and trends",
                "Increased revenue by ₹50L through implementation of predictive analytics models",
                "Led cross-functional team of 5 members to deliver ML solution ahead of schedule"
            ],
            'Software Engineer': [
                "Developed and deployed web application serving 100K+ daily active users",
                "Reduced page load time by 60% through code optimization and caching strategies",
                "Implemented CI/CD pipeline reducing deployment time by 70%",
                "Increased code coverage to 85% through comprehensive automated testing",
                "Led migration of legacy monolith to microservices architecture"
            ]
        }
        return suggestions.get(career_title, [
            "Achieved measurable results through strategic implementation and optimization",
            "Led successful projects with quantifiable business impact",
            "Improved processes and efficiency through innovative solutions"
        ])
    
    def _get_technical_skills_suggestions(self, career_title: str) -> List[str]:
        """Get technical skills suggestions for specific careers"""
        suggestions = {
            'Data Scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch'],
            'Software Engineer': ['JavaScript', 'Python', 'Java', 'React', 'Node.js', 'AWS', 'Docker', 'Git', 'MongoDB', 'PostgreSQL'],
            'Product Manager': ['Agile', 'Scrum', 'Jira', 'Confluence', 'Figma', 'SQL', 'Analytics', 'A/B Testing', 'User Research', 'Stakeholder Management']
        }
        return suggestions.get(career_title, ['Technical Skills', 'Programming', 'Tools', 'Frameworks'])
    
    def _get_tools_suggestions(self, career_title: str) -> List[str]:
        """Get tools and technologies suggestions"""
        suggestions = {
            'Data Scientist': ['Jupyter', 'Tableau', 'Power BI', 'Apache Spark', 'Hadoop', 'AWS S3', 'Google Cloud', 'Docker', 'Kubernetes'],
            'Software Engineer': ['VS Code', 'IntelliJ', 'Postman', 'Jenkins', 'GitLab', 'Docker', 'Kubernetes', 'AWS', 'Azure'],
            'Product Manager': ['Jira', 'Confluence', 'Figma', 'Slack', 'Microsoft Office', 'Google Analytics', 'Mixpanel', 'Hotjar']
        }
        return suggestions.get(career_title, ['Development Tools', 'Collaboration Tools', 'Analytics Tools'])
    
    def _get_keyword_suggestions(self, career_title: str) -> Dict[str, List[str]]:
        """Get keyword suggestions for ATS optimization"""
        return {
            'high_priority': self._get_high_priority_keywords(career_title),
            'medium_priority': self._get_medium_priority_keywords(career_title),
            'action_verbs': ['Developed', 'Implemented', 'Led', 'Optimized', 'Analyzed', 'Created', 'Managed', 'Improved'],
            'quantifiers': ['25%', '50%', '100K+', '₹10L', '3x', '2x faster', '40% reduction']
        }
    
    def _get_high_priority_keywords(self, career_title: str) -> List[str]:
        """Get high priority keywords for specific careers"""
        keywords = {
            'Data Scientist': ['Machine Learning', 'Python', 'Data Analysis', 'Statistics', 'SQL', 'Pandas', 'Scikit-learn'],
            'Software Engineer': ['JavaScript', 'Python', 'React', 'Node.js', 'AWS', 'Docker', 'Git', 'API Development'],
            'Product Manager': ['Product Strategy', 'Agile', 'Scrum', 'User Research', 'A/B Testing', 'Stakeholder Management']
        }
        return keywords.get(career_title, ['Technical Skills', 'Problem Solving', 'Communication'])
    
    def _get_medium_priority_keywords(self, career_title: str) -> List[str]:
        """Get medium priority keywords for specific careers"""
        keywords = {
            'Data Scientist': ['Data Visualization', 'Big Data', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Apache Spark'],
            'Software Engineer': ['Microservices', 'CI/CD', 'Database Design', 'System Architecture', 'Testing', 'DevOps'],
            'Product Manager': ['Product Roadmap', 'User Experience', 'Market Research', 'Competitive Analysis', 'Metrics']
        }
        return keywords.get(career_title, ['Leadership', 'Teamwork', 'Project Management'])
    
    def _get_action_verb_suggestions(self) -> Dict[str, List[str]]:
        """Get action verb suggestions by category"""
        return {
            'leadership': ['Led', 'Managed', 'Directed', 'Oversaw', 'Coordinated', 'Supervised'],
            'achievement': ['Achieved', 'Accomplished', 'Delivered', 'Exceeded', 'Improved', 'Increased'],
            'creation': ['Created', 'Developed', 'Designed', 'Built', 'Implemented', 'Established'],
            'analysis': ['Analyzed', 'Evaluated', 'Assessed', 'Researched', 'Investigated', 'Identified']
        }
    
    def _get_quantification_tips(self, career_title: str) -> List[str]:
        """Get quantification tips for specific careers"""
        tips = {
            'Data Scientist': [
                "Include model accuracy improvements (e.g., 'Improved accuracy by 25%')",
                "Mention data volume processed (e.g., 'Analyzed 10M+ records')",
                "Show business impact (e.g., 'Increased revenue by ₹50L')",
                "Include time savings (e.g., 'Reduced processing time by 40%')"
            ],
            'Software Engineer': [
                "Include user metrics (e.g., 'Serving 100K+ users')",
                "Show performance improvements (e.g., '60% faster load times')",
                "Mention scale and complexity (e.g., 'Microservices architecture')",
                "Include team size (e.g., 'Led team of 5 developers')"
            ]
        }
        return tips.get(career_title, [
            "Use specific numbers and percentages",
            "Include timeframes and scale",
            "Show measurable impact",
            "Highlight team leadership experience"
        ])
    
    def _calculate_ats_score(self, student_data: Dict, career_title: str) -> Dict[str, Any]:
        """Calculate ATS optimization score"""
        # This is a simplified scoring system
        score = 0
        max_score = 100
        
        # Check for essential elements
        if student_data.get('education'):
            score += 15
        if student_data.get('experience'):
            score += 20
        if student_data.get('skills'):
            score += 25
        
        # Add keyword matching score (simplified)
        score += 30
        
        # Add formatting score
        score += 10
        
        return {
            'overall_score': min(score, max_score),
            'breakdown': {
                'content_completeness': 60,
                'keyword_optimization': 30,
                'format_compatibility': 10
            },
            'recommendations': self._get_ats_improvement_recommendations(score)
        }
    
    def _get_ats_improvement_recommendations(self, score: int) -> List[str]:
        """Get ATS improvement recommendations based on score"""
        if score >= 80:
            return ["Excellent ATS optimization! Your resume should pass most ATS systems."]
        elif score >= 60:
            return [
                "Good ATS optimization. Consider adding more relevant keywords.",
                "Ensure all sections are properly formatted for ATS compatibility."
            ]
        else:
            return [
                "Focus on adding more relevant keywords from job descriptions.",
                "Ensure proper section headers and formatting.",
                "Include quantifiable achievements and metrics.",
                "Use standard fonts and avoid graphics or tables."
            ]
    
    def _get_content_optimization_suggestions(self, career_title: str, skills: List[str]) -> List[str]:
        """Get content optimization suggestions"""
        return [
            f"Include more {career_title.lower()} specific keywords",
            "Add quantifiable achievements with numbers and percentages",
            "Use strong action verbs to start bullet points",
            "Ensure consistent formatting throughout the resume",
            "Include relevant technical skills and tools",
            "Add project descriptions with technologies used",
            "Highlight leadership and teamwork experiences"
        ]
    
    def generate_resume_content(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate formatted resume content"""
        personal_info = resume_data.get('personal_info', {})
        summary = resume_data.get('summary', '')
        experience = resume_data.get('experience', [])
        education = resume_data.get('education', [])
        skills = resume_data.get('skills', {})
        projects = resume_data.get('projects', [])
        template = resume_data.get('template', 'modern')

        # If Gemini key is present, enhance summary and achievements lightly
        use_ai = bool(resume_data.get('use_ai'))
        if use_ai:
            enhanced = False
            # Try Gemini first (lazy import)
            genai = _get_genai()
            gemini_key = os.getenv('GEMINI_API_KEY')
            if genai and gemini_key:
                try:
                    genai.configure(api_key=gemini_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')

                    if summary:
                        prompt = (
                            "Rewrite the following resume summary to be concise, ATS-friendly, and professional (max 60 words).\n"
                            f"Text: {summary}"
                        )
                        resp = model.generate_content(prompt)
                        if getattr(resp, 'text', '').strip():
                            summary = resp.text.strip()

                    if experience and isinstance(experience[0].get('achievements', ''), str):
                        bullets = experience[0]['achievements']
                        prompt = (
                            "Convert the following raw achievement lines into crisp, action-verb-led resume bullets (max 4), each on a new line.\n"
                            f"Lines: {bullets}"
                        )
                        resp = model.generate_content(prompt)
                        if getattr(resp, 'text', '').strip():
                            experience[0]['achievements'] = resp.text
                    enhanced = True
                except Exception:
                    enhanced = False

            # Fallback to Perplexity if Gemini not used/failed
            if not enhanced:
                pplx_key = os.getenv('PPLX_API_KEY')
                if pplx_key:
                    headers = {
                        'Authorization': f'Bearer {pplx_key}',
                        'Content-Type': 'application/json'
                    }
                    # Summary enhancement
                    if summary:
                        try:
                            payload = {
                                'model': 'sonar-small-online',
                                'messages': [
                                    {'role': 'system', 'content': 'You are a concise resume writer.'},
                                    {'role': 'user', 'content': f"Rewrite this resume summary to be concise, ATS-friendly, and professional (<=60 words):\n{summary}"}
                                ]
                            }
                            r = requests.post('https://api.perplexity.ai/chat/completions', headers=headers, json=payload, timeout=12)
                            if r.status_code == 200:
                                data = r.json()
                                text = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                                if text:
                                    summary = text
                        except Exception:
                            pass
                    # Experience bullets
                    if experience and isinstance(experience[0].get('achievements', ''), str):
                        try:
                            bullets = experience[0]['achievements']
                            payload = {
                                'model': 'sonar-small-online',
                                'messages': [
                                    {'role': 'system', 'content': 'You are a resume bullet enhancer.'},
                                    {'role': 'user', 'content': f"Turn these raw lines into crisp, action-verb-led resume bullets (max 4), each on a new line:\n{bullets}"}
                                ]
                            }
                            r = requests.post('https://api.perplexity.ai/chat/completions', headers=headers, json=payload, timeout=12)
                            if r.status_code == 200:
                                data = r.json()
                                text = data.get('choices', [{}])[0].get('message', {}).get('content', '').strip()
                                if text:
                                    experience[0]['achievements'] = text
                        except Exception:
                            pass
        
        # Format personal information
        formatted_personal = self._format_personal_info(personal_info)
        
        # Format experience
        formatted_experience = self._format_experience(experience)
        
        # Format education
        formatted_education = self._format_education(education)
        
        # Format skills
        formatted_skills = self._format_skills(skills)
        
        # Format projects
        formatted_projects = self._format_projects(projects)
        
        return {
            'personal_info': formatted_personal,
            'summary': summary,
            'experience': formatted_experience,
            'education': formatted_education,
            'skills': formatted_skills,
            'projects': formatted_projects,
            'template': template,
            'formatted_resume': self._create_formatted_resume(
                formatted_personal, summary, formatted_experience, 
                formatted_education, formatted_skills, formatted_projects, template
            )
        }
    
    def _format_personal_info(self, personal_info: Dict[str, str]) -> Dict[str, str]:
        """Format personal information section"""
        return {
            'name': personal_info.get('full_name', 'Your Name'),
            'email': personal_info.get('email', 'your.email@example.com'),
            'phone': personal_info.get('phone', '+91 98765 43210'),
            'linkedin': personal_info.get('linkedin', ''),
            'github': personal_info.get('github', ''),
            'location': personal_info.get('location', 'City, State'),
            'portfolio': personal_info.get('portfolio', '')
        }
    
    def _format_experience(self, experience: List[Dict]) -> List[Dict]:
        """Format experience section"""
        formatted = []
        for exp in experience:
            formatted.append({
                'title': exp.get('job_title', 'Job Title'),
                'company': exp.get('company', 'Company Name'),
                'location': exp.get('location', 'Location'),
                'start_date': exp.get('start_date', 'Start Date'),
                'end_date': exp.get('end_date', 'End Date'),
                'current': exp.get('current', False),
                'achievements': exp.get('achievements', '').split('\n') if exp.get('achievements') else []
            })
        return formatted
    
    def _format_education(self, education: List[Dict]) -> List[Dict]:
        """Format education section"""
        formatted = []
        for edu in education:
            formatted.append({
                'degree': edu.get('degree', 'Degree'),
                'major': edu.get('major', 'Major'),
                'university': edu.get('university', 'University'),
                'graduation_year': edu.get('graduation_year', 'Year'),
                'gpa': edu.get('gpa', ''),
                'achievements': edu.get('achievements', '').split('\n') if edu.get('achievements') else []
            })
        return formatted
    
    def _format_skills(self, skills: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Format skills section"""
        return {
            'technical': skills.get('technical_skills', []),
            'soft': skills.get('soft_skills', []),
            'tools': skills.get('tools', [])
        }
    
    def _format_projects(self, projects: List[Dict]) -> List[Dict]:
        """Format projects section"""
        formatted = []
        for project in projects:
            formatted.append({
                'name': project.get('project_name', 'Project Name'),
                'description': project.get('description', 'Project description'),
                'technologies': project.get('technologies', []),
                'github_url': project.get('github_url', ''),
                'live_url': project.get('live_url', ''),
                'achievements': project.get('achievements', '').split('\n') if project.get('achievements') else []
            })
        return formatted
    
    def _create_formatted_resume(self, personal_info: Dict, summary: str, 
                               experience: List[Dict], education: List[Dict], 
                               skills: Dict, projects: List[Dict], template: str) -> str:
        """Create a formatted resume text"""
        resume_text = f"""
{personal_info['name'].upper()}
{personal_info['email']} | {personal_info['phone']} | {personal_info['location']}
{personal_info['linkedin']} | {personal_info['github']} | {personal_info['portfolio']}

PROFESSIONAL SUMMARY
{summary}

EXPERIENCE
"""
        
        for exp in experience:
            end_date = "Present" if exp['current'] else exp['end_date']
            resume_text += f"""
{exp['title']} | {exp['company']} | {exp['location']} | {exp['start_date']} - {end_date}
"""
            for achievement in exp['achievements']:
                if achievement.strip():
                    resume_text += f"• {achievement.strip()}\n"
        
        resume_text += "\nEDUCATION\n"
        for edu in education:
            gpa_text = f" | GPA: {edu['gpa']}" if edu['gpa'] else ""
            resume_text += f"{edu['degree']} in {edu['major']} | {edu['university']} | {edu['graduation_year']}{gpa_text}\n"
            for achievement in edu['achievements']:
                if achievement.strip():
                    resume_text += f"• {achievement.strip()}\n"
        
        resume_text += "\nTECHNICAL SKILLS\n"
        if skills['technical']:
            resume_text += f"Programming Languages: {', '.join(skills['technical'])}\n"
        if skills['tools']:
            resume_text += f"Tools & Technologies: {', '.join(skills['tools'])}\n"
        if skills['soft']:
            resume_text += f"Soft Skills: {', '.join(skills['soft'])}\n"
        
        if projects:
            resume_text += "\nPROJECTS\n"
            for project in projects:
                resume_text += f"""
{project['name']}
{project['description']}
Technologies: {', '.join(project['technologies'])}
"""
                if project['github_url']:
                    resume_text += f"GitHub: {project['github_url']}\n"
                if project['live_url']:
                    resume_text += f"Live Demo: {project['live_url']}\n"
                for achievement in project['achievements']:
                    if achievement.strip():
                        resume_text += f"• {achievement.strip()}\n"
        
        return resume_text.strip()
    
    def generate_pdf_resume(self, resume_data: Dict[str, Any], filename: str = None) -> str:
        """Generate a PDF resume"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_{timestamp}.pdf"
        
        # Create downloads directory if it doesn't exist
        downloads_dir = "downloads"
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)
        
        filepath = os.path.join(downloads_dir, filename)
        
        # Generate resume content
        content = self.generate_resume_content(resume_data)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            textColor=colors.darkblue
        )
        
        # Personal Information
        personal_info = content['personal_info']
        story.append(Paragraph(personal_info['name'].upper(), title_style))
        
        contact_info = f"{personal_info['email']} | {personal_info['phone']} | {personal_info['location']}"
        if personal_info['linkedin']:
            contact_info += f" | LinkedIn: {personal_info['linkedin']}"
        if personal_info['github']:
            contact_info += f" | GitHub: {personal_info['github']}"
        
        story.append(Paragraph(contact_info, styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Professional Summary
        if content['summary']:
            story.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
            story.append(Paragraph(content['summary'], styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Experience
        if content['experience']:
            story.append(Paragraph("EXPERIENCE", heading_style))
            for exp in content['experience']:
                end_date = "Present" if exp['current'] else exp['end_date']
                job_title = f"{exp['title']} | {exp['company']} | {exp['location']} | {exp['start_date']} - {end_date}"
                story.append(Paragraph(job_title, styles['Normal']))
                
                for achievement in exp['achievements']:
                    if achievement.strip():
                        story.append(Paragraph(f"• {achievement.strip()}", styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Education
        if content['education']:
            story.append(Paragraph("EDUCATION", heading_style))
            for edu in content['education']:
                gpa_text = f" | GPA: {edu['gpa']}" if edu['gpa'] else ""
                education_text = f"{edu['degree']} in {edu['major']} | {edu['university']} | {edu['graduation_year']}{gpa_text}"
                story.append(Paragraph(education_text, styles['Normal']))
                
                for achievement in edu['achievements']:
                    if achievement.strip():
                        story.append(Paragraph(f"• {achievement.strip()}", styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Skills
        if content['skills']['technical'] or content['skills']['tools'] or content['skills']['soft']:
            story.append(Paragraph("TECHNICAL SKILLS", heading_style))
            skills_text = ""
            if content['skills']['technical']:
                skills_text += f"Programming Languages: {', '.join(content['skills']['technical'])}<br/>"
            if content['skills']['tools']:
                skills_text += f"Tools & Technologies: {', '.join(content['skills']['tools'])}<br/>"
            if content['skills']['soft']:
                skills_text += f"Soft Skills: {', '.join(content['skills']['soft'])}"
            story.append(Paragraph(skills_text, styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Projects
        if content['projects']:
            story.append(Paragraph("PROJECTS", heading_style))
            for project in content['projects']:
                story.append(Paragraph(project['name'], styles['Normal']))
                story.append(Paragraph(project['description'], styles['Normal']))
                if project['technologies']:
                    story.append(Paragraph(f"Technologies: {', '.join(project['technologies'])}", styles['Normal']))
                if project['github_url']:
                    story.append(Paragraph(f"GitHub: {project['github_url']}", styles['Normal']))
                if project['live_url']:
                    story.append(Paragraph(f"Live Demo: {project['live_url']}", styles['Normal']))
                
                for achievement in project['achievements']:
                    if achievement.strip():
                        story.append(Paragraph(f"• {achievement.strip()}", styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
        
        return filepath