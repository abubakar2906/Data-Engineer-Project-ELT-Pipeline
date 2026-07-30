# Data Engineer Project — ELT Pipeline

A simple example ELT pipeline that demonstrates extracting a PostgreSQL source database (schema + sample data) to a SQL dump and loading it into a destination PostgreSQL database. It includes SQL to create the source DB, a full SQL dump, and a small Python orchestration script that runs pg_dump and psql.

## Table of contents
- [What this is](#what-this-is)
- [Repository layout](#repository-layout)
- [Prerequisites](#prerequisites)
- [Quick start](#quick-start)
  - [1. Clone repository](#1-clone-repository)
  - [2. Create databases and seed source (Linux/macOS)](#2-create-databases-and-seed-source-linuxmacos)
  - [3. Run the ELT script (recommended)](#3-run-the-elt-script-recommended)
  - [Alternative: load provided dump directly](#alternative-load-provided-dump-directly)
  - [Windows notes](#windows-notes)
- [Configuration & authentication notes](#configuration--authentication-notes)
- [Troubleshooting](#troubleshooting)

## What this is
A minimal, runnable demo showing:
- A source DB schema + sample data (ELT Pipeline/source_db_init/init.sql)
- A prebuilt SQL dump (ELT Pipeline/data_dump.sql)
- A Python script that orchestrates pg_dump and psql to copy the source DB to a destination DB (ELT Pipeline/elt/elt_script.py)

## Repository layout
```
README.md
ELT Pipeline/
  data_dump.sql                # Full dump of example DB
  elt/
    elt_script.py              # Python orchestration script (pg_isready, pg_dump, psql)
    data_dump.sql              # (another copy inside elt/)
    custom_postgres/           # dbt starter project README only
    logs/                      # logs folder (empty)
  source_db_init/
    init.sql                   # Schema + seed data for the source DB
```

## Prerequisites
- PostgreSQL installed (server + client utilities: pg_dump, psql, pg_isready). Dump created with Postgres 18.1, newer versions are fine.
- Python 3.x
- Access to a shell with permission to create databases (or use a Postgres superuser)

## Quick start

### 1. Clone repository
```bash
git clone https://github.com/abubakar2906/Data-Engineer-Project-ELT-Pipeline.git
cd Data-Engineer-Project-ELT-Pipeline
```

### 2. Create databases and seed source (Linux/macOS)
Run these as a Postgres superuser (or prefix with sudo -u postgres):
```bash
createdb -U postgres source_db
createdb -U postgres destination_db

# Populate the source database with the provided init.sql
psql -U postgres -d source_db -f "ELT Pipeline/source_db_init/init.sql"
```

### 3. Run the ELT script (recommended)
The script waits for Postgres, runs pg_dump against `source_db`, and loads the dump into `destination_db`.
- Ensure pg_dump, psql, and pg_isready are available on PATH, or edit `ELT Pipeline/elt/elt_script.py` to set `pg_bin` to the PostgreSQL bin folder.

Run:
```bash
python3 "ELT Pipeline/elt/elt_script.py"
```

If the script completes, `destination_db` will contain the same schema and sample data as the source.

### Alternative: load the provided dump directly
If you just want the destination DB populated without running the Python script:
```bash
createdb -U postgres destination_db
psql -U postgres -d destination_db -f "ELT Pipeline/data_dump.sql"
```

### Windows notes
The script currently includes a Windows-style default:
```python
pg_bin = r"C:\Program Files\PostgreSQL\18\bin"
```
If you installed PostgreSQL elsewhere, update that path. From PowerShell or cmd:
```powershell
createdb -U postgres source_db
createdb -U postgres destination_db
psql -U postgres -d source_db -f "ELT Pipeline\source_db_init\init.sql"
python "ELT Pipeline\elt\elt_script.py"
```

## Configuration & authentication notes
- The script uses `-w` when calling pg_dump (no password prompt). For automation this requires either:
  - Local trust authentication for the postgres user, or
  - A configured ~/.pgpass (or %APPDATA%\postgresql\pgpass.conf on Windows), or
  - Modifying the script to set PGPASSWORD or use environment variables.
- Recommended improvements:
  - Replace hard-coded paths and credentials in `elt_script.py` with environment variables (PGHOST, PGUSER, PGPASSWORD, PGDATABASE) or a small config file.
  - Use argparse for CLI flags (source/destination connection strings) and prefer binaries on PATH first, falling back to `pg_bin`.

## Troubleshooting
- "pg_isready: command not found": ensure pg_isready is in PATH or set `pg_bin` correctly.
- Authentication errors: configure .pgpass, change pg_hba.conf to allow trusted local connections, or update the script to use secure env-based credentials.
- Permission errors creating DBs: run `createdb` as the Postgres superuser (`sudo -u postgres createdb ...`) or connect with a user that has CREATEDB privileges.

