# seed_data.py
from models import User

# Users to seed
users_to_seed = [
    User(email="alice@example.com", is_admin=True),
    User(email="bob@example.com"),
    User(email="charlie@example.com"),
    User(email="diana@example.com"),
    User(email="evan@example.com"),
    User(email="fiona@example.com"),
    User(email="george@example.com"),
    User(email="hannah@example.com"),
]

# Posts to seed
# user_email is used to map to user_id later
posts_to_seed = [
    {"content": "Just launched my new project management tool! It's built with FastAPI and React, and I'm really excited about how smoothly everything is working together. The performance is outstanding so far.", "user_email": "alice@example.com"},
    {"content": "FastAPI + SQLModel is absolutely awesome! I've been using it for the past month and the developer experience is incredible. The automatic documentation is a game-changer for API development.", "user_email": "alice@example.com"},
    {"content": "Had an amazing day at the tech conference today. Learned so much about modern web development practices and got to network with some brilliant engineers. Can't wait to implement some of these ideas in my projects!", "user_email": "bob@example.com"},
    {"content": "Finally finished debugging that nasty race condition that's been haunting my codebase for weeks. The issue was in the async task queue - turns out the lock timeout was too aggressive. Now everything runs smoothly!", "user_email": "charlie@example.com"},
    {"content": "Just completed a Python course on data structures and algorithms. Understanding the fundamentals really changes how you approach problem-solving. Highly recommend everyone take time to revisit the basics regularly.", "user_email": "diana@example.com"},
    {"content": "Started learning TypeScript today and I'm blown away by how much it improves code maintainability. The type system catches so many errors before runtime. Why didn't I start using this sooner?", "user_email": "evan@example.com"},
    {"content": "Working on an interesting optimization problem today. Managed to reduce database query time by 60% by refactoring the schema and adding proper indexes. Small wins like these really add up over time!", "user_email": "fiona@example.com"},
    {"content": "Version 2.0 of our open source library just hit 1000 stars on GitHub! Super grateful to all the contributors who've helped make this possible. The community support has been incredible.", "user_email": "george@example.com"},
    {"content": "Spent the afternoon refactoring my authentication middleware. The code is now much cleaner and I've added better error handling for edge cases. Security is always a priority when dealing with user data.", "user_email": "hannah@example.com"},
    {"content": "Just deployed our new microservices architecture to production. It took longer than expected but the improved scalability is already paying off. We're now able to handle 3x the traffic without any issues.", "user_email": "alice@example.com"},
    {"content": "Had a great code review session with my team today. We discussed best practices for writing maintainable code and shared some useful refactoring techniques. These discussions really help everyone grow as developers.", "user_email": "bob@example.com"},
    {"content": "Looking for recommendations on UI component libraries. Currently evaluating a few options and would love to hear what the community prefers. Performance and accessibility are my main concerns.", "user_email": "charlie@example.com"},
    {"content": "Just published an article about containerization best practices using Docker. It covers everything from writing efficient Dockerfiles to orchestrating containers in production. Check it out if you're interested!", "user_email": "diana@example.com"},
    {"content": "Implementing real-time notifications in our application using WebSockets. The latency is incredibly low and users are loving the instant updates. This has been a game-changer for user engagement.", "user_email": "evan@example.com"},
    {"content": "Started exploring GraphQL as an alternative to REST APIs. The query language is elegant and really reduces over-fetching of data. Definitely consider this for your next project if you haven't already.", "user_email": "fiona@example.com"},
    {"content": "Just contributed my first significant piece of code to a major open source project. The code review process was thorough but fair, and I learned a lot from the maintainers' feedback. Really proud of this moment!", "user_email": "george@example.com"},
    {"content": "Been diving deep into machine learning lately. Implemented a simple neural network from scratch and it's fascinating to see how the math translates into code. Definitely a steep learning curve but worth every moment.", "user_email": "hannah@example.com"},
    {"content": "Just finished setting up CI/CD pipelines for all our projects. Automated testing and deployment have significantly reduced manual errors and freed up a lot of time for actual development work.", "user_email": "alice@example.com"},
    {"content": "Spent the day optimizing our frontend bundle size. By lazy loading components and using code splitting, we reduced it by 40%. Users on slower connections will definitely notice the improvement in load times.", "user_email": "bob@example.com"},
    {"content": "Working with distributed systems for the first time and it's both challenging and exciting. Understanding concepts like eventual consistency and dealing with network failures has really expanded my perspective on software design.", "user_email": "charlie@example.com"},
]
