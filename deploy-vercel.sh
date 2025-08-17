#!/bin/bash

# Vercel Deployment Script for TDS Project2 Data Analysis API

echo "🚀 Starting Vercel deployment process..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if logged in to Vercel
echo "🔐 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "Please log in to Vercel..."
    vercel login
fi

# Validate required files
echo "📋 Validating project structure..."
required_files=("vercel.json" "api/index.py" "requirements-vercel.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done
echo "✅ All required files present"

# Check environment variables
echo "🔧 Checking environment variables..."
if [ -f ".env" ]; then
    echo "✅ .env file found"
    echo "📝 Make sure to set these environment variables in Vercel dashboard:"
    grep -E "^(AIPIPE_API_KEY|OPENAI_API_KEY|GEMINI_API_KEY)" .env || echo "   No API keys found in .env"
else
    echo "⚠️  No .env file found. Make sure to set environment variables in Vercel dashboard:"
    echo "   - AIPIPE_API_KEY (recommended)"
    echo "   - OPENAI_API_KEY (alternative)"
    echo "   - GEMINI_API_KEY (alternative)"
fi

# Test local dependencies
echo "🧪 Testing local dependencies..."
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
"

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Set environment variables in Vercel dashboard if not already done"
    echo "2. Test your deployment with the health endpoint: /health"
    echo "3. Try the main API endpoint: /api/ with a questions.txt file"
    echo ""
    echo "📚 Documentation: See README-vercel.md for usage examples"
    echo ""
else
    echo "❌ Deployment failed. Check the error messages above."
    echo "💡 Common solutions:"
    echo "   - Check vercel.json syntax"
    echo "   - Verify all dependencies in requirements-vercel.txt"
    echo "   - Ensure proper file structure with api/index.py"
    exit 1
fi
