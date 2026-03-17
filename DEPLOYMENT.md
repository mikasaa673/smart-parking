# 🚀 Deployment Guide

## 📋 Deployment Options

### 1. **Render.com** (Recommended)
1. Push code to GitHub
2. Connect GitHub repo to Render
3. Render will auto-detect from `render.yaml`
4. App will be available at `https://your-app.onrender.com`

### 2. **Vercel**
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel --prod`
3. Use `requirements-vercel.txt` for dependencies
4. Deploy at `https://your-app.vercel.app`

### 3. **Heroku**
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Push: `git push heroku main`
4. Uses `Procfile` and `runtime.txt`

### 4. **PythonAnywhere**
1. Upload files via web interface
2. Create virtual environment
3. Install: `pip install -r requirements.txt`
4. Configure WSGI to run `app.py`

## 🔧 Environment Variables
Set these on your platform:
- `DB_HOST=localhost`
- `DB_USER=root`
- `DB_PASSWORD=your_password`
- `DB_NAME=smart_parking`
- `PORT=5000` (or platform-specific)

## 📝 Notes
- App works in demo mode without MySQL
- Video files are excluded from git (.gitignore)
- OpenCV dependencies may need platform-specific setup
