# Vercel Deployment for TDS Project2 Data Analysis API

## Overview
This is a multi-modal data analysis API built with FastAPI and optimized for deployment on Vercel's serverless platform.

## Features
- **Web Scraping**: Generic table extraction and analysis from any website
- **Data Analysis**: Automated data cleaning, analysis, and visualization
- **Multi-format Support**: Handles CSV, JSON, images, and text files
- **LLM Integration**: Uses AIpipe/OpenAI for intelligent workflow detection
- **Serverless Ready**: Optimized for Vercel's serverless environment

## Live Demo
Once deployed, your API will be available at: `https://your-project-name.vercel.app`

## API Endpoints

### Health Check
```
GET /health
```

### Main Analysis Endpoint
```
POST /api/
```
**Parameters:**
- `questions_txt`: Required file containing analysis questions
- `files`: Optional additional files (CSV, images, etc.)
- `enable_iterative_reasoning`: Boolean for enhanced analysis
- `enable_logging`: Boolean for detailed logging

### Workflow Capabilities
```
GET /api/workflow-capabilities
```

## Example Usage

### Using curl
```bash
curl -X POST "https://your-project-name.vercel.app/api/" \
  -F "questions_txt=@questions.txt" \
  -F "files=@data.csv"
```

### Using Python requests
```python
import requests

url = "https://your-project-name.vercel.app/api/"
files = {
    'questions_txt': ('questions.txt', open('questions.txt', 'rb')),
    'files': ('data.csv', open('data.csv', 'rb'))
}

response = requests.post(url, files=files)
result = response.json()
print(result)
```

### Sample Questions File
Create a `questions.txt` file with content like:
```
Analyze the GDP data from https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)
1. Which country has the highest GDP?
2. What are the top 10 countries by GDP?
3. Create a visualization showing GDP comparison
```

## Environment Variables

### Required for AIpipe (Recommended)
```
AIPIPE_API_KEY=your_aipipe_token
AIPIPE_BASE_URL=https://aipipe.org/openai/v1
```

### Alternative: OpenAI
```
OPENAI_API_KEY=your_openai_api_key
```

### Alternative: Gemini
```
GEMINI_API_KEY=your_gemini_api_key
```

## Deployment Steps

### 1. Local Testing
```bash
# Install dependencies
pip install -r requirements-vercel.txt

# Test locally
uvicorn api.index:app --reload
```

### 2. Deploy to Vercel

#### Option A: Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

#### Option B: GitHub Integration
1. Push your code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy automatically

### 3. Configure Environment Variables
In your Vercel dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add your API keys:
   - `AIPIPE_API_KEY`
   - `AIPIPE_BASE_URL`

## Project Structure
```
Project2/
├── api/
│   └── index.py          # Vercel serverless function
├── chains/               # Analysis workflows
├── utils/                # Utility functions
├── vercel.json          # Vercel configuration
├── requirements-vercel.txt  # Simplified dependencies
└── README-vercel.md     # This file
```

## Key Differences from Docker Version

### Optimizations for Serverless
- **Cold Start Optimization**: Lazy loading of heavy dependencies
- **Memory Efficiency**: Reduced dependency set
- **Timeout Management**: 5-minute function timeout
- **Stateless Design**: No persistent storage dependencies

### Simplified Dependencies
Removed heavy dependencies for serverless:
- ❌ duckdb (database engine)
- ❌ faiss-cpu (vector search)
- ❌ chromadb (vector database)
- ❌ pytesseract (OCR)
- ❌ pillow (image processing)
- ✅ Core ML and data analysis libraries retained

### Fallback Mechanisms
- Graceful degradation when advanced features unavailable
- Minimal orchestrator for core web scraping functionality
- Error handling for missing dependencies

## Supported Workflows

### Primary Workflows (Always Available)
1. **Web Scraping**: Extract and analyze data from any website
2. **Data Analysis**: Process uploaded CSV/JSON files
3. **Question Answering**: Generate insights from data

### Advanced Workflows (When LLM Available)
1. **Image Analysis**: Computer vision tasks
2. **Text Analysis**: NLP and text processing
3. **Code Generation**: Executable Python code
4. **Statistical Analysis**: Correlation and regression
5. **Predictive Modeling**: ML model recommendations
6. **Data Visualization**: Chart generation with base64 encoding

## Performance Considerations

### Cold Starts
- First request may take 10-15 seconds
- Subsequent requests are faster (~2-5 seconds)
- Use keep-alive requests for better performance

### Memory Limits
- Vercel Pro: 1GB RAM limit
- Optimize for large datasets by chunking
- Use streaming for file processing

### Timeout Limits
- Vercel: 300 seconds maximum execution time
- Complex analysis tasks automatically optimized
- Progress indicators for long-running tasks

## Troubleshooting

### Common Issues

#### 1. "Module not found" errors
- Check `requirements-vercel.txt` includes all dependencies
- Verify import paths in `api/index.py`

#### 2. Cold start timeouts
- Increase Vercel function timeout in `vercel.json`
- Optimize import statements for lazy loading

#### 3. API key errors
- Verify environment variables in Vercel dashboard
- Check variable names match exactly
- Ensure quotes are not included in values

#### 4. File upload issues
- Check file size limits (32MB max for Vercel)
- Verify multipart form encoding
- Use proper field names in requests

### Debug Mode
Add debug logging by setting environment variable:
```
DEBUG=true
```

### Health Check
Monitor your deployment:
```bash
curl https://your-project-name.vercel.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-13T...",
  "orchestrator": "available",
  "workflows_available": 1,
  "version": "v1",
  "platform": "Vercel Serverless"
}
```

## Cost Optimization

### Vercel Pricing Tiers
- **Hobby**: Free tier with limitations
- **Pro**: $20/month with higher limits
- **Enterprise**: Custom pricing

### Usage Optimization
- Cache responses where possible
- Implement request throttling
- Monitor function execution time
- Use CDN for static assets

## Security Considerations

### API Security
- Environment variables are encrypted
- HTTPS enforced by default
- CORS configured for cross-origin requests

### Data Privacy
- No persistent data storage
- Files processed in memory only
- Temporary files cleaned up automatically

## Monitoring and Analytics

### Built-in Monitoring
- Vercel provides automatic monitoring
- View logs in Vercel dashboard
- Real-time performance metrics

### Custom Analytics
Add custom logging:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Custom analytics event")
```

## Support and Documentation

### Resources
- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)

### Project Support
For issues specific to this implementation:
1. Check GitHub issues
2. Review deployment logs
3. Test locally first
4. Verify environment variables

## Future Enhancements

### Planned Features
- WebSocket support for real-time updates
- Enhanced caching mechanisms
- Multi-region deployment
- Advanced analytics dashboard

### Scaling Considerations
- Horizontal scaling via Vercel functions
- Database integration for persistence
- Queue system for heavy processing
- CDN optimization for global performance
