"""
Database setup script for Estate Management System
This script creates the PostgreSQL database if it doesn't exist.
"""
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    # Get password from user
    password = input("Enter PostgreSQL 'postgres' user password: ").strip()
    
    if not password:
        print("Password cannot be empty!")
        sys.exit(1)
    
    db_name = "estate_mngt_db"
    
    try:
        # Connect to PostgreSQL server
        print(f"\nConnecting to PostgreSQL server...")
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password=password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", (db_name,)
        )
        exists = cursor.fetchone()
        
        if exists:
            print(f"✓ Database '{db_name}' already exists!")
        else:
            # Create database
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )
            print(f"✓ Database '{db_name}' created successfully!")
        
        cursor.close()
        conn.close()
        
        # Update .env.local file with password
        print(f"\nUpdating .env.local file with database password...")
        env_file = "backend/.envs/.env.local"
        with open(env_file, "r") as f:
            content = f.read()
        
        # Replace empty password with actual password
        content = content.replace('POSTGRES_PASSWORD=""', f'POSTGRES_PASSWORD="{password}"')
        
        with open(env_file, "w") as f:
            f.write(content)
        
        print(f"✓ Configuration file updated!")
        print(f"\n{'='*60}")
        print(f"Database setup completed successfully!")
        print(f"Database Name: {db_name}")
        print(f"Host: localhost")
        print(f"Port: 5432")
        print(f"User: postgres")
        print(f"{'='*60}")
        print(f"\nNext steps:")
        print(f"1. Run migrations: python manage.py migrate")
        print(f"2. Create superuser: python manage.py createsuperuser")
        print(f"3. Start server: python manage.py runserver")
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ Connection failed: {e}")
        print("\nPlease check:")
        print("- PostgreSQL service is running")
        print("- Password is correct")
        print("- PostgreSQL is listening on localhost:5432")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("="*60)
    print(" Estate Management System - Database Setup")
    print("="*60)
    create_database()
