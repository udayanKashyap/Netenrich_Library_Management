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
   fastapi dev src/main.py --port 8000
   ```

4. (Optional) Run Database migrations - if using new database other than the submitted one

   ```bash
   python src/manage.py migrate
   ```

5. Access the interactive API documentation at `http://localhost:8000/docs`

## Interactive Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

**NOTE** - Although API keys need to be stored as environment variables, I have added those directly into the code to easily access the populated database and AI LLM integrations without additional modifications for the purpose of evaluation of this assignment.

### Books Management

#### Create a Book

- **POST** `/books/`
- Create a new book in the library system

**Request Body:**

```json
{
  "title": "The Great Gatsby",
  "isbn": "978-0-7432-7356-5",
  "number_of_copies": 5,
  "author": "F. Scott Fitzgerald",
  "category": "Fiction"
}
```

#### Search Books

- **GET** `/books/search`
- Search books with optional filters

**Query Parameters:**

- `title` (optional): Filter by book title (partial match)
- `author` (optional): Filter by author name (partial match)
- `category` (optional): Filter by book category (partial match)
- `page` (optional, default: 1): Page number
- `limit` (optional, default: 10, max: 100): Books per page

#### Get Book by ID

- **GET** `/books/{book_id}`
- Retrieve a specific book by its ID

#### Update Book

- **PUT** `/books/{book_id}`
- Update book information

**Request Body:**

```json
{
  "title": "Updated Title",
  "isbn": "978-0-7432-7356-6",
  "number_of_copies": 3,
  "author": "Updated Author",
  "category": "Updated Category"
}
```

#### Delete Book

- **DELETE** `/books/{book_id}`
- Remove a book from the system

### Student Management

#### Register Student

- **POST** `/students/`
- Register a new student

**Request Body:**

```json
{
  "name": "John Doe",
  "roll_number": "CS2021001",
  "department": "Computer Science",
  "semester": 6,
  "phone": "+1234567890",
  "email": "john.doe@university.edu"
}
```

#### Search Students

- **GET** `/students/search`
- Search students with filters

**Query Parameters:**

- `department` (optional): Filter by department
- `semester` (optional): Filter by semester
- `name` (optional): Filter by name (partial match)
- `roll_number` (optional): Filter by roll number (partial match)
- `phone` (optional): Filter by phone number (partial match)

### Book Issue Management

#### Issue Book

- **POST** `/book-issue/`
- Issue a book to a student

**Request Body:**

```json
{
  "book_id": 1,
  "student_id": 1,
  "issue_date": "2025-06-08",
  "due_date": "2025-06-22"
}
```

#### Return Book

- **POST** `/book-issue/return`
- Process book return

**Request Body:**

```json
{
  "issue_id": 1,
  "return_date": "2025-06-15"
}
```

#### Get Book Issue Report

- **GET** `/book-issue/`
- Retrieve comprehensive book issue report

#### Get Books Issued to Student

- **GET** `/book-issue/student/{student_id}`
- Get all books currently issued to a specific student

### Overdue Management

#### Send Manual Reminders

- **POST** `/overdue/send-reminders`
- Trigger manual reminder notifications for overdue books

### AI Assistant

#### Ask Question

- **POST** `/ai/ask`
- Ask natural language questions about library operations

**Request Body:**

```json
{
  "question": "How many books are currently issued to students in Computer Science department?"
}
```

## Sample Usage Examples

### Using cURL

#### 1. Create a New Book

```bash
curl -X POST "http://localhost:8000/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction to Algorithms",
    "isbn": "978-0-262-03384-8",
    "number_of_copies": 3,
    "author": "Thomas H. Cormen",
    "category": "Computer Science"
  }'
```

#### 2. Search Books by Category

```bash
curl -X GET "http://localhost:8000/books/search?category=Fiction&page=1&limit=5"
```

#### 3. Register a Student

```bash
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "roll_number": "EE2022015",
    "department": "Electrical Engineering",
    "semester": 4,
    "phone": "+1987654321",
    "email": "alice.johnson@university.edu"
  }'
```

#### 4. Issue a Book

```bash
curl -X POST "http://localhost:8000/book-issue/" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "student_id": 1,
    "issue_date": "2025-06-08",
    "due_date": "2025-06-22"
  }'
```

#### 5. Return a Book

```bash
curl -X POST "http://localhost:8000/book-issue/return" \
  -H "Content-Type: application/json" \
  -d '{
    "issue_id": 1,
    "return_date": "2025-06-15"
  }'
```

### Using Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Create a book
book_data = {
    "title": "Clean Code",
    "isbn": "978-0-13-235088-4",
    "number_of_copies": 2,
    "author": "Robert C. Martin",
    "category": "Programming"
}

response = requests.post(f"{BASE_URL}/books/", json=book_data)
print(f"Book created: {response.status_code}")

# Search books
search_params = {
    "author": "Robert",
    "page": 1,
    "limit": 10
}

response = requests.get(f"{BASE_URL}/books/search", params=search_params)
books = response.json()
print(f"Found books: {json.dumps(books, indent=2)}")

# Register student
student_data = {
    "name": "Bob Smith",
    "roll_number": "ME2023001",
    "department": "Mechanical Engineering",
    "semester": 2,
    "phone": "+1122334455",
    "email": "bob.smith@university.edu"
}

