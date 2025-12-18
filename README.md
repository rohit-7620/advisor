# AI-Powered Career Advisor

A comprehensive AI-driven career advisory system that helps students and professionals discover their ideal career paths through personalized skill analysis, market insights, and learning recommendations.

## Features

### 🧠 AI-Powered Analysis
- **Skill Mapping Engine**: Analyzes student skills and identifies strengths, gaps, and improvement areas
- **Job Market Analysis**: Provides real-time market trends and industry opportunities
- **Career Recommendations**: Suggests personalized career paths based on skills and interests

### 📚 Personalized Learning
- **Learning Plan Generator**: Creates customized learning paths with courses, certifications, and projects
- **Progress Tracking**: Monitors learning progress with milestones and metrics
- **Skill Development**: Recommends specific skills to develop for target careers

### 💼 Career Preparation
- **Resume Optimization**: Provides ATS-friendly resume templates and optimization tips
- **Interview Preparation**: Offers practice questions and preparation strategies
- **Portfolio Guidance**: Suggests projects to build a strong professional portfolio

## Architecture

The system follows the flowchart design with these key components:

1. **Student Inputs**: Skills, interests, educational background, experience
2. **AI Modules**:
   - Skill Mapping Engine
   - Job Market Analysis
   - Learning Plan Generator
3. **Career Path Recommendations**: Suitable career paths and multiple recommended roles
4. **End User**: Delivers personalized recommendations

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd personalized-career-advisor
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:5000`

## Usage

1. **Input Your Information**:
   - Select your skills from the available options
   - Choose your areas of interest
   - Provide your educational background and experience
   - Describe your career goals

2. **Get AI Analysis**:
   - The system analyzes your profile using AI modules
   - Skill mapping identifies your strengths and gaps
   - Market analysis provides industry insights

3. **Receive Recommendations**:
   - Get personalized career path recommendations
   - Access customized learning plans
   - Receive resume and interview preparation guidance

## API Endpoints

- `GET /` - Main application interface
- `POST /api/analyze` - Analyze student profile and get recommendations
- `GET /api/skills` - Get available skills from database
- `GET /api/industries` - Get available industries

## Database Schema

The system uses SQLite with the following tables:
- `skills`: Available skills with categories and descriptions
- `careers`: Career information with required skills and market data

## Modules

### Skill Mapping Engine (`modules/skill_mapping.py`)
- Analyzes student skills against available skill database
- Identifies skill gaps and strengths
- Recommends skills to develop

### Job Market Analysis (`modules/job_market_analysis.py`)
- Analyzes current job market trends
- Provides industry-specific insights
- Calculates opportunity scores

### Career Recommender (`modules/career_recommender.py`)
- Generates personalized career recommendations
- Calculates compatibility scores
- Suggests career progression paths

### Learning Plan Generator (`modules/learning_planner.py`)
- Creates personalized learning timelines
- Recommends courses and certifications
- Suggests portfolio projects

### Resume Preparation (`modules/resume_prep.py`)
- Provides resume templates and optimization tips
- Generates interview questions
- Offers networking guidance

## Customization

### Adding New Skills
1. Add skills to the database using the SQLite interface
2. Update the skill categories and descriptions
3. Modify the skill mapping logic if needed

### Adding New Careers
1. Insert career data into the `careers` table
2. Update the career recommendation logic
3. Add industry-specific templates

### Customizing Learning Plans
1. Modify the course database in `learning_planner.py`
2. Update certification recommendations
3. Add new project suggestions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue in the repository or contact the development team.

## Future Enhancements

- Integration with real job market APIs
- Machine learning model improvements
- Mobile application
- Advanced analytics dashboard
- Integration with learning platforms
- Real-time skill assessment
- Mentorship matching system

