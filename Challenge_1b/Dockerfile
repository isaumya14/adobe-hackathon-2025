# Use slim Python base image and specify amd64 architecture
FROM --platform=linux/amd64 python:3.10-slim

# Install system dependencies required by PyMuPDF
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining code
COPY . .

# Entry point for the container
ENTRYPOINT ["python", "main.py"]

