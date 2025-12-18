# CareerNexus - Vercel Deployment

## 🚀 Quick Deploy to Vercel

### Prerequisites
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Git repository (GitHub, GitLab, or Bitbucket)
- Gemini API key

### Deployment Steps

#### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit for Vercel deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### 2. Deploy to Vercel

**Option A: Using Vercel Dashboard (Recommended)**
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: (leave empty)
   - **Output Directory**: `./`
5. Add Environment Variables:
   - `GEMINI_API_KEY`: Your Gemini API key
   - `GEMINI_INTERVIEW_API_KEY`: Your Gemini API key
6. Click "Deploy"

**Option B: Using Vercel CLI**
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Deploy to production
vercel --prod
```

#### 3. Set Environment Variables (CLI method)
```bash
vercel env add GEMINI_API_KEY
# Paste your API key when prompted

vercel env add GEMINI_INTERVIEW_API_KEY
# Paste your API key when prompted
```

#### 4. Access Your App
After deployment, Vercel will provide a URL like:
- `https://career-nexus.vercel.app`
- Custom domain can be configured in Vercel dashboard

### Project Structure for Vercel

```
career-nexus/
├── api/                    # Serverless functions
│   └── index.py           # Main API handler
├── modules/               # AI modules
│   ├── gemini_ai_engine.py
│   └── ...
├── templates/             # Original templates
├── index_gemini.html      # Main frontend (root)
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── .env                  # Local env vars (not deployed)
```

### How It Works

1. **Frontend**: `index_gemini.html` is served as static file
2. **Backend**: All `/api/*` routes are handled by Python serverless functions in `api/index.py`
3. **Environment**: API keys are securely stored in Vercel environment variables

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app locally
python app.py

# Test at http://localhost:5000
```

### Vercel Deployment Configuration

**vercel.json** handles:
- Python serverless function routing (`/api/*`)
- Static file serving (HTML, CSS, JS)
- Environment variable mapping
- CORS configuration

### Troubleshooting

**Issue**: API returns 500 errors
- Check Vercel function logs in dashboard
- Verify environment variables are set correctly
- Check Python dependencies in `requirements.txt`

**Issue**: Frontend loads but API calls fail
- Ensure `/api` routes are working (check Network tab in browser)
- Verify CORS is enabled in `api/index.py`
- Check that frontend is calling `/api/gemini/*` endpoints

**Issue**: Cold start delays
- Vercel serverless functions have ~1-2s cold start
- First request may be slower
- Consider upgrading to Vercel Pro for faster cold starts

### Performance Tips

1. **Optimize Python imports**: Only import what's needed in each function
2. **Use Vercel Edge Network**: Automatic with Vercel deployment
3. **Enable caching**: Add cache headers for static assets
4. **Monitor usage**: Check Vercel analytics dashboard

### Costs

- **Hobby Plan** (Free):
  - Unlimited deployments
  - 100GB bandwidth/month
  - Serverless function execution included
  - Good for personal projects

- **Pro Plan** ($20/month):
  - Faster builds
  - Advanced analytics
  - Team collaboration
  - Priority support

### Next Steps

1. ✅ Deploy to Vercel
2. 🔗 Add custom domain (optional)
3. 📊 Set up analytics
4. 🔒 Configure security headers
5. 🚀 Scale as needed

### Support

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Python on Vercel](https://vercel.com/docs/runtimes#official-runtimes/python)

---

**Built with ❤️ by CareerNexus Team**
