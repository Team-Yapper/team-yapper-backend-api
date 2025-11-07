#!/bin/bash

# Initialize the database
python -c "from database import init_db; init_db()"
python seed_db.py

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info