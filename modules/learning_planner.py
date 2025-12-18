import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class LearningPlanGenerator:
    def __init__(self):
        self.course_database = self._load_course_database()
        self.certification_database = self._load_certification_database()
        self.project_database = self._load_project_database()
    
    def _load_course_database(self) -> Dict[str, List[Dict]]:
        """Load online course database with Indian pricing and platforms"""
        return {
            'Python Programming': [
                {
                    'title': 'Python for Data Science',
                    'platform': 'Coursera',
                    'duration': '4 weeks',
                    'difficulty': 'Beginner',
                    'cost': 'Free',
                    'rating': 4.7,
                    'description': 'Learn Python fundamentals for data analysis',
                    'url': 'https://coursera.org/learn/python-data-science',
                    'indian_platform': 'NPTEL'
                },
                {
                    'title': 'Complete Python Bootcamp',
                    'platform': 'Udemy',
                    'duration': '6 weeks',
                    'difficulty': 'Intermediate',
                    'cost': '₹3,499',
                    'rating': 4.6,
                    'description': 'Comprehensive Python programming course',
                    'url': 'https://udemy.com/complete-python-bootcamp',
                    'indian_platform': 'Udemy India'
                },
                {
                    'title': 'Python Programming Fundamentals',
                    'platform': 'NPTEL',
                    'duration': '12 weeks',
                    'difficulty': 'Beginner',
                    'cost': 'Free',
                    'rating': 4.8,
                    'description': 'IIT/NIT Python programming course',
                    'url': 'https://nptel.ac.in/courses/python',
                    'indian_platform': 'NPTEL'
                }
            ],
            'Machine Learning': [
                {
                    'title': 'Machine Learning Course',
                    'platform': 'Stanford Online',
                    'duration': '11 weeks',
                    'difficulty': 'Intermediate',
                    'cost': 'Free',
                    'rating': 4.8,
                    'description': 'Andrew Ng\'s famous ML course',
                    'url': 'https://coursera.org/learn/machine-learning',
                    'indian_platform': 'Coursera India'
                },
                {
                    'title': 'Deep Learning Specialization',
                    'platform': 'Coursera',
                    'duration': '16 weeks',
                    'difficulty': 'Advanced',
                    'cost': '₹3,500/month',
                    'rating': 4.7,
                    'description': 'Comprehensive deep learning course',
                    'url': 'https://coursera.org/specializations/deep-learning',
                    'indian_platform': 'Coursera India'
                },
                {
                    'title': 'Machine Learning with Python',
                    'platform': 'NPTEL',
                    'duration': '12 weeks',
                    'difficulty': 'Intermediate',
                    'cost': 'Free',
                    'rating': 4.6,
                    'description': 'IIT ML course with Python implementation',
                    'url': 'https://nptel.ac.in/courses/ml',
                    'indian_platform': 'NPTEL'
                }
            ],
            'Data Analysis': [
                {
                    'title': 'Data Analysis with Python',
                    'platform': 'IBM',
                    'duration': '5 weeks',
                    'difficulty': 'Beginner',
                    'cost': 'Free',
                    'rating': 4.5,
                    'description': 'Learn data analysis using Python and pandas',
                    'url': 'https://coursera.org/learn/data-analysis-with-python',
                    'indian_platform': 'Coursera India'
                },
                {
                    'title': 'Data Science and Analytics',
                    'platform': 'NPTEL',
                    'duration': '12 weeks',
                    'difficulty': 'Intermediate',
                    'cost': 'Free',
                    'rating': 4.7,
                    'description': 'IIT data science course with real-world projects',
                    'url': 'https://nptel.ac.in/courses/data-science',
                    'indian_platform': 'NPTEL'
                }
            ],
            'Communication': [
                {
                    'title': 'Business Communication',
                    'platform': 'LinkedIn Learning',
                    'duration': '3 weeks',
                    'difficulty': 'Beginner',
                    'cost': '₹1,999/month',
                    'rating': 4.4,
                    'description': 'Improve professional communication skills',
                    'url': 'https://linkedin.com/learning/business-communication',
                    'indian_platform': 'LinkedIn Learning India'
                },
                {
                    'title': 'Professional Communication',
                    'platform': 'NPTEL',
                    'duration': '8 weeks',
                    'difficulty': 'Beginner',
                    'cost': 'Free',
                    'rating': 4.5,
                    'description': 'IIT professional communication course',
                    'url': 'https://nptel.ac.in/courses/communication',
                    'indian_platform': 'NPTEL'
                }
            ],
            'Project Management': [
                {
                    'title': 'Project Management Fundamentals',
                    'platform': 'Google',
                    'duration': '6 weeks',
                    'difficulty': 'Beginner',
                    'cost': 'Free',
                    'rating': 4.6,
                    'description': 'Google\'s project management certificate',
                    'url': 'https://coursera.org/professional-certificates/google-project-management',
                    'indian_platform': 'Coursera India'
                },
                {
                    'title': 'Project Management',
                    'platform': 'NPTEL',
                    'duration': '12 weeks',
                    'difficulty': 'Intermediate',
                    'cost': 'Free',
                    'rating': 4.6,
                    'description': 'IIT project management course with PMP preparation',
                    'url': 'https://nptel.ac.in/courses/project-management',
                    'indian_platform': 'NPTEL'
                }
            ]
        }
    
    def _load_certification_database(self) -> Dict[str, List[Dict]]:
        """Load certification database with Indian certifications and pricing"""
        return {
            'Python Programming': [
                {
                    'name': 'PCAP - Certified Associate in Python Programming',
                    'issuer': 'Python Institute',
                    'duration': '3-6 months',
                    'cost': '₹22,000',
                    'difficulty': 'Intermediate',
                    'description': 'Official Python programming certification',
                    'url': 'https://pythoninstitute.org/pcap',
                    'indian_equivalent': 'NPTEL Python Certification'
                },
                {
                    'name': 'NPTEL Python Programming Certification',
                    'issuer': 'NPTEL (IIT/NIT)',
                    'duration': '4-6 months',
                    'cost': '₹1,000',
                    'difficulty': 'Intermediate',
                    'description': 'IIT/NIT Python programming certification',
                    'url': 'https://nptel.ac.in/certificates/python',
                    'indian_equivalent': 'NPTEL'
                }
            ],
            'Machine Learning': [
                {
                    'name': 'AWS Machine Learning Specialty',
                    'issuer': 'Amazon Web Services',
                    'duration': '2-4 months',
                    'cost': '₹22,500',
                    'difficulty': 'Advanced',
                    'description': 'AWS ML services and solutions certification',
                    'url': 'https://aws.amazon.com/certification/certified-machine-learning-specialty/',
                    'indian_equivalent': 'AWS India'
                },
                {
                    'name': 'NPTEL Machine Learning Certification',
                    'issuer': 'NPTEL (IIT)',
                    'duration': '3-4 months',
                    'cost': '₹1,000',
                    'difficulty': 'Intermediate',
                    'description': 'IIT machine learning certification',
                    'url': 'https://nptel.ac.in/certificates/ml',
                    'indian_equivalent': 'NPTEL'
                }
            ],
            'Data Analysis': [
                {
                    'name': 'Google Data Analytics Certificate',
                    'issuer': 'Google',
                    'duration': '6 months',
                    'cost': '₹2,900/month',
                    'difficulty': 'Beginner',
                    'description': 'Comprehensive data analytics certification',
                    'url': 'https://coursera.org/professional-certificates/google-data-analytics',
                    'indian_equivalent': 'Coursera India'
                },
                {
                    'name': 'NPTEL Data Science Certification',
                    'issuer': 'NPTEL (IIT)',
                    'duration': '4-6 months',
                    'cost': '₹1,000',
                    'difficulty': 'Intermediate',
                    'description': 'IIT data science and analytics certification',
                    'url': 'https://nptel.ac.in/certificates/data-science',
                    'indian_equivalent': 'NPTEL'
                }
            ],
            'Project Management': [
                {
                    'name': 'PMP - Project Management Professional',
                    'issuer': 'PMI',
                    'duration': '3-6 months',
                    'cost': '₹30,000',
                    'difficulty': 'Advanced',
                    'description': 'World\'s leading project management certification',
                    'url': 'https://pmi.org/certifications/project-management-pmp',
                    'indian_equivalent': 'PMI India'
                },
                {
                    'name': 'NPTEL Project Management Certification',
                    'issuer': 'NPTEL (IIT)',
                    'duration': '3-4 months',
                    'cost': '₹1,000',
                    'difficulty': 'Intermediate',
                    'description': 'IIT project management certification',
                    'url': 'https://nptel.ac.in/certificates/project-management',
                    'indian_equivalent': 'NPTEL'
                }
            ]
        }
    
    def _load_project_database(self) -> Dict[str, List[Dict]]:
        """Load project database"""
        return {
            'Python Programming': [
                {
                    'title': 'Web Scraper Project',
                    'difficulty': 'Beginner',
                    'duration': '2-3 weeks',
                    'description': 'Build a web scraper to collect data from websites',
                    'skills_developed': ['Python', 'Web Scraping', 'Data Collection'],
                    'github_template': 'https://github.com/example/web-scraper-template'
                },
                {
                    'title': 'Data Visualization Dashboard',
                    'difficulty': 'Intermediate',
                    'duration': '3-4 weeks',
                    'description': 'Create interactive dashboards using Python libraries',
                    'skills_developed': ['Python', 'Data Visualization', 'Dashboard Design'],
                    'github_template': 'https://github.com/example/dashboard-template'
                }
            ],
            'Machine Learning': [
                {
                    'title': 'Predictive Model Project',
                    'difficulty': 'Intermediate',
                    'duration': '4-6 weeks',
                    'description': 'Build a machine learning model to predict outcomes',
                    'skills_developed': ['Machine Learning', 'Python', 'Data Analysis'],
                    'github_template': 'https://github.com/example/ml-prediction-template'
                }
            ],
            'Data Analysis': [
                {
                    'title': 'Business Intelligence Report',
                    'difficulty': 'Beginner',
                    'duration': '2-3 weeks',
                    'description': 'Analyze business data and create insights report',
                    'skills_developed': ['Data Analysis', 'SQL', 'Reporting'],
                    'github_template': 'https://github.com/example/bi-report-template'
                }
            ]
        }
    
    def generate_plan(self, skill_analysis: Dict, career_recommendations: Dict, 
                     student_data: Dict) -> Dict[str, Any]:
        """
        Generate personalized learning plan based on skill gaps and career goals
        """
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        # Get top career recommendations
        top_careers = career_recommendations.get('top_careers', [])
        if not top_careers:
            return {'error': 'No career recommendations available'}
        
        # Identify skill gaps from top careers
        skill_gaps = self._identify_skill_gaps(top_careers, skill_names)
        
        # Generate learning recommendations
        course_recommendations = self._recommend_courses(skill_gaps)
        certification_recommendations = self._recommend_certifications(skill_gaps)
        project_recommendations = self._recommend_projects(skill_gaps)
        
        # Create learning timeline
        learning_timeline = self._create_learning_timeline(
            course_recommendations, certification_recommendations, project_recommendations
        )
        
        # Generate study schedule
        study_schedule = self._generate_study_schedule(student_data)
        
        # Calculate learning metrics
        learning_metrics = self._calculate_learning_metrics(
            skill_gaps, course_recommendations, certification_recommendations
        )
        
        return {
            'skill_gaps': skill_gaps,
            'course_recommendations': course_recommendations,
            'certification_recommendations': certification_recommendations,
            'project_recommendations': project_recommendations,
            'learning_timeline': learning_timeline,
            'study_schedule': study_schedule,
            'learning_metrics': learning_metrics,
            'learning_goals': self._generate_learning_goals(skill_gaps, top_careers),
            'progress_tracking': self._setup_progress_tracking()
        }
    
    def _identify_skill_gaps(self, top_careers: List[Dict], current_skills: List[str]) -> List[Dict[str, Any]]:
        """Identify skill gaps from top career recommendations"""
        skill_gaps = []
        skill_priority = {}
        
        for career in top_careers[:3]:  # Top 3 careers
            missing_skills = career.get('missing_skills', [])
            for skill in missing_skills:
                if skill not in current_skills:
                    if skill in skill_priority:
                        skill_priority[skill] += 1
                    else:
                        skill_priority[skill] = 1
        
        # Sort by priority and create gap analysis
        for skill, priority in sorted(skill_priority.items(), key=lambda x: x[1], reverse=True):
            skill_gaps.append({
                'skill': skill,
                'priority': priority,
                'difficulty': self._estimate_skill_difficulty(skill),
                'estimated_time': self._estimate_learning_time(skill),
                'careers_needing': [c['title'] for c in top_careers if skill in c.get('missing_skills', [])]
            })
        
        return skill_gaps[:8]  # Top 8 skill gaps
    
    def _estimate_skill_difficulty(self, skill: str) -> str:
        """Estimate difficulty level for learning a skill"""
        difficulty_map = {
            'Python Programming': 'Beginner',
            'Machine Learning': 'Advanced',
            'Data Analysis': 'Beginner',
            'Communication': 'Beginner',
            'Project Management': 'Intermediate',
            'Leadership': 'Intermediate',
            'Critical Thinking': 'Intermediate',
            'Problem Solving': 'Intermediate'
        }
        return difficulty_map.get(skill, 'Intermediate')
    
    def _estimate_learning_time(self, skill: str) -> str:
        """Estimate time required to learn a skill"""
        time_map = {
            'Python Programming': '2-3 months',
            'Machine Learning': '4-6 months',
            'Data Analysis': '1-2 months',
            'Communication': '1-2 months',
            'Project Management': '2-3 months',
            'Leadership': '3-6 months',
            'Critical Thinking': '2-4 months',
            'Problem Solving': '2-3 months'
        }
        return time_map.get(skill, '2-3 months')
    
    def _recommend_courses(self, skill_gaps: List[Dict]) -> List[Dict[str, Any]]:
        """Recommend courses for skill gaps"""
        recommendations = []
        
        for gap in skill_gaps[:5]:  # Top 5 skill gaps
            skill = gap['skill']
            courses = self.course_database.get(skill, [])
            
            if courses:
                # Select best course based on difficulty match
                suitable_courses = [c for c in courses if c['difficulty'] == gap['difficulty']]
                if not suitable_courses:
                    suitable_courses = courses[:2]  # Take first 2 if no exact match
                
                for course in suitable_courses[:2]:  # Max 2 courses per skill
                    recommendations.append({
                        'skill': skill,
                        'course': course,
                        'priority': gap['priority'],
                        'estimated_completion': self._calculate_course_completion_time(course)
                    })
        
        return sorted(recommendations, key=lambda x: x['priority'], reverse=True)
    
    def _calculate_course_completion_time(self, course: Dict) -> str:
        """Calculate estimated completion time for course"""
        duration = course.get('duration', '4 weeks')
        # Add some buffer time
        if 'weeks' in duration:
            weeks = int(duration.split()[0])
            return f"{weeks + 1}-{weeks + 2} weeks"
        return duration
    
    def _recommend_certifications(self, skill_gaps: List[Dict]) -> List[Dict[str, Any]]:
        """Recommend certifications for skill gaps"""
        recommendations = []
        
        for gap in skill_gaps[:3]:  # Top 3 skill gaps
            skill = gap['skill']
            certifications = self.certification_database.get(skill, [])
            
            for cert in certifications:
                recommendations.append({
                    'skill': skill,
                    'certification': cert,
                    'priority': gap['priority'],
                    'recommended_timeline': self._calculate_cert_timeline(cert)
                })
        
        return sorted(recommendations, key=lambda x: x['priority'], reverse=True)
    
    def _calculate_cert_timeline(self, cert: Dict) -> str:
        """Calculate recommended timeline for certification"""
        duration = cert.get('duration', '3-6 months')
        return f"Start after 2-3 months of learning: {duration}"
    
    def _recommend_projects(self, skill_gaps: List[Dict]) -> List[Dict[str, Any]]:
        """Recommend projects for skill gaps"""
        recommendations = []
        
        for gap in skill_gaps[:4]:  # Top 4 skill gaps
            skill = gap['skill']
            projects = self.project_database.get(skill, [])
            
            for project in projects:
                recommendations.append({
                    'skill': skill,
                    'project': project,
                    'priority': gap['priority'],
                    'recommended_order': len(recommendations) + 1
                })
        
        return sorted(recommendations, key=lambda x: x['priority'], reverse=True)
    
    def _create_learning_timeline(self, courses: List, certifications: List, 
                                 projects: List) -> List[Dict[str, Any]]:
        """Create a comprehensive learning timeline according to problem statement"""
        timeline = []
        current_week = 1
        
        # Phase 1: Foundation Building (Weeks 1-12)
        foundation_courses = [c for c in courses if c['course']['difficulty'] == 'Beginner'][:4]
        for i, course in enumerate(foundation_courses):
            duration = 3 if i < 2 else 4  # First 2 courses: 3 weeks each, rest: 4 weeks
            timeline.append({
                'phase': 'Foundation Building',
                'week': f"Week {current_week}-{current_week + duration - 1}",
                'activity': 'Online Course',
                'title': course['course']['title'],
                'skill': course['skill'],
                'platform': course['course'].get('indian_platform', course['course']['platform']),
                'cost': course['course']['cost'],
                'description': f"Master {course['skill']} fundamentals through {course['course']['title']}",
                'deliverables': [
                    f"Complete all course modules",
                    f"Submit assignments and quizzes",
                    f"Build mini-projects in {course['skill']}"
                ]
            })
            current_week += duration
        
        # Phase 2: Skill Application (Weeks 13-20)
        foundation_projects = [p for p in projects if p['project']['difficulty'] == 'Beginner'][:3]
        for i, project in enumerate(foundation_projects):
            duration = 2 if i < 2 else 3
            timeline.append({
                'phase': 'Skill Application',
                'week': f"Week {current_week}-{current_week + duration - 1}",
                'activity': 'Portfolio Project',
                'title': project['project']['title'],
                'skill': project['skill'],
                'platform': 'GitHub',
                'cost': 'Free',
                'description': f"Build {project['project']['title']} to demonstrate {project['skill']} proficiency",
                'deliverables': [
                    f"Complete {project['project']['title']} project",
                    f"Document code with README",
                    f"Deploy project online",
                    f"Create project presentation"
                ]
            })
            current_week += duration
        
        # Phase 3: Advanced Learning (Weeks 21-32)
        advanced_courses = [c for c in courses if c['course']['difficulty'] in ['Intermediate', 'Advanced']][:3]
        for i, course in enumerate(advanced_courses):
            duration = 4 if i < 2 else 5
            timeline.append({
                'phase': 'Advanced Learning',
                'week': f"Week {current_week}-{current_week + duration - 1}",
                'activity': 'Advanced Course',
                'title': course['course']['title'],
                'skill': course['skill'],
                'platform': course['course'].get('indian_platform', course['course']['platform']),
                'cost': course['course']['cost'],
                'description': f"Deep dive into {course['skill']} with {course['course']['title']}",
                'deliverables': [
                    f"Complete advanced course modules",
                    f"Build complex projects",
                    f"Participate in course discussions",
                    f"Submit final project"
                ]
            })
            current_week += duration
        
        # Phase 4: Certification Preparation (Weeks 33-40)
        for i, cert in enumerate(certifications[:2]):
            duration = 4 if i < 1 else 5
            timeline.append({
                'phase': 'Certification Preparation',
                'week': f"Week {current_week}-{current_week + duration - 1}",
                'activity': 'Certification',
                'title': cert['certification']['name'],
                'skill': cert['skill'],
                'platform': cert['certification'].get('indian_equivalent', cert['certification']['issuer']),
                'cost': cert['certification']['cost'],
                'description': f"Prepare for and earn {cert['certification']['name']} certification",
                'deliverables': [
                    f"Complete certification study materials",
                    f"Take practice exams",
                    f"Schedule and pass certification exam",
                    f"Update LinkedIn with certification"
                ]
            })
            current_week += duration
        
        # Phase 5: Portfolio Enhancement (Weeks 41-48)
        timeline.append({
            'phase': 'Portfolio Enhancement',
            'week': f"Week {current_week}-{current_week + 7}",
            'activity': 'Portfolio Development',
            'title': 'Professional Portfolio Creation',
            'skill': 'Portfolio Development',
            'platform': 'GitHub + Personal Website',
            'cost': '₹500-2000 (hosting)',
            'description': 'Create comprehensive professional portfolio showcasing all projects and skills',
            'deliverables': [
                'Build personal website/portfolio',
                'Organize GitHub repositories',
                'Create project case studies',
                'Write technical blog posts',
                'Prepare resume and cover letter'
            ]
        })
        
        return timeline
    
    def _generate_study_schedule(self, student_data: Dict) -> Dict[str, Any]:
        """Generate personalized study schedule"""
        # Default schedule - can be customized based on student preferences
        return {
            'weekly_hours': 10,  # Default 10 hours per week
            'study_days': ['Monday', 'Wednesday', 'Friday', 'Saturday'],
            'daily_schedule': {
                'Monday': '2.5 hours - Course work',
                'Wednesday': '2.5 hours - Course work',
                'Friday': '2.5 hours - Project work',
                'Saturday': '2.5 hours - Review and practice'
            },
            'recommended_times': 'Evenings (7-9 PM) or weekends',
            'break_schedule': '10-minute break every 50 minutes',
            'study_environment': 'Quiet space with good internet connection'
        }
    
    def _calculate_learning_metrics(self, skill_gaps: List, courses: List, 
                                   certifications: List) -> Dict[str, Any]:
        """Calculate learning metrics and milestones"""
        total_skills = len(skill_gaps)
        courses_count = len(courses)
        certs_count = len(certifications)
        
        return {
            'total_skills_to_develop': total_skills,
            'courses_to_complete': courses_count,
            'certifications_to_earn': certs_count,
            'estimated_total_time': f"{total_skills * 2}-{total_skills * 3} months",
            'weekly_commitment': '10 hours',
            'success_metrics': [
                'Complete 80% of recommended courses',
                'Finish 2-3 portfolio projects',
                'Earn 1-2 relevant certifications',
                'Build GitHub portfolio with 5+ projects'
            ],
            'milestones': [
                'Month 1: Complete foundation courses',
                'Month 2: Finish first portfolio project',
                'Month 3: Start intermediate courses',
                'Month 4: Complete second project',
                'Month 5: Begin certification preparation',
                'Month 6: Earn first certification'
            ]
        }
    
    def _generate_learning_goals(self, skill_gaps: List, top_careers: List) -> List[Dict[str, str]]:
        """Generate specific learning goals"""
        goals = []
        
        # Short-term goals (1-3 months)
        short_term_skills = [gap for gap in skill_gaps if gap['difficulty'] == 'Beginner'][:3]
        for skill in short_term_skills:
            goals.append({
                'timeline': 'Short-term (1-3 months)',
                'goal': f"Master {skill['skill']} fundamentals",
                'measurement': f"Complete 2 courses and 1 project in {skill['skill']}"
            })
        
        # Medium-term goals (3-6 months)
        medium_term_skills = [gap for gap in skill_gaps if gap['difficulty'] == 'Intermediate'][:2]
        for skill in medium_term_skills:
            goals.append({
                'timeline': 'Medium-term (3-6 months)',
                'goal': f"Develop advanced {skill['skill']} capabilities",
                'measurement': f"Complete advanced course and build portfolio project"
            })
        
        # Long-term goals (6+ months)
        if top_careers:
            best_career = top_careers[0]['title']
            goals.append({
                'timeline': 'Long-term (6+ months)',
                'goal': f"Prepare for {best_career} role",
                'measurement': f"Complete all skill requirements and earn relevant certification"
            })
        
        return goals
    
    def _setup_progress_tracking(self) -> Dict[str, Any]:
        """Set up progress tracking system"""
        return {
            'tracking_methods': [
                'Weekly skill assessment quizzes',
                'Project completion milestones',
                'Course completion certificates',
                'GitHub commit activity',
                'Certification exam scores'
            ],
            'progress_indicators': [
                'Skills mastered: 0/8',
                'Courses completed: 0/6',
                'Projects finished: 0/4',
                'Certifications earned: 0/2',
                'Overall progress: 0%'
            ],
            'review_schedule': 'Weekly progress review every Sunday',
            'adjustment_triggers': [
                'If falling behind schedule by 2+ weeks',
                'If course difficulty is too high/low',
                'If career goals change',
                'If new opportunities arise'
            ]
        }
