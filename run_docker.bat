@echo off
REM Build and run the Data Analysis API Docker container - Windows version

set IMAGE_NAME=data-analysis-api
set CONTAINER_NAME=data-analysis-api-container
set PORT=8000

echo Building Docker image: %IMAGE_NAME%
docker build -t %IMAGE_NAME% .

if %ERRORLEVEL% neq 0 (
    echo Failed to build Docker image!
    pause
    exit /b 1
)

REM Remove any existing container with the same name
FOR /f "tokens=*" %%i IN ('docker ps -aq -f name=%CONTAINER_NAME% 2^>nul') DO (
    echo Removing existing container: %CONTAINER_NAME%
    docker rm -f %CONTAINER_NAME%
)

echo Starting Docker container: %CONTAINER_NAME%
docker run -d --name %CONTAINER_NAME% -p %PORT%:80 --env-file .env %IMAGE_NAME%

if %ERRORLEVEL% neq 0 (
    echo Failed to start Docker container!
    pause
    exit /b 1
)

echo.
echo ================================
echo Container started successfully!
echo API is available at: http://localhost:%PORT%/
echo Health check: http://localhost:%PORT%/health
echo API docs: http://localhost:%PORT%/docs
echo ================================
echo.
echo Press any key to continue...
pause > nul
