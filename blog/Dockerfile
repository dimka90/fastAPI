FROM python:3.11.13-slim

WORKDIR /app
COPY  requirements.txt .
RUN  pip install -r requirements.txt
COPY main.py .
EXPOSE 7000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
