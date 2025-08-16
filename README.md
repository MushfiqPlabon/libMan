# Library Management System API

## Project Description

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

5.  **Create a superuser (optional, for Django Admin access):**

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an administrator account.

## API Endpoints

## Authentication & Authorization

This API uses Djoser and Simple JWT for user authentication and token management. Permissions are implemented to control access to various endpoints based on user roles.

### User Authentication Endpoints

*   `POST /auth/users/`: Register a new user.
*   `POST /auth/jwt/create/`: Obtain access and refresh tokens.
*   `POST /auth/jwt/refresh/`: Refresh an expired access token.
*   `POST /auth/jwt/verify/`: Verify the validity of an access token.

### Role-Based Permissions

*   **Librarian (IsAdminUser):** Has full access to Author and Member management endpoints.
*   **Authenticated Users (IsAuthenticated):** Can borrow and return books.
*   **Authenticated Users (IsAuthenticatedOrReadOnly):** Can view books. Only Librarians can add, update, or delete books.

The API exposes the following endpoints:

### Book Endpoints

*   `GET /api/books/`: Retrieve a list of all books.
*   `POST /api/books/`: Add a new book to the library.
*   `GET /api/books/{id}/`: Retrieve details for a specific book.
*   `PUT /api/books/{id}/`: Update the details of a specific book.
*   `DELETE /api/books/{id}/`: Remove a book from the library.

### Member Endpoints

*   `GET /api/members/`: Retrieve a list of all members.
*   `POST /api/members/`: Add a new member to the system.

### Author Endpoints

*   `GET /api/authors/`: Retrieve a list of all authors.
*   `POST /api/authors/`: Add a new author to the system.

### Borrowing Endpoints

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

## Running the Application

## API Documentation

Interactive API documentation is available through Swagger UI and ReDoc.

*   **Swagger UI:** `http://127.0.0.1:8000/swagger/`
*   **ReDoc:** `http://127.0.0.1:8000/redoc/`

To start the Django development server:

```bash
python manage.py runserver
```

The API will be accessible at `http://127.0.0.1:8000/api/`.

**Note:** To test authenticated endpoints, you will need to create a superuser (`python manage.py createsuperuser`) or register a new user via the `/auth/users/` endpoint.

## Project Structure

*   `libMan/`: The main Django project directory, containing settings and URL configurations.
*   `library_api/`: The Django app containing models, serializers, views, and app-specific URLs.
*   `manage.py`: Django's command-line utility for administrative tasks.
*   `requirements.txt`: Lists all Python dependencies required for the project.
*   `.gitignore`: Specifies intentionally untracked files to ignore.
*   `README.md`: This file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
