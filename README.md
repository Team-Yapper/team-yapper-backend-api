# team-yapper-backend-api
Backend module project for Multiverse, a mini twitter creating CRUD routes for post and Auth0 for authentication and authorization 

## 

## Installation 📦
1. **Clone the Repository**
   ```
   git clone https://github.com/Team-Yapper/team-yapper-backend-api.git
   cd team-yapper-backend-api
   ```
2. **Create and activate virtual environment**
    ```
    python -m venv .venv    
    ```
    Activation on Mac:
    ``` 
    source .venv/bin/activate
    ```
    Activation on Windows:
    ``` 
    source .venv/Scripts/activate
    ```
    Deactivation:
    ``` 
    deactivate
    ```
  
4. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```
5. **Create a .env file**
   ```
   # Store environment variables here, such as API keys and tokens
   ```
6. **Seed the database**
   ```
   python seed_db.py
   ```
7. **Start server**
   ```
   uvicorn main:app --reload
   ```

## API Documentation 📄

## Deployment URL 🚀
   ```
   https://team-yapper-backend-api.onrender.com/posts
   ```
***
