# EmbedGuard Safety

EmbedGuard is a DevSecOps-style static code analysis platform for **C/C++ projects**.

It scans source code for potential vulnerabilities using **Cppcheck**, processes tasks asynchronously using **Celery + Redis**, and stores results in **PostgreSQL**.

The system supports scanning:

* Single C/C++ files
* Entire projects (ZIP upload)
* (Upcoming) GitHub repositories

---

# Features

* Static code analysis for C/C++
* Asynchronous analysis pipeline
* File hash caching to avoid duplicate scans
* Project ZIP scanning
* Dockerized architecture
* Database-backed issue tracking

---

# Architecture

```
Client
   │
   ▼
FastAPI API
   │
   ├── File hashing (SHA256)
   │
   ▼
PostgreSQL
   │
   ▼
Redis Queue
   │
   ▼
Celery Worker
   │
   ▼
Cppcheck Analyzer
   │
   ▼
Store vulnerabilities
```

---

# Tech Stack

* FastAPI
* Celery
* Redis
* PostgreSQL
* Alembic
* Docker
* Cppcheck

---

# Project Structure

```
embedguard-safety/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── analyze.py
│   │   │
│   │   ├── core/
│   │   │   ├── database.py
│   │   │   └── celery_app.py
│   │   │
│   │   ├── models/
│   │   │   ├── analysis.py
│   │   │   └── issue.py
│   │   │
│   │   ├── tasks/
│   │   │   └── analyze_task.py
│   │   │
│   │   └── main.py
│   │
│   ├── alembic/
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
└── README.md
```

---

# API Endpoints

## Upload and analyze a single file

```
POST /analyze
```

Upload `.c` or `.cpp` files.

---

## Scan an entire project

```
POST /analyze/project
```

Upload a `.zip` project containing C/C++ source files.

---

## Retrieve analysis results

```
GET /analyze/{analysis_id}
```

Returns detected vulnerabilities.

---

# Run the Project

Start the full system:

```
docker-compose up --build
```

Open API documentation:

```
http://localhost:8000/docs
```

---

# Example Workflow

1. Upload a file or project
2. Task is queued in Redis
3. Celery worker runs Cppcheck
4. Issues are stored in PostgreSQL
5. Results can be retrieved via API

---

# Future Improvements

* GitHub repository scanning
* Security scoring engine
* Web dashboard
* CI/CD integration
* AI vulnerability explanations

---

# Author

Mohamed Drissi
