# 🚗 Vehicle Parking Management System — Version 2

An API-driven full-stack Vehicle Parking Management System built using Flask, Vue.js, Redis, and Celery. This version is a scalable redesign of V1 with a modern frontend, RESTful APIs, caching, and background task processing.

## 🎥 Application Demo

Watch the complete project demonstration here:

🔗 Demo Video: https://drive.google.com/file/d/1jqcUi-PMO9QFKCfTsKEv-WxJWQ0F4Qua/view?usp=sharing

### Features Demonstrated

* User Registration & Login
* JWT Authentication
* Role-Based Access Control (Admin/User)
* Parking Lot & Parking Spot Management
* Vehicle Reservation System
* Admin Dashboard
* User Dashboard
* Redis Caching
* Celery Background Jobs
* Monthly Report Generation
* REST API Integration with VueJS Frontend

---

## 🔗 Repository

GitHub Repository:
https://github.com/24dp1000047/Vehicle_Parking_v2

🔁 Previous Version:
Vehicle_Parking_App (V1) — Server-side Flask + Jinja2 Architecture

---

## 📦 Tech Stack

| Layer           | Technology         |
| --------------- | ------------------ |
| Backend         | Flask (REST API)   |
| Frontend        | Vue.js, Bootstrap  |
| Database        | SQLite             |
| Authentication  | JWT Authentication |
| Caching         | Redis              |
| Background Jobs | Celery             |
| Version Control | Git, GitHub        |

---

## ✨ Key Features

### 🔐 Authentication & Authorization

* JWT-based authentication
* Secure login and registration
* Role-Based Access Control (RBAC)
* Separate Admin and User access levels

### 🚗 Parking Management

* Parking lot management
* Parking spot allocation
* Vehicle reservation system
* Parking history tracking
* Automatic parking fee calculation

### 📊 Dashboard & Reporting

* Admin Dashboard
* User Dashboard
* Parking utilization insights
* Monthly activity reports

### ⚡ Performance Optimization

* Redis caching for frequently accessed data
* Faster API response times
* Optimized database interactions

### 📬 Background Processing

* Celery background workers
* Automated reminder notifications
* Monthly report generation
* Asynchronous task execution

---

## 🏗️ System Architecture

Frontend (Vue.js SPA)
⬇
Flask REST API Backend
⬇
SQLite Database

↕ Redis Cache

↕ Celery Background Jobs

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8+
* Node.js 16+
* Redis Server
* Git

---

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

### Redis & Celery Setup

Start Redis:

```bash
redis-server
```

Start Celery Worker:

```bash
celery -A app.celery worker --loglevel=info
```

---

## 📁 Project Structure

```text
Vehicle_Parking_v2/
│
├── backend/
│   ├── application/
│   ├── instance/
│   ├── app.py
│   └── celerybeat-schedule
│
└── frontend/
    ├── src/
    ├── public/
    ├── dist/
    ├── index.html
    ├── package.json
    ├── package-lock.json
    └── vite.config.js
```

---

## 🎯 Learning Outcomes

This project helped me gain hands-on experience with:

* Full Stack Development
* REST API Design
* JWT Authentication
* Role-Based Access Control
* Vue.js Single Page Applications
* Redis Caching
* Celery Task Queues
* Database Design
* Asynchronous Processing
* Software Architecture

---

## 👨‍💻 Author

Prateek Sharma

GitHub:
https://github.com/24dp1000047

Email:
[24dp1000047@ds.study.iitm.ac.in](mailto:24dp1000047@ds.study.iitm.ac.in)