response = requests.post(f"{BASE_URL}/students/", json=student_data)
print(f"Student registered: {response.status_code}")

# Ask AI assistant
question_data = {
    "question": "What are the most popular book categories in our library?"
}

response = requests.post(f"{BASE_URL}/ai/ask", json=question_data)
ai_response = response.json()
print(f"AI Response: {ai_response}")
```

### Using JavaScript/Fetch

```javascript
const BASE_URL = "http://localhost:8000";

// Create a book
async function createBook() {
  const bookData = {
    title: "Design Patterns",
    isbn: "978-0-201-63361-0",
    number_of_copies: 4,
    author: "Gang of Four",
    category: "Software Engineering",
  };

  try {
    const response = await fetch(`${BASE_URL}/books/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bookData),
    });

    const result = await response.json();
    console.log("Book created:", result);
  } catch (error) {
    console.error("Error creating book:", error);
  }
}

// Search students
async function searchStudents(department = "Computer Science") {
  try {
    const response = await fetch(
      `${BASE_URL}/students/search?department=${encodeURIComponent(department)}`,
    );
    const students = await response.json();
    console.log("Students found:", students);
  } catch (error) {
    console.error("Error searching students:", error);
  }
}

// Get book issue report
async function getBookIssueReport() {
  try {
    const response = await fetch(`${BASE_URL}/book-issue/`);
    const report = await response.json();
    console.log("Book issue report:", report);
  } catch (error) {
    console.error("Error getting report:", error);
  }
}

// Usage
createBook();
searchStudents();
getBookIssueReport();
```

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **201**: Created successfully
- **422**: Validation Error
- **404**: Resource not found
- **500**: Internal server error

### Validation Error Response Format

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Database Schema Overview

The system uses a relational database with four main entities designed to handle all aspects of library management:

### Core Tables

#### 1. Books Table

Stores information about all books in the library inventory.

**Fields:**

- `id` - Primary key (auto-increment)
- `title` - Book title (indexed for search performance)
- `isbn` - Unique 14-character ISBN identifier
- `number_of_copies` - Available copies count (default: 1)
- `author` - Author name (indexed)
- `category` - Book category/genre (indexed)
- `created_at` / `updated_at` - Audit timestamps

#### 2. Students Table

Manages student information and library membership.

**Fields:**

- `id` - Primary key (auto-increment)
- `name` - Student's full name (indexed)
- `roll_number` - Unique student identifier (max 51 chars)
- `department` - Academic department (indexed)
- `semester` - Current semester number
- `phone` - Contact number (11 digits)
- `email` - Unique email address
- `created_at` / `updated_at` - Audit timestamps

#### 3. BookIssues Table

Tracks all book borrowing transactions and their status.

**Fields:**

- `id` - Primary key (auto-increment)
- `book_id` - Foreign key to Books table
- `student_id` - Foreign key to Students table
- `issue_date` - When book was issued (defaults to today)
- `due_date` - Return deadline
- `return_date` - Actual return date (NULL if not returned)
- `created_at` / `updated_at` - Audit timestamps

#### 4. ReminderHistory Table

Logs all reminder communications sent to students.

**Fields:**

- `id` - Primary key (auto-increment)
- `student_id` - Foreign key to Students table
- `book_issue_id` - Foreign key to BookIssues table
- `reminder_type` - Type of reminder sent (e.g., "email", "sms")
- `sent_date` - When reminder was sent
- `days_before_due` - How many days before due date reminder was sent
- `created_at` - Audit timestamp

## Project Structure

The application follows a clean, modular architecture pattern:

### Root Level

```
Netenrich_Library_Management/
├── README.md           # Project documentation
└── src/               # Main source code directory
```

### Source Code Organization (`src/`)

#### **Configuration (`config/`)**

- `db.py` - Database connection and session management

#### **Data Models (`models/`)**

- `models.py` - SQLAlchemy ORM models (the schema you provided)
- Contains all table definitions and relationships

#### **API Routes (`routers/`)**

Route handlers for different API endpoints:

- `bookRouter.py` - Book management endpoints (CRUD operations)
- `studentRouter.py` - Student management endpoints
- `bookIssueRouter.py` - Book issuing/returning endpoints
- `overdueRouter.py` - Overdue tracking and reporting
- `aiRouter.py` - AI-powered features (recommendations, analytics)

#### **Business Logic (`controllers/`)**

Core application logic separated from API routing:

- `bookController.py` - Book business logic
- `studentController.py` - Student management logic
- `bookIssueController.py` - Issue/return processing
- `overdueTrackingController.py` - Overdue monitoring and alerts
- `aiController.py` - AI/ML functionality

#### **Data Validation (`schemas/`)**

Pydantic models for request/response validation:

- `book.py` - Book data validation schemas
- `student.py` - Student data validation schemas
- `bookIssue.py` - Book issue validation schemas
- `reminder.py` - Reminder data schemas
- `ai.py` - AI feature schemas

#### **Application Entry Points**

- `main.py` - FastAPI application initialization and startup
- `manage.py` - Database management and utility scripts
- `requirements.txt` - Python dependencies
