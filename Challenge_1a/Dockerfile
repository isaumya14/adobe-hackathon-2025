# Use AMD64 explicitly for compatibility
FROM --platform=linux/amd64 python:3.10-slim

# Install system dependencies for PyMuPDF (fitz)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies first for Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Run the processor
ENTRYPOINT ["python", "process_pdfs.py"]
