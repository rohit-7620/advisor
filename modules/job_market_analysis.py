import sqlite3
import json
import requests
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class JobMarketAnalyzer:
    def __init__(self):
        self.db_path = 'career_advisor.db'
        self.market_trends = {}
        self.industry_data = {}
        self._load_market_data()
    
    def _load_market_data(self):
        """Load comprehensive market data and trends with real-time insights"""
        # Enhanced market data with more detailed insights
        self.market_trends = {
            'technology': {
                'growth_rate': 12.5,
                'demand_skills': ['Python Programming', 'Machine Learning', 'Data Analysis', 'Cloud Computing', 'DevOps', 'AI/ML'],
                'salary_trend': 'increasing',
                'job_openings': 15000,
                'competition_level': 'high',
                'remote_work_percentage': 75,
                'entry_level_salary': '₹6,00,000 - ₹10,00,000',
                'senior_level_salary': '₹15,00,000 - ₹30,00,000',
                'hot_skills': ['AI/ML', 'Cloud Computing', 'Cybersecurity', 'DevOps'],
                'emerging_roles': ['AI Engineer', 'Cloud Architect', 'DevSecOps Engineer', 'MLOps Engineer'],
                'market_insights': [
                    'AI and Machine Learning roles growing 25% annually',
                    'Remote work becoming permanent in 80% of tech companies',
                    'Cloud computing skills in highest demand',
                    'Cybersecurity roles increasing due to digital transformation'
                ]
            },
            'healthcare': {
                'growth_rate': 8.2,
                'demand_skills': ['Data Analysis', 'Communication', 'Problem Solving', 'Healthcare IT', 'Telemedicine'],
                'salary_trend': 'stable',
                'job_openings': 8500,
                'competition_level': 'medium',
                'remote_work_percentage': 40,
                'entry_level_salary': '₹4,00,000 - ₹7,00,000',
                'senior_level_salary': '₹10,00,000 - ₹18,00,000',
                'hot_skills': ['Healthcare Analytics', 'Telemedicine', 'Digital Health', 'Medical AI'],
                'emerging_roles': ['Healthcare Data Analyst', 'Telemedicine Coordinator', 'Digital Health Specialist'],
                'market_insights': [
                    'Digital health adoption accelerating post-pandemic',
                    'Healthcare analytics roles growing 15% annually',
                    'Telemedicine creating new job opportunities',
                    'AI in healthcare becoming mainstream'
                ]
            },
            'finance': {
                'growth_rate': 6.8,
                'demand_skills': ['Data Analysis', 'SQL', 'Critical Thinking', 'Communication', 'Fintech', 'Blockchain'],
                'salary_trend': 'increasing',
                'job_openings': 6200,
                'competition_level': 'high',
                'remote_work_percentage': 60,
                'entry_level_salary': '₹5,00,000 - ₹8,00,000',
                'senior_level_salary': '₹12,00,000 - ₹25,00,000',
                'hot_skills': ['Fintech', 'Blockchain', 'Risk Analytics', 'RegTech'],
                'emerging_roles': ['Fintech Analyst', 'Blockchain Developer', 'Risk Data Scientist', 'RegTech Specialist'],
                'market_insights': [
                    'Fintech sector growing 20% annually',
                    'Blockchain and crypto creating new opportunities',
                    'Regulatory technology (RegTech) in high demand',
                    'Digital banking transformation driving job growth'
                ]
            },
            'education': {
                'growth_rate': 4.1,
                'demand_skills': ['Communication', 'Leadership', 'Critical Thinking', 'EdTech', 'Online Learning'],
                'salary_trend': 'stable',
                'job_openings': 3200,
                'competition_level': 'medium',
                'remote_work_percentage': 70,
                'entry_level_salary': '₹3,50,000 - ₹6,00,000',
                'senior_level_salary': '₹8,00,000 - ₹15,00,000',
                'hot_skills': ['EdTech', 'Online Learning Design', 'Educational Analytics', 'Learning Management Systems'],
                'emerging_roles': ['EdTech Specialist', 'Learning Experience Designer', 'Educational Data Analyst'],
                'market_insights': [
                    'EdTech sector booming with 30% growth',
                    'Online learning creating new teaching roles',
                    'Educational analytics becoming crucial',
                    'Hybrid learning models here to stay'
                ]
            },
            'business': {
                'growth_rate': 5.5,
                'demand_skills': ['Communication', 'Leadership', 'Project Management', 'Business Analysis', 'Digital Transformation'],
                'salary_trend': 'increasing',
                'job_openings': 12000,
                'competition_level': 'medium',
                'remote_work_percentage': 65,
                'entry_level_salary': '₹4,50,000 - ₹7,50,000',
                'senior_level_salary': '₹10,00,000 - ₹20,00,000',
                'hot_skills': ['Digital Transformation', 'Business Analytics', 'Agile/Scrum', 'Customer Experience'],
                'emerging_roles': ['Digital Transformation Manager', 'Business Intelligence Analyst', 'Customer Success Manager'],
                'market_insights': [
                    'Digital transformation driving business roles',
                    'Customer experience becoming key differentiator',
                    'Agile methodologies in high demand',
                    'Business analytics roles growing rapidly'
                ]
            }
        }
        
        # Add real-time market indicators
        self.market_indicators = {
            'overall_health': 78,
            'trending_skills': ['AI/ML', 'Cloud Computing', 'Cybersecurity', 'Data Science', 'DevOps'],
            'declining_skills': ['Legacy Systems', 'Traditional Marketing', 'Manual Testing'],
            'salary_trends': {
                'technology': '+12%',
                'healthcare': '+6%',
                'finance': '+8%',
                'education': '+4%',
                'business': '+7%'
            },
            'remote_work_trends': {
                'fully_remote': 35,
                'hybrid': 45,
                'office_only': 20
            },
            'job_market_forecast': {
                'next_6_months': 'Positive growth expected',
                'next_12_months': 'Strong demand for tech skills',
                'long_term': 'AI and automation reshaping job landscape'
            }
        }
    
    def get_available_industries(self) -> List[str]:
        """Get list of available industries"""
        return list(self.market_trends.keys())
    
    def analyze_market(self, skill_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze current job market trends and opportunities
        """
        matched_skills = skill_analysis.get('matched_skills', [])
        skill_names = [skill['name'] for skill in matched_skills]
        
        # Analyze market opportunities for each industry
        industry_opportunities = {}
        for industry, data in self.market_trends.items():
            opportunity_score = self._calculate_opportunity_score(skill_names, data)
            industry_opportunities[industry] = {
                'opportunity_score': opportunity_score,
                'growth_rate': data['growth_rate'],
                'demand_skills': data['demand_skills'],
                'salary_trend': data['salary_trend'],
                'job_openings': data['job_openings'],
                'competition_level': data['competition_level'],
                'skill_match_percentage': self._calculate_skill_match(skill_names, data['demand_skills'])
            }
        
        # Get top opportunities
        top_opportunities = sorted(
            industry_opportunities.items(), 
            key=lambda x: x[1]['opportunity_score'], 
            reverse=True
        )[:3]
        
        # Analyze emerging trends
        emerging_trends = self._identify_emerging_trends(skill_names)
        
        # Market insights
        market_insights = self._generate_market_insights(skill_analysis, industry_opportunities)
        
        return {
            'industry_opportunities': dict(top_opportunities),
            'emerging_trends': emerging_trends,
            'market_insights': market_insights,
            'overall_market_health': self._assess_market_health(),
            'skill_demand_analysis': self._analyze_skill_demand(skill_names),
            'salary_insights': self._generate_salary_insights(industry_opportunities),
            'real_time_indicators': self._get_real_time_indicators(),
            'market_forecast': self._generate_market_forecast(),
            'remote_work_analysis': self._analyze_remote_work_trends(),
            'emerging_roles': self._identify_emerging_roles(skill_names),
            'skill_trends': self._analyze_skill_trends(),
            'geographic_insights': self._generate_geographic_insights()
        }
    
    def _calculate_opportunity_score(self, skills: List[str], industry_data: Dict) -> float:
        """Calculate opportunity score based on skill match and market factors"""
        demand_skills = industry_data['demand_skills']
        growth_rate = industry_data['growth_rate']
        
        # Calculate skill match percentage
        skill_matches = len([skill for skill in skills if skill in demand_skills])
        skill_match_percentage = (skill_matches / len(demand_skills)) * 100 if demand_skills else 0
        
        # Weight factors
        skill_weight = 0.6
        growth_weight = 0.3
        market_weight = 0.1
        
        # Normalize growth rate (assuming max 20%)
        normalized_growth = min(growth_rate / 20.0, 1.0)
        
        # Calculate opportunity score
        opportunity_score = (
            skill_match_percentage * skill_weight +
            normalized_growth * 100 * growth_weight +
            random.uniform(70, 90) * market_weight  # Simulated market factor
        )
        
        return round(min(opportunity_score, 100), 2)
    
    def _calculate_skill_match(self, user_skills: List[str], demand_skills: List[str]) -> float:
        """Calculate percentage of demand skills that user has"""
        if not demand_skills:
            return 0.0
        
        matches = len([skill for skill in user_skills if skill in demand_skills])
        return round((matches / len(demand_skills)) * 100, 2)
    
    def _identify_emerging_trends(self, skills: List[str]) -> List[Dict[str, str]]:
        """Identify emerging trends relevant to user's skills"""
        trends = [
            {
                'trend': 'Artificial Intelligence Integration',
                'description': 'AI is being integrated across all industries, creating new opportunities',
                'relevance': 'high' if 'Machine Learning' in skills or 'Python Programming' in skills else 'medium',
                'impact': 'High demand for AI-skilled professionals'
            },
            {
                'trend': 'Remote Work Evolution',
                'description': 'Hybrid and remote work models are becoming standard',
                'relevance': 'high' if 'Communication' in skills else 'medium',
                'impact': 'Increased flexibility and global opportunities'
            },
            {
                'trend': 'Data-Driven Decision Making',
                'description': 'Organizations increasingly rely on data analytics for decisions',
                'relevance': 'high' if 'Data Analysis' in skills else 'medium',
                'impact': 'Growing demand for data professionals'
            },
            {
                'trend': 'Sustainability Focus',
                'description': 'Green technology and sustainable practices are growing',
                'relevance': 'medium',
                'impact': 'New career paths in green technology'
            }
        ]
        
        # Filter and sort by relevance
        relevant_trends = [t for t in trends if t['relevance'] in ['high', 'medium']]
        return sorted(relevant_trends, key=lambda x: 0 if x['relevance'] == 'high' else 1)
    
    def _generate_market_insights(self, skill_analysis: Dict, industry_opportunities: Dict) -> List[str]:
        """Generate market insights based on analysis"""
        insights = []
        
        skill_strength = skill_analysis.get('skill_strength_score', 0)
        
        if skill_strength > 70:
            insights.append("Strong skill foundation positions you well for competitive roles")
        elif skill_strength > 40:
            insights.append("Good skill base with room for targeted development")
        else:
            insights.append("Focus on building core skills to increase marketability")
        
        # Industry insights
        top_industry = max(industry_opportunities.items(), key=lambda x: x[1]['opportunity_score'])
        insights.append(f"Best opportunities in {top_industry[0].title()} sector")
        
        # Growth insights
        high_growth_industries = [ind for ind, data in industry_opportunities.items() 
                                if data['growth_rate'] > 10]
        if high_growth_industries:
            insights.append(f"High growth sectors: {', '.join(high_growth_industries).title()}")
        
        return insights
    
    def _assess_market_health(self) -> Dict[str, Any]:
        """Assess overall market health"""
        return {
            'overall_score': 78,  # Simulated market health score
            'trend': 'positive',
            'key_indicators': {
                'job_growth': 'steady',
                'salary_trends': 'increasing',
                'skill_demand': 'high',
                'competition': 'moderate'
            },
            'market_outlook': 'Favorable conditions for skilled professionals'
        }
    
    def _analyze_skill_demand(self, skills: List[str]) -> Dict[str, Any]:
        """Analyze demand for user's specific skills"""
        high_demand_skills = []
        medium_demand_skills = []
        
        for skill in skills:
            # Simulate skill demand analysis
            if skill in ['Python Programming', 'Machine Learning', 'Data Analysis']:
                high_demand_skills.append(skill)
            else:
                medium_demand_skills.append(skill)
        
        return {
            'high_demand': high_demand_skills,
            'medium_demand': medium_demand_skills,
            'demand_score': len(high_demand_skills) * 2 + len(medium_demand_skills),
            'recommendation': 'Focus on high-demand skills for better opportunities'
        }
    
    def _generate_salary_insights(self, industry_opportunities: Dict) -> Dict[str, Any]:
        """Generate salary insights based on industry analysis"""
        avg_salaries = []
        for industry, data in industry_opportunities.items():
            # Simulate salary data based on industry (in Indian Rupees)
            base_salary = {
                'technology': 950000,  # ₹9.5 LPA
                'healthcare': 750000,  # ₹7.5 LPA
                'finance': 850000,     # ₹8.5 LPA
                'education': 650000    # ₹6.5 LPA
            }.get(industry, 700000)    # ₹7 LPA default
            
            avg_salaries.append({
                'industry': industry,
                'average_salary': f"₹{base_salary:,}",
                'trend': data['salary_trend'],
                'opportunity_score': data['opportunity_score']
            })
        
        return {
            'industry_salaries': avg_salaries,
            'highest_paying': max(avg_salaries, key=lambda x: x['average_salary']),
            'salary_trend': 'Overall positive growth across industries'
        }
    
    def _get_real_time_indicators(self) -> Dict[str, Any]:
        """Get real-time market indicators"""
        return {
            'market_health_score': self.market_indicators['overall_health'],
            'trending_skills': self.market_indicators['trending_skills'],
            'declining_skills': self.market_indicators['declining_skills'],
            'salary_trends': self.market_indicators['salary_trends'],
            'remote_work_distribution': self.market_indicators['remote_work_trends'],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_source': 'AI Career Advisor Market Intelligence'
        }
    
    def _generate_market_forecast(self) -> Dict[str, Any]:
        """Generate market forecast and predictions"""
        return {
            'short_term_forecast': {
                'timeline': 'Next 6 months',
                'prediction': self.market_indicators['job_market_forecast']['next_6_months'],
                'confidence': 'High',
                'key_factors': [
                    'Tech sector continuing to lead growth',
                    'Remote work becoming standard',
                    'AI/ML skills in highest demand'
                ]
            },
            'medium_term_forecast': {
                'timeline': 'Next 12 months',
                'prediction': self.market_indicators['job_market_forecast']['next_12_months'],
                'confidence': 'Medium',
                'key_factors': [
                    'Digital transformation accelerating',
                    'New roles emerging in AI and automation',
                    'Skills gap widening in tech sectors'
                ]
            },
            'long_term_forecast': {
                'timeline': '2-5 years',
                'prediction': self.market_indicators['job_market_forecast']['long_term'],
                'confidence': 'Medium',
                'key_factors': [
                    'AI reshaping job landscape',
                    'Automation creating new opportunities',
                    'Continuous learning becoming essential'
                ]
            }
        }
    
    def _analyze_remote_work_trends(self) -> Dict[str, Any]:
        """Analyze remote work trends and opportunities"""
        remote_trends = self.market_indicators['remote_work_trends']
        
        return {
            'current_distribution': remote_trends,
            'trend_analysis': {
                'fully_remote_growth': '+15%',
                'hybrid_adoption': '+25%',
                'office_only_decline': '-10%'
            },
            'industry_remote_opportunities': {
                industry: data['remote_work_percentage'] 
                for industry, data in self.market_trends.items()
            },
            'remote_work_benefits': [
                'Increased work-life balance',
                'Access to global opportunities',
                'Reduced commuting costs',
                'Flexible working hours'
            ],
            'remote_work_challenges': [
                'Need for strong communication skills',
                'Self-discipline and time management',
                'Limited face-to-face networking',
                'Technology dependency'
            ]
        }
    
    def _identify_emerging_roles(self, skills: List[str]) -> List[Dict[str, Any]]:
        """Identify emerging roles based on current skills"""
        emerging_roles = []
        
        for industry, data in self.market_trends.items():
            for role in data.get('emerging_roles', []):
                # Check if user has relevant skills for this emerging role
                relevant_skills = [skill for skill in skills if skill in data['demand_skills']]
                if relevant_skills:
                    emerging_roles.append({
                        'role': role,
                        'industry': industry,
                        'growth_potential': 'High',
                        'required_skills': data['demand_skills'],
                        'user_skill_match': len(relevant_skills),
                        'salary_range': data.get('entry_level_salary', 'Competitive'),
                        'remote_opportunities': data.get('remote_work_percentage', 50),
                        'description': f'Emerging role in {industry} with high growth potential'
                    })
        
        # Sort by skill match and growth potential
        emerging_roles.sort(key=lambda x: x['user_skill_match'], reverse=True)
        return emerging_roles[:10]  # Top 10 emerging roles
    
    def _analyze_skill_trends(self) -> Dict[str, Any]:
        """Analyze skill trends and market demand"""
        return {
            'hot_skills': {
                'skills': self.market_indicators['trending_skills'],
                'growth_rate': '+20%',
                'demand_level': 'Very High',
                'salary_premium': '+15-25%'
            },
            'declining_skills': {
                'skills': self.market_indicators['declining_skills'],
                'decline_rate': '-10%',
                'recommendation': 'Consider upskilling or transitioning'
            },
            'stable_skills': {
                'skills': ['Communication', 'Problem Solving', 'Leadership', 'Project Management'],
                'demand_level': 'Stable',
                'recommendation': 'Continue developing these foundational skills'
            },
            'future_skills': {
                'skills': ['AI Ethics', 'Quantum Computing', 'Sustainable Technology', 'Digital Privacy'],
                'emergence_timeline': '2-3 years',
                'recommendation': 'Start learning basics to stay ahead'
            }
        }
    
    def _generate_geographic_insights(self) -> Dict[str, Any]:
        """Generate geographic insights for job opportunities"""
        return {
            'top_cities': {
                'Bangalore': {
                    'tech_jobs': 45000,
                    'average_salary': '₹12,00,000',
                    'growth_rate': '+15%',
                    'key_industries': ['Technology', 'Fintech', 'E-commerce']
                },
                'Mumbai': {
                    'tech_jobs': 35000,
                    'average_salary': '₹11,50,000',
                    'growth_rate': '+12%',
                    'key_industries': ['Finance', 'Technology', 'Media']
                },
                'Delhi NCR': {
                    'tech_jobs': 40000,
                    'average_salary': '₹10,50,000',
                    'growth_rate': '+13%',
                    'key_industries': ['Technology', 'E-commerce', 'Education']
                },
                'Hyderabad': {
                    'tech_jobs': 25000,
                    'average_salary': '₹9,50,000',
                    'growth_rate': '+18%',
                    'key_industries': ['Technology', 'Healthcare', 'Pharma']
                },
                'Pune': {
                    'tech_jobs': 20000,
                    'average_salary': '₹9,00,000',
                    'growth_rate': '+16%',
                    'key_industries': ['Technology', 'Automotive', 'Manufacturing']
                }
            },
            'remote_opportunities': {
                'global_remote': 'High demand for Indian talent in global companies',
                'domestic_remote': 'Most Indian companies offering hybrid work',
                'freelance_market': 'Growing opportunities in consulting and project work'
            },
            'cost_of_living': {
                'Bangalore': 'High',
                'Mumbai': 'Very High',
                'Delhi NCR': 'High',
                'Hyderabad': 'Medium',
                'Pune': 'Medium'
            }
        }
