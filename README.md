# Django REST API - Chat App backend

This is the **backend API** for the full stack chat application. It's built with Django and DJANGO REST framework, handling authentication, user management and chat endpoints.

## Live API
[API ROOT ENDPOINT]

## TECH STACK
- **Django**
- **Django REST Framework**
- **Supabase (profile image URLs)**
- **Render (deployment)**
- **SQLite/PostgreSQL**

## Features
- Token-based user authentication
- Custom user model with profile picture field
- RESTful API endpoints for chat functionality
- CORS support for frontend intergration
- Environment variable handling via .env

## What I learned
This project helped me separate the frontend and backend, set up RESTful APIs with Django, deploy on render, and intergrate Supabase for external storage.

## How to run locally

### 1. Clone the repo
```bash
git clone https://github.com/SithabileM/chatApp.git
cd backend
```

### 2. Set up virtual environment
```bash
python -m venv venv
source venv\Scripts\Activate
```

### 3. Install dpendencies
```bash
pip install -r requirements.txt
```

### 4. Create a .env file
*Your .env file should include sensitive credentials. Ensure that it is included in your .gitignore.*

SUPABASE_PROJECT_ID=your-supabase-project-id
SUPABASE_API_KEY=your-supabase-api-key
SUPABASE_BUCKET=your-supabase-bucket-name
DATABASE_URL=your-database-url
DJANGO_SECRET_KEY=your-django-secret-key
DEBUG=True

### 5. Run migrations and start server
```bash
python manage.py migrate
python manage.py runserver
```

## API Endpoints

### /logout
Method: POST
Description: Logs a logged in user out

### /login
Method: POST
Description: Logs a user in with their username and password

### /login
Method: POST
Description: Signs a user up with their username, password and email

### /users
Method: GET
Description: Gets all signed up users

### /users/<int:pk>
Method: GET
Description: Fetches the users with the specified primary key

### /create_chatRoom
Method: POST
Description: Generate a unique room for two users based on the individual ids of the two users. 
example data:
{
    "id":"1_3",
    "user_1":1,
    "user_2":3}

### /post_message
Method: POST
Description: Sends a message to a specific room
example data:
{
    "room":"ChatRoom(1_3)",
    "sender":1,
    "recipient": 3,
    "message": "This is the message"}

### /room/<int:userId_1>/<int:userId_2>
Method: GET
Description: Fetch the room which contains the specified users

### get_messages/<str:roomId>
Method: GET
Description: Fetch all messages in the specified roomId

### /get_connections
Method: GET
Description: Fetch ids of all the users with whom the currently logged in user has sent or received a message from

### /profile_picture
Method: GET
Description: Fetch The url of the profile picture of the currently logged in user

method: PUT
description: Update the url of the profile picture of the currenly logged in user with the new url

### /users/delete
Method: DELETE
Description: Deletes a users account

## Deployment
This api is deployed on Render. The deployed version is conected to the React frontend via CORS.

## Author
Sithabile Monde






