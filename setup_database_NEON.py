"""
Neon database setup script for Estate Management System

What this script does:
1. Connects to the ESTATE_MNGT branch using the DIRECT Neon connection
2. Connects first to an existing database (usually neondb)
3. Checks whether estate_mngt_db exists
4. Creates estate_mngt_db if it does not exist
5. Optionally grants privileges to neon_superuser
6. Updates .envs/.env.local with a DATABASE_URL for estate_mngt_db

Important:
- Use the DIRECT Neon host, not the pooler host, for CREATE DATABASE
- The branch is chosen by the Neon host/endpoint you connect to
"""

import os
import sys
import getpass
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# ======== CONFIG YOU SHOULD CHANGE ========
NEON_HOST = "ep-spring-fog-a8ejnwzx.eastus2.azure.neon.tech"   # DIRECT host (no -pooler!)
NEON_PORT = 5432
NEON_USER = "neondb_owner"                          # e.g. neondb_owner
ADMIN_DB = "neondb"                                  # existing DB to connect to first
TARGET_DB = "estate_mngt_db"
ENV_FILE = "backend/.envs/.env.local"
# ==========================================


def build_database_url(user: str, password: str, host: str, port: int, dbname: str) -> str:
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}?sslmode=require"


def connect_admin(password: str):
    """
    Connect to an existing database in Neon so we can run CREATE DATABASE.
    """
    return psycopg2.connect(
        host=NEON_HOST,
        port=NEON_PORT,
        dbname=ADMIN_DB,
        user=NEON_USER,
        password=password,
        sslmode="require",
    )


def database_exists(cursor, db_name: str) -> bool:
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    return cursor.fetchone() is not None


def create_database_if_needed(cursor, db_name: str):
    if database_exists(cursor, db_name):
        print(f"✓ Database '{db_name}' already exists.")
        return False

    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
    print(f"✓ Database '{db_name}' created successfully.")
    return True


def grant_neon_superuser_if_possible(password: str, db_name: str):
    """
    Optional but useful in Neon when DB was created via SQL.
    This may fail depending on your role/permissions; if so, we just warn and continue.
    """
    try:
        conn = psycopg2.connect(
            host=NEON_HOST,
            port=NEON_PORT,
            dbname=db_name,
            user=NEON_USER,
            password=password,
            sslmode="require",
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Database-level grant
        cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO neon_superuser").format(
            sql.Identifier(db_name)
        ))

        print("✓ Granted database privileges to neon_superuser.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"⚠ Could not grant privileges to neon_superuser: {e}")
        print("  This is not always fatal for app usage. Your app may still work fine.")


def update_env_file(password: str):
    """
    Updates or appends DATABASE_URL in .envs/.env.local
    """
    database_url = build_database_url(
        user=NEON_USER,
        password=password,
        host=NEON_HOST,
        port=NEON_PORT,
        dbname=TARGET_DB,
    )

    lines = []
    found = False

    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        for line in lines:
            if line.startswith("DATABASE_URL="):
                new_lines.append(f'DATABASE_URL="{database_url}"\n')
                found = True
            else:
                new_lines.append(line)
        lines = new_lines

    if not found:
        lines.append(f'DATABASE_URL="{database_url}"\n')

    os.makedirs(os.path.dirname(ENV_FILE), exist_ok=True)
    with open(ENV_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✓ Updated {ENV_FILE} with DATABASE_URL.")


def main():
    print("=" * 70)
    print(" Estate Management System - Neon Database Setup")
    print("=" * 70)
    print(f"Target branch host : {NEON_HOST}")
    print(f"Admin database     : {ADMIN_DB}")
    print(f"Target database    : {TARGET_DB}")
    print(f"Role/user          : {NEON_USER}")
    print()

    #password = getpass.getpass("Enter Neon database password: ").strip()
    password = "npg_M0zvn2macAGV"
    if not password:
        print("✗ Password cannot be empty.")
        sys.exit(1)

    try:
        print("\nConnecting to Neon...")
        conn = connect_admin(password)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        created = create_database_if_needed(cursor, TARGET_DB)

        cursor.close()
        conn.close()

        # Optional Neon-specific grant
        grant_neon_superuser_if_possible(password, TARGET_DB)

        # Update env file for your app
        update_env_file(password)

        print("\n" + "=" * 70)
        print("Setup completed successfully.")
        print(f"Branch host   : {NEON_HOST}")
        print(f"Database name : {TARGET_DB}")
        print(f"Connect using : DATABASE_URL in {ENV_FILE}")
        print("=" * 70)

        print("\nNext steps:")
        print("1. Run migrations: python manage.py migrate")
        print("2. Create superuser: python manage.py createsuperuser")
        print("3. Start server: python manage.py runserver")

        if created:
            print("\nNote: The database was just created in the branch mapped to the host above.")

    except psycopg2.OperationalError as e:
        print(f"\n✗ Connection failed: {e}")
        print("\nCheck these:")
        print("- Host is the DIRECT host for the ESTATE_MNGT branch")
        print("- Username is correct")
        print("- Password is correct")
        print("- sslmode=require is being used")
        sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()