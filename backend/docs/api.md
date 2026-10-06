# REST API Documentation

## Overview

The AI Software Engineering Assistant exposes a RESTful API built with FastAPI.

The API provides endpoints for:

- User authentication
- Project management
- AI-powered project interaction

All endpoints exchange data using JSON.

---

# Base URL

Development

```
http://localhost:8000/api/v1
```

Production

```
https://your-domain.com/api/v1
```

---

# Authentication

Most endpoints require authentication using a JSON Web Token (JWT).

Include the access token in the Authorization header.

```
Authorization: Bearer <access_token>
```

---

# Authentication Flow

```
Register
    │
    ▼
Login
    │
    ▼
Receive JWT
    │
    ▼
Call Protected Endpoints
```

---

# Response Format

Successful responses

```json
{
    "data": { }
}
```

or

```json
{
    "message": "Operation completed successfully."
}
```

AI responses

```json
{
    "answer": "..."
}
```

---

# Error Responses

## 400 Bad Request

```json
{
    "detail": "Invalid request."
}
```

---

## 401 Unauthorized

```json
{
    "detail": "Could not validate credentials."
}
```

---

## 403 Forbidden

```json
{
    "detail": "Access denied."
}
```

---

## 404 Not Found

```json
{
    "detail": "Resource not found."
}
```

---

## 500 Internal Server Error

```json
{
    "detail": "Unexpected server error."
}
```

---

# Authentication Endpoints

## Register User

**POST**

```
/users/register
```

### Description

Create a new user account.

### Request

```json
{
    "username": "adam",
    "email": "adam@example.com",
    "password": "password123"
}
```

### Response

```json
{
    "id": 1,
    "username": "adam",
    "email": "adam@example.com"
}
```

---

## Login

**POST**

```
/users/login
```

### Description

Authenticate a user and return a JWT.

### Request

```json
{
    "username": "amr",
    "password": "password123"
}
```

### Response

```json
{
    "access_token": "...",
    "token_type": "bearer"
}
```

---

# Project Endpoints

## Create Project

**POST**

```
/projects
```

### Description

Create a new software project.

---

## Get Projects

**GET**

```
/projects
```

### Description

Return all projects owned by the authenticated user.

---

## Get Project

**GET**

```
/projects/{project_id}
```

### Description

Retrieve a single project.

---

## Update Project

**PUT**

```
/projects/{project_id}
```

### Description

Update project information.

---

## Delete Project

**DELETE**

```
/projects/{project_id}
```

### Description

Delete a project.

---

# AI Endpoints

## Chat With Project

**POST**

```
/projects/{project_id}/chat
```

### Description

Send a natural language request to the AI assistant.

The assistant may inspect project files, execute tools, and return a project-aware response.

### Request

```json
{
    "message": "Explain the architecture."
}
```

### Response

```json
{
    "answer": "..."
}
```

---

# AI Workflow

```
Client

 │

 ▼

POST /chat

 │

 ▼

Agent Service

 │

 ▼

Large Language Model

 │

 ▼

Project Tools (if needed)

 │

 ▼

Response
```

---

# Planned Endpoints

The following endpoints are planned for future releases.

## Project Files

```
POST   /projects/{id}/upload

POST   /projects/{id}/upload-folder

GET    /projects/{id}/files

GET    /projects/{id}/files/{path}

DELETE /projects/{id}/files/{path}
```

---

## Project Analysis

```
POST /projects/{id}/scan

POST /projects/{id}/search

POST /projects/{id}/summarize

POST /projects/{id}/document
```

---

## AI Features

```
POST /projects/{id}/explain

POST /projects/{id}/refactor

POST /projects/{id}/uml

POST /projects/{id}/review
```

---

# API Versioning

The API uses URL versioning.

Current version

```
/api/v1
```

Future versions

```
/api/v2
```

Breaking changes will be introduced through new API versions to preserve backward compatibility.

---

# Interactive Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

These interfaces allow developers to explore and test every endpoint directly from the browser.

---

# Design Principles

The API follows standard REST conventions.

- Resource-oriented endpoints
- JSON request and response bodies
- Stateless authentication
- Consistent HTTP status codes
- JWT-secured endpoints
- Versioned API structure

---

# Summary

The REST API serves as the communication layer between the frontend and backend.

It provides secure access to authentication, project management, and AI-powered software engineering capabilities while remaining easy to extend as new features are introduced.