# Full-Stack Web Application with AI Chatbot - Advanced Cloud Deployment

A professional full-stack todo application with Next.js frontend featuring public access without authentication, local storage persistence, dark-first theme with blue accents, AI-powered task management, and comprehensive task management features. This project implements an advanced cloud-native architecture with event-driven microservices, Dapr sidecars, and deployment to managed Kubernetes services.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Monorepo Structure](#monorepo-structure)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Development Workflow](#development-workflow)
- [Deployment](#deployment)
- [AI Chatbot API](#ai-chatbot-api)
- [MCP Tools](#mcp-tools)
- [Testing](#testing)
- [Contributing](#contributing)

## Overview

This project demonstrates a modern, cloud-native approach to building full-stack applications with AI integration. It follows a spec-driven development methodology using Claude Code and implements advanced features like event-driven architecture, distributed tracing, and microservices orchestration.

## Architecture

The application follows a cloud-native microservices architecture with the following components:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            Cloud-Native Architecture                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐              │
│  │   Frontend      │    │   Backend       │    │   AI Agent      │              │
│  │   (Next.js)     │    │   (FastAPI)     │    │   (OpenAI)      │              │
│  │                 │    │                 │    │                 │              │
│  │  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │              │
│  │  │ Chat UI   │  │    │  │ Chat API  │  │    │  │ MCP Tools │  │              │
│  │  │           │  │    │  │           │  │    │  │           │  │              │
│  │  └───────────┘  │    │  └───────────┘  │    │  └───────────┘  │              │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘              │
│                                    │                                           │
│                                    ▼                                           │
│                    ┌─────────────────────────────────────────────────────────┐ │
│                    │                Dapr Sidecars                          │ │
│                    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │ │
│                    │  │ State Store │ │ Pub/Sub     │ │ Service Invoke│  │ │
│                    │  │ (PostgreSQL)│ │ (Kafka)     │ │ (HTTP/gRPC)   │  │ │
│                    │  └─────────────┘ └─────────────┘ └─────────────────┘  │ │
│                    └─────────────────────────────────────────────────────────┘ │
│                                    │                                           │
│                                    ▼                                           │
│                    ┌─────────────────────────────────────────────────────────┐ │
│                    │              Event-Driven Services                    │ │
│                    │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐  │ │
│                    │  │ Task Mgmt   │ │ Notification│ │ Recurring Task  │  │ │
│                    │  │ Service     │ │ Service     │ │ Service         │  │ │
│                    │  └─────────────┘ └─────────────┘ └─────────────────┘  │ │
│                    └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with custom dark-first theme
- **State Management**: Zustand with persistence
- **Animations**: Framer Motion
- **Drag & Drop**: dnd-kit
- **UI Components**: Custom-built with accessibility in mind

### Backend
- **Framework**: Python FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth (JWT tokens)
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK

### Cloud-Native Infrastructure
- **Event Streaming**: Apache Kafka / Redpanda
- **Service Mesh**: Dapr (Distributed Application Runtime)
- **Orchestration**: Kubernetes (Minikube → Cloud)
- **Containerization**: Docker
- **Package Management**: Helm Charts
- **Monitoring**: Distributed tracing, structured logging

### AI & Automation
- **AI Agent**: OpenAI GPT models
- **MCP Tools**: Model Context Protocol for task management
- **AI Ops**: kubectl-ai, kagent for cluster management
- **AI Containerization**: Gordon (Docker AI) for Dockerfile generation

## Monorepo Structure

```
monorepo root/
├── .specify/                     # Spec-Driven Development tools
│   ├── memory/                   # Project constitution and principles
│   ├── templates/                # PHR and ADR templates
│   └── scripts/                  # Automation scripts
├── specs/                        # Feature specifications
│   ├── todo/                     # Todo feature specs
│   │   ├── spec.md               # Feature requirements
│   │   ├── plan.md               # Architecture decisions
│   │   └── tasks.md              # Testable tasks
│   └── ...
├── frontend/                     # Next.js frontend application
│   ├── app/                      # App Router pages
│   ├── components/               # React components
│   ├── lib/                      # Utilities and store
│   ├── styles/                   # Global styles
│   ├── hooks/                    # Custom React hooks
│   ├── types/                    # TypeScript type definitions
│   ├── public/                   # Static assets
│   ├── package.json              # Frontend dependencies
│   └── next.config.js            # Next.js configuration
├── backend/                      # Python FastAPI backend
│   ├── src/                      # Source code
│   │   ├── main.py               # Application entry point
│   │   ├── api/                  # API route definitions
│   │   ├── models/               # SQLModel database models
│   │   ├── mcp/                  # Model Context Protocol tools
│   │   ├── agent/                # AI Agent implementation
│   │   ├── services/             # Business logic services
│   │   ├── utils/                # Utility functions
│   │   └── config/               # Configuration files
│   ├── requirements.txt          # Python dependencies
│   ├── alembic/                  # Database migration files
│   └── tests/                    # Backend tests
├── k8s/                          # Kubernetes manifests
│   ├── base/                     # Base configurations
│   ├── overlays/                 # Environment-specific configs
│   └── charts/                   # Helm charts
├── dapr/                         # Dapr component configurations
│   ├── components/               # Component definitions
│   └── configs/                  # Configuration files
├── kafka/                        # Kafka schemas and configurations
│   ├── schemas/                  # Avro/JSON schemas
│   └── topics/                   # Topic definitions
├── scripts/                      # Automation and utility scripts
├── docs/                         # Documentation
├── history/                      # Historical records
│   ├── prompts/                  # Prompt History Records
│   └── adr/                      # Architecture Decision Records
├── .env.example                  # Example environment variables
├── docker-compose.yml            # Local development containers
├── Dockerfile.frontend           # Frontend container build
├── Dockerfile.backend            # Backend container build
├── README.md                     # This file
└── ...
```

## Features

### Basic Features
- Add Task – Create new todo items
- Delete Task – Remove tasks from the list
- Update Task – Modify existing task details
- View Task List – Display all tasks
- Mark as Complete – Toggle task completion status

### Intermediate Features
- Priorities & Tags/Categories – Assign levels (high/medium/low) or labels (work/home)
- Search & Filter – Search by keyword; filter by status, priority, or date
- Sort Tasks – Reorder by due date, priority, or alphabetically

### Advanced Features
- Recurring Tasks – Auto-reschedule repeating tasks
- Due Dates & Time Reminders – Set deadlines with date/time pickers; browser notifications
- Event-Driven Architecture – Using Kafka/Redpanda for task state changes
- Dapr Integration – Sidecar pattern for state, pub/sub, and service invocation
- Cloud-Native Deployment – Kubernetes-ready with Helm charts

### AI-Powered Features
- Natural Language Processing – Understand user commands in plain English
- Task Management via Chat – Add, update, complete tasks through conversation
- Smart Suggestions – AI-powered recommendations based on task patterns
- Contextual Understanding – Maintain conversation context across interactions

## Prerequisites

### Local Development
- Node.js v20+
- Python 3.11+
- Docker Desktop with Kubernetes enabled
- Git
- npm or yarn

### Cloud Deployment
- Kubernetes cluster (Minikube, DigitalOcean DOKS, AKS, GKE, or OKE)
- Helm 3+
- Dapr CLI
- kubectl

### AI Services
- OpenAI API key
- (Optional) Cohere API key for alternative AI processing

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/HamzaSheikh768/Full-Stack-Web-Application-AI-Chatbot-Advanced-Cloud-Deployment.git
cd Full-Stack-Web-Application-AI-Chatbot-Advanced-Cloud-Deployment
```

### 2. Install Dependencies

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Update environment variables as needed
```

#### Backend Setup
```bash
# Navigate to backend directory
cd ../backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Update environment variables as needed
```

### 3. Run the Application Locally

#### Option A: Separate Terminals
```bash
# Terminal 1: Start frontend
cd frontend
npm run dev

# Terminal 2: Start backend
cd backend
uvicorn src.main:app --reload
```

#### Option B: Using Docker Compose
```bash
# From the project root
docker-compose up --build
```

### 4. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Dapr dashboard: http://localhost:8080 (if running Dapr locally)

## Development Workflow

### Spec-Driven Development
This project follows a spec-driven development approach:

1. **Specify**: Define requirements in `specs/<feature>/spec.md`
2. **Plan**: Document architecture decisions in `specs/<feature>/plan.md`
3. **Tasks**: Break down work into testable tasks in `specs/<feature>/tasks.md`
4. **Implement**: Develop features following the specifications

### Creating New Features
1. Create a new directory in `specs/` for your feature
2. Write the specification (`spec.md`) with user stories and acceptance criteria
3. Create the architectural plan (`plan.md`) with technology choices and data models
4. Break down the work into tasks (`tasks.md`) with test cases
5. Implement the feature following the specifications
6. Create Prompt History Records (PHRs) for significant changes
7. Document architectural decisions as ADRs when needed

### Code Standards
- Follow the principles outlined in `.specify/memory/constitution.md`
- Write comprehensive tests for all new functionality
- Maintain consistent code style using project linters/formatters
- Document public APIs and complex business logic
- Use meaningful commit messages following conventional commits

## Deployment

### Local Kubernetes (Minikube)
```bash
# Start Minikube
minikube start --driver=docker --cpus=4 --memory=8192

# Install Dapr
dapr init -k

# Deploy using Helm
helm install todo-frontend ./k8s/charts/frontend
helm install todo-backend ./k8s/charts/backend
```

### Cloud Deployment
For cloud deployment to DigitalOcean DOKS, AKS, GKE, or OKE:

1. Configure your cloud provider's CLI tools
2. Create a Kubernetes cluster
3. Install Dapr in the cluster
4. Update Helm values for your environment
5. Deploy using Helm

```bash
# Example for DigitalOcean
doctl kubernetes cluster kubeconfig save <cluster-name>
helm install todo-frontend ./k8s/charts/frontend -f k8s/values/prod.yaml
helm install todo-backend ./k8s/charts/backend -f k8s/values/prod.yaml
```

## AI Chatbot API

The backend includes an AI-powered chatbot that allows users to manage tasks through natural language.

### Chat API Endpoint

- **Endpoint**: `POST /api/{user_id}/chat`
- **Description**: Send a message to the AI assistant and receive a response
- **Headers**:
  - `Content-Type: application/json`
  - Authentication cookie (Better Auth session)
- **Request Body**:
  ```json
  {
    "message": "string",
    "conversation_id": "number (optional)"
  }
  ```
- **Response**:
  ```json
  {
    "conversation_id": "number",
    "response": "string",
    "tool_calls": "array"
  }
  ```

### Supported Commands

The AI assistant can handle various task management commands:

- **Add tasks**: "Add a task to buy groceries", "Create a task to call mom"
- **List tasks**: "Show my tasks", "What do I have to do?", "Show completed tasks"
- **Complete tasks**: "Mark task 1 as complete", "Finish the shopping task"
- **Delete tasks**: "Delete task 1", "Remove the meeting task"
- **Update tasks**: "Change task 1 to 'Call dad'", "Update the grocery task description"

## MCP Tools

The application implements Model Context Protocol (MCP) tools for AI interaction:

### Tool: add_task
- **Purpose**: Create a new task
- **Parameters**: user_id (required), title (required), description (optional)
- **Returns**: task_id, status, title

### Tool: list_tasks
- **Purpose**: Retrieve tasks from the list
- **Parameters**: user_id (required), status (optional: "all", "pending", "completed")
- **Returns**: Array of task objects

### Tool: complete_task
- **Purpose**: Mark a task as complete
- **Parameters**: user_id (required), task_id (required)
- **Returns**: task_id, status, title

### Tool: delete_task
- **Purpose**: Remove a task from the list
- **Parameters**: user_id (required), task_id (required)
- **Returns**: task_id, status, title

### Tool: update_task
- **Purpose**: Modify task title or description
- **Parameters**: user_id (required), task_id (required), title (optional), description (optional)
- **Returns**: task_id, status, title

## Testing

### Frontend Testing
```bash
cd frontend
npm run test
npm run test:coverage
```

### Backend Testing
```bash
cd backend
python -m pytest tests/
python -m pytest tests/ --cov=src
```

### End-to-End Testing
```bash
# Run integration tests
npm run test:e2e
```

## Contributing

We welcome contributions to this project! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the spec-driven development approach
4. Add tests for new functionality
5. Update documentation as needed
6. Commit your changes using conventional commits
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

Before submitting a PR, ensure:
- All tests pass
- Code follows project standards
- Specifications are updated if needed
- Prompt History Records are created for significant changes
- Architectural decisions are documented as ADRs if applicable

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the existing [Issues](https://github.com/HamzaSheikh768/Full-Stack-Web-Application-AI-Chatbot-Advanced-Cloud-Deployment/issues)
2. Search the documentation in the `docs/` directory
3. Create a new issue with detailed information about your problem
4. For urgent matters, contact the maintainers directly

## Acknowledgments

- Built with Next.js, FastAPI, and modern web technologies
- AI capabilities powered by OpenAI
- Cloud-native infrastructure with Dapr and Kubernetes
- Spec-driven development methodology with Claude Code