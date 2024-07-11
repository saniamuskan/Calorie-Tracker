# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create a working directory
WORKDIR /app

# Copy the requirements file into the image
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]
