# finance-analytics-dashboard

## Project Summary

Full-stack finance analytics dashboard for managing and analyzing financial transactions using an interactive table and charts.

## Key Features

- Interactive transaction table with sorting, filtering and pagination
- Create and Delete transaction
- Update transaction categories
- Display total spend and remaining budget based on filters
- Visualization of spending vs. budget
- Monthly spending trend analysis

## Technology Stack

### Frontend:

- Framework: SvelteKit
- Styling: CSS, Bootstrap
- Data Visualisation: Chart.js

### Backend:

- API Framework: FastAPI
- ORM/Data Layer: SQLModel
- Server (ASGI): Uvicorn

### Database:

- SQLite

## Prerequisites

- Python >=3.14 (with uv package manager)
- Node.js LTS

## Setup

1. Install Python & Node.js
2. Clone repository
3. Install dependencies
4. Run application

### Installing dependencies & running application:
Backend:
1. uv sync
2. uv run uvicorn main:app --reload

Frontend:
1. npm install
2. npm run dev

### Access
- Frontend: http://localhost:5173/transactions
- Backend API: http://localhost:8000/docs

## Seed Data
Database tables are automatically initialized on first startup, and categories populated.
Seed data can optionally be added executing seed.py.
