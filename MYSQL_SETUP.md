# MySQL Database Setup & Troubleshooting Guide

## Common Error: Access Denied for user 'root'@'localhost'

This error typically occurs because:
1. MySQL root user uses socket authentication (not password)
2. Wrong password in connection string
3. Database user doesn't exist or lacks permissions

## Solution 1: Create a Dedicated Database User (Recommended)

This is the safest and most recommended approach.

### Step 1: Access MySQL

```bash
# On Linux, you might need to use sudo:
sudo mysql -u root

# Or if you have password:
mysql -u root -p
```

### Step 2: Create Database and User

```sql
-- Create the database
CREATE DATABASE college_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create a dedicated user for the application
CREATE USER 'college_user'@'localhost' IDENTIFIED BY 'your_secure_password_here';

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON college_management.* TO 'newcollege'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- Verify
SHOW GRANTS FOR 'newcollege'@'localhost';

-- Exit
EXIT;
```

### Step 3: Update app.py

Edit `app.py` line 27:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://college_user:your_secure_password_here@localhost/college_management'
```

**Or use environment variable:**

```bash
export DATABASE_URL='mysql+pymysql://college_user:your_secure_password_here@localhost/college_management'
```

---

## Solution 2: Fix Root User Authentication (For Development Only)

If you need to use root user for development:

### Step 1: Access MySQL with sudo

```bash
sudo mysql -u root
```

### Step 2: Change root authentication method

```sql
-- For MySQL 5.7+
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password_here';
FLUSH PRIVILEGES;

-- For MariaDB
UPDATE mysql.user SET plugin='mysql_native_password' WHERE User='root';
FLUSH PRIVILEGES;
```

### Step 3: Update app.py

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:your_password_here@localhost/college_management'
```

---

## Solution 3: Use Environment Variables (Recommended for Production)

### Create .env file

```bash
DATABASE_URL=mysql+pymysql://college_user:your_password@localhost/college_management
SECRET_KEY=your-secret-key-here
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
WEATHER_API_KEY=your-weather-api-key
WEATHER_CITY=Mumbai
COLLEGE_EMAIL=college-management@example.com
```

### Install python-dotenv (if not already installed)

```bash
pip install python-dotenv
```

The app.py already supports reading from environment variables!

---

## Quick Test Commands

### Test MySQL Connection

```bash
# Test connection with credentials
mysql -u college_user -p college_management

# If successful, you'll see MySQL prompt
```

### Test from Python

```python
import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='college_user',
        password='your_password',
        database='college_management'
    )
    print("Connection successful!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}")
```

---

## Common Issues & Solutions

### Issue 1: "Access denied for user 'root'@'localhost'"

**Cause**: Root user using socket authentication

**Solution**: Use Solution 1 (create dedicated user) or Solution 2 (change root auth)

---

### Issue 2: "Can't connect to local MySQL server"

**Cause**: MySQL service not running

**Solution**:

```bash
# Check MySQL status
sudo systemctl status mysql

# Start MySQL
sudo systemctl start mysql

# Enable auto-start
sudo systemctl enable mysql
```

---

### Issue 3: "Unknown database 'college_management'"

**Cause**: Database not created

**Solution**:

```sql
CREATE DATABASE college_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

### Issue 4: "Access denied" even with correct password

**Cause**: User doesn't have privileges or wrong host

**Solution**:

```sql
-- Grant privileges
GRANT ALL PRIVILEGES ON college_management.* TO 'college_user'@'localhost';
FLUSH PRIVILEGES;

-- Or grant from any host (less secure, for development only)
GRANT ALL PRIVILEGES ON college_management.* TO 'college_user'@'%';
FLUSH PRIVILEGES;
```

---

### Issue 5: "Plugin caching_sha2_password cannot be loaded"

**Cause**: PyMySQL doesn't support caching_sha2_password (MySQL 8.0+ default)

**Solution**:

```sql
-- Change user to use mysql_native_password
ALTER USER 'college_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';
FLUSH PRIVILEGES;
```

---

## Database Creation Script

Run this complete setup script:

```sql
-- 1. Create database
CREATE DATABASE IF NOT EXISTS college_management 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

-- 2. Create user
CREATE USER IF NOT EXISTS 'college_user'@'localhost' 
    IDENTIFIED BY 'change_this_password';

-- 3. Grant privileges
GRANT ALL PRIVILEGES ON college_management.* 
    TO 'college_user'@'localhost';

-- 4. Apply changes
FLUSH PRIVILEGES;

-- 5. Verify
SHOW DATABASES LIKE 'college_management';
SELECT user, host FROM mysql.user WHERE user='college_user';

-- 6. Exit
EXIT;
```

---

## Security Best Practices

1. **Never use root user in production**
   - Create dedicated application user
   - Use strong passwords

2. **Limit user privileges**
   - Only grant necessary permissions
   - Use specific database privileges

3. **Use environment variables**
   - Don't hardcode passwords in code
   - Use .env file (add to .gitignore)

4. **Regular backups**
   ```bash
   mysqldump -u college_user -p college_management > backup.sql
   ```

---

## Verification Steps

After setup, verify everything works:

```bash
# 1. Create tables
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Success!')"

# 2. Check tables created
mysql -u college_user -p college_management -e "SHOW TABLES;"

# 3. Run the application
python app.py
```

---

## Still Having Issues?

1. Check MySQL error log:
   ```bash
   sudo tail -f /var/log/mysql/error.log
   ```

2. Verify MySQL version:
   ```bash
   mysql --version
   ```

3. Check user privileges:
   ```sql
   SHOW GRANTS FOR 'college_user'@'localhost';
   ```

4. Test connection manually:
   ```bash
   mysql -u college_user -p -h localhost college_management
   ```

---

## Summary

**Best Practice for Production:**
1. Create dedicated database user
2. Use environment variables for credentials
3. Grant only necessary privileges
4. Use strong passwords
5. Regular backups

**Quick Setup Command:**
```bash
mysql -u root -p < setup_database.sql
```

Where `setup_database.sql` contains the database creation script above.

---

For more help, check the main SETUP_GUIDE.md file.

