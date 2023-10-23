FROM python:3.11

COPY . app/
WORKDIR app

RUN pip install .

CMD uvicorn src.api:app --reload --host 0.0.0.0 --port 45678
