# CareerNexus - Vercel Deployment Script for Windows
# Run this with: .\deploy.ps1

Write-Host "`n🚀 CareerNexus - Vercel Deployment Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
} else {
    Write-Host "✓ Git repository already initialized" -ForegroundColor Green
}

# Add all files
Write-Host "📝 Adding files to Git..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "💾 Creating commit..." -ForegroundColor Yellow
git commit -m "Deploy CareerNexus to Vercel"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Nothing new to commit" -ForegroundColor Gray
}

# Check if Vercel CLI is installed
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "`n⚠️  Vercel CLI not found!" -ForegroundColor Red
    Write-Host "Install it with: npm install -g vercel`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n✅ Ready for deployment!`n" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: vercel login" -ForegroundColor White
Write-Host "2. Run: vercel" -ForegroundColor White
Write-Host "3. Follow the prompts" -ForegroundColor White
Write-Host "4. Set environment variables:" -ForegroundColor White
Write-Host "   vercel env add GEMINI_API_KEY" -ForegroundColor Gray
Write-Host "   vercel env add GEMINI_INTERVIEW_API_KEY" -ForegroundColor Gray
Write-Host "5. Run: vercel --prod`n" -ForegroundColor White

Write-Host "Or deploy via Vercel Dashboard:" -ForegroundColor Cyan
Write-Host "1. Go to https://vercel.com" -ForegroundColor White
Write-Host "2. Click 'Add New Project'" -ForegroundColor White
Write-Host "3. Import your Git repository" -ForegroundColor White
Write-Host "4. Add environment variables in settings" -ForegroundColor White
Write-Host "5. Deploy!`n" -ForegroundColor White

$deploy = Read-Host "Would you like to start deployment now? (y/n)"
if ($deploy -eq "y" -or $deploy -eq "Y") {
    Write-Host "`n🚀 Starting Vercel deployment...`n" -ForegroundColor Cyan
    vercel
}
