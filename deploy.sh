#!/bin/bash

# CareerNexus - Quick Deploy Script for Vercel

echo "🚀 CareerNexus - Vercel Deployment Setup"
echo "========================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
else
    echo "✓ Git repository already initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
.venv/
__pycache__/
*.pyc
.env
.env.local
*.db
*.sqlite
uploads/*
downloads/*
!uploads/.gitkeep
!downloads/.gitkeep
.vercel
EOF
fi

# Add all files
echo "📝 Adding files to Git..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Deploy CareerNexus to Vercel" || echo "Nothing to commit"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo ""
    echo "⚠️  Vercel CLI not found. Install it with:"
    echo "   npm install -g vercel"
    echo ""
    exit 1
fi

echo ""
echo "✅ Ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Run: vercel login"
echo "2. Run: vercel"
echo "3. Follow the prompts"
echo "4. Set environment variables:"
echo "   vercel env add GEMINI_API_KEY"
echo "   vercel env add GEMINI_INTERVIEW_API_KEY"
echo "5. Run: vercel --prod"
echo ""
echo "Or deploy via Vercel Dashboard:"
echo "1. Go to https://vercel.com"
echo "2. Import your Git repository"
echo "3. Add environment variables in settings"
echo "4. Deploy!"
echo ""
