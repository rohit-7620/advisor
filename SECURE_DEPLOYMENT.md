# 🔒 SECURE DEPLOYMENT GUIDE - CareerNexus AI

## ⚠️ IMPORTANT SECURITY NOTICE

**NEVER commit API keys or secrets to Git!** This guide shows you how to deploy securely.

---

## 📋 Pre-Deployment Checklist

- [ ] Get Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Create Vercel account at https://vercel.com
- [ ] Create GitHub repository (can be public or private)
- [ ] Install Git on your system

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### Step 1: Get Your API Key

1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)
4. **Keep it safe - don't share it publicly!**

---

### Step 2: Push Code to GitHub

```powershell
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - CareerNexus AI"

# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

---

### Step 3: Deploy to Vercel

#### Method A: Vercel Dashboard (Recommended)

1. **Go to Vercel:**
   - Visit https://vercel.com/new
   - Sign in with GitHub

2. **Import Repository:**
   - Click "Import Project"
   - Select your repository (e.g., `YOUR_USERNAME/YOUR_REPO_NAME`)
   - Click "Import"

3. **Configure Project:**
   - **Framework Preset:** Other
   - **Root Directory:** `./` (keep default)
   - **Build Command:** (leave empty)
   - **Output Directory:** `./` (keep default)

4. **Add Environment Variables:**
   Click "Environment Variables" and add:
   
   | Name | Value |
   |------|-------|
   | `GEMINI_API_KEY` | Your API key from Step 1 |
   | `GEMINI_INTERVIEW_API_KEY` | Same API key from Step 1 |

5. **Deploy:**
   - Click "Deploy" button
   - Wait 2-3 minutes for deployment
   - Your app will be live at `https://your-app-name.vercel.app`

---

#### Method B: Vercel CLI (Advanced)

```powershell
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy to preview
vercel

# Add environment variables
vercel env add GEMINI_API_KEY
# Paste your API key when prompted

vercel env add GEMINI_INTERVIEW_API_KEY
# Paste your API key when prompted

# Deploy to production
vercel --prod
```

---

## ✅ What We've Secured

- ✅ API keys removed from all documentation files
- ✅ `.env.example` template created (no real secrets)
- ✅ `.gitignore` configured to exclude `.env` file
- ✅ Git history cleaned (old commits with exposed keys removed)
- ✅ Environment variables handled securely via Vercel dashboard

---

## 🎯 After Deployment

### Test Your Deployment

1. Visit your Vercel URL
2. Test each AI feature:
   - ATS Resume Analyzer
   - Cover Letter Generator
   - LinkedIn Profile Optimizer
   - AI Mock Interview
   - Career Trajectory Planner
   - Skill Gap Analysis
   - Salary Negotiation Coach
   - Job Description Analyzer
   - Personalized Learning Path
   - Resume Analyzer

---

## 🔧 Troubleshooting

### Issue: "API Key Error" or "500 Internal Server Error"

**Solution:** Check environment variables in Vercel
1. Go to your project on Vercel dashboard
2. Click "Settings" > "Environment Variables"
3. Verify both `GEMINI_API_KEY` and `GEMINI_INTERVIEW_API_KEY` are set
4. Redeploy: Go to "Deployments" > Click "..." > "Redeploy"

### Issue: "Failed to fetch" when importing GitHub repo

**Solution:** Make repository public
1. Go to your GitHub repo settings
2. Scroll to "Danger Zone"
3. Click "Change visibility" > "Make public"
4. Retry importing on Vercel

### Issue: Frontend loads but features don't work

**Solution:** Check API routes
1. Open browser Developer Tools (F12)
2. Go to "Network" tab
3. Try a feature and check for failed API calls
4. If you see CORS errors, verify `api/index.py` has proper CORS headers

---

## 📊 Monitoring & Maintenance

### Check Logs
1. Go to Vercel dashboard
2. Select your project
3. Click "Logs" to see function execution logs

### Update API Key
If you need to change your API key:
1. Go to Vercel project settings
2. Environment Variables
3. Edit the variable
4. Redeploy the project

---

## 💡 Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` for safety
2. **Use environment variables** - Always use Vercel dashboard for secrets
3. **Regenerate compromised keys** - If your API key is exposed, create a new one immediately
4. **Monitor usage** - Check Gemini API usage regularly
5. **Set up alerts** - Use Vercel monitoring for production issues

---

## 🎉 Success!

Your CareerNexus AI application is now:
- ✅ Deployed securely on Vercel
- ✅ API keys protected (not in code)
- ✅ Accessible worldwide
- ✅ Auto-scaling and fast
- ✅ Free to use (on Vercel Hobby plan)

---

## 📞 Need Help?

- **Vercel Docs:** https://vercel.com/docs
- **Gemini API Docs:** https://ai.google.dev/docs
- **Project Issues:** Create an issue on your GitHub repo

---

## 🔗 Useful Links

- **Get Gemini API Key:** https://makersuite.google.com/app/apikey
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Vercel Documentation:** https://vercel.com/docs
- **Deploy New Project:** https://vercel.com/new
