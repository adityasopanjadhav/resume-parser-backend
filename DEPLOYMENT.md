# Resume Parser Backend - Deployment Guide

## Quick Start for Local Development

### 1. Using Docker Compose (Recommended)
```bash
docker-compose up -d
```

This will:
- Create PostgreSQL database
- Build and run FastAPI backend
- Make API available at http://localhost:8000

### 2. Test the API
```bash
# Swagger UI
http://localhost:8000/docs

# Health check
http://localhost:8000/health
```

---

## Railway Deployment

### Prerequisites
- GitHub account
- Railway account (railway.app)
- Repository pushed to GitHub

### Deployment Steps

1. **Connect to Railway**
   - Go to railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Adjachav123/resume-parser`

2. **Create PostgreSQL Database**
   - In Railway project, click "+ Create"
   - Select "Database" → "PostgreSQL"
   - Wait for initialization

3. **Configure Environment Variables**
   - Click on backend service
   - Go to "Variables" tab
   - Add:
     - DATABASE_URL (copy from PostgreSQL service)
     - SECRET_KEY
     - ALGORITHM (HS256)
     - ACCESS_TOKEN_EXPIRE_MINUTES (30)

4. **Deploy**
   - Push code to GitHub
   - Railway auto-deploys
   - Wait 5-10 minutes for build

5. **Get Backend URL**
   - Find "Public URL" in backend service settings
   - Use this URL in frontend configuration

---

## Files Structure

- `Dockerfile` - Docker image configuration
- `.dockerignore` - Files to exclude from Docker build
- `docker-compose.yml` - Local development setup
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore rules
- `requirements.txt` - Python dependencies

---

## Environment Variables

See `.env.example` for all required variables.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - JWT secret key
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

---

## Testing

### Local Testing
```bash
# Run with docker-compose
docker-compose up

# Test health check
curl http://localhost:8000/health

# View API docs
http://localhost:8000/docs
```

### Production Testing
```bash
# Test your Railway URL
curl https://your-railway-url.railway.app/health
```

---

## Troubleshooting

### Build Issues
- Check `requirements.txt` syntax
- Verify all dependencies are available
- Check Dockerfile syntax

### Database Connection Issues
- Verify `DATABASE_URL` is correct
- Ensure PostgreSQL service is running
- Check environment variables are set

### Port Issues
- Local: Make sure port 8000 is not in use
- Railway: Uses assigned port automatically

---

## Next Steps

1. Update frontend API URL to your Railway backend URL
2. Configure CORS in `app/main.py`
3. Set up CI/CD pipeline (optional)
4. Configure custom domain (optional)
