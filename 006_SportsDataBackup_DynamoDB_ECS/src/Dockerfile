#Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt fetch.py process_videos.py mediaconvert_process.py run_all.py config.py ./ 

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y awscli

ENTRYPOINT ["python", "run_all.py"]