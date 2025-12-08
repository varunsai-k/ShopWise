# ShopWise - AI-Powered E-Commerce Multi-Agent System
🚀 Intelligent Multi-Agent Shopping Assistant (LangGraph + FastAPI + Streamlit)

<p align="center"><img width="500" height="500" alt="MultiAgentIcon" src="https://github.com/user-attachments/assets/a7bf018f-a6dc-4582-82b0-d89f618e4df4" /></p>

## Overview

The AI-Powered E-Commerce Multi-Agent System is a complete intelligent shopping assistant built using LangGraph, LangChain, FastAPI, and Streamlit UI.

It uses a Supervisor Agent to route user instructions to specialized agents handling:
- 🔍 Product search & filtering
- 🛍️ Vision-based product recommendations
- 🛒 Cart management operations
- 📦 Order placement, tracking & cancellation
- 🧠 Intelligent workflow routing using LangGraph
  
The entire project is modular, event-driven, and containerized using Docker for production-ready deployment.

## Table of Contents

1. [Features](#features)
2. [Demo](#demo)
3. [Architecture Overview](#architecture-overview)
4. [Graph Architecture](#graph-architecture)
5. [Project Structure](#-project-structure)
6. [Tech Stack](#tech-stack)
7. [Setup & Installation](#setup--installation)
8. [Running Using Docker](#running-using-docker-recommended)
9. [Running Locally Without Docker](#running-locally-without-docker)
10. [API Usage](#api-usage)

## Features
* Supervisor Agent to route user workflows
* Product Agent for search, filters, recommendations
* Vision Agent for image → product similarity
* Cart Agent for add/update/remove operations
* Orders Agent for placement, tracking & cancellation
* Graph-based orchestration using LangGraph
* FastAPI backend with auto API docs
* Streamlit UI for user experience
* Dockerized deployment (UI + API)
  
## Demo


https://github.com/user-attachments/assets/32b7aa01-f638-471f-a2ce-04728b04d95f


👉 Watch the full Demo walkthrough on YouTube covering Live Agent Workflow and Graph Debugging: [https://youtu.be/HIIaS840zWo](https://youtu.be/HIIaS840zWo)

## Architecture Overview
<img width="1421" height="513" alt="ShopWise drawio" src="https://github.com/user-attachments/assets/3479f130-1bae-403f-a494-4fe66bc8e282" />

The high-level architecture uses a decoupled two-container model:

**(1) UI Container (Streamlit)**

  - Serves the ShopWise Chat Interface
  - Handles user queries and image uploads
  - Encodes inputs (text/base64 images)
  - Sends requests to the API service via internal Docker networking

**(2) Backend Container (FastAPI + LangGraph)**
  - Hosts the LangGraph Runtime and multi-agent workflow
  - Executes Supervisor + Agents (Products, Orders, Cart, Vision)
  - Uses SQLite (ecommerce.db) mounted within the container
  - Returns structured agent responses to the UI

The containers communicate over Docker’s default bridge network (http://agent_api:8000), enabling clean separation of concerns, easier scaling, and independent development of UI and backend components.

Flow Summary:
- User interacts via Streamlit UI
- Query forwarded to FastAPI
- Supervisor Agent interprets intent
- Route to correct specialized agent
- Agent executes via DB/tools
- Aggregated response sent back to UI

## Graph Architecture
<p align="center"><img width="800" height="500" alt="MultiAgentSystem" src="https://github.com/user-attachments/assets/d7504e08-1836-46a9-a568-e3a12a8493ca" /></p>

This project uses LangGraph to orchestrate a multi-agent workflow, where the Supervisor routes user intents to the appropriate specialized agent.
The graph consists of four main nodes and tool sub-nodes, as shown in the diagram.

### Graph Overview

  - Supervisor
      Central controller — interprets the user query and selects the correct agent node.

  - Products Agent
      Handles product search, categories, filters, and vision-based recommendations.
      Uses: ProductAgentTools

  - Cart Management Agent
    Adds, updates, and removes cart items.
    Uses: CartTools

  - Orders Agent
    Places orders, checks order status, fetches order history.
    Uses: OrdersAgentTools

  Flow Summary

  1. Conversation begins at __start__
  2. Supervisor receives the query and decides which agent to activate
  3. The selected agent runs its tools
  4. Agent either delegates again or ends the workflow
  5. Graph finishes at __end__

### Graph Architecture Diagram

``` (Generated from LangGraph Visualizer — included in repo) MultiAgentSystem.png ```

## 📁 Project Structure
```
.
└── ShopWise/
    ├── assets/                               # Static images/icons for UI
    │   ├── MultiAgentIcon.png                # Icon for multi-agent system
    │   ├── MultiAgentSystem.png              # Architecture or system diagram
    │   ├── boticon.png                       # Chatbot icon
    │   ├── chaticon3.png                     # Chat bubble icon
    │   ├── men__5.jpg                        # Sample product image (men)
    │   ├── men__6.jpg                        # Sample product image (men)
    │   └── women__1.jpg                      # Sample product image (women)
    ├── pages/                                # Streamlit multipage UI screens
    │   ├── chat.py                           # Chatbot UI page
    │   ├── faqs.py                           # FAQs page
    │   ├── guest.py                          # Guest user page
    │   └── home.py                           # Home/landing page UI
    ├── src/                                  # Backend logic & agent code
    │   ├── agents/                           # LangGraph agent implementations
    │   │   ├── CartManagementAgent.py        # Logic for cart operations
    │   │   ├── OrdesAgent.py                 # Orders processing agent
    │   │   └── ProductsAgent.py              # Product search & recommendations agent
    │   ├── __init__.py                       # Marks directory as a module
    │   ├── ecommerce.db                      # SQLite database file
    │   ├── graph.py                          # LangGraph workflow graph definition
    │   ├── langgraph.json                    # Graph visualization export
    │   ├── llms.py                           # LLM initialization/config
    │   ├── main.py                           # FastAPI entry point for backend API
    │   ├── nodes.py                          # Nodes used inside the LangGraph pipeline
    │   ├── prompts.py                        # Prompt templates for agents/LLMs
    │   ├── state.py                          # Shared graph state definitions
    │   ├── tools.py                          # Tools used by agents (DB ops, APIs, etc.)
    │   └── utils.py                          # Helper utilities (common functions)
    ├── .env                                  # Environment variables (DB_PATH, API keys)
    ├── DockerFile.api                        # Dockerfile for API backend container
    ├── DockerFile.ui                         # Dockerfile for Streamlit UI container
    ├── README.md                             # Project documentation & architecture overview
    ├── app.py                                # Streamlit main entry (launcher)
    ├── config.py                             # Project-wide configuration/settings
    ├── docker-compose.yaml                   # Multi-container setup (API + UI + network)
    └── requirements.txt                      # Python dependencies for both UI + API

```
## Tech Stack
### Backend
- LangGraph
- LangChain
- FastAPI
- SQLite
### Frontend
- Streamlit
- Custom CSS
### Infra
- Docker
- Docker Compose

## Setup & Installation

Step 1: Clone Repository
```
git clone https://github.com/varunsai-k/ShopWise.git
cd ShopWise
```
Step 2: Environment Variables
Create ```.env```:

```
GOOGLE_API_KEY=
LANGSMITH_API_KEY=
LANGSMITH_TRACING=true
DB_PATH="ecommerce.db"

```
## Running Using Docker (Recommended)

```
docker compose up --build

```
#### Services
```
Component	                 URL
FastAPI Backend	      http://localhost:8000

Streamlit UI	      http://localhost:8501

```
## Running Locally (Without Docker)

### Backend
```
cd src
uvicorn main:app --reload --port 8000
```

### Frontend
```
streamlit run app.py

```
## API Usage

Interactive docs: ``` http://localhost:8000/docs ```


👉 Watch the full Demo walkthrough on YouTube covering Live Agent Workflow and Graph Debugging: [https://youtu.be/HIIaS840zWo](https://youtu.be/HIIaS840zWo)
