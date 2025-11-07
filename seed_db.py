from sqlmodel import SQLModel, Session, select
from database import engine, init_db
from seed_data import users_to_seed, posts_to_seed
from models import User, Post

def seed_db():
    init_db()  # safe to call (no-op if already created)

    with Session(engine) as session:
        # If users already exist, assume DB was seeded
        existing_user = session.exec(select(User)).first()
        if existing_user:
            print("✅ Users already exist — skipping seed.")
            return

        # Insert users
        created_users = {}
        for u in users_to_seed:
            session.add(u)
        session.commit()

        # refresh users to get ids
        for u in session.exec(select(User)).all():
            created_users[u.email] = u.id

        # Insert posts mapping by user_email
        for p in posts_to_seed:
            user_id = created_users.get(p["user_email"])
            if user_id:
                post = Post(content=p["content"], user_id=user_id)
                session.add(post)

        session.commit()
        print("🌱 Database seeded successfully.")


if __name__ == "__main__":
    seed_db()
