#!/bin/bash
set -e

# Check if the database exists
if ! psql -U "$POSTGRES_USER" -lqt | cut -d \| -f 1 | grep -qw "${DB_NAME:-baseball}"; then
    # Create the database if it doesn't exist
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
        CREATE DATABASE ${DB_NAME:-baseball} OWNER baseball_admin;
EOSQL
fi

# Create the user and grant privileges
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
    -- Create the user if it doesn't exist
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'baseball_admin') THEN
            CREATE USER baseball_admin WITH PASSWORD '${DB_PASSWORD}';
        END IF;
    END \$\$;

    -- Grant privileges
    \\c ${DB_NAME:-baseball}
    -- Grant all privileges on the database to the user
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME:-baseball} TO baseball_admin;

    -- Grant all privileges on the public schema
    GRANT ALL PRIVILEGES ON SCHEMA public TO baseball_admin;

    -- Grant all privileges on all tables in the public schema
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO baseball_admin;

    -- Grant all privileges on all sequences in the public schema
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO baseball_admin;

    -- Grant all privileges on all functions in the public schema
    GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO baseball_admin;
EOSQL