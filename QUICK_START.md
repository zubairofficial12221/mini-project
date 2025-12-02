# Quick Start Guide

Get the College Management System up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL installed and running
- [ ] Gmail account (for email)
- [ ] OpenWeatherMap account (free)

## 5-Minute Setup

### 1. Install Dependencies (1 minute)
```bash
pip install -r requirements.txt
```

### 2. Create Database (30 seconds)
```sql
CREATE DATABASE college_management;
```

### 3. Update Database Connection (30 seconds)
Edit `app.py` line 23:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:YOUR_PASSWORD@localhost/college_management'
```

### 4. Configure Email (2 minutes)
1. Enable 2FA on Gmail
2. Generate App Password: Google Account → Security → App passwords
3. Edit `app.py` lines 25-26:
```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-16-char-app-password'
```

### 5. Get Weather API Key (1 minute)
1. Sign up at: https://openweathermap.org/api
2. Copy API key
3. Edit `app.py` line 30:
```python
app.config['WEATHER_API_KEY'] = 'your-api-key'
```

### 6. Run Application (10 seconds)
```bash
python app.py
```

### 7. Access Application
- Open: http://localhost:5000
- Login: `admin` / `admin123`

## First Steps After Login

1. **Add Students**
   - Go to Students → Add New Student
   - Add at least 2-3 students

2. **Mark Attendance**
   - Go to Attendance
   - Select date and hour
   - Mark students as present/absent

3. **Check Weather**
   - Go to Weather
   - Verify weather is displayed

4. **Create Seat Arrangement**
   - Go to Seat Arrangement → Create New
   - Enter exam details
   - Generate and download PDF

## Troubleshooting

**Database Error?**
- Check MySQL is running
- Verify username/password
- Ensure database exists

**Email Not Sending?**
- Use App Password (not regular password)
- Check 2FA is enabled
- Verify credentials in app.py

**Weather Not Loading?**
- API key may take few hours to activate
- Check internet connection
- Verify API key is correct

**PDF Not Generating?**
- Create folder: `static/pdfs/`
- Check write permissions

## Need Help?

See detailed documentation:
- `SETUP_GUIDE.md` - Complete setup instructions
- `README.md` - Project overview
- `API_ENDPOINTS.md` - API documentation

---

**You're all set! 🎉**

