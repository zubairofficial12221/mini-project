# Project Structure

Complete file structure and description of the College Management System.

```
college-management/
│
├── app.py                          # Main Flask application file
│                                   # Contains: routes, models, configuration, scheduler
│
├── config.py                       # Configuration class (optional, can use .env)
│
├── requirements.txt                # Python package dependencies
│
├── README.md                       # Main project documentation
│
├── SETUP_GUIDE.md                 # Detailed setup instructions
│
├── DATABASE_SCHEMA.md             # Database structure documentation
│
├── API_ENDPOINTS.md               # API endpoints documentation
│
├── PROJECT_STRUCTURE.md           # This file
│
├── .gitignore                     # Git ignore file
│
├── templates/                     # HTML templates directory
│   ├── base.html                  # Base template with navigation
│   ├── login.html                 # Login page
│   ├── dashboard.html             # Main dashboard
│   ├── students.html              # Students list page
│   ├── add_student.html           # Add student form
│   ├── attendance.html            # Attendance marking page
│   ├── weather.html               # Weather dashboard
│   ├── seating.html               # Seating arrangements list
│   ├── create_seating.html        # Create seating arrangement form
│   └── view_seating.html          # View seating arrangement details
│
└── static/                        # Static files directory
    ├── css/
    │   └── style.css              # Custom CSS styles
    │
    ├── js/
    │   └── main.js                # Custom JavaScript
    │
    └── pdfs/                      # Generated PDF files (created at runtime)
        └── (PDF files stored here)
```

---

## File Descriptions

### Core Application Files

#### `app.py`
**Main application file** containing:
- Flask app initialization
- Database models (User, Student, Attendance, Room, SeatingArrangement, WeatherLog)
- All route handlers
- Email sending functionality
- Weather checking scheduler
- PDF generation for seating arrangements
- Authentication decorators

**Key Functions:**
- `check_weather()` - Scheduled weather checking
- `mark_attendance()` - Mark attendance with email notifications
- `create_seating()` - Generate seating arrangements
- `download_seating_pdf()` - Generate PDF seating charts

#### `config.py`
**Configuration management** (optional)
- Environment variable loading
- Configuration class for Flask app

#### `requirements.txt`
**Python dependencies:**
- Flask - Web framework
- Flask-SQLAlchemy - Database ORM
- Flask-Bcrypt - Password hashing
- Flask-Mail - Email sending
- PyMySQL - MySQL connector
- APScheduler - Task scheduling
- requests - HTTP library
- reportlab - PDF generation
- python-dotenv - Environment variables

---

### Template Files

#### `templates/base.html`
**Base template** with:
- Bootstrap 5 framework
- Navigation bar
- Flash message handling
- Common layout structure

#### `templates/login.html`
**Login page** with:
- Username/password form
- Error message display
- Gradient background styling

#### `templates/dashboard.html`
**Main dashboard** showing:
- Statistics cards (students, attendance, weather)
- Weather alerts
- Quick action buttons
- Recent attendance records

#### `templates/students.html`
**Students list** with:
- Table of all students
- Add student button
- Student details display

#### `templates/add_student.html`
**Add student form** with:
- Roll number input
- Name input
- Department dropdown
- Email inputs (student and mentor)

#### `templates/attendance.html`
**Attendance marking page** with:
- Date and hour filter
- Student list with status
- Present/Absent buttons
- Mark all present option

#### `templates/weather.html`
**Weather dashboard** with:
- Current weather display
- Weather alerts
- Weather history table
- AJAX weather updates

#### `templates/seating.html`
**Seating arrangements list** with:
- All arrangements table
- View and download PDF buttons
- Create new arrangement button

#### `templates/create_seating.html`
**Create seating form** with:
- Exam name input
- Number of rooms input
- Seats per room input

#### `templates/view_seating.html`
**Seating arrangement view** with:
- Room-wise student display
- Table format showing seat, roll, name, department
- Download PDF button

---

### Static Files

#### `static/css/style.css`
**Custom styles:**
- Color variables
- Card styling
- Table styling
- Responsive design
- Button hover effects
- Weather icon styling

#### `static/js/main.js`
**JavaScript utilities:**
- Tooltip initialization
- Auto-dismiss alerts
- Date formatting
- Loading states
- Error handling

---

### Documentation Files

#### `README.md`
- Project overview
- Features list
- Quick start guide
- Tech stack
- Basic usage

#### `SETUP_GUIDE.md`
- Step-by-step installation
- Database setup
- Email configuration
- Weather API setup
- Troubleshooting

