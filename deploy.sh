#!/bin/bash

# Railway Deployment Script
# Usage: ./deploy.sh

echo "Starting Railway Deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Git not initialized. Run 'git init' first."
    exit 1
fi

# Check if files exist
echo "Checking deployment files..."
if [ ! -f "Dockerfile" ]; then
    echo "ERROR: Dockerfile not found"
    exit 1
fi

if [ ! -f ".env.example" ]; then
    echo "ERROR: .env.example not found"
    exit 1
fi

# Check if .env exists (for local testing)
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Update .env with your actual values"
fi

# Add files to git
echo "Adding files to git..."
git add Dockerfile .dockerignore docker-compose.yml .env.example DEPLOYMENT.md .gitignore

# Commit
echo "Committing changes..."
git commit -m "Add Docker and deployment configuration"

# Push to GitHub
echo "Pushing to GitHub..."
git push origin main

echo "✅ Deployment files created and pushed!"
echo ""
echo "Next steps:"
echo "1. Go to railway.app"
echo "2. Create new project from GitHub"
echo "3. Select this repository"
echo "4. Add PostgreSQL database"
echo "5. Configure environment variables"
echo "6. Deploy!"
