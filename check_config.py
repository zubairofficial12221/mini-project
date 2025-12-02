"""
Simple script to check application configuration without connecting to database
"""

import os
import sys

# Get database URI from environment or default
database_url = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/college_management'

print("=" * 60)
print("Database Configuration")
print("=" * 60)
print(f"Database URI: {database_url}")
print()

# Parse connection details
try:
    # Format: mysql+pymysql://username:password@host/database
    if '@' in database_url:
        protocol, rest = database_url.split('://')
        if ':' in rest.split('@')[0]:
            user_pass, host_db = rest.split('@')
            if ':' in user_pass:
                username, password = user_pass.split(':')
                print(f"Username: {username}")
                print(f"Password: {'*' * len(password) if password else 'Not set'}")
        if '/' in host_db:
            host, database = host_db.split('/', 1)
            print(f"Host: {host}")
            print(f"Database: {database}")
except:
    pass

print()
print("=" * 60)
print("To update the database URI:")
print("1. Edit app.py line 28")
print("2. Or set environment variable: DATABASE_URL")
print("=" * 60)

