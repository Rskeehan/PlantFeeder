# Use a base image compatible with your Raspberry Pi's architecture
FROM balenalib/rpi-raspbian:buster

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install schedule requests

# Set the working directory
WORKDIR /app

# Copy the application code
COPY . .

# Run the application
CMD ["python3", "app.py"]