#!/bin/bash

# Initialize the database
python -c "from database import init_db; init_db()"

# Start the application
uvicorn main:app --host 127.0.0.1 --port 8000