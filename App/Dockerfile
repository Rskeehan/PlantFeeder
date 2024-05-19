# Use a base image that is compatible with Raspberry Pi
FROM balenalib/raspberrypi3-python:latest

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (they can be overridden at runtime)
ENV API_KEY=f
ENV CITY_ID=4

# Command to run the application
CMD ["python3", "app.py"]
