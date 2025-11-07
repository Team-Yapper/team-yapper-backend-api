#!/bin/bash

# Initialize the database structure first
echo "🔧 Initializing database structure..."
python -c "from database import init_db; init_db()"

# Wait a moment for tables to be created
sleep 1

# Check if database already has users
HAS_DATA=$(python -c "
from database import engine
from sqlmodel import Session, select
from models import User

try:
    with Session(engine) as session:
        users = session.exec(select(User)).first()
        print('1' if users else '0')
except Exception as e:
    print('0')
")

# Only seed if no data exists
if [ "$HAS_DATA" = "0" ]; then
    echo "🌱 Database is empty, seeding initial data..."
    python seed_db.py
else
    echo "✅ Database already contains data, skipping seed"
fi

# Start the application
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info