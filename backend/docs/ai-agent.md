# AI Agent

## Overview

The AI Agent is the core of the AI Software Engineering Assistant. It enables users to interact with their software projects using natural language.

Instead of answering questions solely from the language model's knowledge, the agent can inspect the user's project, execute tools, and use the results to produce accurate, project-specific responses.

---

# Goals

The AI Agent is designed to:

- Understand software projects.
- Read project files.
- Modify project files.
- Create new files.
- Delete files.
- Analyze source code.
- Generate documentation.
- Answer questions about a project.
- Serve as an intelligent software engineering assistant.

---

# Main Components

```
User
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
Tool Registry
 │
 ▼
Project Tools
```

Each component has a specific responsibility.

---

# Agent Workflow

The agent follows the same workflow for every request.

```
User Request
      │
      ▼
Build Conversation
      │
      ▼
Send to LLM
      │
      ▼
Tool Requested?
      │
 ┌────┴─────┐
 │          │
 ▼          ▼
No         Yes
 │          │
 ▼          ▼
Return   Execute Tool
Answer       │
             ▼
      Add Tool Result
             │
             ▼
      Continue Conversation
             │
             ▼
        Final Response
```

This process repeats until the language model returns a normal response.

---

# Conversation Lifecycle

Every request begins by creating a conversation.

The conversation initially contains:

1. System Prompt
2. User Message

Example:

```
System
↓

User
```

If the model requests a tool, additional messages are added.

```
System

↓

User

↓

Assistant (Tool Request)

↓

Tool Result

↓

Assistant
```

The conversation continues until the assistant returns a final answer.

---

# System Prompt

The System Prompt defines the assistant's behavior.

Responsibilities include:

- Explaining available tools.
- Defining safety rules.
- Guiding tool usage.
- Preventing hallucinations.
- Controlling the assistant's behavior.

The prompt is always the first message in the conversation.

---

# Tool Calling

Instead of guessing project information, the model can request tools.

Example:

```
User

↓

"Improve README.md"

↓

LLM

↓

read_file("README.md")

↓

Tool

↓

README contents

↓

LLM

↓

Generate improved README
```

The language model never accesses the filesystem directly.

All file operations go through registered tools.

---

# Tool Registry

The Tool Registry acts as the bridge between the LLM and the available project tools.

Responsibilities:

- Register tools.
- Expose tool schemas.
- Locate tools by name.
- Execute the correct implementation.

The agent never communicates with tools directly.

Instead:

```
AgentService

↓

ToolRegistry

↓

Requested Tool
```

This makes the system easy to extend.

---

# Tool Execution

Each tool follows the same lifecycle.

```
Tool Requested

↓

Validate Arguments

↓

Execute

↓

Return Result

↓

Continue Conversation
```

Tool results become part of the conversation history.

---

# Error Handling

Tool execution is protected against common errors.

Examples include:

- File not found
- Invalid path
- Permission denied
- Invalid arguments
- Unexpected exceptions

Instead of crashing, errors are returned to the language model so it can respond appropriately.

---

# Current Tools

The current implementation includes:

| Tool | Purpose |
|------|---------|
| ListFilesTool | List project files |
| ReadFileTool | Read file contents |
| WriteFileTool | Create or modify files |
| DeleteFileTool | Delete files |

Additional tools can be added without modifying the AI workflow.

---

# Adding a New Tool

Every tool follows the same pattern.

1. Create a new tool class.
2. Inherit from `BaseTool`.
3. Implement:
   - `name`
   - `description`
   - `schema`
   - `execute()`
4. Register the tool in `ToolRegistry`.

No changes to `AgentService` are required.

---

# Design Principles

## Extensible

New tools can be added independently.

---

## Modular

Each tool performs one specific task.

---

## Secure

All filesystem operations validate project boundaries to prevent path traversal.

---

## Stateless

Each request starts with a fresh conversation.

Future versions may introduce persistent conversation memory.

---

# Current Limitations

Current limitations include:

- No long-term memory.
- No project indexing.
- No semantic search.
- No Git integration.
- No terminal access.
- No code execution.
- No vector database.

These features are planned for future releases.

---

# Future Enhancements

Planned AI improvements include:

- Conversation memory
- Retrieval-Augmented Generation (RAG)
- Project indexing
- Semantic code search
- Git integration
- Terminal integration
- Test execution
- Automatic code refactoring
- Documentation generation
- UML generation
- Multi-agent workflows

---

# Summary

The AI Agent combines a Large Language Model with project-aware tools to provide intelligent software engineering assistance.

By separating orchestration, tool execution, and business logic, the architecture remains modular, maintainable, and easy to extend as new AI capabilities are introduced.