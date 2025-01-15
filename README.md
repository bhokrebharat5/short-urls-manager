# short-urls-manager
A simple and lightweight URL shortening service built using FastAPI


## Features

- **User Authentication**: Register, log in, and log out.
- **URL Management**: Add and delete short URLs.
- **Redirection**: Short URLs redirect to the original URL.
- **JSON-Based Storage**: User data and URLs are stored in JSON files.

## Prerequisites

- Python 3.7 or higher
- FastAPI and Uvicorn installed
- Jinja2Templates 

## Installation 
- pip install "fastapi[standard]"
- pip install Jinja2

## Run the App
- fastapi dev index.py

-- The application will be available at http://127.0.0.1:8000.

## Endpoints

Public Endpoints
- GET /: User login page.
- GET /register: User registration page.

Authenticated Endpoints
- GET  /dashboard: Dashboard for managing URLs.
- POST /create_url: Add a new URL.
- POST /url/delete/{short_id}: Delete a short URL.

Redirection
GET /r/{short_id}: Redirects to the original URL.


