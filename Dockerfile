# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port
EXPOSE 5000

# Run the web app with gunicorn
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "2" ]
