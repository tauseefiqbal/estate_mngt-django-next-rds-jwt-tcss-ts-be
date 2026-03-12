"""
Complete Estate Management System Setup Script
This script will:
1. Create PostgreSQL database
2. Update environment configuration
3. Run Django migrations
4. Create superuser
"""
import os
import sys
import subprocess
import getpass

def run_command(command, description, check=True):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"▶ {description}")
    print(f"{'='*60}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr and "warning" not in result.stderr.lower():
        print(result.stderr)
    if check and result.returncode != 0:
        print(f"✗ Failed: {description}")
        return False
    print(f"✓ Success: {description}")
    return True

def setup_database():
    """Setup PostgreSQL database"""
    print("\n" + "="*60)
    print(" POSTGRESQL DATABASE SETUP")
    print("="*60)
    
    # Get password
    pg_password = getpass.getpass("Enter PostgreSQL 'postgres' user password: ")
    
    if not pg_password:
        print("Trying with empty password...")
        pg_password = ""
    
    # Set environment variable for password
    os.environ['PGPASSWORD'] = pg_password
    
    psql_path = r"C:\Program Files\PostgreSQL\16\bin\psql.exe"
    
    # Try to create database
    print("\nCreating database 'estate_mngt_db'...")
    result = subprocess.run(
        f'"{psql_path}" -U postgres -c "SELECT 1 FROM pg_database WHERE datname=\'estate_mngt_db\'" -t',
        shell=True,
        capture_output=True,
        text=True
    )
    
    if "1" in result.stdout:
        print("✓ Database 'estate_mngt_db' already exists!")
    else:
        result = subprocess.run(
            f'"{psql_path}" -U postgres -c "CREATE DATABASE estate_mngt_db;"',
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ Database 'estate_mngt_db' created successfully!")
        else:
            print("✗ Failed to create database")
            print(result.stderr)
            return None
    
    # Update .env.local file
    env_file = os.path.join("backend", ".envs", ".env.local")
    print(f"\nUpdating {env_file} with database password...")
    
    try:
        with open(env_file, "r") as f:
            content = f.read()
        
        content = content.replace('POSTGRES_PASSWORD=""', f'POSTGRES_PASSWORD="{pg_password}"')
        
        with open(env_file, "w") as f:
            f.write(content)
        
        print(f"✓ Configuration file updated!")
        return pg_password
    except Exception as e:
        print(f"✗ Error updating config: {e}")
        return None

def setup_django():
    """Setup Django application"""
    print("\n" + "="*60)
    print(" DJANGO APPLICATION SETUP")
    print("="*60)
    
    # Load environment variables
    env_file = os.path.join(".envs", ".env.local")
    if os.path.exists(env_file):
        print(f"\nLoading environment from {env_file}...")
        with open(env_file, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#") and "=" in line:
                    key, value = line.strip().split("=", 1)
                    # Remove quotes from value
                    value = value.strip('"').strip("'")
                    os.environ[key] = value
        print("✓ Environment variables loaded!")
    
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        return False
    
    # Collect static files (optional)
    print("\n" + "="*60)
    print("▶ Collecting static files (optional, can skip)")
    print("="*60)
    subprocess.run("python manage.py collectstatic --noinput", shell=True)
    
    return True

def create_superuser():
    """Create Django superuser"""
    print("\n" + "="*60)
    print(" CREATE ADMIN USER")
    print("="*60)
    
    create = input("\nDo you want to create an admin superuser? (y/n): ").lower()
    if create == 'y':
        print("\nRunning interactive superuser creation...")
        subprocess.run("python manage.py createsuperuser", shell=True)
    else:
        print("Skipping superuser creation.")
        print("You can create one later with: python manage.py createsuperuser")

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print(" " * 15 + "ESTATE MANAGEMENT SYSTEM")
    print(" " * 20 + "Complete Setup Script")
    print("="*70)
    
    # Change to project directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print(f"\nWorking directory: {os.getcwd()}")
    
    # Step 1: Setup Database
    pg_password = setup_database()
    if pg_password is None:
        print("\n✗ Database setup failed. Please check your PostgreSQL configuration.")
        sys.exit(1)
    
    # Step 2: Setup Django
    if not setup_django():
        print("\n✗ Django setup failed. Please check the error messages above.")
        sys.exit(1)
    
    # Step 3: Create superuser
    create_superuser()
    
    # Final message
    print("\n" + "="*70)
    print(" " * 20 + "SETUP COMPLETED!")
    print("="*70)
    print("\n✓ Database created: estate_mngt_db")
    print("✓ Migrations completed")
    print("✓ Application is ready to use")
    print("\n" + "-"*70)
    print("Next steps:")
    print("-"*70)
    print("1. Start Redis (required for Celery):")
    print("   Download from: https://github.com/microsoftarchive/redis/releases")
    print("   Or use Docker: docker run -p 6379:6379 redis")
    print("\n2. Start development server:")
    print("   python manage.py runserver")
    print("\n3. Access admin panel:")
    print("   http://localhost:8000/admin/")
    print("\n4. Optional - Start Celery worker (in new terminal):")
    print("   celery -A config.celery_app worker -l info")
    print("\n5. Optional - Start Celery beat (in new terminal):")
    print("   celery -A config.celery_app beat -l info")
    print("\n6. Optional - Start Flower (Celery monitoring):")
    print("   celery -A config.celery_app flower")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
