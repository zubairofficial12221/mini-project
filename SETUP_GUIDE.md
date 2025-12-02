# Step-by-Step Setup Guide

This guide will help you set up the Student Attendance & College Management System from scratch.

## Prerequisites

Before starting, ensure you have the following installed:

- **Python 3.8 or higher**
- **MySQL Server 5.7 or higher**
- **pip** (Python package installer)
- **Git** (optional, for cloning repository)

## Step 1: Install Python Dependencies

1. Open terminal/command prompt in the project directory
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
3. Activate virtual environment:
   - **Windows**: `venv\Scripts\activate`
   - **Linux/Mac**: `source venv/bin/activate`
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Set Up MySQL Database

1. **Start MySQL Server**
   - Windows: Start MySQL service from Services
   - Linux: `sudo systemctl start mysql`
   - Mac: `brew services start mysql`

2. **Access MySQL**
   ```bash
   mysql -u root -p
   ```

3. **Create Database**
   ```sql
   CREATE DATABASE college_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

4. **Create Database User (Optional but recommended)**
   ```sql
   CREATE USER 'college_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON college_management.* TO 'college_user'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```

## Step 3: Configure Database Connection

Edit `app.py` and update the database connection string:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/college_management'
```

Replace:
- `username` with your MySQL username (e.g., `root` or `college_user`)
- `password` with your MySQL password
- `localhost` if your MySQL is on a different host

## Step 4: Set Up Email Configuration (Gmail)

### Option A: Using Environment Variables (Recommended)

1. Create a `.env` file in the project root:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   COLLEGE_EMAIL=college-management@example.com
   WEATHER_API_KEY=your-weather-api-key
   WEATHER_CITY=Mumbai
   ```

2. Get Gmail App Password:
   - Go to your Google Account settings
   - Enable 2-Factor Authentication
   - Go to Security → App passwords
   - Generate a new app password for "Mail"
   - Use this 16-character password in `MAIL_PASSWORD`

### Option B: Direct Configuration in app.py

Update these lines in `app.py`:
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['COLLEGE_EMAIL'] = 'college-management@example.com'
```

## Step 5: Get OpenWeatherMap API Key

1. **Sign Up**: Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. **Create Account**: Sign up for a free account
3. **Get API Key**: 
   - Navigate to API keys section
   - Copy your API key
   - Add to `.env` file or `app.py`:
   ```python
   app.config['WEATHER_API_KEY'] = 'your-api-key-here'
   ```
4. **Set City**: Update the city name:
   ```python
   app.config['WEATHER_CITY'] = 'YourCity'
   ```

## Step 6: Initialize Database Tables

1. The application will automatically create tables on first run
2. Alternatively, you can run:
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

3. **Verify Tables Created**:
   ```sql
   USE college_management;
   SHOW TABLES;
   ```
   You should see:
   - users
   - students
   - attendances
   - rooms
   - seating_arrangements
   - weather_logs

## Step 7: Create Required Directories

Create directories for static files:
```bash
mkdir -p static/pdfs
```

Or manually create:
- `static/pdfs/` folder (for generated PDF files)

## Step 8: Run the Application

1. **Start Flask Application**:
   ```bash
   python app.py
   ```

2. **Access Application**:
   - Open browser
   - Navigate to: `http://localhost:5000`
   - Default login credentials:
     - Username: `admin`
     - Password: `admin123`

## Step 9: Initial Setup in Application

1. **Login** with default admin credentials
2. **Add Students**:
   - Go to Students → Add New Student
   - Add at least a few students with:
     - Roll number
     - Name
     - Department
     - Class mentor email (for absence notifications)

3. **Test Attendance**:
   - Go to Attendance
   - Select date and hour
   - Mark attendance for students

4. **Test Weather**:
   - Go to Weather section
   - Verify current weather is displayed
   - Check weather history

5. **Test Seat Arrangement**:
   - Go to Seat Arrangement → Create New
   - Enter exam name, number of rooms, seats per room
   - Generate seating arrangement
   - Download PDF

## Step 10: Change Default Admin Password

1. For production, change the default admin password:
   - Option 1: Directly in database:
     ```sql
     UPDATE users SET password = '<hashed_password>' WHERE username = 'admin';
     ```
   - Option 2: Create a script to hash new password:
     ```python
     from flask_bcrypt import Bcrypt
     bcrypt = Bcrypt()
     print(bcrypt.generate_password_hash('new_password').decode('utf-8'))
     ```

## Troubleshooting

### Issue: Cannot connect to MySQL

**Solution**:
- Verify MySQL is running
- Check username/password
- Ensure database `college_management` exists
- Check if PyMySQL is installed: `pip install PyMySQL`

### Issue: Email not sending

**Solution**:
- Verify Gmail app password (not regular password)
- Check 2FA is enabled on Gmail
- Ensure `MAIL_USERNAME` and `MAIL_PASSWORD` are correct
- Check firewall/antivirus isn't blocking SMTP

### Issue: Weather API not working

**Solution**:
- Verify API key is correct
- Check API key is activated (may take a few hours)
- Ensure internet connection
- Verify city name is correct

### Issue: PDF generation fails

**Solution**:
- Ensure `static/pdfs/` directory exists
- Check write permissions on directory
- Verify ReportLab is installed: `pip install reportlab`

### Issue: Tables not creating

**Solution**:
- Check database connection
- Verify user has CREATE privileges
- Manually run: `db.create_all()` in Python shell

## Production Deployment

For production deployment:

1. **Change Secret Key**:
   ```python
   app.config['SECRET_KEY'] = os.urandom(32)
   ```

2. **Use Environment Variables** for all sensitive data

3. **Disable Debug Mode**:
   ```python
   app.run(debug=False)
   ```

4. **Use Production WSGI Server** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

5. **Set Up Reverse Proxy** (Nginx) for better performance

6. **Configure HTTPS** with SSL certificate

7. **Regular Backups** of MySQL database

## Additional Configuration

### Customize Weather Check Interval

Edit in `app.py`:
```python
scheduler.add_job(
    func=check_weather,
    trigger="interval",
    hours=1,  # Change to desired interval
    ...
)
```

### Customize Bad Weather Thresholds

Edit `check_weather()` function in `app.py`:
```python
is_high_temp = temp > 40  # Change threshold
```

### Add More Departments

Edit `add_student.html` template to add more department options.

## Support

If you encounter any issues:
1. Check error logs in terminal
2. Verify all prerequisites are installed
3. Check database connection
4. Verify API keys and credentials
5. Review troubleshooting section above

## Next Steps

After setup:
1. Add all students
2. Configure class mentor emails
3. Set up email notifications
4. Test all features
5. Train staff on using the system

Happy managing! 🎓

