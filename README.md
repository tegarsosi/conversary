# Conversary

A conversational AI application built with FastAPI and Phi-4-mini-instruct model.

## Features

- Conversational AI using Microsoft's Phi-4-mini-instruct model
- Conversation history persistence
- RESTful API endpoints
- Optimized for Apple Silicon (M-series) processors
- Database storage for conversations

## Prerequisites

- Python 3.12+
- Poetry for dependency management
- macOS with M-series chip (for MPS acceleration)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tegarsosi/conversary.git
cd conversary
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Activate the Poetry environment:
```bash
poetry shell
```

## Running the Application

Start the FastAPI server:
```bash
poetry run uvicorn backend.main:app --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Conversations

- `POST /conversations/`
  - Create a new conversation entry
  - Request body: `{"user_message": "string"}`

- `GET /conversations/`
  - Get all conversations

- `GET /conversations/{date}`
  - Get conversations for a specific date
  - Date format: YYYY-MM-DD

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
