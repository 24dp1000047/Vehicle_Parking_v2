# 🚗 Vehicle Parking Management System — Version 2

An API-driven full-stack Vehicle Parking Management System built using Flask, Vue.js, Redis, and Celery. This version is a scalable redesign of V1 with a modern frontend, RESTful APIs, caching, background task processing, and dynamic parking fee calculation.

---

## 🎥 Application Demo

Watch the complete project demonstration here:

🔗 Demo Video: https://drive.google.com/file/d/1jqcUi-PMO9QFKCfTsKEv-WxJWQ0F4Qua/view?usp=sharing

### Features Demonstrated

* User Registration & Login
* JWT Authentication
* Role-Based Access Control (Admin/User)
* Parking Lot & Parking Spot Management
* Vehicle Reservation System
* Dynamic Parking Fee Calculation
* Admin Dashboard
* User Dashboard
* Redis Caching
* Celery Background Jobs
* Monthly Report Generation
* REST API Integration with Vue.js Frontend

---

## 🔗 Repository

GitHub Repository:

https://github.com/24dp1000047/Vehicle_Parking_v2

🔁 Previous Version:

Vehicle_Parking_App (V1) — Flask + Jinja2 Server-Side Architecture

---

## 📦 Tech Stack

| Layer           | Technology         |
| --------------- | ------------------ |
| Backend         | Flask REST API     |
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
* Secure user login and registration
* Role-Based Access Control (RBAC)
* Separate Admin and User dashboards

### 🚗 Parking Management

* Create and manage parking lots
* Automatic parking spot allocation
* Vehicle reservation system
* Parking history tracking
* Real-time parking occupancy management

### 💰 Dynamic Parking Fee Calculation

* Automatic entry timestamp recording during reservation
* Exit timestamp recording during vehicle release
* Real-time parking duration calculation
* Dynamic parking charge computation based on parking lot rates
* Accurate billing and fee tracking
* Reservation-wise parking cost history

### 📊 Dashboard & Reports

* Admin Dashboard
* User Dashboard
* Parking usage statistics
* Reservation history
* Monthly activity reports

### ⚡ Performance Optimization

* Redis caching for frequently accessed data
* Faster API response times
* Reduced database load
* Optimized backend performance

### 📬 Background Processing

* Celery background workers
* Automated reminder notifications
* Monthly report generation
* Asynchronous task execution



### 🌐 RESTful Architecture

* Complete frontend-backend separation
* REST API communication
* Modern Vue.js frontend
* Component-based user interface
* Dynamic client-side routing
* Scalable and maintainable architecture


## 🏗️ System Architecture

```text
Vue.js Frontend (SPA)
           │
           ▼
Flask REST API Backend
           │
           ▼
       SQLite DB
           │
 ┌─────────┴─────────┐
 ▼                   ▼
Redis Cache     Celery Workers
```

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

This project helped me gain practical experience in:

* Full Stack Development
* Flask REST API Development
* Vue.js Single Page Applications
* JWT Authentication
* Role-Based Access Control (RBAC)
* Redis Caching
* Celery Task Queues
* Database Design
* Asynchronous Processing
* Dynamic Fee Calculation Logic
* System Architecture Design
* Frontend-Backend Integration

---

## 👨‍💻 Author

**Prateek Sharma**

📧 [24dp1000047@ds.study.iitm.ac.in](mailto:24dp1000047@ds.study.iitm.ac.in)

🔗 GitHub: https://github.com/24dp1000047

