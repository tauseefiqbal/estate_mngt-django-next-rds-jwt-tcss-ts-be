from pathlib import Path
from os import getenv, path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
local_env_file = path.join(BASE_DIR, "backend", ".envs", ".env.local")

print(f"Looking for env file at: {local_env_file}")
print(f"File exists: {path.isfile(local_env_file)}")

if path.isfile(local_env_file):
    result = load_dotenv(local_env_file)
    print(f"load_dotenv result: {result}")

print(f"\nPOSTGRES_HOST: {getenv('POSTGRES_HOST')}")
print(f"POSTGRES_DB: {getenv('POSTGRES_DB')}")
print(f"POSTGRES_USER: {getenv('POSTGRES_USER')}")
print(f"POSTGRES_PORT: {getenv('POSTGRES_PORT')}")
