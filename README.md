# Library Management System API

## Table of Contents
*   [Project Description](#project-description)
*   [Features](#features)
*   [Technologies Used](#technologies-used)
*   [Getting Started](#getting-started)
    *   [Prerequisites](#prerequisites)
    *   [Installation](#installation)
    *   [Environment Variables](#environment-variables)
*   [API Reference](#api-reference)
    *   [Running the Application](#running-the-application)
    *   [Authentication & Authorization](#authentication--authorization)
    *   [API Endpoints](#api-endpoints)
*   [Project Structure](#project-structure)
*   [Caching](#caching)
*   [License](#license)

## Project Description
This project was built as part of Phitron's SDT track's Django Week 5, Module 26.5 (DRF Practice 2).

This project implements a RESTful API for managing a library's operations. The API provides functionalities for managing the library's collection of books, information about authors and members, and the process of borrowing and returning books. It serves as the backend for a potential web or mobile application.

## Features

The API supports the following core functionalities:

*   **Book Management:** Add, retrieve, update, and delete books.
*   **Author Management:** Add and retrieve author information.
*   **Member Management:** Add and retrieve library member information.
*   **Borrowing & Returning:** Record book borrowing and returning processes.
*   **User Authentication & Authorization:** Secure API access using Djoser and JWT.
*   **Role-Based Permissions:** Granular control over API endpoints based on user roles (Librarian, Member).
*   **API Documentation:** Interactive API documentation using Swagger UI and ReDoc.

## Technologies Used

*   **Django**: High-level Python web framework.
*   **Django REST Framework (DRF)**: Powerful and flexible toolkit for building Web APIs.
*   **Djoser**: REST implementation of Django authentication system.
*   **Simple JWT**: JSON Web Token authentication for Django REST Framework.
*   **Swagger UI**: Interactive API documentation.
*   **ReDoc**: OpenAPI/Swagger-generated API documentation.
*   **python-dotenv**: For managing environment variables.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.x
*   pip (Python package installer)
*   Virtual environment (recommended)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/MushfiqPlabon/libMan.git
    cd libMan
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    pip install python-dotenv  # For environment variable management
    ```
    `python-dotenv` is used to load environment variables from a `.env` file, keeping sensitive configurations out of version control.

4.  **Set up environment variables:**

    Create a `.env` file in the root directory of the project based on the `.env.example` file.

    ```bash
    cp .env.example .env
    ```

    Edit the `.env` file with your actual secret key and other configurations.

5.  **Apply database migrations:**

    ```bash
    python manage.py makemigrations library_api
    python manage.py migrate
    ```

6.  **Create a superuser (optional, for Django Admin access):**

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an administrator account.

### Environment Variables

The project uses environment variables for configuration. A `.env.example` file is provided as a template.

| Variable        | Description                                                              | Example Value          |
| :-------------- | :----------------------------------------------------------------------- | :--------------------- |
| `SECRET_KEY`    | Django secret key for cryptographic signing. **Keep this secure!**       | `your_secret_key_here` |
| `DEBUG`         | Boolean indicating if debug mode is enabled. Set to `False` in production. | `True`                 |
| `ALLOWED_HOSTS` | Comma-separated list of host/domain names that this Django site can serve. | `localhost,127.0.0.1`  |

## API Reference

### Running the Application

To start the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/api/`.

Interactive API documentation is available through Swagger UI and ReDoc:

*   **Swagger UI:** `http://127.0.0.1:8000/swagger/`
*   **ReDoc:** `http://127.0.0.1:8000/redoc/`

**Note:** To test authenticated endpoints, you will need to create a superuser (`python manage.py createsuperuser`) or register a new user via the `/auth/users/` endpoint.

### Authentication & Authorization

This API uses Djoser and Simple JWT for user authentication and token management. Permissions are implemented to control access to various endpoints based on user roles.

#### User Authentication Endpoints

*   `POST /auth/users/`: Register a new user.
    *   **Request Body (JSON):**
        ```json
        {
          "username": "newuser",
          "email": "user@example.com",
          "password": "strongpassword"
        }
        ```
        *   **Expected Response (201 Created):**
        ```json
        {
          "id": 1,
          "username": "newuser",
          "email": "user@example.com"
        }
        ```
    *   **Example `curl` command:**
        ```bash
        curl -X POST http://127.0.0.1:8000/auth/users/ \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "email": "test@example.com", "password": "testpassword"}'
        ```
*   `POST /auth/jwt/create/`: Obtain access and refresh tokens.
    *   **Request Body (JSON):**
        ```json
        {
          "username": "your_username",
          "password": "your_password"
        }
        ```
    *   **Expected Response (200 OK):**
        ```json
        {
          "access": "eyJ...",
          "refresh": "eyJ..."
        }
        ```
    *   **Example `curl` command:**
        ```bash
        curl -X POST http://127.0.0.1:8000/auth/jwt/create/ \
        -H "Content-Type: application/json" \
        -d '{"username": "testuser", "password": "testpassword"}'
        ```
*   `POST /auth/jwt/refresh/`: Refresh an expired access token.
    *   **Request Body (JSON):**
        ```json
        {
          "refresh": "eyJ..."
        }
        ```
    *   **Expected Response (200 OK):**
        ```json
        {
          "access": "eyJ..."
        }
        ```
    *   **Example `curl` command:**
        ```bash
        curl -X POST http://127.0.0.1:8000/auth/jwt/refresh/ \
        -H "Content-Type: application/json" \
        -d '{"refresh": "YOUR_REFRESH_TOKEN_HERE"}'
        ```
*   `POST /auth/jwt/verify/`: Verify the validity of an access token.
    *   **Request Body (JSON):**
        ```json
        {
          "token": "eyJ..."
        }
        ```
    *   **Expected Response (200 OK):** (Empty response if valid)
    *   **Example `curl` command:**
        ```bash
        curl -X POST http://127.0.0.1:8000/auth/jwt/verify/ \
        -H "Content-Type: application/json" \
        -d '{"token": "YOUR_ACCESS_TOKEN_HERE"}'
        ```

**Note on Token Lifetimes:** Access tokens are valid for 5 minutes, and refresh tokens are valid for 90 days. Refresh tokens are rotated upon use.

#### Role-Based Permissions

*   **Librarian (IsAdminUser):** Has full access to Author and Member management endpoints.
*   **Authenticated Users (IsAuthenticated):** Can borrow and return books.
*   **Authenticated Users (IsAuthenticatedOrReadOnly):** Can view books. Only Librarians can add, update, or delete books.

### API Endpoints

The API exposes the following endpoints:

#### Book Endpoints

*   `GET /api/books/`: Retrieve a list of all books.
    *   **Example `curl` command:**
        ```bash
        curl http://127.0.0.1:8000/api/books/
        ```
*   `POST /api/books/`: Add a new book to the library.
    *   **Request Body (JSON):**
        ```json
        {
          "title": "The Great Gatsby",
          "author": 1,
          "isbn": "978-0743273565",
          "publication_date": "1925-04-10",
          "genre": "Fiction",
          "available_copies": 5
        }
        ```
    *   **Expected Response (201 Created):**
        ```json
        {
          "id": 1,
          "title": "The Great Gatsby",
          "author": 1,
          "isbn": "978-0743273565",
          "publication_date": "1925-04-10",
          "genre": "Fiction",
          "available_copies": 5
        }
        ```
    *   **Example `curl` command (requires authentication token):**
        ```bash
        curl -X POST http://127.0.0.1:8000/api/books/ \
        -H "Content-Type: application/json" \
        -H "Authorization: JWT YOUR_ACCESS_TOKEN_HERE" \
        -d '{"title": "The Great Gatsby", "author": 1, "isbn": "978-0743273565", "publication_date": "1925-04-10", "genre": "Fiction", "available_copies": 5}'
        ```
*   `GET /api/books/{id}/`: Retrieve details for a specific book.
    *   **Example `curl` command:**
        ```bash
        curl http://127.0.0.1:8000/api/books/1/
        ```
*   `PUT /api/books/{id}/`: Update the details of a specific book.
    *   **Request Body (JSON):**
        ```json
        {
          "title": "The Great Gatsby (Revised)",
          "available_copies": 4
        }
        ```
    *   **Expected Response (200 OK):**
        ```json
        {
          "id": 1,
          "title": "The Great Gatsby (Revised)",
          "author": 1,
          "isbn": "978-0743273565",
          "publication_date": "1925-04-10",
          "genre": "Fiction",
          "available_copies": 4
        }
        ```
    *   **Example `curl` command (requires authentication token):**
        ```bash
        curl -X PUT http://127.0.0.1:8000/api/books/1/ \
        -H "Content-Type: application/json" \
        -H "Authorization: JWT YOUR_ACCESS_TOKEN_HERE" \
        -d '{"title": "The Great Gatsby (Revised)", "available_copies": 4}'
        ```
*   `DELETE /api/books/{id}/`: Remove a book from the library.
    *   **Example `curl` command (requires authentication token):**
        ```bash
        curl -X DELETE http://127.0.0.1:8000/api/books/1/ \
        -H "Authorization: JWT YOUR_ACCESS_TOKEN_HERE"
        ```

#### Member Endpoints

*   `GET /api/members/`: Retrieve a list of all members.
    *   **Example `curl` command:**
        ```bash
        curl http://127.0.0.1:8000/api/members/
        ```
*   `POST /api/members/`: Add a new member to the system.
    *   **Request Body (JSON):**
        ```json
        {
          "user": 1,
          "address": "123 Library Lane",
          "phone_number": "555-1234"
        }
        ```
    *   **Expected Response (201 Created):**
        ```json
        {
          "id": 1,
          "user": 1,
          "address": "123 Library Lane",
          "phone_number": "555-1234"
        }
        ```
    *   **Example `curl` command (requires authentication token):**
        ```bash
        curl -X POST http://127.0.0.1:8000/api/members/ \
        -H "Content-Type: application/json" \
        -H "Authorization: JWT YOUR_ACCESS_TOKEN_HERE" \
        -d '{"user": 1, "address": "123 Library Lane", "phone_number": "555-1234"}'
        ```

#### Author Endpoints

*   `GET /api/authors/`: Retrieve a list of all authors.
    *   **Example `curl` command:**
        ```bash
        curl http://127.0.0.1:8000/api/authors/
        ```
*   `POST /api/authors/`: Add a new author to the system.
    *   **Request Body (JSON):**
        ```json
        {
          "name": "F. Scott Fitzgerald",
          "biography": "American novelist and short story writer."
        }
        ```
    *   **Expected Response (201 Created):**
        ```json
        {
          "id": 1,
          "name": "F. Scott Fitzgerald",
          "biography": "American novelist and short story writer."
        }
        ```
    *   **Example `curl` command (requires authentication token):**
        ```bash
        curl -X POST http://127.0.0.1:8000/api/authors/ \
        -H "Content-Type: application/json" \
        -H "Authorization: JWT YOUR_ACCESS_TOKEN_HERE" \
        -d '{"name": "F. Scott Fitzgerald", "biography": "American novelist and short story writer."}'
        ```

#### Borrowing Endpoints

*   `POST /api/borrow-records/borrow/`: Record a book being borrowed by a member.
    *   **Request Body (JSON):**
        ```json
        {
          "book_id": 123,
          "member_id": 456
        }
        ```
    *   **Expected Response (201 Created):**
        ```json
        {
          "id": 789,
          "book_id": 123,
          "member_id": 456,
          "borrow_date": "2025-08-11T17:30:00Z",
          "return_date": null
        }
        ```
    *   **Example `curl` command (requires authentication token):**
        ```bash
        curl -X POST http://127.0.0.1:8000/api/borrow-records/borrow/ \
        -H "Content-Type: application/json" \
        -H "Authorization: JWT YOUR_ACCESS_TOKEN_HERE" \
        -d '{"book_id": 1, "member_id": 1}'
        ```

*   `POST /api/borrow-records/return/`: Record a book being returned.
    *   **Request Body (JSON):**
        ```json
        {
          "borrow_record_id": 789
        }
        ```
    *   **Expected Response (200 OK):**
        ```json
        {
          "id": 789,
          "book_id": 123,
          "member_id": 456,
          "borrow_date": "2025-08-11T17:30:00Z",
          "return_date": "2025-08-11"
        }
        ```
    *   **Example `curl` command (requires authentication token):**
        ```bash
        curl -X POST http://127.0.0.1:8000/api/borrow-records/return/ \
        -H "Content-Type: application/json" \
        -H "Authorization: JWT YOUR_ACCESS_TOKEN_HERE" \
        -d '{"borrow_record_id": 1}'
        ```

## Project Structure

*   `libMan/`: The main Django project directory, containing settings and URL configurations.
*   `library_api/`: The Django app containing models, serializers, views, and app-specific URLs.
*   `manage.py`: Django's command-line utility for administrative tasks.
*   `requirements.txt`: Lists all Python dependencies required for the project.
*   `.gitignore`: Specifies intentionally untracked files to ignore.
*   `README.md`: This file.

## Caching

This project utilizes Django's file-based caching system. Cache files are stored in the `django_cache/` directory at the project root. The cache is configured to expire after 15 minutes and has a maximum of 1000 entries.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
