FROM python:3.12-slim

WORKDIR /app

# Create directory for persistent data
RUN mkdir -p /app/data

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Create a startup script
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000

CMD ["./start.sh"]

# CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]