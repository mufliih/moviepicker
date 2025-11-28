# Deployment Guide

## Prerequisites

Since Git is not installed on your system, you have two options:

### Option 1: Install Git (Recommended)

1. Download Git from: https://git-scm.com/download/win
2. Install it with default settings
3. Restart your terminal
4. Follow the steps below

### Option 2: Use GitHub Desktop

1. Download GitHub Desktop from: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Use the GUI to create a repository and push your code

## Steps to Deploy (After Installing Git)

### 1. Initialize Git Repository

```bash
cd "c:\Users\LOQ\Documents\e commerce"
git init
git add .
git commit -m "Initial commit: Movie Picker app with language search"
```

### 2. Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "movie-picker")
3. Don't initialize with README (we already have one)

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/movie-picker.git
git branch -M main
git push -u origin main
```

### 4. Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
npm install -g vercel
vercel login
vercel
```

#### Option B: Using Vercel Dashboard (Easier)
1. Go to https://vercel.com/
2. Sign in with GitHub
3. Click "Add New Project"
4. Import your GitHub repository
5. Vercel will auto-detect the Flask app
6. Click "Deploy"

## Important Notes

- The `vercel.json` file is already configured for Flask
- The `.gitignore` file will exclude sensitive files
- Make sure your `.env` file (if any) is NOT pushed to GitHub
- Vercel will automatically install dependencies from `requirements.txt`

## Troubleshooting

If deployment fails on Vercel:
1. Check the build logs
2. Ensure all dependencies are in `requirements.txt`
3. Verify `vercel.json` is in the root directory
4. Make sure `app.py` is in the root directory
