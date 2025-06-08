# Library Management System API

A comprehensive FastAPI-based library management system that provides endpoints for managing books, students, book issues/returns, overdue management, and AI-powered assistance.

## Features

- **Book Management**: Create, read, update, delete, and search books
- **Student Management**: Register students and search student records
- **Book Issue/Return System**: Issue books to students and handle returns
- **Overdue Management**: Automated reminder system for overdue books
- **AI Assistant**: Natural language query support for library operations
- **RESTful API**: Clean, well-documented API endpoints

## API Overview

The API is built with FastAPI and follows REST principles. All endpoints return JSON responses and include proper HTTP status codes and error handling.

### Base URL

```
http://localhost:8000
```

## Installation and Setup

1. Create Virtual Environment

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:

   ```bash
   uvicorn main:app --reload
   ```

   or

   ```bash
   fastapi dev main.py --port 8000
   ```

4. Access the interactive API documentation at `http://localhost:8000/docs`

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

### Books Management

# Library Management System API

A comprehensive FastAPI-based library management system that provides endpoints for managing books, students, book issues/returns, overdue management, and AI-powered assistance.
