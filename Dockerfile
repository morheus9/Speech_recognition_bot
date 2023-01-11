FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt && apt update -y && apt install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
COPY . .
CMD ["python3", "main.py"]
