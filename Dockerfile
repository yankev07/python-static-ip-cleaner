# Use the official Python image as base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies (in case requirements.txt is not up-to-date)
RUN pip install --no-cache-dir requests flask mysql-connector-python boto3 datetime pandas

# Install any needed 3rd party dependencies (e.g. Google Cloud SDK)
RUN pip install --no-cache-dir gunicorn google-auth google-api-python-client google-cloud-container oauth2client kubernetes

# Copy the entire project directory into the container
COPY . .

# Expose the port on which your application will run
EXPOSE 3000
ENV PORT=3000

# Command to run your application
CMD ["python", "app.py"]

