FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y python3-pip

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 5000

COPY requirements.txt /app

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"


RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "run.py"]
