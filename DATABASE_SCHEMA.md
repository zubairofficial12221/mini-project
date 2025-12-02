# Database Schema Documentation

This document describes the database structure for the College Management System.

## Database: `college_management`

Character Set: `utf8mb4`
Collation: `utf8mb4_unicode_ci`

---

## Table: `users`

Stores admin and teacher user accounts for authentication.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier |
| username | VARCHAR(80) | UNIQUE, NOT NULL | Login username |
| email | VARCHAR(120) | UNIQUE, NOT NULL | User email address |
| password | VARCHAR(255) | NOT NULL | Hashed password (BCrypt) |
| role | VARCHAR(20) | NOT NULL, DEFAULT 'teacher' | User role: 'admin' or 'teacher' |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |

**Default Admin User:**
- Username: `admin`
- Password: `admin123` (hashed)
- Role: `admin`

---

## Table: `students`

Stores student information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique student identifier |
| roll_number | VARCHAR(50) | UNIQUE, NOT NULL | Student roll number |
| name | VARCHAR(100) | NOT NULL | Student full name |
| department | VARCHAR(100) | NOT NULL | Student department |
| email | VARCHAR(120) | NULL | Student email (optional) |
| class_mentor_email | VARCHAR(120) | NOT NULL | Email for absence notifications |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**Relationships:**
- One-to-Many with `attendances` (one student can have many attendance records)

---

## Table: `attendances`

Stores attendance records for students by date and hour/period.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique attendance record identifier |
| student_id | INT | FOREIGN KEY → students.id, NOT NULL | Reference to student |
| date | DATE | NOT NULL | Attendance date |
| hour | VARCHAR(10) | NOT NULL | Period/hour number (e.g., "1", "2") |
| status | VARCHAR(20) | NOT NULL | 'present' or 'absent' |
| reason | TEXT | NULL | Optional reason for absence |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |
| updated_at | DATETIME | DEFAULT CURRENT_TIMESTAMP, ON UPDATE | Last update timestamp |

**Unique Constraint:**
- `(student_id, date, hour)` - One attendance record per student per date per hour

**Relationships:**
- Many-to-One with `students` (many attendance records belong to one student)

---

## Table: `rooms`

Stores examination room information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique room identifier |
| name | VARCHAR(100) | NOT NULL | Room name (e.g., "Room 1") |
| capacity | INT | NOT NULL | Maximum number of seats |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Record creation timestamp |

**Usage:**
- Created dynamically when generating seating arrangements
- Linked to seating arrangements through arrangement_data JSON

---

## Table: `seating_arrangements`

Stores exam seating arrangement data.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique arrangement identifier |
| exam_name | VARCHAR(200) | NOT NULL | Name of the examination |
| num_rooms | INT | NOT NULL | Number of rooms used |
| seats_per_room | INT | NOT NULL | Seats per room |
| arrangement_data | TEXT | NOT NULL | JSON string containing seating data |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

**arrangement_data JSON Structure:**
```json
[
    {
        "student_id": 1,
        "student_name": "John Doe",
        "student_roll": "CS001",
        "student_dept": "Computer Science",
        "room_id": 1,
        "room_name": "Room 1",
        "seat_number": 1
    },
    ...
]
```

---

## Table: `weather_logs`

Stores weather data retrieved from OpenWeatherMap API.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | Unique log identifier |
| temperature | FLOAT | NOT NULL | Temperature in Celsius |
| description | VARCHAR(200) | NOT NULL | Weather description |
| main_condition | VARCHAR(100) | NOT NULL | Main weather condition |
| city | VARCHAR(100) | NOT NULL | City name |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Log timestamp |

**Usage:**
- Updated hourly via scheduled task
- Used for weather alerts and history

---

## Entity Relationship Diagram

```
users (1) ──┐
            │
            │ (created by)
            │
            │
students (1) ──< (N) attendances
            │
            │ (arranged in)
            │
            │
seating_arrangements (1) ──< (JSON data) ──< rooms
            │
            │
            │
weather_logs (independent)
```

---

## Indexes

### Primary Keys
- All tables have `id` as PRIMARY KEY

### Unique Indexes
- `users.username` - Unique username
- `users.email` - Unique email
- `students.roll_number` - Unique roll number
- `attendances(student_id, date, hour)` - Unique attendance per student/date/hour

### Foreign Keys
- `attendances.student_id` → `students.id`

---

## Sample Queries

### Get all students with their attendance count
```sql
SELECT s.*, COUNT(a.id) as attendance_count
FROM students s
LEFT JOIN attendances a ON s.id = a.student_id
GROUP BY s.id;
```

### Get today's absent students
```sql
SELECT s.name, s.roll_number, s.class_mentor_email, a.hour
FROM students s
JOIN attendances a ON s.id = a.student_id
WHERE a.date = CURDATE() AND a.status = 'absent';
```

### Get weather alerts (bad conditions)
```sql
SELECT *
FROM weather_logs
WHERE (main_condition IN ('rain', 'storm', 'snow', 'thunderstorm')
   OR temperature > 40)
AND created_at >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY created_at DESC;
```

### Get seating arrangement for exam
```sql
SELECT exam_name, num_rooms, seats_per_room, created_at
FROM seating_arrangements
WHERE exam_name LIKE '%Mid-Term%'
ORDER BY created_at DESC
LIMIT 1;
```

---

## Database Maintenance

### Backup
```bash
mysqldump -u root -p college_management > backup.sql
```

### Restore
```bash
mysql -u root -p college_management < backup.sql
```

### Optimize Tables
```sql
OPTIMIZE TABLE users, students, attendances, rooms, seating_arrangements, weather_logs;
```

---

## Notes

1. **Password Storage**: Passwords are hashed using BCrypt (not stored in plain text)
2. **JSON Storage**: Seating arrangement data is stored as JSON string in TEXT field
3. **Soft Deletes**: Currently no soft delete mechanism (can be added if needed)
4. **Audit Trail**: `created_at` and `updated_at` timestamps provide basic audit trail
5. **Timezone**: All timestamps use server timezone (configure MySQL timezone if needed)

---

## Future Enhancements

Potential additions:
- User activity logs table
- Email notification logs
- Student photos
- Course/subject management
- Timetable management
- Grade management
- Reports and analytics

