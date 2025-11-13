# Start from the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code (app.py, etc.)
COPY . .

# Command to run your bot
# This should match your Start Command logic
CMD ["python", "app.py"]
