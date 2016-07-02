FROM python:2.7-slim

COPY . /hail
WORKDIR /hail

CMD ["python", "setup.py", "test"]
