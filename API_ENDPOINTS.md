# API Endpoints Documentation

This document describes all API endpoints and routes in the College Management System.

## Base URL

- **Development**: `http://localhost:5000`
- **Production**: `https://your-domain.com`

---

## Authentication Endpoints

### POST /login
Login user (admin/teacher)

**Request:**
- Method: `POST`
- Content-Type: `application/x-www-form-urlencoded`
- Body:
  - `username` (string, required): Username
  - `password` (string, required): Password

**Response:**
- Success (302): Redirects to `/dashboard`
- Error: Renders login page with error message

**Example:**
```bash
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=admin123"
```

---

### GET /logout
Logout current user

**Response:**
- Success (302): Redirects to `/login`
- Clears session

**Example:**
```bash
curl http://localhost:5000/logout
```

---

## Dashboard Endpoints

### GET /dashboard
Main dashboard page (requires login)

**Response:**
- Renders dashboard with statistics:
  - Total students count
  - Today's attendance count
  - Latest weather information
  - Recent attendance records

**Example:**
```bash
curl http://localhost:5000/dashboard \
  -H "Cookie: session=<session_cookie>"
```

---

## Student Management Endpoints

### GET /students
List all students

**Response:**
- Renders students list page

**Example:**
```bash
curl http://localhost:5000/students \
  -H "Cookie: session=<session_cookie>"
```

---

### GET /students/add
Show add student form

**Response:**
- Renders add student form

---

### POST /students/add
Create new student

**Request:**
- Method: `POST`
- Content-Type: `application/x-www-form-urlencoded`
- Body:
  - `roll_number` (string, required): Student roll number
  - `name` (string, required): Student name
  - `department` (string, required): Department
  - `email` (string, optional): Student email
  - `class_mentor_email` (string, required): Mentor email

**Response:**
- Success (302): Redirects to `/students`

**Example:**
```bash
curl -X POST http://localhost:5000/students/add \
  -d "roll_number=CS001&name=John Doe&department=Computer Science&class_mentor_email=mentor@college.com"
```

---

## Attendance Endpoints

### GET /attendance
View/mark attendance page

**Query Parameters:**
- `date` (string, optional): Date in YYYY-MM-DD format (default: today)
- `hour` (string, optional): Hour/period number (default: "1")

**Response:**
- Renders attendance marking page

**Example:**
```bash
curl "http://localhost:5000/attendance?date=2024-01-15&hour=1" \
  -H "Cookie: session=<session_cookie>"
```

---

### POST /attendance/mark
Mark attendance for a student (JSON API)

**Request:**
- Method: `POST`
- Content-Type: `application/json`
- Body:
  ```json
  {
    "student_id": 1,
    "date": "2024-01-15",
    "hour": "1",
    "status": "present"
  }
  ```

**Response:**
```json
{
  "success": true
}
```

**Notes:**
- If student is marked absent, automatic email is sent to class mentor
- Status can be: `"present"` or `"absent"`

**Example:**
```bash
curl -X POST http://localhost:5000/attendance/mark \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<session_cookie>" \
  -d '{
    "student_id": 1,
    "date": "2024-01-15",
    "hour": "1",
    "status": "present"
  }'
```

---

## Weather Endpoints

### GET /weather
Weather dashboard page

**Response:**
- Renders weather information page with:
  - Current weather
  - Weather alerts
  - Weather history (last 24 hours)

**Example:**
```bash
curl http://localhost:5000/weather \
  -H "Cookie: session=<session_cookie>"
```

---

### GET /api/weather/current
Get current weather data (JSON API)

**Response:**
```json
{
  "success": true,
  "data": {
    "temperature": 28.5,
    "description": "clear sky",
    "main": "Clear",
    "humidity": 65,
    "wind_speed": 3.2,
    "city": "Mumbai"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Weather API error"
}
```

