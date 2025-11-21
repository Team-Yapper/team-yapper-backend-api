
from models import User, Post

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Test reading a specific post
def test_read_post_success(client, session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(content="Hello this is my yapper post!", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    response = client.get(f"/posts/{post.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": post.id,
        "content": "Hello this is my yapper post!",
        "user": {
            "id": user.id,
            "email": "test@example.com"
        }
    }

# Test reading a non-existent post
def test_read_post_invalid_id(client):
    response = client.get("/posts/abc")
    assert response.status_code == 422

#Test reading a specific posts info
def test_read_post_info_success(client, session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create a post linked to the user
    post = Post(content="Hello this is my yapper post!", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    # Call the endpoint
    response = client.get(f"/posts/{post.id}/info")

    # Validate response
    assert response.status_code == 200
    assert response.json() == {
        "id": post.id,
        "content": "Hello this is my yapper post!",
        "user_id": user.id,
        "user": {
            "email": "test@example.com"
        }
    }

# Test reading a non-existent post
def test_read_post_info_not_found(client):
    response = client.get("/posts/999/info")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}

# Test getting all posts for a specific user
def test_get_user_posts_success(client, session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create posts for the user
    post1 = Post(content="First post", user_id=user.id)
    post2 = Post(content="Second post", user_id=user.id)
    session.add(post1)
    session.add(post2)
    session.commit()

    # Call the endpoint
    response = client.get(f"/user/{user.id}/posts")

    assert response.status_code == 200
    assert response.json() == {
        "email": "test@example.com",
        "posts": [
            {"id": post1.id, "content": "First post"},
            {"id": post2.id, "content": "Second post"}
        ]
    }

# Test getting posts for a user with no posts
def test_get_user_posts_empty_list(client, session):
    # Create a user with no posts
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Call endpoint
    response = client.get(f"/user/{user.id}/posts")

    assert response.status_code == 200
    assert response.json() == {
        "email": "test@example.com",
        "posts": []
    }

# Test getting posts for a non-existent user
def test_get_user_posts_user_not_found(client):
    response = client.get("/user/999/posts")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}