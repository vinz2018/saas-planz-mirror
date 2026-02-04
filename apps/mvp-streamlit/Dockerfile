# Dockerfile for SaaS Planz Streamlit App
# Python 3.11 with Debian Slim for optimal size

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for ortools)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY apps/mvp-streamlit/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from project root
COPY core/ ./core/
COPY docs/ ./docs/
COPY apps/mvp-streamlit/app.py .
COPY apps/mvp-streamlit/pages/ ./pages/

# Expose Streamlit default port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
