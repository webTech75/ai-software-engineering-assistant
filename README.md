<h1 align="center">🤖 AI Software Engineering Assistant</h1>

<p align="center">
Build • Analyze • Improve • Document Software with AI
</p>

<p align="center">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&pause=1000&center=true&vCenter=true&width=900&lines=AI+Software+Engineering+Assistant;FastAPI+Backend;Clean+Architecture;JWT+Authentication;Project+Management;AI+Code+Analysis+Coming+Soon!" />
</p>

---

<p align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)

![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

![Alembic](https://img.shields.io/badge/Alembic-Migrations-orange)

![JWT](https://img.shields.io/badge/JWT-Authentication-success)

![SQLite](https://img.shields.io/badge/SQLite-Database-blue)

![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen)

</p>

---

# 📖 Overview

AI Software Engineering Assistant is a modern backend application built with **FastAPI** following clean software architecture principles.

The goal of this project is to provide developers with an intelligent assistant capable of:

- Managing software projects
- Uploading source code
- Understanding software architecture
- Analyzing code using AI
- Detecting bugs
- Suggesting improvements
- Generating documentation
- Assisting developers throughout the software development lifecycle

---

# ✨ Current Features

## 🔐 Authentication

- ✅ User Registration
- ✅ User Login
- ✅ JWT Authentication
- ✅ Password Hashing (bcrypt)
- ✅ Protected API Endpoints

---

## 📂 Project Management

- ✅ Create Project
- ✅ Get All Projects
- ✅ Get Project by ID
- ✅ Update Project
- ✅ Delete Project

---

## 🗄 Database

- ✅ SQLAlchemy ORM
- ✅ Alembic Migrations
- ✅ SQLite (Development)

---

## 🏗 Software Architecture

- ✅ Repository Pattern
- ✅ Service Layer
- ✅ Dependency Injection
- ✅ REST API
- ✅ Clean Architecture

---

# 🚀 Technology Stack

| Backend | Database | Security | Tools |
|----------|----------|----------|-------|
| FastAPI | SQLite | JWT | Git |
| SQLAlchemy | Alembic | Passlib | GitHub |
| Python 3.12 | ORM | OAuth2 | Swagger UI |

---

# 🏛 Architecture

```
                Frontend (Coming Soon)
                         │
                         ▼
                 FastAPI Backend
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
 Authentication     Project API      AI Engine
        ▼                ▼                ▼
             SQLAlchemy ORM
                    │
                    ▼
                 SQLite
```

---

# 📂 Project Structure

```
backend/
│
├── alembic/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── requirements.txt
└── .env.example
```

---

# 📡 API Endpoints

## 👤 Users

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /users/register | Register a new user |
| POST | /users/login | Login and receive JWT |

---

## 📁 Projects

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | /projects | Create Project |
| GET | /projects | Get All Projects |
| GET | /projects/{id} | Get Project by ID |
| PUT | /projects/{id} | Update Project |
| DELETE | /projects/{id} | Delete Project |

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/webTech75/ai-software-engineering-assistant.git
```

---

## Navigate to Backend

```bash
cd ai-software-engineering-assistant/backend
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file using the provided `.env.example`.

---

## Run Database Migrations

```bash
alembic upgrade head
```

---

## Start the Server

```bash
uvicorn app.main:app --reload
```

---

## Swagger API

```
http://127.0.0.1:8000/docs
```

---

# 🚧 Roadmap

## ✅ Phase 1

- [x] User Authentication
- [x] JWT Authentication
- [x] Project CRUD
- [x] SQLAlchemy ORM
- [x] Alembic Migrations

---

## 🚀 Phase 2

- [ ] File Upload
- [ ] ZIP Extraction
- [ ] Source Code Storage
- [ ] Project File Management

---

## 🤖 Phase 3

- [ ] AI Code Analysis
- [ ] Explain Source Code
- [ ] Bug Detection
- [ ] Refactoring Suggestions
- [ ] Documentation Generator
- [ ] UML Diagram Generation

---

## 🌐 Phase 4

- [ ] React Frontend
- [ ] Docker
- [ ] PostgreSQL
- [ ] Automated Testing
- [ ] CI/CD
- [ ] Cloud Deployment

---

# 🎯 Learning Objectives

This project demonstrates practical experience with:

- FastAPI
- SQLAlchemy
- Alembic
- JWT Authentication
- OAuth2
- Clean Architecture
- Repository Pattern
- Service Layer
- REST APIs
- AI Integration
- Modern Backend Development

---

# 🌟 Future Vision

The long-term vision is to transform this application into a complete AI Software Engineering Assistant capable of helping developers understand, improve, and maintain software projects using Large Language Models.

Future capabilities include:

- 📂 Upload an entire software project
- 🤖 Chat with your codebase
- 🐞 Detect bugs automatically
- 📖 Generate technical documentation
- 🏛 Explain software architecture
- 📊 Generate UML diagrams
- ✨ Recommend best practices
- 🚀 Improve code quality

---

# 👨‍💻 Author

Developed by **Amr Elhabbal**

---

<p align="center">

⭐ If you like this project, consider giving it a star!

🚀 More exciting AI features coming soon.

</p>