FROM python:3.11

COPY . app/
WORKDIR app

RUN pip install .

CMD uvicorn src.api:app --host 0.0.0.0 --port 45678 --workers 4
