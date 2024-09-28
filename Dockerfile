FROM python:3.11

ENV PYTHONBUFFERED = 1


COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY what_happened_bot what_happened_bot
WORKDIR  what_happened_bot
ENTRYPOINT ["python", "main.py"]
