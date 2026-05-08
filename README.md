# AI Coding Agent CLI (Python)

A minimal, extensible CLI AI agent harness built in Python that can chat and call local tools to read, list and edit files.

This project was inspired by Thorsten Ball's note, **[How to Build an Agent](https://ampcode.com/notes/how-to-build-an-agent)** on Amp.
I used it as a conceptual guide for the core agent loop (LLM + tools + iteration), and adapted the implementation to Python + OpenAI Responses API.

## Why build your own agent

Mainly because it was fun. Writing an agent harness from scratch and going from zero to an actually useful tool makes you realize about how simple yet powerful an AI agent can be.

I wanted to  understand how real agents work under the hood: 
- How context is handled in a harness
- How to create tools that the model can use
- How to structure an iterative agent loop for multi-step tasks

## Demo

https://github.com/user-attachments/assets/348fefef-7ecb-48b9-aa22-7ebd85742ea7

## Features

- Interactive terminal chat interface
- Built-in local tools:
  - `read_file`: read file contents
  - `list_files`: list directory contents
  - `edit_files`: perform text replacement / create files
- Multi-turn loop with conversation context and follow-up tool execution

## Tech Stack

- Python
- OpenAI Python SDK
- `uv` for dependency/runtime workflow
- Standard library modules (`json`, `os`, `typing`)
