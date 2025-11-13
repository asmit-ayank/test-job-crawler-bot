# Start from the official Python image
FROM python:3.11-slim

# Set environment variables for non-interactive commands
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required by Playwright/Chromium on Linux
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm-dev \
    libxkbcommon-dev \
    libgbm-dev \
    libasound2 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browser binaries
RUN playwright install --with-deps

# Copy the rest of the application code
COPY . .

# Command to run your bot
# Assumes your main script is app.py
CMD ["python", "app.py"]
