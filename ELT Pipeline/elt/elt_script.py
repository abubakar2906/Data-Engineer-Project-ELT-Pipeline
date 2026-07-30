import subprocess
import time
import os

def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Successfully connected to Postgres")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to Postgres: {e}")
            retries += 1
            print(f"Retrying in {delay_seconds} seconds...(Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting")
    return False

if not wait_for_postgres(host="localhost"):
    exit(1)

print("Starting ELT Script")

# Find your PostgreSQL version folder
pg_bin = r"C:\Program Files\PostgreSQL\18\bin"  # Change 18 to your version if different

source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': '',
    'host': 'localhost'
}

destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': '',
    'host': 'localhost'
}

dump_command = [
    os.path.join(pg_bin, 'pg_dump.exe'),  # Use full path
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'
]

# Don't pass empty password env if using trust auth
subprocess.run(dump_command, check=True)
print("✓ Database dumped")

load_command = [
    os.path.join(pg_bin, 'psql.exe'),  # Use full path
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-f', 'data_dump.sql',
]

subprocess.run(load_command, check=True)
print("✓ Data loaded")
print("Ending ELT Script - Success!")