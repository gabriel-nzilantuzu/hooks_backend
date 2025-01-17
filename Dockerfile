# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django app into the container
COPY . /app/

# Expose the ports
EXPOSE 8000

# Use Daphne to serve the app
CMD ["daphne", "-u", "/tmp/daphne.sock", "hooks_backend.asgi:application"]
