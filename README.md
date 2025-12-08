# ShopWise - AI-Powered E-Commerce Multi-Agent System
Intelligent Multi-Agent Shopping Assistant (LangGraph + FastAPI + Streamlit)

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
5. [Project Structure](#project-structure)
6. [Tech Stack](#tech-stack)
7. [Setup & Installation](#setup--installation)
8. [Running Using Docker](#running-using-docker)
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
<img width="1092" height="661" alt="MultiAgentSystem" src="https://github.com/user-attachments/assets/d7504e08-1836-46a9-a568-e3a12a8493ca" />






