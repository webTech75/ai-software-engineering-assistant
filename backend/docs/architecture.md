# AI Software Engineering Assistant Architecture

## Overview

The AI Software Engineering Assistant is a modern backend application built with FastAPI that combines traditional REST APIs with a Large Language Model (LLM) to help developers understand, analyze, and manipulate software projects.

The system follows a layered architecture to separate responsibilities and improve maintainability.

---

# High-Level Architecture

```
                        React Frontend
                              │
                              ▼
                    FastAPI REST API
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
 Project Management API                      AI Chat API
        │                                           │
        ▼                                           ▼
   Service Layer                            Agent Service
        │                                           │
        ▼                                           ▼
 Repository Layer                         Tool Registry
        │                                           │
        ▼                                           ▼
  SQLAlchemy ORM                         Project Tools
        │
        ▼
     SQLite Database
```

---

# Request Lifecycle

A standard REST request follows this flow:

```
Client
   │
   ▼
FastAPI Endpoint
   │
   ▼
Service Layer
   │
   ▼
Repository
   │
   ▼
Database
   │
   ▼
Response
```

Each layer has a single responsibility.

---

# AI Request Lifecycle

AI requests use a different workflow.

```
User
 │
 ▼
POST /projects/{id}/chat
 │
 ▼
AgentService
 │
 ▼
System Prompt
 │
 ▼
Large Language Model
 │
 ▼
Needs Tool?
 │
 ├───────────────┐
 │               │
 ▼               ▼
No              Yes
 │               │
 ▼               ▼
Answer      Tool Registry
                 │
                 ▼
          Execute Tool
                 │
                 ▼
          Tool Result
                 │
                 ▼
      Continue Conversation
                 │
                 ▼
           Final Answer
```

The LLM can request one or more tools before producing its final response.

---

# Project Structure

```
backend/
│
├── alembic/
│
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

# Layer Responsibilities

## API Layer

Responsible for:

- Receiving HTTP requests
- Validating input
- Authenticating users
- Calling the appropriate service
- Returning responses

Business logic should never live in the API layer.

---

## Service Layer

Contains the application's business rules.

Responsibilities include:

- Validation
- Authorization
- Coordinating repositories
- Applying business logic

Services should not communicate directly with the database.

---

## Repository Layer

Handles all persistence operations.

Responsibilities include:

- Database queries
- Inserts
- Updates
- Deletes

Repositories contain no business logic.

---

## Database Layer

Responsible for:

- SQLAlchemy models
- Sessions
- Database engine
- Alembic migrations

---

## AI Layer

The AI layer powers the intelligent assistant.

Main components include:

- AgentService
- System Prompt
- Tool Registry
- Project Tools
- LLM Client

Unlike the REST API, the AI layer allows the language model to execute tools before answering.

---

# Tool System

The assistant can extend its capabilities using tools.

Current tools include:

- ListFilesTool
- ReadFileTool
- WriteFileTool
- DeleteFileTool

Future tools can be added without modifying the AI orchestration logic.

---

# Design Principles

The project follows several software engineering principles.

## Separation of Concerns

Each layer has a single responsibility.

---

## Dependency Injection

Dependencies are injected rather than created directly.

---

## Repository Pattern

Database access is isolated from business logic.

---

## Service Layer Pattern

Business logic remains independent of HTTP and persistence.

---

## Extensible AI

New AI capabilities can be added by registering additional tools.

---

# Future Architecture

The backend has been designed with future expansion in mind.

Planned improvements include:

- PostgreSQL
- Docker
- Redis
- Background Workers
- Vector Database
- Retrieval-Augmented Generation (RAG)
- Conversation Memory
- Git Integration
- Terminal Integration
- Code Indexing
- Multi-Agent Workflows

These features can be added with minimal changes to the existing architecture.

---

# Architecture Summary

```
                React Frontend
                       │
                       ▼
                 FastAPI Backend
                       │
      ┌────────────────┴────────────────┐
      ▼                                 ▼
 REST API                        AI Agent
      │                                 │
      ▼                                 ▼
 Services                     Tool Registry
      │                                 │
      ▼                                 ▼
Repositories                 Project Tools
      │
      ▼
 SQLAlchemy
      │
      ▼
   Database
```

The layered architecture keeps responsibilities separated, making the project easier to maintain, test, and extend as new AI capabilities are introduced.