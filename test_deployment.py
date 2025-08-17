#!/usr/bin/env python3
"""
Local testing script for Vercel deployment
Tests the API functionality before deploying to Vercel
"""

import requests
import json
import os
import tempfile
import time
from typing import Dict, Any

def create_test_questions_file() -> str:
    """Create a temporary questions.txt file for testing"""
    content = """Analyze the GDP data from https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)

Questions to answer:
1. Which country has the highest GDP?
2. What are the top 10 countries by GDP?
3. What is the total GDP of the top 5 countries?
4. Create a visualization showing GDP comparison of top 10 countries
5. Which countries have GDP over $5 trillion?"""
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

def test_health_endpoint(base_url: str) -> Dict[str, Any]:
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=30)
        response.raise_for_status()
        result = response.json()
        print("✅ Health check passed")
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return {"status": "error", "error": str(e)}

def test_capabilities_endpoint(base_url: str) -> Dict[str, Any]:
    """Test the workflow capabilities endpoint"""
    print("⚙️ Testing capabilities endpoint...")
    try:
        response = requests.get(f"{base_url}/api/workflow-capabilities", timeout=30)
        response.raise_for_status()
        result = response.json()
        print("✅ Capabilities check passed")
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"❌ Capabilities check failed: {e}")
        return {"status": "error", "error": str(e)}

def test_main_api_endpoint(base_url: str) -> Dict[str, Any]:
    """Test the main API endpoint with file upload"""
    print("🔍 Testing main API endpoint...")
    
    # Create test questions file
    questions_file_path = create_test_questions_file()
    
    try:
        with open(questions_file_path, 'rb') as questions_file:
            files = {
                'questions_txt': ('questions.txt', questions_file, 'text/plain')
            }
            data = {
                'enable_iterative_reasoning': 'false',
                'enable_logging': 'true'
            }
            
            print("📤 Uploading test data...")
            response = requests.post(
                f"{base_url}/api/",
                files=files,
                data=data,
                timeout=300  # 5 minutes timeout
            )
            
            response.raise_for_status()
            result = response.json()
            print("✅ Main API test passed")
            return {"status": "success", "data": result}
            
    except Exception as e:
        print(f"❌ Main API test failed: {e}")
        return {"status": "error", "error": str(e)}
    finally:
        # Clean up temporary file
        try:
            os.unlink(questions_file_path)
        except:
            pass

def test_local_server():
    """Test the local development server"""
    base_url = "http://localhost:8000"
    print(f"🧪 Testing local server at {base_url}")
    
    print("\n" + "="*50)
    print("LOCAL SERVER TESTS")
    print("="*50)
    
    # Test health
    health_result = test_health_endpoint(base_url)
    print(f"Health: {health_result['status']}")
    if health_result['status'] == 'success':
        print(f"  Orchestrator: {health_result['data'].get('orchestrator', 'unknown')}")
        print(f"  Workflows: {health_result['data'].get('workflows_available', 0)}")
    
    # Test capabilities
    cap_result = test_capabilities_endpoint(base_url)
    print(f"Capabilities: {cap_result['status']}")
    if cap_result['status'] == 'success':
        workflows = cap_result['data'].get('available_workflows', [])
        print(f"  Available workflows: {len(workflows)}")
        for workflow in workflows:
            print(f"    - {workflow}")
    
    # Test main API
    api_result = test_main_api_endpoint(base_url)
    print(f"Main API: {api_result['status']}")
    if api_result['status'] == 'success':
        task_id = api_result['data'].get('task_id', 'unknown')
        workflow_type = api_result['data'].get('workflow_type', 'unknown')
        status = api_result['data'].get('status', 'unknown')
        print(f"  Task ID: {task_id}")
        print(f"  Workflow: {workflow_type}")
        print(f"  Status: {status}")
        
        # Check if we have results
        result = api_result['data'].get('result', {})
        if result:
            print(f"  Result keys: {list(result.keys())}")
            if 'results' in result:
                print(f"  Analysis results available: {bool(result['results'])}")
            if 'plot_base64' in result:
                print(f"  Visualization generated: {bool(result['plot_base64'])}")
    
    return {
        "health": health_result,
        "capabilities": cap_result,
        "main_api": api_result
    }

