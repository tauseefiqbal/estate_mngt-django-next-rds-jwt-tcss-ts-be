import psycopg2
from dotenv import load_dotenv
from os import getenv, path

# Load environment variables
BASE_DIR = path.dirname(path.abspath(__file__))
local_env_file = path.join(BASE_DIR, "backend", ".envs", ".env.local")
load_dotenv(local_env_file)

print("Testing Neon Database Connection...")
print("=" * 60)

# Get credentials
host = getenv("POSTGRES_HOST")
port = getenv("POSTGRES_PORT")
database = getenv("POSTGRES_DB")
user = getenv("POSTGRES_USER")
password = getenv("POSTGRES_PASSWORD")

print(f"Host: {host}")
print(f"Port: {port}")
print(f"Database: {database}")
print(f"User: {user}")
print(f"Password: {'*' * len(password) if password else 'NOT SET'}")
print("=" * 60)

try:
    print("\nAttempting to connect...")
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        sslmode='require',
        connect_timeout=10
    )
    
    print("✓ Connection successful!")
    
    # Test query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"\nPostgreSQL version: {version[0]}")
    
    cursor.close()
    conn.close()
    print("\n✓ Database is ready for migrations!")
    
except psycopg2.OperationalError as e:
    print(f"\n✗ Connection failed!")
    print(f"Error: {e}")
    print("\nPossible causes:")
    print("1. Database is suspended - Visit https://console.neon.tech to wake it up")
    print("2. Network/firewall blocking the connection")
    print("3. Invalid credentials")
    print("\nTo wake up your Neon database:")
    print("  - Go to https://console.neon.tech")
    print("  - Click on your project")
    print("  - The database will automatically wake up")
    print("  - Then run this script again")
    
except Exception as e:
    print(f"\n✗ Unexpected error: {e}")
