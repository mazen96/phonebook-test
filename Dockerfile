FROM python:3.9.5
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install -y default-mysql-client
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app