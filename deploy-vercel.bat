@echo off
REM Vercel Deployment Script for Windows - TDS Project2 Data Analysis API

echo 🚀 Starting Vercel deployment process...

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found. Please install Node.js first.
    echo Download from: https://nodejs.org/
    exit /b 1
)

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Vercel CLI not found. Installing...
    npm install -g vercel
)

REM Check if logged in to Vercel
echo 🔐 Checking Vercel authentication...
vercel whoami >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Please log in to Vercel...
    vercel login
)

REM Validate required files
echo 📋 Validating project structure...
if not exist "vercel.json" (
    echo ❌ Missing required file: vercel.json
    exit /b 1
)
if not exist "api\index.py" (
    echo ❌ Missing required file: api\index.py
    exit /b 1
)
if not exist "requirements-vercel.txt" (
    echo ❌ Missing required file: requirements-vercel.txt
    exit /b 1
)
echo ✅ All required files present

REM Check environment variables
echo 🔧 Checking environment variables...
if exist ".env" (
    echo ✅ .env file found
    echo 📝 Make sure to set these environment variables in Vercel dashboard:
    findstr "^AIPIPE_API_KEY\|^OPENAI_API_KEY\|^GEMINI_API_KEY" .env 2>nul || echo    No API keys found in .env
) else (
    echo ⚠️  No .env file found. Make sure to set environment variables in Vercel dashboard:
    echo    - AIPIPE_API_KEY ^(recommended^)
    echo    - OPENAI_API_KEY ^(alternative^)
    echo    - GEMINI_API_KEY ^(alternative^)
)

REM Test Python dependencies
echo 🧪 Testing Python dependencies...
python -c "
import sys
try:
    import fastapi
    import pandas
    import requests
    print('✅ Core dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Please run: pip install -r requirements-vercel.txt')
    sys.exit(1)
" || (
    echo ❌ Dependency check failed
    echo Please run: pip install -r requirements-vercel.txt
    exit /b 1
)

REM Deploy to Vercel
echo 🚀 Deploying to Vercel...
vercel --prod

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 🎉 Deployment completed successfully!
    echo.
    echo 📋 Next steps:
    echo 1. Set environment variables in Vercel dashboard if not already done
    echo 2. Test your deployment with the health endpoint: /health
    echo 3. Try the main API endpoint: /api/ with a questions.txt file
    echo.
    echo 📚 Documentation: See README-vercel.md for usage examples
    echo.
) else (
    echo ❌ Deployment failed. Check the error messages above.
    echo 💡 Common solutions:
    echo    - Check vercel.json syntax
    echo    - Verify all dependencies in requirements-vercel.txt
    echo    - Ensure proper file structure with api\index.py
    exit /b 1
)
