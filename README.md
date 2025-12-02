# Student Attendance & College Management System

A comprehensive web application for managing student attendance, weather monitoring, and exam seat arrangements in educational institutions.

## Features

### 1. Student Attendance System
- Admin/Teacher login with role-based access
- Student management with roll numbers, names, and departments
- Mark attendance by hour/period
- Automatic email notifications to class mentors when students are absent
- Attendance records stored in MySQL database

### 2. Weather API Automation
- Integration with OpenWeatherMap API
- Automatic weather checks every hour
- Bad weather alerts sent to college management email
- Weather dashboard with current conditions and history
- Holiday recommendation system based on severe weather

### 3. Automatic Exam Seat Arrangement
- Admin can create seating arrangements for exams
- Automatic distribution of students across rooms
- Algorithm ensures no two same-department students sit adjacent
- Generate downloadable PDF seating arrangements
- Visual display of seating arrangements on dashboard

## Tech Stack

- **Backend**: Python 3.8+, Flask
- **Database**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Email**: SMTP (Gmail)
- **Scheduling**: APScheduler
- **PDF Generation**: ReportLab
- **Weather API**: OpenWeatherMap

## Project Structure

```
college-management/
├── app.py                  # Main Flask application
├── models.py              # Database models (optional, models in app.py)
├── config.py              # Configuration file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── SETUP_GUIDE.md        # Detailed setup instructions
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── students.html
│   ├── add_student.html
│   ├── attendance.html
│   ├── weather.html
│   ├── seating.html
│   ├── create_seating.html
│   └── view_seating.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── pdfs/             # Generated PDF files stored here
└── .env                  # Environment variables (create this)
```

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Database**
   - Create MySQL database named `college_management`
   - Update database credentials in `app.py` or use environment variables

3. **Configure Environment Variables**
   - Set up email credentials (Gmail)
   - Get OpenWeatherMap API key
   - Configure college management email

4. **Run Application**
   ```bash
   python app.py
   ```

5. **Access Application**
   - Open browser: `http://localhost:5000`
   - Default login: `admin` / `admin123`

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## API Endpoints

### Authentication
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - Main dashboard

### Students
- `GET /students` - List all students
- `GET/POST /students/add` - Add new student

### Attendance
- `GET /attendance` - View/mark attendance
- `POST /attendance/mark` - Mark attendance (API)

### Weather
- `GET /weather` - Weather dashboard
- `GET /api/weather/current` - Current weather API

### Seating Arrangement
- `GET /seating` - List seating arrangements
- `GET/POST /seating/create` - Create new arrangement
- `GET /seating/<id>` - View arrangement
- `GET /seating/<id>/pdf` - Download PDF

## Database Schema

See [DATABASE_SCHEMA.md](DATABASE_SCHEMA.md) for detailed database structure.

## Configuration

### Email Configuration
1. Use Gmail with App Password (not regular password)
2. Enable 2-factor authentication
3. Generate App Password from Google Account settings
4. Set `MAIL_USERNAME` and `MAIL_PASSWORD` in environment variables

### Weather API
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get free API key
3. Set `WEATHER_API_KEY` in environment variables
4. Configure `WEATHER_CITY` for your location

## Default Credentials

- **Username**: `admin`
- **Password**: `admin123`

**⚠️ Important**: Change the default password in production!

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please refer to the documentation or contact the development team.

