# Use a base image with Python
FROM python:3.8-alpine

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Create and set the working directory in the container
WORKDIR /app

# Install Flask
RUN pip install Flask

# Copy the requirements file into the container and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the Flask application code into the container
COPY . .

# Expose the port that Flask will run on (usually 5000)
EXPOSE 5000:5006

# Define the command to run the Flask application
CMD ["flask", "run"]
