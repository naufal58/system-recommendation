FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y

# Create the working directory and set it as the working directory
WORKDIR /app

# Copy only the requirements file and cache dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set NLTK data directory
ENV NLTK_DATA=/opt/nltk_data

# Download NLTK data
RUN python -m nltk.downloader -d /opt/nltk_data punkt wordnet averaged_perceptron_tagger

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the rest of the application code
COPY . /app/

# Expose the necessary port
EXPOSE 5006

# Run the application
CMD ["gunicorn", "-c", "src/utils/gunicorn.conf.py", "app:app"]
