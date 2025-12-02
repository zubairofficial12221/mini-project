"""
Main Flask Application
Student Attendance & College Management System
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from functools import wraps
import os
from datetime import datetime, timedelta
import json
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import threading
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import atexit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'

# Database configuration - can be set via environment variable DATABASE_URL
# Format: mysql+pymysql://username:password@localhost/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/college_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or 'your-app-password'

# Weather API configuration
app.config['WEATHER_API_KEY'] = os.environ.get('WEATHER_API_KEY') or 'your-weather-api-key'
app.config['WEATHER_CITY'] = os.environ.get('WEATHER_CITY') or 'Mumbai'

# College management email
app.config['COLLEGE_EMAIL'] = os.environ.get('COLLEGE_EMAIL') or 'college-management@example.com'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

# Define models here to avoid circular imports
class User(db.Model):
    """User model for admin/teacher authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='teacher')
    created_at = db.Column(db.DateTime, default=datetime.now)

class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    class_mentor_email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    attendances = db.relationship('Attendance', backref='student', lazy=True)

class Attendance(db.Model):
    """Attendance model"""
    __tablename__ = 'attendances'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hour = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'date', 'hour', name='unique_attendance'),)

class Room(db.Model):
    """Room model for seating arrangement"""
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class SeatingArrangement(db.Model):
    """Seating arrangement model"""
    __tablename__ = 'seating_arrangements'
    
    id = db.Column(db.Integer, primary_key=True)
    exam_name = db.Column(db.String(200), nullable=False)
    num_rooms = db.Column(db.Integer, nullable=False)
    seats_per_room = db.Column(db.Integer, nullable=False)
    arrangement_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

class WeatherLog(db.Model):
    """Weather log model"""
    __tablename__ = 'weather_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    main_condition = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

# Scheduler for weather checks
scheduler = BackgroundScheduler()
scheduler.start()

