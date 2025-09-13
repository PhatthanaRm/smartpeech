# Use Debian as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libxrender1 \
    libfontconfig1 \
    libfreetype6 \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff6 \
    libopenjp2-7 \
    libwebp7 \
    libharfbuzz0b \
    libfribidi0 \
    libx11-6 \
    libxext6 \
    libxcb1 \
    libxau6 \
    libxdmcp6 \
    libbsd0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port 5000 (as specified in FastHTML documentation)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
