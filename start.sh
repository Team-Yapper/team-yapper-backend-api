#!/bin/bash

DB_FILE="/app/data/yapper.db"

# Ensure data dir exists (volume mount will persist)
mkdir -p /app/data

if [ ! -f "$DB_FILE" ]; then
    echo "🔧 Database file not found — initializing and seeding..."
    python -c "from database import init_db; init_db()"
    python seed_db.py
else
    echo "✅ Database file exists, skipping init/seed"
fi

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info