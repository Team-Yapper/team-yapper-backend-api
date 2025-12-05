
from models import User, Post
from sqlmodel import select

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Test reading a specific post
def test_read_post_success(client, session):
    # Create a user
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    post = Post(content="hi", user_id=user.id)
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


# Test that there are no posts yet
def test_get_all_posts_empty(client):
    response = client.get("/posts")
    assert response.status_code == 200
    # data hasn't been added yet, so expect this to be empty
    assert response.json() == []

# Test to check /GET all posts
def test_get_all_posts_with_data(client, session):
    # create a user and posts
    user = User(email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    post1 = Post(content="First post", user_id=user.id)
    post2 = Post(content="Second post", user_id=user.id)
    session.add_all([post1, post2])
    session.commit()

    # get all posts created
    response = client.get("/posts")

    # assert that the data is correct
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 2
    assert posts[0]["content"] == "First post"
    assert posts[1]["content"] == "Second post"

# Test to check /GET/{post_id}
def test_get_post_by_id(client, session):
    # Create test user
    user = User(email="testuser@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create test post
    post = Post(content="Specific post", user_id=user.id)
    session.add(post)
    session.commit()
    session.refresh(post)

    # get /posts/{post_id}
    response = client.get(f"/posts/{post.id}")
    assert response.status_code == 200

    assert response.json() == {
        "id": post.id,
        "content": post.content,
        "user": {
            "id": user.id,
            "email": user.email
        }
    }


# Test to check /POST a new post
def test_create_post(client, session):
    # create a user
    user = User(email="testuser@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    payload = {"content": "Hello world"}

    # make /POST request
    response = client.post("/posts", json=payload)

    # assert that the data is correct
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["content"] == "Hello world"
    assert data["user_id"] == user.id
    assert "id" in data

# Test that data is persistent
def test_create_post_persists(client, session):
    user = User(email="testuser@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)

    payload = {"content": "Persistent post"}
    client.post("/posts", json=payload)

    posts = session.exec(select(Post)).all()
    assert len(posts) == 1
    assert posts[0].content == "Persistent post"