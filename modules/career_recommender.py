import sqlite3
import json
from typing import Dict, List, Any
import random

class CareerRecommender:
    def __init__(self):
        self.db_path = 'career_advisor.db'
        self.career_database = {}
        self._load_career_data()
    
    def _load_career_data(self):
        """Load career data from database and add comprehensive career information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT title, industry, required_skills, salary_range, growth_rate, description 
            FROM careers
        ''')
        
        careers = cursor.fetchall()
        
        for career in careers:
            self.career_database[career[0]] = {
                'title': career[0],
                'industry': career[1],
                'required_skills': career[2].split(',') if career[2] else [],
                'salary_range': career[3],
                'growth_rate': career[4],
                'description': career[5]
            }
        
        # Add comprehensive career data
        self._add_comprehensive_career_data()
        
        conn.close()
    
    def _add_comprehensive_career_data(self):
        """Add comprehensive career information for better recommendations"""
        comprehensive_careers = {
            'Data Scientist': {
                'title': 'Data Scientist',
                'industry': 'Technology',
                'required_skills': ['Python Programming', 'Machine Learning', 'Data Analysis', 'Statistics', 'SQL'],
                'salary_range': '₹8,00,000 - ₹20,00,000',
                'growth_rate': 15.0,
                'description': 'Analyze complex data to help organizations make data-driven decisions',
                'entry_level': 'Data Analyst',
                'senior_level': 'Senior Data Scientist',
                'leadership_path': 'Data Science Manager',
                'alternative_roles': ['Machine Learning Engineer', 'Data Engineer', 'Business Intelligence Analyst'],
                'certifications': ['AWS Machine Learning', 'Google Data Analytics', 'Microsoft Azure Data Scientist'],
                'skills_breakdown': {
                    'technical': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics'],
                    'tools': ['TensorFlow', 'PyTorch', 'Pandas', 'Scikit-learn', 'Tableau'],
                    'soft_skills': ['Communication', 'Problem Solving', 'Critical Thinking']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 4.2,
                'work_life_balance': 3.8,
                'career_progression': '2-3 years to Senior, 5-7 years to Lead/Manager'
            },
            'Software Engineer': {
                'title': 'Software Engineer',
                'industry': 'Technology',
                'required_skills': ['Python Programming', 'JavaScript', 'SQL', 'Problem Solving', 'Communication'],
                'salary_range': '₹7,00,000 - ₹18,00,000',
                'growth_rate': 12.0,
                'description': 'Design and develop software applications and systems',
                'entry_level': 'Junior Software Engineer',
                'senior_level': 'Senior Software Engineer',
                'leadership_path': 'Engineering Manager',
                'alternative_roles': ['Full Stack Developer', 'DevOps Engineer', 'Technical Lead'],
                'certifications': ['AWS Solutions Architect', 'Google Cloud Professional', 'Microsoft Azure Developer'],
                'skills_breakdown': {
                    'technical': ['JavaScript', 'Python', 'Java', 'React', 'Node.js'],
                    'tools': ['Git', 'Docker', 'Kubernetes', 'Jenkins', 'VS Code'],
                    'soft_skills': ['Communication', 'Teamwork', 'Problem Solving']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 4.0,
                'work_life_balance': 3.5,
                'career_progression': '2-3 years to Senior, 5-7 years to Lead/Manager'
            },
            'Product Manager': {
                'title': 'Product Manager',
                'industry': 'Technology',
                'required_skills': ['Project Management', 'Communication', 'Leadership', 'Critical Thinking'],
                'salary_range': '₹9,00,000 - ₹22,00,000',
                'growth_rate': 8.0,
                'description': 'Lead product development and strategy for technology products',
                'entry_level': 'Associate Product Manager',
                'senior_level': 'Senior Product Manager',
                'leadership_path': 'Director of Product',
                'alternative_roles': ['Product Owner', 'Program Manager', 'Business Analyst'],
                'certifications': ['PMP', 'Certified Scrum Product Owner', 'Google Product Management'],
                'skills_breakdown': {
                    'technical': ['Product Strategy', 'Market Research', 'Data Analysis'],
                    'tools': ['Jira', 'Confluence', 'Figma', 'Analytics Tools'],
                    'soft_skills': ['Communication', 'Leadership', 'Project Management']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 4.1,
                'work_life_balance': 3.2,
                'career_progression': '2-3 years to Senior, 5-7 years to Director'
            },
            'Data Analyst': {
                'title': 'Data Analyst',
                'industry': 'Technology',
                'required_skills': ['Data Analysis', 'SQL', 'Python Programming', 'Communication'],
                'salary_range': '₹6,00,000 - ₹12,00,000',
                'growth_rate': 10.0,
                'description': 'Interpret data and turn it into information for business decisions',
                'entry_level': 'Junior Data Analyst',
                'senior_level': 'Senior Data Analyst',
                'leadership_path': 'Analytics Manager',
                'alternative_roles': ['Business Intelligence Analyst', 'Data Scientist', 'Research Analyst'],
                'certifications': ['Google Data Analytics', 'Microsoft Power BI', 'Tableau Desktop Specialist'],
                'skills_breakdown': {
                    'technical': ['SQL', 'Python', 'Excel', 'Statistics', 'Data Visualization'],
                    'tools': ['Tableau', 'Power BI', 'Pandas', 'NumPy', 'Matplotlib'],
                    'soft_skills': ['Communication', 'Problem Solving', 'Critical Thinking']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 4.0,
                'work_life_balance': 4.0,
                'career_progression': '2-3 years to Senior, 4-6 years to Manager'
            },
            'Machine Learning Engineer': {
                'title': 'Machine Learning Engineer',
                'industry': 'Technology',
                'required_skills': ['Machine Learning', 'Python Programming', 'Data Analysis', 'Problem Solving'],
                'salary_range': '₹8,50,000 - ₹19,00,000',
                'growth_rate': 20.0,
                'description': 'Build and deploy machine learning models in production environments',
                'entry_level': 'Junior ML Engineer',
                'senior_level': 'Senior ML Engineer',
                'leadership_path': 'ML Engineering Manager',
                'alternative_roles': ['Data Scientist', 'AI Engineer', 'Research Scientist'],
                'certifications': ['AWS Machine Learning', 'Google ML Engineer', 'Microsoft Azure AI Engineer'],
                'skills_breakdown': {
                    'technical': ['Python', 'Machine Learning', 'Deep Learning', 'Statistics', 'Cloud Computing'],
                    'tools': ['TensorFlow', 'PyTorch', 'Scikit-learn', 'Docker', 'Kubernetes'],
                    'soft_skills': ['Communication', 'Problem Solving', 'Critical Thinking']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 4.3,
                'work_life_balance': 3.7,
                'career_progression': '2-3 years to Senior, 5-7 years to Lead/Manager'
            },
            'UX Designer': {
                'title': 'UX Designer',
                'industry': 'Technology',
                'required_skills': ['Communication', 'Problem Solving', 'Critical Thinking', 'Leadership'],
                'salary_range': '₹6,50,000 - ₹15,00,000',
                'growth_rate': 9.0,
                'description': 'Design user experiences for digital products and services',
                'entry_level': 'Junior UX Designer',
                'senior_level': 'Senior UX Designer',
                'leadership_path': 'UX Design Manager',
                'alternative_roles': ['UI Designer', 'Product Designer', 'User Researcher'],
                'certifications': ['Google UX Design', 'Adobe Certified Expert', 'Nielsen Norman Group'],
                'skills_breakdown': {
                    'technical': ['User Research', 'Wireframing', 'Prototyping', 'Design Systems'],
                    'tools': ['Figma', 'Sketch', 'Adobe XD', 'InVision', 'Miro'],
                    'soft_skills': ['Communication', 'Empathy', 'Problem Solving']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 4.2,
                'work_life_balance': 4.1,
                'career_progression': '2-3 years to Senior, 5-7 years to Lead/Manager'
            },
            'DevOps Engineer': {
                'title': 'DevOps Engineer',
                'industry': 'Technology',
                'required_skills': ['Python Programming', 'Problem Solving', 'Communication', 'Leadership'],
                'salary_range': '₹8,00,000 - ₹18,00,000',
                'growth_rate': 14.0,
                'description': 'Manage deployment and infrastructure for software applications',
                'entry_level': 'Junior DevOps Engineer',
                'senior_level': 'Senior DevOps Engineer',
                'leadership_path': 'DevOps Manager',
                'alternative_roles': ['Site Reliability Engineer', 'Cloud Engineer', 'Infrastructure Engineer'],
                'certifications': ['AWS DevOps Engineer', 'Google Cloud Professional', 'Microsoft Azure DevOps'],
                'skills_breakdown': {
                    'technical': ['Python', 'Linux', 'Cloud Computing', 'Containerization', 'CI/CD'],
                    'tools': ['Docker', 'Kubernetes', 'Jenkins', 'Terraform', 'Ansible'],
                    'soft_skills': ['Communication', 'Problem Solving', 'Teamwork']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 4.1,
                'work_life_balance': 3.6,
                'career_progression': '2-3 years to Senior, 5-7 years to Lead/Manager'
            },
            'Business Analyst': {
                'title': 'Business Analyst',
                'industry': 'Business',
                'required_skills': ['Communication', 'Problem Solving', 'Critical Thinking', 'Data Analysis'],
                'salary_range': '₹5,50,000 - ₹12,00,000',
                'growth_rate': 7.0,
                'description': 'Analyze business processes and recommend improvements',
                'entry_level': 'Junior Business Analyst',
                'senior_level': 'Senior Business Analyst',
                'leadership_path': 'Business Analysis Manager',
                'alternative_roles': ['Product Manager', 'Data Analyst', 'Process Improvement Specialist'],
                'certifications': ['CBAP', 'PMP', 'Six Sigma', 'Agile Business Analysis'],
                'skills_breakdown': {
                    'technical': ['Data Analysis', 'Process Mapping', 'Requirements Gathering', 'SQL'],
                    'tools': ['Excel', 'Power BI', 'Visio', 'Jira', 'Confluence'],
                    'soft_skills': ['Communication', 'Problem Solving', 'Stakeholder Management']
                },
                'work_environment': 'Office/Remote Hybrid',
                'job_satisfaction': 3.9,
                'work_life_balance': 4.0,
                'career_progression': '2-3 years to Senior, 4-6 years to Manager'
            }
        }
        
        # Update career database with comprehensive data
        for title, data in comprehensive_careers.items():
            if title in self.career_database:
                self.career_database[title].update(data)
            else:
                self.career_database[title] = data
    
    def get_recommendations(self, skill_analysis: Dict, market_analysis: Dict, 
                          student_data: Dict) -> Dict[str, Any]:
        """
        Generate personalized career path recommendations
        """
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        interests = student_data.get('interests', [])
        
        # Calculate career compatibility scores
        career_scores = self._calculate_career_scores(skill_names, interests)
        
        # Get top recommendations
        top_careers = sorted(career_scores.items(), key=lambda x: x[1]['score'], reverse=True)[:5]
        
        # Generate career paths
        career_paths = self._generate_career_paths(top_careers, skill_analysis, market_analysis)
        
        # Analyze career progression
        progression_analysis = self._analyze_career_progression(top_careers, skill_analysis)
        
        # Generate role recommendations
        role_recommendations = self._generate_role_recommendations(top_careers, skill_analysis)
        
        return {
            'top_careers': [self._format_career_recommendation(career, score) 
                           for career, score in top_careers],
            'career_paths': career_paths,
            'progression_analysis': progression_analysis,
            'role_recommendations': role_recommendations,
            'compatibility_summary': self._generate_compatibility_summary(career_scores),
            'next_steps': self._generate_next_steps(top_careers, skill_analysis),
            'detailed_career_analysis': self._generate_detailed_career_analysis(top_careers, skill_analysis),
            'career_comparison': self._generate_career_comparison(top_careers[:3]),
            'industry_insights': self._generate_industry_insights(top_careers, market_analysis),
            'skill_roadmap': self._generate_skill_roadmap(top_careers, skill_analysis)
        }
    
    def _calculate_career_scores(self, skills: List[str], interests: List[str]) -> Dict[str, Dict]:
        """Calculate compatibility scores for each career"""
        career_scores = {}
        
        for title, career_data in self.career_database.items():
            required_skills = career_data['required_skills']
            
            # Calculate skill match score
            skill_matches = len([skill for skill in skills if skill in required_skills])
            skill_score = (skill_matches / len(required_skills)) * 100 if required_skills else 0
            
            # Calculate interest alignment
            interest_score = self._calculate_interest_alignment(career_data['industry'], interests)
            
            # Calculate market opportunity score
            market_score = self._calculate_market_score(career_data)
            
            # Weighted total score
            total_score = (skill_score * 0.5 + interest_score * 0.3 + market_score * 0.2)
            
            career_scores[title] = {
                'score': round(total_score, 2),
                'skill_score': round(skill_score, 2),
                'interest_score': round(interest_score, 2),
                'market_score': round(market_score, 2),
                'skill_matches': skill_matches,
                'total_required': len(required_skills),
                'missing_skills': [skill for skill in required_skills if skill not in skills]
            }
        
        return career_scores
    
    def _calculate_interest_alignment(self, industry: str, interests: List[str]) -> float:
        """Calculate how well career aligns with user interests"""
        if not interests:
            return 50.0  # Neutral score if no interests specified
        
        # Industry-interest mapping
        industry_keywords = {
            'Technology': ['technology', 'programming', 'software', 'ai', 'data', 'tech'],
            'Healthcare': ['healthcare', 'health', 'medical', 'science', 'research'],
            'Finance': ['finance', 'banking', 'business', 'economics', 'money'],
            'Education': ['education', 'teaching', 'learning', 'academic', 'research']
        }
        
        industry_keywords_list = industry_keywords.get(industry, [])
        
        # Check for keyword matches
        matches = 0
        for interest in interests:
            for keyword in industry_keywords_list:
                if keyword.lower() in interest.lower():
                    matches += 1
                    break
        
        return (matches / len(interests)) * 100 if interests else 50.0
    
    def _calculate_market_score(self, career_data: Dict) -> float:
        """Calculate market opportunity score for career"""
        growth_rate = career_data.get('growth_rate', 0)
        
        # Convert growth rate to score (0-100)
        # Assuming 0-20% growth rate maps to 0-100 score
        market_score = min(growth_rate * 5, 100)
        
        # Add some randomness to simulate market factors
        market_score += random.uniform(-5, 5)
        
        return max(0, min(100, market_score))
    
    def _format_career_recommendation(self, career_title: str, score_data: Dict) -> Dict[str, Any]:
        """Format career recommendation with all relevant data"""
        career_data = self.career_database[career_title]
        
        return {
            'title': career_title,
            'industry': career_data['industry'],
            'description': career_data['description'],
            'salary_range': career_data['salary_range'],
            'growth_rate': career_data['growth_rate'],
            'compatibility_score': score_data['score'],
            'skill_match_percentage': round((score_data['skill_matches'] / score_data['total_required']) * 100, 2),
            'missing_skills': score_data['missing_skills'],
            'required_skills': career_data['required_skills'],
            'why_recommended': self._generate_recommendation_reason(score_data, career_data)
        }
    
    def _generate_recommendation_reason(self, score_data: Dict, career_data: Dict) -> str:
        """Generate explanation for why this career is recommended"""
        reasons = []
        
        if score_data['skill_score'] > 70:
            reasons.append("Strong skill alignment")
        elif score_data['skill_score'] > 40:
            reasons.append("Good skill foundation")
        
        if score_data['interest_score'] > 70:
            reasons.append("Matches your interests")
        
        if career_data['growth_rate'] > 10:
            reasons.append("High growth industry")
        elif career_data['growth_rate'] > 5:
            reasons.append("Stable growth prospects")
        
        if not reasons:
            reasons.append("Good potential with skill development")
        
        return "; ".join(reasons)
    
    def _generate_career_paths(self, top_careers: List, skill_analysis: Dict, 
                             market_analysis: Dict) -> List[Dict[str, Any]]:
        """Generate career progression paths"""
        paths = []
        
        for career_title, score_data in top_careers[:3]:  # Top 3 careers
            career_data = self.career_database[career_title]
            
            # Generate entry-level to senior progression
            path = {
                'career_title': career_title,
                'industry': career_data['industry'],
                'stages': [
                    {
                        'level': 'Entry Level',
                        'title': f'Junior {career_title}',
                        'timeline': '0-2 years',
                        'required_skills': score_data['missing_skills'][:3],  # Top 3 missing
                        'salary_estimate': self._estimate_salary(career_data, 0.6),
                        'description': f'Entry-level position in {career_data["industry"]}'
                    },
                    {
                        'level': 'Mid Level',
                        'title': career_title,
                        'timeline': '2-5 years',
                        'required_skills': score_data['missing_skills'][:5],
                        'salary_estimate': self._estimate_salary(career_data, 1.0),
                        'description': f'Mid-level {career_title} role with increased responsibilities'
                    },
                    {
                        'level': 'Senior Level',
                        'title': f'Senior {career_title}',
                        'timeline': '5+ years',
                        'required_skills': score_data['missing_skills'],
                        'salary_estimate': self._estimate_salary(career_data, 1.4),
                        'description': f'Senior-level position with leadership responsibilities'
                    }
                ]
            }
            paths.append(path)
        
        return paths
    
    def _estimate_salary(self, career_data: Dict, multiplier: float) -> str:
        """Estimate salary based on career data and level multiplier"""
        # Extract base salary from salary range (simplified)
        salary_range = career_data.get('salary_range', '₹5,00,000 - ₹8,00,000')
        
        # This is a simplified estimation - in reality, you'd parse the range properly
        base_salary = 650000  # Default base in Indian Rupees
        estimated = int(base_salary * multiplier)
        
        return f'₹{estimated:,}'
    
    def _analyze_career_progression(self, top_careers: List, skill_analysis: Dict) -> Dict[str, Any]:
        """Analyze career progression opportunities"""
        if not top_careers:
            return {'message': 'No career recommendations available'}
        
        best_career = top_careers[0]
        career_data = self.career_database[best_career[0]]
        
        return {
            'primary_career': best_career[0],
            'progression_potential': 'High' if best_career[1]['score'] > 70 else 'Medium',
            'skill_gap_analysis': {
                'critical_skills': best_career[1]['missing_skills'][:3],
                'development_time': '6-12 months',
                'priority_skills': best_career[1]['missing_skills'][:5]
            },
            'industry_opportunities': career_data['industry'],
            'growth_trajectory': f"{career_data['growth_rate']}% annual growth"
        }
    
    def _generate_role_recommendations(self, top_careers: List, skill_analysis: Dict) -> List[Dict[str, str]]:
        """Generate specific role recommendations"""
        roles = []
        
        for career_title, score_data in top_careers[:3]:
            career_data = self.career_database[career_title]
            
            # Generate related roles
            related_roles = self._get_related_roles(career_title, career_data['industry'])
            
            for role in related_roles:
                roles.append({
                    'title': role['title'],
                    'industry': career_data['industry'],
                    'compatibility': role['compatibility'],
                    'description': role['description'],
                    'requirements': role['requirements']
                })
        
        return roles[:6]  # Top 6 roles
    
    def _get_related_roles(self, career_title: str, industry: str) -> List[Dict[str, Any]]:
        """Get related roles for a career"""
        # This would typically come from a more comprehensive database
        related_roles_map = {
            'Data Scientist': [
                {'title': 'Data Analyst', 'compatibility': 'High', 'description': 'Analyze data to help business decisions', 'requirements': 'Data Analysis, SQL, Statistics'},
                {'title': 'Machine Learning Engineer', 'compatibility': 'High', 'description': 'Build and deploy ML models', 'requirements': 'Machine Learning, Python, Cloud Computing'},
                {'title': 'Business Intelligence Analyst', 'compatibility': 'Medium', 'description': 'Create reports and dashboards', 'requirements': 'Data Analysis, Communication, Business Knowledge'}
            ],
            'Software Engineer': [
                {'title': 'Full Stack Developer', 'compatibility': 'High', 'description': 'Develop both frontend and backend', 'requirements': 'JavaScript, Python, Database Design'},
                {'title': 'DevOps Engineer', 'compatibility': 'Medium', 'description': 'Manage deployment and infrastructure', 'requirements': 'Cloud Computing, Automation, System Administration'},
                {'title': 'Product Manager', 'compatibility': 'Medium', 'description': 'Lead product development', 'requirements': 'Project Management, Communication, Technical Knowledge'}
            ]
        }
        
        return related_roles_map.get(career_title, [
            {'title': f'Related {career_title}', 'compatibility': 'Medium', 'description': 'Related role in same field', 'requirements': 'Similar skills'}
        ])
    
    def _generate_compatibility_summary(self, career_scores: Dict) -> Dict[str, Any]:
        """Generate summary of career compatibility"""
        if not career_scores:
            return {'message': 'No career data available'}
        
        scores = [data['score'] for data in career_scores.values()]
        
        return {
            'average_compatibility': round(sum(scores) / len(scores), 2),
            'highest_score': max(scores),
            'careers_above_70': len([s for s in scores if s > 70]),
            'total_careers_analyzed': len(scores),
            'recommendation': 'Focus on top 3 careers for best opportunities' if max(scores) > 60 else 'Consider skill development before career transition'
        }
    
    def _generate_next_steps(self, top_careers: List, skill_analysis: Dict) -> List[str]:
        """Generate next steps for career development"""
        if not top_careers:
            return ['Complete skill assessment to get personalized recommendations']
        
        steps = []
        best_career = top_careers[0]
        missing_skills = best_career[1]['missing_skills']
        
        if missing_skills:
            steps.append(f"Develop key skills: {', '.join(missing_skills[:3])}")
        
        steps.append(f"Research {best_career[0]} roles and requirements")
        steps.append("Build portfolio projects in your target field")
        steps.append("Network with professionals in your target industry")
        steps.append("Consider relevant certifications or courses")
        
        return steps
    
    def _generate_detailed_career_analysis(self, top_careers: List, skill_analysis: Dict) -> Dict[str, Any]:
        """Generate detailed analysis for top career recommendations"""
        if not top_careers:
            return {'message': 'No career recommendations available'}
        
        detailed_analysis = {}
        
        for career_title, score_data in top_careers[:3]:  # Top 3 careers
            career_data = self.career_database[career_title]
            
            detailed_analysis[career_title] = {
                'overview': {
                    'title': career_title,
                    'industry': career_data['industry'],
                    'compatibility_score': score_data['score'],
                    'description': career_data['description'],
                    'growth_rate': career_data['growth_rate'],
                    'salary_range': career_data['salary_range']
                },
                'career_progression': {
                    'entry_level': career_data.get('entry_level', f'Junior {career_title}'),
                    'senior_level': career_data.get('senior_level', f'Senior {career_title}'),
                    'leadership_path': career_data.get('leadership_path', f'{career_title} Manager'),
                    'progression_timeline': career_data.get('career_progression', '2-3 years to Senior level')
                },
                'skills_analysis': {
                    'required_skills': career_data['required_skills'],
                    'missing_skills': score_data['missing_skills'],
                    'skill_match_percentage': round((score_data['skill_matches'] / score_data['total_required']) * 100, 2),
                    'skills_breakdown': career_data.get('skills_breakdown', {})
                },
                'work_environment': {
                    'type': career_data.get('work_environment', 'Office/Remote Hybrid'),
                    'job_satisfaction': career_data.get('job_satisfaction', 4.0),
                    'work_life_balance': career_data.get('work_life_balance', 3.5)
                },
                'certifications': career_data.get('certifications', []),
                'alternative_roles': career_data.get('alternative_roles', []),
                'market_demand': self._assess_market_demand(career_title, career_data),
                'learning_path': self._generate_learning_path(career_title, score_data['missing_skills'])
            }
        
        return detailed_analysis
    
    def _generate_career_comparison(self, top_careers: List) -> Dict[str, Any]:
        """Generate side-by-side comparison of top careers"""
        if len(top_careers) < 2:
            return {'message': 'Need at least 2 careers for comparison'}
        
        comparison = {
            'careers': [],
            'comparison_matrix': {
                'salary': {},
                'growth_rate': {},
                'skill_requirements': {},
                'work_life_balance': {},
                'job_satisfaction': {}
            }
        }
        
        for career_title, score_data in top_careers:
            career_data = self.career_database[career_title]
            
            comparison['careers'].append({
                'title': career_title,
                'compatibility_score': score_data['score'],
                'industry': career_data['industry'],
                'salary_range': career_data['salary_range'],
                'growth_rate': career_data['growth_rate'],
                'work_life_balance': career_data.get('work_life_balance', 3.5),
                'job_satisfaction': career_data.get('job_satisfaction', 4.0)
            })
            
            # Populate comparison matrix
            comparison['comparison_matrix']['salary'][career_title] = career_data['salary_range']
            comparison['comparison_matrix']['growth_rate'][career_title] = career_data['growth_rate']
            comparison['comparison_matrix']['skill_requirements'][career_title] = len(career_data['required_skills'])
            comparison['comparison_matrix']['work_life_balance'][career_title] = career_data.get('work_life_balance', 3.5)
            comparison['comparison_matrix']['job_satisfaction'][career_title] = career_data.get('job_satisfaction', 4.0)
        
        return comparison
    
    def _generate_industry_insights(self, top_careers: List, market_analysis: Dict) -> Dict[str, Any]:
        """Generate industry-specific insights for recommended careers"""
        industries = {}
        
        for career_title, score_data in top_careers:
            career_data = self.career_database[career_title]
            industry = career_data['industry']
            
            if industry not in industries:
                industries[industry] = {
                    'industry_name': industry,
                    'careers': [],
                    'total_opportunities': 0,
                    'average_growth_rate': 0,
                    'key_trends': []
                }
            
            industries[industry]['careers'].append({
                'title': career_title,
                'compatibility_score': score_data['score'],
                'growth_rate': career_data['growth_rate']
            })
        
        # Calculate industry metrics
        for industry, data in industries.items():
            data['total_opportunities'] = len(data['careers'])
            data['average_growth_rate'] = round(
                sum(career['growth_rate'] for career in data['careers']) / len(data['careers']), 1
            )
            
            # Add industry trends
            if industry == 'Technology':
                data['key_trends'] = [
                    'AI and Machine Learning integration',
                    'Remote work becoming standard',
                    'Cloud computing adoption',
                    'Cybersecurity focus'
                ]
            elif industry == 'Business':
                data['key_trends'] = [
                    'Data-driven decision making',
                    'Digital transformation',
                    'Agile methodologies',
                    'Customer experience focus'
                ]
            else:
                data['key_trends'] = ['Industry growth and innovation']
        
        return industries
    
    def _generate_skill_roadmap(self, top_careers: List, skill_analysis: Dict) -> Dict[str, Any]:
        """Generate skill development roadmap for recommended careers"""
        if not top_careers:
            return {'message': 'No career recommendations available'}
        
        # Collect all missing skills from top careers
        all_missing_skills = {}
        for career_title, score_data in top_careers:
            for skill in score_data['missing_skills']:
                if skill not in all_missing_skills:
                    all_missing_skills[skill] = []
                all_missing_skills[skill].append(career_title)
        
        # Prioritize skills by frequency across careers
        skill_priority = sorted(
            all_missing_skills.items(), 
            key=lambda x: len(x[1]), 
            reverse=True
        )
        
        roadmap = {
            'immediate_skills': [],  # 0-3 months
            'short_term_skills': [],  # 3-6 months
            'medium_term_skills': [],  # 6-12 months
            'long_term_skills': [],  # 12+ months
            'skill_development_plan': {}
        }
        
        # Categorize skills by development timeline
        for skill, careers_needing in skill_priority[:12]:  # Top 12 skills
            skill_info = {
                'skill': skill,
                'careers_needing': careers_needing,
                'priority': len(careers_needing),
                'estimated_time': self._estimate_skill_learning_time(skill),
                'learning_resources': self._get_skill_learning_resources(skill)
            }
            
            if len(careers_needing) >= 3:  # High priority
                roadmap['immediate_skills'].append(skill_info)
            elif len(careers_needing) == 2:  # Medium priority
                roadmap['short_term_skills'].append(skill_info)
            else:  # Lower priority
                roadmap['medium_term_skills'].append(skill_info)
        
        # Create development plan
        roadmap['skill_development_plan'] = {
            'phase_1': {
                'timeline': '0-3 months',
                'focus': 'Core skills for immediate opportunities',
                'skills': [s['skill'] for s in roadmap['immediate_skills'][:3]]
            },
            'phase_2': {
                'timeline': '3-6 months',
                'focus': 'Expanding skill set for better opportunities',
                'skills': [s['skill'] for s in roadmap['short_term_skills'][:3]]
            },
            'phase_3': {
                'timeline': '6-12 months',
                'focus': 'Advanced skills for senior roles',
                'skills': [s['skill'] for s in roadmap['medium_term_skills'][:3]]
            }
        }
        
        return roadmap
    
    def _assess_market_demand(self, career_title: str, career_data: Dict) -> Dict[str, Any]:
        """Assess market demand for a specific career"""
        growth_rate = career_data['growth_rate']
        
        if growth_rate >= 15:
            demand_level = 'Very High'
            market_outlook = 'Excellent growth prospects'
        elif growth_rate >= 10:
            demand_level = 'High'
            market_outlook = 'Strong growth prospects'
        elif growth_rate >= 5:
            demand_level = 'Medium'
            market_outlook = 'Stable growth prospects'
        else:
            demand_level = 'Low'
            market_outlook = 'Limited growth prospects'
        
        return {
            'demand_level': demand_level,
            'growth_rate': growth_rate,
            'market_outlook': market_outlook,
            'competition_level': 'High' if growth_rate >= 12 else 'Medium',
            'job_availability': 'High' if growth_rate >= 10 else 'Medium'
        }
    
    def _generate_learning_path(self, career_title: str, missing_skills: List[str]) -> Dict[str, Any]:
        """Generate learning path for a specific career"""
        career_data = self.career_database[career_title]
        
        return {
            'foundation_skills': missing_skills[:3],  # Top 3 missing skills
            'advanced_skills': missing_skills[3:6],  # Next 3 skills
            'certifications': career_data.get('certifications', [])[:2],  # Top 2 certifications
            'learning_timeline': '6-12 months for foundation, 12-18 months for advanced',
            'recommended_order': [
                'Start with foundation skills',
                'Build practical projects',
                'Earn relevant certifications',
                'Develop advanced skills',
                'Build portfolio and network'
            ]
        }
    
    def _estimate_skill_learning_time(self, skill: str) -> str:
        """Estimate time required to learn a skill"""
        time_estimates = {
            'Python Programming': '2-3 months',
            'Machine Learning': '4-6 months',
            'Data Analysis': '1-2 months',
            'JavaScript': '2-3 months',
            'SQL': '1-2 months',
            'Communication': '1-2 months',
            'Leadership': '3-6 months',
            'Project Management': '2-3 months',
            'Problem Solving': '2-3 months',
            'Critical Thinking': '2-4 months'
        }
        return time_estimates.get(skill, '2-3 months')
    
    def _get_skill_learning_resources(self, skill: str) -> List[str]:
        """Get learning resources for a specific skill"""
        resources = {
            'Python Programming': [
                'Python.org official tutorial',
                'Coursera Python for Everybody',
                'NPTEL Python Programming course'
            ],
            'Machine Learning': [
                'Andrew Ng\'s Machine Learning course',
                'NPTEL Machine Learning course',
                'Kaggle Learn modules'
            ],
            'Data Analysis': [
                'Google Data Analytics Certificate',
                'NPTEL Data Science course',
                'Pandas documentation'
            ],
            'Communication': [
                'LinkedIn Learning Communication courses',
                'Toastmasters International',
                'NPTEL Professional Communication'
            ]
        }
        return resources.get(skill, ['Online courses and tutorials', 'Practice projects', 'Professional development'])
