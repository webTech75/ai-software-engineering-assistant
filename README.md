# 🤖 Neura
## AI Software Engineering Agent

<p align="center">
  <img src="docs/assets/neura_icon.png" width="120" alt="Neura Logo">
</p>
<!-- <p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=48&duration=3000&pause=1000&center=true&vCenter=true&width=600&lines=Neura" alt="Neura">
</p> -->
<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=24&duration=3500&pause=900&center=true&vCenter=true&width=900&lines=Neura;AI+Software+Engineering+Agent;Your+AI+Engineering+Partner+That+Understands+Your+Codebase;Analyze+Software+Projects;Generate+Documentation;Explain+Architecture;AI-Powered+Software+Engineering;Powered+by+Meta+AI+Muse+Spark+1.3" alt="Neura Typing Animation">
</p>

<h3 align="center">
Your AI Engineering Partner That Understands Your Codebase
</h3>

<p align="center">
Hackathon version powered by <b>Meta Muse Spark AI</b> for the Meta AI Developer Hackathon 2026
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AI-Meta%20Muse-blue">
  <img src="https://img.shields.io/badge/Backend-FastAPI-green">
  <img src="https://img.shields.io/badge/Frontend-React-blue">
  <img src="https://img.shields.io/badge/Language-Python-yellow">
  <img src="https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/website?url=https%3A%2F%2Fneura-g8wk.onrender.com%2Fhealth&label=backend&up_message=online&down_message=sleeping">
</p>

<p align="center">
  <a href="https://neura-client.onrender.com/"><img src="https://img.shields.io/badge/🌐_Live_Demo-Open_App-brightgreen?style=for-the-badge"></a>
  <a href="https://www.youtube.com/watch?v=kV16cjZw4ok"><img src="https://img.shields.io/badge/▶️_Demo_Video-Watch-red?style=for-the-badge"></a>
  <a href="https://neura-g8wk.onrender.com/health"><img src="https://img.shields.io/badge/💚_Wake_Backend-Health_Check-blue?style=for-the-badge"></a>
</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-demo">Demo</a> •
  <a href="#-problem">Problem</a> •
  <a href="#-solution">Solution</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-screenshots">Screenshots</a>
</p>

---

## 🚀 Overview

Neura is an AI-powered software engineering agent that helps developers understand, analyze, and interact with software projects using natural language.

Powered by **Meta Muse AI**, Neura combines a large language model with a secure AI Agent architecture that allows developers to communicate with their codebase.

Instead of only answering questions from general knowledge, Neura can understand uploaded projects, analyze source code, inspect files, and assist developers with engineering tasks.

Neura transforms AI from a chatbot into a **project-aware engineering partner**.

---

## 🎥 Demo

▶️ **Demo Video**

[![Neura Demo](https://img.youtube.com/vi/kV16cjZw4ok/maxresdefault.jpg)](https://www.youtube.com/watch?v=kV16cjZw4ok)

🌐 **Live Application:** https://neura-client.onrender.com/

<details>
<summary><b>⚙️ Deployment notes (read before trying the live app)</b></summary>

<br>

Neura has an existing production deployment foundation. The hackathon version extends this foundation by integrating Meta models as the AI reasoning layer.

Neura is deployed on Render. The backend service may require a short startup time after inactivity due to the free-tier sleep behavior.

Before using the application, you can verify that the backend is ready:

Health Check:

```text
https://neura-g8wk.onrender.com/health
```

Once the health check responds, open the live application.

</details>

---

## 💡 Problem

Software developers spend significant time:

- Understanding unfamiliar repositories
- Searching large codebases
- Finding bugs
- Reviewing code quality
- Explaining architecture
- Writing documentation
- Performing repetitive development tasks

Traditional AI assistants often require manually copying code snippets and lack full project context.

---

## 🧠 Solution

Neura provides an AI software engineering agent that can:

✨ Understand uploaded projects  
✨ Analyze source code structure  
✨ Explain architecture  
✨ Review code quality  
✨ Identify potential issues  
✨ Read project files  
✨ Create files  
✨ Modify files  
✨ Delete files  
✨ Answer engineering questions  

Unlike traditional coding assistants, Neura combines repository analysis, engineering tools, and AI reasoning to provide project-level assistance.

Developers interact with Neura in natural language, for example:

<details>
<summary><b>💬 Example prompts</b></summary>

<br>

- "Explain the architecture of this project."
- "Find potential bugs in the authentication module."
- "Review the code quality of this repository."
- "Add a README section describing the API endpoints."

</details>

---

## 🏗️ Architecture

```text
                        ┌──────────────────────────┐
                        │      React Frontend      │
                        │  Chat • Projects • Auth  │
                        └─────────────┬────────────┘
                                      │
                                      ▼
                         FastAPI REST API (/api/v1)
                                      │
                 ┌────────────────────┴────────────────────┐
                 │                                         │
                 ▼                                         ▼
        Authentication                           Project Management
     JWT • Users • Sessions                 Upload • Files • Metadata
                 │                                         │
                 └────────────────────┬────────────────────┘
                                      ▼
                             Agent Service
                                      │
                ┌─────────────────────┼─────────────────────┐
                │                     │                     │
                ▼                     ▼                     ▼
          LLM Client            Tool Execution      Conversation History
        (Muse Spark/OpenAI)      (Function Calls)     (Recent Messages)
                │
                ▼
          Project Analysis
                │
     ┌──────────┼───────────┬───────────┬────────────┐
     ▼          ▼           ▼           ▼            ▼
 Structure   Security    Quality     Metrics    Dependencies
 Analyzer    Analyzer    Analyzer    Analyzer    Analyzer
     │
     ▼
      Project Review Engine
                │
                ▼
        Unified Analysis Result
                │
                ▼
            React Frontend
```

---

## 📸 Screenshots

<details open>
<summary><b>🔐 Login & Authentication</b></summary>

<br>

Secure user authentication to access Neura projects.

![Neura Landing](docs/screenshots/landing.png)

</details>

<details>
<summary><b>📁 Project Dashboard</b></summary>

<br>

Create and manage software projects with Neura.

![Project Creation Dashboard](docs/screenshots/dashboard_create.png)
![Projects List Dashboard](docs/screenshots/dashboard_projects.png)

</details>

<details>
<summary><b>🔍 Project Analysis</b></summary>

<br>

Analyze code quality, security, bugs, and technology stack.

![Analysis](docs/screenshots/analysis.png)

</details>

<details>
<summary><b>💬 AI Agent Chat</b></summary>

<br>

Interact with Neura using natural language and project context.

![AI Chat](docs/screenshots/chat.png)

</details>