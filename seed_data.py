# seed_data.py
from models import User

# Users to seed
users_to_seed = [
    User(email="alice@example.com"),
    User(email="bob@example.com"),
]

# Posts to seed
# user_email is used to map to user_id later
posts_to_seed = [
    {"content": "Hello world!", "user_email": "alice@example.com"},
    {"content": "FastAPI + SQLModel is awesome!",
        "user_email": "alice@example.com"},
    {"content": "Bob's first post", "user_email": "bob@example.com"},
]
