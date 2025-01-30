# Dockerfile

# Use the official lightweight Python 3.9 image as the base image.
# The 'slim' variant reduces the image size by omitting unnecessary packages.
FROM python:3.9-slim

# Set the working directory inside the container to /app.
# All subsequent commands will be executed from this directory.
WORKDIR /app

# Copy the 'requirements.txt' file from the host machine to the current working directory in the container.
COPY requirements.txt .

# Install the Python dependencies listed in 'requirements.txt'.
# '--no-cache-dir' option prevents the caching of packages, reducing the image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python scripts and configuration file from the host machine to the current working directory in the container.
# This includes 'fetch.py', 'process_one_video.py', 'mediaconvert_process.py', 'run_all.py', and 'config.py'.
COPY fetch.py process_one_video.py mediaconvert_process.py run_all.py config.py ./ 

# Update the package lists for 'apt-get' and install the AWS Command Line Interface (CLI).
# This allows the container to interact with AWS services if needed.
# '&&' ensures that the 'apt-get install' command runs only if 'apt-get update' succeeds.
RUN apt-get update && apt-get install -y awscli

# Define the default command to run when the container starts.
# This uses the Python interpreter to execute the 'run_all.py' script.
# 'ENTRYPOINT' ensures that this command is always executed, allowing for easier command overrides if necessary.
ENTRYPOINT ["python", "run_all.py"]
