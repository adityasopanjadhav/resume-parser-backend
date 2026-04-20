@echo off
REM Railway Deployment Script for Windows
REM Usage: deploy.bat

echo Starting Railway Deployment...

REM Check if git is initialized
if not exist ".git" (
    echo Git not initialized. Run 'git init' first.
    exit /b 1
)

REM Check if files exist
echo Checking deployment files...
if not exist "Dockerfile" (
    echo ERROR: Dockerfile not found
    exit /b 1
)

if not exist ".env.example" (
    echo ERROR: .env.example not found
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo WARNING: Update .env with your actual values
)

REM Add files to git
echo Adding files to git...
git add Dockerfile .dockerignore docker-compose.yml .env.example DEPLOYMENT.md .gitignore

REM Commit
echo Committing changes...
git commit -m "Add Docker and deployment configuration"

REM Push to GitHub
echo Pushing to GitHub...
git push origin main

echo.
echo Deployment files created and pushed!
echo.
echo Next steps:
echo 1. Go to railway.app
echo 2. Create new project from GitHub
echo 3. Select this repository
echo 4. Add PostgreSQL database
echo 5. Configure environment variables
echo 6. Deploy!
