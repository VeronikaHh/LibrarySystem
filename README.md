# LibrarySystem

## Description:
The Library Management System is an efficient web application designed to streamline the management of library
resources. This project leverages the high-performance FastAPI framework to provide a fast and modern API
interface for handling various library operations.

## Features
- Book Management:
Add, update, delete, and search for books.
- Member Management:
Register new members, update member details, and manage membership statuses.
- Loan Management:
Issue and return books, track overdue items, and manage fines.
- Authentication & Authorization(in progress): 
Secure access with user roles (admin, librarian, member).
- Search Functionality(in progress): 
Advanced search options for books and members.
- Responsive API:
Fast and efficient API responses with comprehensive custom error handling.
- Swagger Documentation:
Built-in API documentation using Swagger UI for easy API exploration.
## Technologies Used
- FastAPI: For building the API.
- SQLAlchemy: For database interactions.
- PostgreSQL: As the database backend.
- Docker: For containerized deployment.
- Ruff: As a linter.
- Alembic: For auto-generating database migrations.
- Pytest: For testing.
## Installation Steps
First step, installing dependencies:

`pip install -r requirements.txt`

Create `.env` file and then copy content of `.env.sample` to your file.
Write your environmental variables in your `.env` file.

Then run Postgres database in docker:

`docker-compose up postgres`

Run a migration(after setting up a database):

`alembic upgrade head`

Run server locally:
`fastapi run` (run this command in LibrarySystem/app directory)

Open Swager API docs:
http://0.0.0.0:8000/docs

Open FastApi documentation:
http://0.0.0.0:8000/redoc

If you want to run API as docker container:
```
docker build -t library-management-api .
docker run -p 8000:8000 library-management-api
```

If you want to launch your API with Postgres database using docker-compose:

`docker-compose up`