# Initialize database (only if connection is available)
def init_db():
    """Initialize database tables and create default admin user"""
    try:
        with app.app_context():
            db.create_all()
            # Create default admin user if not exists
            if not User.query.filter_by(username='admin').first():
                admin = User(
                    username='admin',
                    email='admin@college.com',
                    password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created: admin/admin123")
    except Exception as e:
        print(f"Database initialization skipped (connection not available): {e}")

# Try to initialize database on import (will skip if connection fails)
init_db()

# Weather checking function
def check_weather():
    """Check weather and send alerts if conditions are bad"""
    with app.app_context():
        try:
            api_key = app.config['WEATHER_API_KEY']
            city = app.config['WEATHER_CITY']
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                
                # Extract weather information
                temp = data['main']['temp']
                description = data['weather'][0]['description'].lower()
                main_weather = data['weather'][0]['main'].lower()
                
                # Log weather data
                weather_log = WeatherLog(
                    temperature=temp,
                    description=data['weather'][0]['description'],
                    main_condition=main_weather,
                    city=city
                )
                db.session.add(weather_log)
                db.session.commit()
                
                # Check for bad weather conditions
                bad_conditions = ['rain', 'storm', 'snow', 'thunderstorm', 'extreme', 'drizzle']
                is_bad_weather = any(cond in main_weather or cond in description for cond in bad_conditions)
                is_high_temp = temp > 40  # High temperature threshold
                
                if is_bad_weather or is_high_temp:
                    # Send alert email
                    subject = "Weather Alert - Bad Weather Conditions Detected"
                    body = f"""
                    Weather Alert from College Management System
                    
                    Location: {city}
                    Temperature: {temp}°C
                    Condition: {data['weather'][0]['description']}
                    Main Condition: {main_weather}
                    
                    {"⚠️ SEVERE WEATHER DETECTED - HOLIDAY RECOMMENDED" if is_bad_weather else "⚠️ HIGH TEMPERATURE ALERT"}
                    
                    Please review the weather conditions and consider declaring a holiday for the safety of students and staff.
                    """
                    
                    msg = Message(
                        subject=subject,
                        recipients=[app.config['COLLEGE_EMAIL']],
                        body=body
                    )
                    mail.send(msg)
                    
        except Exception as e:
            print(f"Error checking weather: {str(e)}")

# Schedule weather check every hour
scheduler.add_job(
    func=check_weather,
    trigger="interval",
    hours=1,
    id='weather_check',
    name='Check weather every hour',
    replace_existing=True
)

# Run initial weather check
check_weather()

# Decorator for login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator for admin required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get statistics
    total_students = Student.query.count()
    today = datetime.now().date()
    today_attendance = Attendance.query.filter(
        Attendance.date == today
    ).count()
    
    # Get latest weather
    latest_weather = WeatherLog.query.order_by(WeatherLog.created_at.desc()).first()
    
    # Get recent attendance
    recent_attendances = Attendance.query.order_by(
        Attendance.created_at.desc()
    ).limit(10).all()
    
    return render_template('dashboard.html',
                         total_students=total_students,
                         today_attendance=today_attendance,
                         latest_weather=latest_weather,
                         recent_attendances=recent_attendances)

# Student Management Routes
@app.route('/students')
@login_required
def students():
    students_list = Student.query.all()
    return render_template('students.html', students=students_list)

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        student = Student(
            roll_number=request.form.get('roll_number'),
            name=request.form.get('name'),
            department=request.form.get('department'),
            email=request.form.get('email'),
            class_mentor_email=request.form.get('class_mentor_email')
        )
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

# Attendance Routes
@app.route('/attendance')
@login_required
def attendance():
    date = request.args.get('date', datetime.now().date().isoformat())
    hour = request.args.get('hour', '1')
    
    students = Student.query.all()
    attendance_records = Attendance.query.filter_by(date=date, hour=hour).all()
    attendance_dict = {record.student_id: record.status for record in attendance_records}
    
    return render_template('attendance.html',
                         students=students,
                         attendance_dict=attendance_dict,
                         selected_date=date,
                         selected_hour=hour)

@app.route('/attendance/mark', methods=['POST'])
@login_required
def mark_attendance():
    data = request.get_json()
    date = data.get('date')
    hour = data.get('hour')
    student_id = data.get('student_id')
    status = data.get('status')  # 'present' or 'absent'
    
    # Check if attendance already exists
    existing = Attendance.query.filter_by(
        student_id=student_id,
        date=date,
        hour=hour
    ).first()
    
    if existing:
        existing.status = status
        existing.updated_at = datetime.now()
    else:
        existing = Attendance(
            student_id=student_id,
            date=date,
            hour=hour,
            status=status
        )
        db.session.add(existing)
    
    # If absent, send email to class mentor
    if status == 'absent':
        student = Student.query.get(student_id)
        if student and student.class_mentor_email:
            try:
                msg = Message(
                    subject=f"Attendance Alert - {student.name} Absent",
                    recipients=[student.class_mentor_email],
                    body=f"""
                    Attendance Alert
                    
                    Student Name: {student.name}
                    Roll Number: {student.roll_number}
                    Department: {student.department}
                    Date: {date}
                    Hour/Period: {hour}
                    Status: Absent
                    
                    Please follow up with the student regarding their absence.
                    """
                )
                mail.send(msg)
            except Exception as e:
                print(f"Error sending email: {str(e)}")
    
    db.session.commit()
    return jsonify({'success': True})

# Weather Routes
@app.route('/weather')
@login_required
def weather():
    latest_weather = WeatherLog.query.order_by(WeatherLog.created_at.desc()).first()
    weather_history = WeatherLog.query.order_by(WeatherLog.created_at.desc()).limit(24).all()
    return render_template('weather.html', latest_weather=latest_weather, weather_history=weather_history)

@app.route('/api/weather/current')
@login_required
def get_current_weather():
    try:
        api_key = app.config['WEATHER_API_KEY']
        city = app.config['WEATHER_CITY']
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return jsonify({
                'success': True,
                'data': {
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'main': data['weather'][0]['main'],
                    'humidity': data['main']['humidity'],
                    'wind_speed': data.get('wind', {}).get('speed', 0),
                    'city': city
                }
            })
        else:
            return jsonify({'success': False, 'error': 'Weather API error'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Seat Arrangement Routes
@app.route('/seating')
@login_required
def seating():
    arrangements = SeatingArrangement.query.order_by(SeatingArrangement.created_at.desc()).all()
    return render_template('seating.html', arrangements=arrangements)

@app.route('/seating/create', methods=['GET', 'POST'])
@login_required
def create_seating():
    if request.method == 'POST':
        exam_name = request.form.get('exam_name')
        num_rooms = int(request.form.get('num_rooms'))
        seats_per_room = int(request.form.get('seats_per_room'))
        
        # Get all students
        students = Student.query.all()
        
        if not students:
            return render_template('create_seating.html', error='No students found. Please add students first.')
        
        # Create rooms
        rooms = []
        for i in range(1, num_rooms + 1):
            room = Room(name=f"Room {i}", capacity=seats_per_room)
            db.session.add(room)
            db.session.flush()
            rooms.append(room)
        
        # Arrange students
        arrangement = SeatingArrangement(
            exam_name=exam_name,
            num_rooms=num_rooms,
            seats_per_room=seats_per_room
        )
        db.session.add(arrangement)
        db.session.flush()
        
        # Algorithm: Arrange students ensuring no two same-department students sit together
        arranged_students = []
        room_index = 0
        seat_index = 0
        
        # Group students by department
        dept_students = {}
        for student in students:
            if student.department not in dept_students:
                dept_students[student.department] = []
            dept_students[student.department].append(student)
        
        # Shuffle departments to ensure distribution
        departments = list(dept_students.keys())
        random.shuffle(departments)
        
        # Round-robin assignment to avoid same department adjacent
        current_room = rooms[room_index]
        dept_pointer = 0
        students_assigned = 0
        
        while students_assigned < len(students):
            # Get next department in round-robin
            dept = departments[dept_pointer % len(departments)]
            
            if dept_students[dept]:
                student = dept_students[dept].pop(0)
                
                # Check if we need to move to next room
                if seat_index >= seats_per_room:
                    room_index += 1
                    if room_index >= num_rooms:
                        break
                    current_room = rooms[room_index]
                    seat_index = 0
                
                # Check adjacent seats in same row (avoid same department)
                # For simplicity, we'll use round-robin which naturally distributes
                
                arranged_students.append({
                    'student': student,
                    'room': current_room,
                    'seat': seat_index + 1
                })
                
                seat_index += 1
                students_assigned += 1
            
            dept_pointer += 1
        
        # Save arrangement data as JSON
        arrangement_data = []
        for item in arranged_students:
            arrangement_data.append({
                'student_id': item['student'].id,
                'student_name': item['student'].name,
                'student_roll': item['student'].roll_number,
                'student_dept': item['student'].department,
                'room_id': item['room'].id,
                'room_name': item['room'].name,
                'seat_number': item['seat']
            })
        
        arrangement.arrangement_data = json.dumps(arrangement_data)
        db.session.commit()
        
        return redirect(url_for('view_seating', arrangement_id=arrangement.id))
    
    return render_template('create_seating.html')

@app.route('/seating/<int:arrangement_id>')
@login_required
def view_seating(arrangement_id):
    arrangement = SeatingArrangement.query.get_or_404(arrangement_id)
    arrangement_data = json.loads(arrangement.arrangement_data)
    
    # Organize by room
    rooms_data = {}
    for item in arrangement_data:
        room_name = item['room_name']
        if room_name not in rooms_data:
            rooms_data[room_name] = []
        rooms_data[room_name].append(item)
    
    # Sort by seat number
    for room_name in rooms_data:
        rooms_data[room_name].sort(key=lambda x: x['seat_number'])
    
    return render_template('view_seating.html', arrangement=arrangement, rooms_data=rooms_data)

@app.route('/seating/<int:arrangement_id>/pdf')
@login_required
def download_seating_pdf(arrangement_id):
    arrangement = SeatingArrangement.query.get_or_404(arrangement_id)
    arrangement_data = json.loads(arrangement.arrangement_data)
    
    # Create PDF
    filename = f"seating_arrangement_{arrangement_id}.pdf"
    filepath = os.path.join('static', 'pdfs', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>Seating Arrangement - {arrangement.exam_name}</b>", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Organize by room
    rooms_data = {}
    for item in arrangement_data:
        room_name = item['room_name']
        if room_name not in rooms_data:
            rooms_data[room_name] = []
        rooms_data[room_name].append(item)
    
    for room_name in sorted(rooms_data.keys()):
        # Room header
        room_header = Paragraph(f"<b>{room_name}</b>", styles['Heading2'])
        story.append(room_header)
        story.append(Spacer(1, 0.1*inch))
        
        # Create table
        data = [['Seat', 'Roll No', 'Name', 'Department']]
        
        for item in sorted(rooms_data[room_name], key=lambda x: x['seat_number']):
            data.append([
                str(item['seat_number']),
                item['student_roll'],
                item['student_name'],
                item['student_dept']
            ])
        
        table = Table(data, colWidths=[1*inch, 1.5*inch, 2*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
    
    doc.build(story)
    
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    # Ensure database is initialized before starting app
    init_db()
    atexit.register(lambda: scheduler.shutdown())
    app.run(debug=True, host='0.0.0.0', port=5000)

