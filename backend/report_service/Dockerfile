FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_all.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_all.txt

# Copy shared modules
COPY shared/ ./shared/

# Copy service code
COPY report_service/ ./report_service/

WORKDIR /app/report_service

# Expose port
EXPOSE 8008

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8008/health')"

# Run service
CMD ["python", "main.py"]