#### `DATABASE_SCHEMA.md`
- Table structures
- Relationships
- Indexes
- Sample queries
- Maintenance commands

#### `API_ENDPOINTS.md`
- All route documentation
- Request/response formats
- Authentication requirements
- Examples

#### `PROJECT_STRUCTURE.md`
- This file
- File descriptions
- Directory structure

---

## Directory Structure Details

### `/templates`
**Flask template directory** - Contains all HTML templates using Jinja2 templating engine.

### `/static`
**Static files directory** - Contains CSS, JavaScript, and generated files.

#### `/static/css`
Custom stylesheet files.

#### `/static/js`
Client-side JavaScript files.

#### `/static/pdfs`
Generated PDF files (created at runtime, should be in `.gitignore`).

---

## Database Models (in app.py)

1. **User** - Admin/teacher accounts
2. **Student** - Student information
3. **Attendance** - Attendance records
4. **Room** - Examination rooms
5. **SeatingArrangement** - Exam seating arrangements
6. **WeatherLog** - Weather data logs

---

## Key Features Implementation

### 1. Attendance System
- **Location**: `app.py` - `/attendance` and `/attendance/mark` routes
- **Template**: `templates/attendance.html`
- **Email**: Triggered in `mark_attendance()` function

### 2. Weather Automation
- **Location**: `app.py` - `check_weather()` function
- **Scheduler**: APScheduler configured in `app.py`
- **Template**: `templates/weather.html`
- **API**: `/api/weather/current` endpoint

### 3. Seat Arrangement
- **Location**: `app.py` - `/seating/create` route
- **Algorithm**: Round-robin department distribution
- **PDF**: `download_seating_pdf()` function using ReportLab
- **Templates**: `create_seating.html`, `view_seating.html`

---

## Dependencies Flow

```
app.py
├── Flask → Web server
├── SQLAlchemy → Database ORM
├── Bcrypt → Password hashing
├── Mail → Email sending
├── APScheduler → Weather checking
├── ReportLab → PDF generation
└── requests → Weather API calls

templates/
└── Jinja2 → Template rendering

static/
├── Bootstrap 5 → UI framework (CDN)
├── Font Awesome → Icons (CDN)
└── Custom CSS/JS → Additional styling/functionality
```

---

## Configuration Points

### Environment Variables (.env)
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - MySQL connection string
- `MAIL_USERNAME` - Gmail username
- `MAIL_PASSWORD` - Gmail app password
- `WEATHER_API_KEY` - OpenWeatherMap API key
- `WEATHER_CITY` - City for weather checks
- `COLLEGE_EMAIL` - Management email for alerts

### In-app Configuration (app.py)
- Database connection
- Email server settings
- Weather API configuration
- Scheduler interval (default: 1 hour)

---

## Runtime Generated Files

### Database
- MySQL tables created automatically on first run
- Tables: users, students, attendances, rooms, seating_arrangements, weather_logs

### PDFs
- Generated in `static/pdfs/` directory
- Filename format: `seating_arrangement_<id>.pdf`

### Logs
- Weather logs stored in database
- Application logs to console (can be configured for file logging)

---

## Extensibility Points

### Adding New Features
1. Add model in `app.py`
2. Create route handler
3. Create template in `templates/`
4. Add navigation link in `base.html`

### Customization
- Colors: Edit `static/css/style.css` variables
- Departments: Edit `add_student.html` dropdown
- Weather thresholds: Edit `check_weather()` function
- Email templates: Edit email body in `mark_attendance()`

---

## Security Considerations

1. **Passwords**: Hashed using BCrypt
2. **Sessions**: Flask sessions with secret key
3. **SQL Injection**: Protected by SQLAlchemy ORM
4. **XSS**: Jinja2 auto-escaping enabled
5. **CSRF**: Can be added with Flask-WTF

---

## Deployment Checklist

- [ ] Change `SECRET_KEY` in production
- [ ] Use environment variables for sensitive data
- [ ] Disable debug mode
- [ ] Set up production database
- [ ] Configure email credentials
- [ ] Get production weather API key
- [ ] Set up SSL/HTTPS
- [ ] Configure production WSGI server
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Test all features
- [ ] Change default admin password

---

## Maintenance Tasks

### Regular
- Database backups (daily)
- Check weather logs
- Monitor email sending
- Review attendance records

### Periodic
- Update dependencies
- Database optimization
- Clean old PDFs
- Review logs

---

This structure is designed to be clean, maintainable, and easily extensible.

