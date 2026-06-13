# 🚗 Vehicle Parking Management System — Version 2

An API-driven full-stack Vehicle Parking Management System with a VueJS frontend, Flask RESTful backend, Redis caching, and Celery background jobs. This version is a redesigned, scalable upgrade over V1.

---

## 🔗 Repository

[Vehicle_Parking_v2](https://github.com/24dp1000047/Vehicle_Parking_v2)
🌐 [Live Demo](https://vehicle-parking-v2-1.onrender.com)

> 🔁 **Previous Version:** [Vehicle_Parking_App (V1)](https://github.com/24dp1000047/Vehicle_Parking_App) — Server-side Flask + Jinja2

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (RESTful API) |
| Frontend | VueJS + Bootstrap |
| Database | SQLite |
| Caching | Redis |
| Background Jobs | Celery |
| Authentication | JWT / Token-based |

---

## ✨ Features

- 🔐 **Role-Based Access Control (RBAC)** with API-based authentication
- ⚡ **Redis caching** for improved performance and faster response times
- 📬 **Celery background jobs** for reminder notifications and monthly reports
- 🔄 **Asynchronous workflows** for report generation and data processing
- 🌐 **RESTful API** backend with complete frontend-backend separation
- 🖥️ Modern **VueJS** single-page application frontend
- 📊 Admin and user dashboards for parking management

---

## 🏗️ Architecture

```
Frontend (VueJS)  ←──→  Backend (Flask REST API)  ←──→  SQLite DB
                                  ↕
                          Redis (Cache)
                                  ↕
                        Celery (Background Jobs)
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- Redis

### Backend Setup

```bash
git clone https://github.com/24dp1000047/Vehicle_Parking_v2
cd Vehicle_Parking_v2/backend
pip install -r requirements.txt
flask run
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Redis & Celery

```bash
# Terminal 1 — Start Redis
redis-server

# Terminal 2 — Start Celery worker
celery -A app.celery worker --loglevel=info
```

---

## 📁 Project Structure

```
Vehicle_Parking_v2/
├── backend/
│   ├── application/          # Core app modules
│   ├── instance/             # SQLite DB instance
│   ├── app.py
│   └── celerybeat-schedule   # Celery periodic task schedule
└── frontend/
    ├── src/                  # VueJS source code
    ├── dist/                 # Production build
    ├── public/
    ├── index.html
    ├── vite.config.js
    ├── package.json
    └── package-lock.json
```

---

## 👤 Author

**24dp1000047**  
[GitHub Profile](https://github.com/24dp1000047)

---