def test_vercel_deployment(vercel_url: str):
    """Test a Vercel deployment"""
    print(f"🚀 Testing Vercel deployment at {vercel_url}")
    
    print("\n" + "="*50)
    print("VERCEL DEPLOYMENT TESTS")
    print("="*50)
    
    # Test health
    health_result = test_health_endpoint(vercel_url)
    print(f"Health: {health_result['status']}")
    if health_result['status'] == 'success':
        print(f"  Platform: {health_result['data'].get('platform', 'unknown')}")
        print(f"  Orchestrator: {health_result['data'].get('orchestrator', 'unknown')}")
        print(f"  Workflows: {health_result['data'].get('workflows_available', 0)}")
    
    # Test capabilities
    cap_result = test_capabilities_endpoint(vercel_url)
    print(f"Capabilities: {cap_result['status']}")
    if cap_result['status'] == 'success':
        workflows = cap_result['data'].get('available_workflows', [])
        print(f"  Available workflows: {len(workflows)}")
        platform = cap_result['data'].get('platform', 'unknown')
        print(f"  Platform: {platform}")
    
    # Test main API (this might take longer on cold start)
    print("⏳ Testing main API (may take longer on cold start)...")
    start_time = time.time()
    api_result = test_main_api_endpoint(vercel_url)
    duration = time.time() - start_time
    
    print(f"Main API: {api_result['status']} (took {duration:.1f}s)")
    if api_result['status'] == 'success':
        task_id = api_result['data'].get('task_id', 'unknown')
        workflow_type = api_result['data'].get('workflow_type', 'unknown')
        status = api_result['data'].get('status', 'unknown')
        print(f"  Task ID: {task_id}")
        print(f"  Workflow: {workflow_type}")
        print(f"  Status: {status}")
        
        # Check processing info
        proc_info = api_result['data'].get('processing_info', {})
        if proc_info:
            platform = proc_info.get('platform', 'unknown')
            print(f"  Platform: {platform}")
            features = proc_info.get('enhanced_features', [])
            print(f"  Features: {', '.join(features)}")
    
    return {
        "health": health_result,
        "capabilities": cap_result,
        "main_api": api_result,
        "duration": duration
    }

def main():
    """Main testing function"""
    print("🧪 API Testing Suite for TDS Project2")
    print("="*50)
    
    import argparse
    parser = argparse.ArgumentParser(description='Test the API deployment')
    parser.add_argument('--local', action='store_true', help='Test local server')
    parser.add_argument('--vercel', type=str, help='Test Vercel deployment URL')
    parser.add_argument('--both', action='store_true', help='Test both local and example Vercel URL')
    
    args = parser.parse_args()
    
    results = {}
    
    if args.local or args.both:
        print("\n🏠 Starting local server tests...")
        print("Make sure your local server is running with:")
        print("  uvicorn api.index:app --reload")
        print("")
        input("Press Enter when server is ready...")
        results['local'] = test_local_server()
    
    if args.vercel:
        print(f"\n🚀 Starting Vercel deployment tests...")
        results['vercel'] = test_vercel_deployment(args.vercel)
    
    if args.both:
        print(f"\n🚀 Starting example Vercel deployment tests...")
        example_url = "https://your-project-name.vercel.app"
        print(f"Testing example URL: {example_url}")
        print("(This will fail unless you update the URL)")
        results['vercel'] = test_vercel_deployment(example_url)
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    for env, env_results in results.items():
        print(f"\n{env.upper()} Environment:")
        for test_name, test_result in env_results.items():
            if test_name == 'duration':
                continue
            status = test_result['status']
            emoji = "✅" if status == 'success' else "❌"
            print(f"  {emoji} {test_name}: {status}")
            if status == 'error':
                print(f"    Error: {test_result.get('error', 'Unknown')}")
    
    print("\n📋 Next steps:")
    if 'local' in results and all(r['status'] == 'success' for r in results['local'].values() if isinstance(r, dict)):
        print("✅ Local tests passed - ready for Vercel deployment")
        print("   Run: deploy-vercel.bat (Windows) or deploy-vercel.sh (Linux/Mac)")
    else:
        print("❌ Local tests failed - fix issues before deploying")
        print("   Check dependencies: pip install -r requirements-vercel.txt")
        print("   Check server: uvicorn api.index:app --reload")
    
    if 'vercel' in results:
        vercel_success = all(r['status'] == 'success' for r in results['vercel'].values() if isinstance(r, dict))
        if vercel_success:
            print("✅ Vercel deployment working correctly")
            duration = results['vercel'].get('duration', 0)
            if duration > 10:
                print(f"⏳ Cold start took {duration:.1f}s - this is normal for first request")
        else:
            print("❌ Vercel deployment has issues")
            print("   Check environment variables in Vercel dashboard")
            print("   Check deployment logs in Vercel")

if __name__ == "__main__":
    main()
