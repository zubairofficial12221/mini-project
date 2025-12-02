"""
Test database connection with the provided credentials
"""

import pymysql
import sys

# Database connection details from your connection string
DB_CONFIG = {
    'host': 'localhost',
    'user': 'newcollege',
    'password': 'newians',
    'database': 'college_management'
}

print("Testing database connection...")
print(f"Host: {DB_CONFIG['host']}")
print(f"User: {DB_CONFIG['user']}")
print(f"Database: {DB_CONFIG['database']}")
print()

try:
    connection = pymysql.connect(**DB_CONFIG)
    print("✅ Connection successful!")
    
    # Test query
    with connection.cursor() as cursor:
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL Version: {version[0]}")
        
        cursor.execute("SHOW DATABASES LIKE 'college_management'")
        db_exists = cursor.fetchone()
        if db_exists:
            print("✅ Database 'college_management' exists")
        else:
            print("⚠️  Database 'college_management' does not exist")
            print("   You need to create it first")
    
    connection.close()
    print()
    print("✅ Database connection test passed!")
    
except pymysql.err.OperationalError as e:
    error_code, error_msg = e.args
    print(f"❌ Connection failed!")
    print(f"Error {error_code}: {error_msg}")
    print()
    
    if error_code == 1698:
        print("This usually means:")
        print("- User authentication method issue (socket auth vs password)")
        print("Solution: Use Solution 1 or 2 from MYSQL_SETUP.md")
    elif error_code == 1045:
        print("This usually means:")
        print("- Wrong username or password")
        print("- User doesn't exist")
    elif error_code == 1049:
        print("This usually means:")
        print("- Database doesn't exist")
        print("Create it: CREATE DATABASE college_management;")
    elif error_code == 2003:
        print("This usually means:")
        print("- MySQL server is not running")
        print("Start it: sudo systemctl start mysql")
    
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)

