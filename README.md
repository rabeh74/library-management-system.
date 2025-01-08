# Library Management System

## Overview
The **Library Management System** is a comprehensive application designed to manage a library's key operations. This includes tracking books, authors, members, reviews, and borrow records. The system provides APIs for CRUD operations and integrates additional tools for authentication, background task processing, and documentation.

---

## Features
- User authentication (JWT-based) and registration.
- Book management (CRUD operations, filtering by categories and authors).
- Member management with administrative creation.
- Borrow and return book functionality.
- API documentation with DRF Spectacular.
- Background tasks using Celery.
- Support for image uploads for books and authors.
- Dockerized environment for development and deployment.
- Test Driven Development (TDD): To ensure code reliability by writing tests before implementation.

---

## Technologies Used

### Core Frameworks and Libraries:
- **Python 3.9**
- **Django 3.2**
- **Django REST Framework**
- **PostgreSQL**

### Enhancements and Utilities:
- **DRF Spectacular**: For API documentation.
- **Django Filter**: For advanced query filtering.
- **Celery**: For asynchronous task processing.
- **Redis**: As the Celery message broker.

### Deployment and Development:
- **Docker**: For containerized application.
- **Docker Compose**: For orchestration.

---

## Setup and Running the Application

### Prerequisites:
- Install **Docker** and **Docker Compose** on your machine.

### Steps to Run:
1. Clone the repository:
   ```bash
   git clone https://github.com/rabeh74/library-management-system..git
   cd <repository_folder>
   ```

2. Create an `.env` file with the following environment variables:
   ```env
   DJANGO_SECRET_KEY=<your-secret-key>
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=library_db
   REDIS_PASSWORD=redis
   ```

3. Build and start the Docker containers:
   ```bash
   docker-compose up --build
   ```

4. Apply database migrations:
   ```bash
   docker-compose exec app python manage.py migrate
   ```

5. Create a superuser to access the admin panel:
   ```bash
   docker-compose exec app python manage.py createsuperuser
   ```

6. Access the application:
   - API Documentation: [http://localhost:8000/api/docs/swagger/](http://localhost:8000/api/docs/swagger/)
   - Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)


## Testing
Run the test suite:
```bash
   docker-compose exec app python manage.py test
```

---

## Directory Structure
```
project_root
├── app
│   ├── library_management_system  # Core Django project
│   ├── user                       # Custom user model and authentication
│   ├── books                      # Books, authors, categories API
│   ├── members                    # Library members API
│   ├── borrow                     # Borrowing-related API
│   └── static, media              # Static and media files
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## Author
**Rabeeh Rabie Abdelatty**

