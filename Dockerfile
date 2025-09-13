# Use Debian as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including libxrender1
RUN apt-get update && apt-get install -y \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libfontconfig1 \
    libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 5000 (as specified in FastHTML docs)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
