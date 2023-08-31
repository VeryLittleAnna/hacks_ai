# Build docker image: docker build -t hacks_ai .
# Run docker image: docker run --name webapp hacks_ai
# после name указываем имя контейнера, а потом образа
FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /hacks_ai

COPY ./requirements.txt /hacks_ai/requirements.txt
RUN apt-get update && pip install -r /hacks_ai/requirements.txt

COPY . /hacks_ai

EXPOSE 8000
CMD  ["python3", "fullstack_django/manage.py", "runserver", "0.0.0.0:8000"]
