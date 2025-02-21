# Baseball Analytics Application

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker
- Docker Compose
- Git

## Project Overview

This application is a Baseball Analytics platform consisting of:
- Frontend (React with Vite)
- Backend (Python FastAPI)
- PostgreSQL Database
- Ollama (Local AI Model Server)

## Setup and Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Environment Configuration

The application uses environment variables for configuration. A sample `.env` file is used with the following configuration:

```
DB_USER=baseball_admin
DB_PASSWORD=baseball_secret
DB_NAME=baseball_db
```

> **Note:** For production, replace these with your own secure credentials.

### 3. Docker Compose Setup

This project uses Docker Compose to manage multi-container deployment. The configuration includes:
- Ollama (AI Model Server)
- PostgreSQL Database
- Backend API Server
- Frontend Web Application

#### Starting the Application

To start all services:

```bash
docker-compose up --build
```

This command will:
- Build all necessary Docker images
- Start containers for each service
- Initialize the database
- Launch the application

#### Accessing the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Ollama Server: http://localhost:11434

### 4. Database Initialization

The `init-db.sh` script is automatically executed during the first database container startup to set up initial database schema and data.

### 5. Stopping the Application

To stop all running containers:

```bash
docker-compose down
```

To stop and remove volumes:

```bash
docker-compose down -v
```

## Development

### Backend (Python FastAPI)
- Located in `./server`
- Uses `uvicorn` as the ASGI server
- Dependencies managed via `requirements.txt`

### Frontend (React with Vite)
- Located in `./client`
- Uses Vite for fast development and build
- Dependencies managed via `package.json`

## Troubleshooting

- Ensure Docker and Docker Compose are up to date
- Check Docker logs for specific service issues:
  ```bash
  docker-compose logs [service-name]
  ```
- Verify all environment variables are correctly set

### Accessing PostgreSQL Database

To access the PostgreSQL database running in the Docker container via psql:

```bash
# Connect to the database container
docker-compose exec postgres psql -U baseball_admin -d baseball_db
```

Parameters:
- `-U baseball_admin`: Username from the .env file
- `-d baseball_db`: Database name from the .env file

To run specific SQL queries:
```bash
# List all tables in the database
docker-compose exec postgres psql -U baseball_admin -d baseball_db -c '\dt'

# Run a query directly (e.g., select first 5 players with specific columns)
docker-compose exec postgres psql -U baseball_admin -d baseball_db -c 'SELECT id, player_name, position, games, hits FROM players LIMIT 5;'

# List column names for the players table
docker-compose exec postgres psql -U baseball_admin -d baseball_db -c '\d players'

# Execute a SQL script
docker-compose exec postgres psql -U baseball_admin -d baseball_db -f /path/to/your/script.sql
```

Useful psql commands:
- `\dt`: List all tables
- `\d tablename`: Describe a specific table
- `\l`: List all databases
- `\c database_name`: Connect to a specific database
- `\q`: Quit psql

Note: Use `postgres` as the service name when using docker-compose exec, not `db`.

### Connecting with DBeaver

To connect to the PostgreSQL database using DBeaver, follow these steps:

1.  Create a new connection in DBeaver.
2.  Select "PostgreSQL" as the database type.
3.  Enter the following connection details:

    *   **Host:** `localhost`
    *   **Port:** `5432`
    *   **Database:** `baseball_db`
    *   **Username:** `baseball_admin`
    *   **Password:** `baseball_secret`
    *   **JDBC URL:** `jdbc:postgresql://localhost:5432/baseball_db`

4.  Test the connection to ensure it is successful.
5.  Click "Finish" to create the connection.

You should now be able to browse and query the database using DBeaver.

## Security Considerations

- Never commit sensitive information like actual database passwords to version control
- Use strong, unique passwords in production
- Consider using Docker secrets or a secure secret management system for credentials

## Contributing

Please read `ARCHITECTURE_DECISIONS.md` for insights into the project's architectural choices and development guidelines.