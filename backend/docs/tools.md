# AI Tool System

## Overview

The AI Tool System extends the capabilities of the Large Language Model by allowing it to interact with the user's software project.

Instead of relying solely on the model's internal knowledge, tools enable the assistant to inspect, modify, and manage project files safely.

Each tool performs one well-defined task and can be independently added or removed without changing the AI orchestration logic.

---

# Architecture

```
                User
                 │
                 ▼
          AgentService
                 │
                 ▼
          Tool Registry
                 │
      ┌──────────┴──────────┐
      ▼          ▼          ▼
 ListFiles   ReadFile   WriteFile
                 │
                 ▼
           DeleteFile
```

The AI never communicates directly with the operating system.

Every filesystem operation goes through a registered tool.

---

# Tool Lifecycle

Every tool follows the same execution flow.

```
LLM requests tool
        │
        ▼
Tool Registry
        │
        ▼
Locate Tool
        │
        ▼
Validate Arguments
        │
        ▼
Execute
        │
        ▼
Return Result
        │
        ▼
Continue Conversation
```

---

# Tool Interface

Every tool inherits from `BaseTool`.

A tool must implement:

- `name`
- `description`
- `schema`
- `execute()`

Example:

```python
class ExampleTool(BaseTool):

    @property
    def name(self):
        ...

    @property
    def description(self):
        ...

    @property
    def schema(self):
        ...

    def execute(...):
        ...
```

This standard interface allows every tool to be automatically discovered and registered.

---

# Current Tools

## ListFilesTool

### Purpose

Returns all files within the project directory.

### Arguments

None.

### Returns

A sorted list of relative file paths.

### Example

```
User

↓

"Show me every file in this project."

↓

Tool

↓

[
    "README.md",
    "app/main.py",
    "app/api/chat.py"
]
```

---

## ReadFileTool

### Purpose

Reads the contents of a project file.

### Arguments

| Name | Description |
|------|-------------|
| path | Relative path of the file |

### Returns

The complete contents of the requested file.

### Example

```
ReadFileTool

↓

README.md

↓

"# AI Software Engineering Assistant..."
```

---

## WriteFileTool

### Purpose

Creates a new file or updates an existing file.

### Arguments

| Name | Description |
|------|-------------|
| path | Relative file path |
| content | File contents |

### Returns

A confirmation message indicating success.

### Example

```
WriteFileTool

↓

README.md

↓

Updated successfully
```

---

## DeleteFileTool

### Purpose

Deletes an existing file.

### Arguments

| Name | Description |
|------|-------------|
| path | Relative file path |

### Returns

Confirmation that the file was removed.

---

# Safety

Every filesystem tool validates project boundaries before executing.

This prevents:

- Path traversal (`../`)
- Access outside the project
- Invalid file locations

Example:

```
Allowed

project/
    README.md

Denied

../../etc/passwd
```

---

# Error Handling

Tools should never crash the AI Agent.

Common errors include:

- File not found
- Invalid path
- Permission denied
- Invalid arguments

Errors are returned to the language model so it can generate a helpful response for the user.

---

# Tool Registry

The Tool Registry is responsible for:

- Registering available tools
- Exposing tool schemas to the LLM
- Looking up tools by name
- Returning the correct tool implementation

Adding a new tool only requires registering it in the registry.

No changes to the AI agent are necessary.

---

# Adding a New Tool

Every new tool should follow these steps.

1. Create a new class that inherits from `BaseTool`.
2. Implement:
   - `name`
   - `description`
   - `schema`
   - `execute()`
3. Register the tool in `ToolRegistry`.

The agent will automatically expose the new tool to the language model.

---

# Planned Tools

The current implementation focuses on file management.

Future tools may include:

## Project Management

- SearchProjectTool
- RenameFileTool
- MoveFileTool
- CopyFileTool
- CreateDirectoryTool
- DeleteDirectoryTool

---

## Code Editing

- ReplaceTextTool
- InsertTextTool
- FormatCodeTool
- RefactorFileTool

---

## Analysis

- AnalyzeProjectTool
- ExplainCodeTool
- GenerateDocumentationTool
- GenerateUMLTool
- FindUnusedCodeTool

---

## Development

- RunTestsTool
- RunLinterTool
- RunFormatterTool
- ExecuteCommandTool

---

## Git

- GitStatusTool
- GitDiffTool
- GitCommitTool
- GitBranchTool

---

# Design Principles

Every tool should follow these principles.

## Single Responsibility

A tool performs one task only.

---

## Safe

A tool must never access files outside the project directory.

---

## Predictable

The same inputs should produce the same outputs.

---

## Independent

Tools should not depend on one another.

---

## Reusable

Each tool should be usable by any future AI workflow.

---

# Summary

The Tool System provides the AI assistant with secure, modular, and extensible access to the user's project.

By separating project operations into individual tools, the AI remains easy to extend while keeping filesystem interactions safe, predictable, and maintainable.