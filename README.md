# PROWEB Test Task - Todo Manager
Simple test todo manager project to the PROWEB company. In this project I added swagger documentations with drf-spectacular, jwt authentication with drf simple-jwt, and dockerized the project. I have only two tags: Task and Comment, both of them have filtration and validation.

## Prerequisites
- Docker (https://docs.docker.com/get-docker/)
- Docker Compose (https://docs.docker.com/compose/install/)
- Make (https://www.gnu.org/software/make/)
- Python 3.12.x (https://www.python.org/downloads/)

## API Documentation
- Swagger UI: http://localhost:8000/swagger/
- Redoc: http://localhost:8000/redoc/

## Detailed Endpoints

### Authentication
- **POST /api/token/**: Obtain JWT token pair (access and refresh tokens).
- **POST /api/token/refresh/**: Refresh the access token using the refresh token.
- **POST /api/token/verify/**: Verify the validity of a token.

### Tasks
- **GET /task/**: Retrieve a list of all todos.
- **POST /task/**: Create a new todo.
- **GET /task/{id}/**: Retrieve a specific todo by ID.
- **PUT /task/{id}/**: Update a specific todo by ID.
- **PATCH /task/{id}/**: Partially update a specific todo by ID.
- **DELETE /task/{id}/**: Delete a specific todo by ID.

### Comments
- **GET /comment/**: Retrieve a list of all comments.
- **POST /comment/**: Create a new comment.
- **GET /comment/{id}/**: Retrieve a specific comment by ID.
- **PUT /comment/{id}/**: Update a specific comment by ID.
- **PATCH /comment/{id}/**: Partially update a specific comment by ID.
- **DELETE /comment/{id}/**: Delete a specific comment by ID.


## Installation
1. Clone the repository
    ```bash
    git clone https://github.com/batirniyaz/todo-manager_proweb.git
    cd todo_proweb
    ```
2. Create venv file
   - For Linux
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
    - For Windows
     ```bash
    python -m venv venv
    venv\Scripts\activate
   ```
3. Create `.env` file from `.env-example` and fill the variables
    ```bash
    cp .env-example .env
    ```
4. Install the project dependencies
    - installing
    ```bash
   pip install -r requirements.txt
    ```
    - migrating
    ```bash
    python manage.py migrate
    ```
    - creating superuser
    ```bash
    python manage.py createsuperuser
    ```
   - running
    ```bash
    python manage.py runserver
    ```
5. Or just run with DOCKER
    - If Linux or MacOS
    ```bash
    make start
    ```
    - If Windows
    ```bash
    docker-compose up --build
    ```

## Usage
Some useful commands
- Run the project
    ```bash
    python manage.py runserver
    ```
- Build with Docker
    ```bash
    make build
    ```
- Run with Docker
    ```bash
    make start
    ```
- Stop with Docker
    ```bash
    make stop
    ```

### The project is ready to use. Enjoy it!
