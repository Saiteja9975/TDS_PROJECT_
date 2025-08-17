#!/usr/bin/env python3
"""
Simple validation script for Vercel deployment files
"""

import os
import json

def validate_vercel_files():
    """Validate that all required Vercel deployment files exist and are properly formatted"""
    
    print("🔍 Validating Vercel deployment files...")
    
    required_files = {
        'vercel.json': 'Vercel configuration',
        'api/index.py': 'Main FastAPI serverless function', 
        'requirements-vercel.txt': 'Python dependencies for Vercel',
        'README-vercel.md': 'Deployment documentation',
        'test-vercel.html': 'Web testing interface',
        'example-questions.txt': 'Example questions file'
    }
    
    missing_files = []
    
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - {description} (MISSING)")
            missing_files.append(file_path)
    
    # Validate vercel.json syntax
    try:
        with open('vercel.json', 'r') as f:
            config = json.load(f)
        print("✅ vercel.json - Valid JSON syntax")
        
        # Check required fields
        if 'builds' in config and 'routes' in config:
            print("✅ vercel.json - Has required builds and routes")
        else:
            print("❌ vercel.json - Missing builds or routes configuration")
            
    except FileNotFoundError:
        print("❌ vercel.json - File not found")
    except json.JSONDecodeError as e:
        print(f"❌ vercel.json - Invalid JSON: {e}")
    
    # Check api/index.py imports
    try:
        with open('api/index.py', 'r') as f:
            content = f.read()
        
        required_imports = ['FastAPI', 'UploadFile', 'File', 'HTTPException']
        missing_imports = []
        
        for imp in required_imports:
            if imp in content:
                print(f"✅ api/index.py - Has {imp} import")
            else:
                print(f"❌ api/index.py - Missing {imp} import")
                missing_imports.append(imp)
                
    except FileNotFoundError:
        print("❌ api/index.py - File not found")
    
    # Summary
    print("\n" + "="*50)
    print("VALIDATION SUMMARY")
    print("="*50)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        print("\n📋 Ready for Vercel deployment!")
        print("\nNext steps:")
        print("1. Install Vercel CLI: npm install -g vercel")
        print("2. Login to Vercel: vercel login")
        print("3. Deploy: vercel --prod")
        print("4. Set environment variables in Vercel dashboard:")
        print("   - AIPIPE_API_KEY (recommended)")
        print("   - OPENAI_API_KEY (alternative)")
        print("5. Test deployment with test-vercel.html")
        return True

if __name__ == "__main__":
    validate_vercel_files()