**Example:**
```bash
curl http://localhost:5000/api/weather/current \
  -H "Cookie: session=<session_cookie>"
```

---

## Seating Arrangement Endpoints

### GET /seating
List all seating arrangements

**Response:**
- Renders seating arrangements list page

**Example:**
```bash
curl http://localhost:5000/seating \
  -H "Cookie: session=<session_cookie>"
```

---

### GET /seating/create
Show create seating arrangement form

**Response:**
- Renders create seating arrangement form

---

### POST /seating/create
Create new seating arrangement

**Request:**
- Method: `POST`
- Content-Type: `application/x-www-form-urlencoded`
- Body:
  - `exam_name` (string, required): Exam name
  - `num_rooms` (int, required): Number of rooms
  - `seats_per_room` (int, required): Seats per room

**Response:**
- Success (302): Redirects to `/seating/<arrangement_id>`

**Example:**
```bash
curl -X POST http://localhost:5000/seating/create \
  -d "exam_name=Mid-Term Exam&num_rooms=5&seats_per_room=30"
```

---

### GET /seating/<arrangement_id>
View specific seating arrangement

**Parameters:**
- `arrangement_id` (int, required): Arrangement ID

**Response:**
- Renders seating arrangement view page

**Example:**
```bash
curl http://localhost:5000/seating/1 \
  -H "Cookie: session=<session_cookie>"
```

---

### GET /seating/<arrangement_id>/pdf
Download seating arrangement as PDF

**Parameters:**
- `arrangement_id` (int, required): Arrangement ID

**Response:**
- PDF file download

**Example:**
```bash
curl http://localhost:5000/seating/1/pdf \
  -H "Cookie: session=<session_cookie>" \
  -o seating_arrangement.pdf
```

---

## Authentication Requirements

Most endpoints require authentication. Unauthenticated requests will redirect to `/login`.

### Session Management

The application uses Flask sessions. Include session cookie in requests:
```bash
-H "Cookie: session=<session_cookie>"
```

---

## Error Responses

### 401 Unauthorized
User not logged in
- Redirects to `/login`

### 403 Forbidden
Insufficient permissions (admin required)
```json
{
  "error": "Admin access required"
}
```

### 404 Not Found
Resource not found
- Standard Flask 404 page

### 500 Internal Server Error
Server error
- Check server logs for details

---

## Rate Limiting

Currently no rate limiting implemented. Can be added using Flask-Limiter if needed.

---

## CORS

CORS is not configured by default. For API access from different origins, configure CORS:
```python
from flask_cors import CORS
CORS(app)
```

---

## Testing Endpoints

### Using cURL

```bash
# Login and get session
curl -c cookies.txt -X POST http://localhost:5000/login \
  -d "username=admin&password=admin123"

# Use session in subsequent requests
curl -b cookies.txt http://localhost:5000/dashboard
```

### Using Python requests

```python
import requests

session = requests.Session()

# Login
response = session.post('http://localhost:5000/login', data={
    'username': 'admin',
    'password': 'admin123'
})

# Use session for authenticated requests
response = session.get('http://localhost:5000/students')
print(response.text)
```

### Using Postman

1. Set method and URL
2. For POST requests, add form-data or JSON body
3. For authenticated requests, enable cookies or add session cookie header

---

## Notes

1. **Date Format**: Use `YYYY-MM-DD` format for dates
2. **Time Format**: All times are in server timezone
3. **File Downloads**: PDF downloads use `attachment` disposition
4. **Email Trigger**: Attendance marking with status "absent" triggers email automatically
5. **Weather Updates**: Weather is checked hourly via background scheduler

---

## Future API Enhancements

Potential additions:
- RESTful API endpoints with JSON responses
- API authentication tokens (JWT)
- Bulk operations (bulk attendance, bulk student import)
- Export endpoints (CSV, Excel)
- Search and filter endpoints
- Pagination for large datasets
- WebSocket for real-time updates

