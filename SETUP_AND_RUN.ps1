# TMU 360 Analytics Hub - Systematic Setup & Run Script
# This script orchestrates the entire application using Docker Compose

Write-Host "🚀 Starting TMU 360 Analytics Hub System..." -ForegroundColor Green

# Check for Docker
if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker is not installed or not in PATH. Please install Docker Desktop." -ForegroundColor Red
    Exit
}

# 1. Stop existing containers to avoid port conflicts
Write-Host "1️⃣  stopping existing services..." -ForegroundColor Cyan
docker-compose down

# 2. Build the services (Systematic Build with unified context)
Write-Host "2️⃣  Building services (this may take a few minutes)..." -ForegroundColor Cyan
docker-compose build

# 3. Start the Database first
Write-Host "3️⃣  Starting Database..." -ForegroundColor Cyan
docker-compose up -d postgres
Start-Sleep -Seconds 10 # Wait for DB to be ready

# 4. Start all other services
Write-Host "4️⃣  Starting Microservices..." -ForegroundColor Cyan
docker-compose up -d

Write-Host "✅ System is RUNNING!" -ForegroundColor Green
Write-Host "   - Auth Service: http://localhost:8001"
Write-Host "   - Text Service: http://localhost:8002"
Write-Host "   - Voice Service: http://localhost:8003"
Write-Host "   - Face Service: http://localhost:8004"
Write-Host "   - Fusion Service: http://localhost:8005"
Write-Host "   - Doctor Service: http://localhost:8006"
Write-Host "   - Notification: http://localhost:8007"
Write-Host "   - Report Service: http://localhost:8008"
Write-Host "   - Knowledge Service: http://localhost:8009"
Write-Host ""
Write-Host "⚠️  Please ensure your Frontend connects to these ports."
Write-Host "To run frontend: cd frontend; npm run dev"
