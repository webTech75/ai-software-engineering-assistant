# Development Guide

## Overview

This guide explains how to set up the AI Software Engineering Assistant for local development.

It covers:

- Prerequisites
- Installation
- Configuration
- Database setup
- Running the application
- Coding standards
- Project structure
- Contributing

---

# Prerequisites

Before getting started, ensure the following software is installed:

- Python 3.12 or later
- Git
- SQLite
- pip
- Virtual environment support (`venv`)

Recommended:

- Visual Studio Code
- Postman (optional)
- DB Browser for SQLite (optional)

---

# Clone the Repository

```bash
git clone https://github.com/webTech75/ai-software-engineering-assistant.git

cd ai-software-engineering-assistant/backend
```

---

# Create a Virtual Environment

Linux/macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows

```powershell
python -m venv .venv

.venv\Scripts\activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the backend directory.

Example:

```env
OPENAI_API_KEY=your_openai_api_key

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

DATABASE_URL=sqlite:///./app.db

LLM_MODEL=gpt-5.6
```

Adjust values as needed for your development environment.

---

# Database Setup

Run all database migrations.

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "Describe changes"
```

Apply the migration:

```bash
alembic upgrade head
```

---

# Running the Application

Start the development server.

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

---

# API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Project Structure

```
backend/

├── alembic/
├── app/
│   ├── ai/
│   ├── agent/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── docs/
│
├── requirements.txt
│
└── README.md
```

---

# Coding Standards

The project follows these principles:

- Follow PEP 8.
- Write descriptive variable and function names.
- Keep functions focused on a single responsibility.
- Separate business logic from persistence logic.
- Prefer composition over duplication.
- Document public modules, classes, and methods.

---

# Architecture

The backend follows a layered architecture.

```
API

↓

Services

↓

Repositories

↓

Database
```

The AI subsystem follows a separate architecture.

```
Agent Service

↓

Tool Registry

↓

Project Tools
```

---

# Working with the AI Agent

The AI assistant communicates with the language model using function calling.

Project interactions are performed through registered tools.

Current capabilities include:

- List project files
- Read files
- Create files
- Modify files
- Delete files

Future tools can be added without changing the agent workflow.

---

# Git Workflow

A typical development workflow:

```bash
git checkout -b feature/my-feature

git add .

git commit -m "Add my feature"

git push origin feature/my-feature
```

Create a Pull Request after testing your changes.

---

# Testing

Before committing changes:

- Run the application.
- Verify affected endpoints.
- Confirm database migrations work.
- Test AI interactions if applicable.

Automated testing will be introduced in a future release.

---

# Troubleshooting

## Virtual environment not activated

Activate the virtual environment before installing packages.

---

## Database migration errors

Ensure all migrations have been applied.

```bash
alembic upgrade head
```

---

## OpenAI API errors

Verify:

- OPENAI_API_KEY
- Internet connection
- Model configuration

---

## Import errors

Ensure dependencies are installed.

```bash
pip install -r requirements.txt
```

---

# Contributing

Contributions are welcome.

When contributing:

- Follow the project's coding standards.
- Keep commits focused and descriptive.
- Update documentation when adding features.
- Add comments where appropriate.
- Keep the architecture modular.

---

# Future Improvements

Planned improvements to the development workflow include:

- Docker support
- PostgreSQL
- Automated testing
- GitHub Actions
- CI/CD pipeline
- Code formatting with Black
- Linting with Ruff
- Pre-commit hooks

---

# Summary

This guide provides everything needed to set up and contribute to the AI Software Engineering Assistant. As the project evolves, this document will be updated to reflect new tools, workflows, and development practices.