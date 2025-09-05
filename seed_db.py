from sqlmodel import SQLModel, Session
from sqlalchemy import delete
from models import User, Post
from database import engine, init_db
# your separate seed data file
from seed_data import users_to_seed, posts_to_seed


def seed_db(force: bool = False):
    """Seed the database with initial data using SQLModel + delete()."""

    if force:
        print("⚠️ Dropping and recreating all tables...")
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)
    else:
        print("Ensuring tables exist...")
        init_db()  # just ensures tables exist

    # opens a database session
    # session automatically closes at the end of this
    with Session(engine) as session:
        # Clear existing data (order matters: Posts first due to FK)
        session.exec(delete(Post))
        session.exec(delete(User))
        session.commit()

        # Add users
        session.add_all(users_to_seed)
        session.commit()
        for user in users_to_seed:
            session.refresh(user)

        # Map emails to user IDs for posts
        email_to_id = {user.email: user.id for user in users_to_seed}

        # Add posts
        posts = [
            Post(
                content=p["content"],
                user_id=email_to_id[p["user_email"]]
            )
            for p in posts_to_seed
        ]
        session.add_all(posts)
        session.commit()

        print("🌱 Database seeded successfully!")


if __name__ == "__main__":
    # force=True will drop tables and recreate them
    seed_db(force=True)
