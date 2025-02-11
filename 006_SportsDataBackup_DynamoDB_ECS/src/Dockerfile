#Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all scripts (including config.py) into the container
COPY fetch.py process_videos.py mediaconvert_process.py run_all.py config.py . 

RUN apt-get update && apt-get install -y awscli

ENTRYPOINT ["python", "run_all.py"]
