FROM python:3.11.13-slim

WORKDIR /app
RUN  pip install "fastapi[standard]"
COPY main.py .
EXPOSE 8000
# CMD [ "fastapi", "dev" , "main.py"  ]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["fastapi", "dev", "main.py", "--host", "0.0.0.0"]