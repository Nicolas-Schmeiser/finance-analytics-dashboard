# finance-analytics-dashboard

## Project Summary

This project implements a full-stack finance analytics dashboard that allows users to view, categorize, and analyze financial transactions through an interactive table and visual charts.

The application demonstrates the integration of frontend, backend, and database components in a web application.

## Key Features

- Interactive transaction table with sorting and filtering
- Editing transaction categories
- Display of total spend based on filters
- Dashboard with financial visualizations
- Comparison of expenses against budget
- Monthly spending trend analysis

## Technology Stack

### Frontend:

- SvelteKit
- Bootstrap
- DataTables.js
- Chart.js

### Backend:

- FastAPI (Python)

### Database:

- SQLite

## Prerequisites

- Python >=3.14 (with uv package manager)
- Node.js LTS

## Setup

1. Install prerequisites
2. Clone repository
3. Install depedencies (backend and frontend separately, see following instruction)
4. Run application

### Installing depedencies & running application:
Backend:
uv sync
uv run uvicorn main:app --reload

Frontend:
npm install
npm run dev


## Troubleshooting (Windows PowerShell)

If you receive the following error when running `npm install`:

running scripts is disabled on this system

This is caused by the Windows PowerShell execution policy blocking script execution.

### Option 1 — Run npm using Command Prompt (no system changes required)

Open Command Prompt (cmd) instead of PowerShell and run:

npm install
npm run dev

### Option 2 — Temporarily bypass the policy (session only)

Run in PowerShell:

powershell -ExecutionPolicy Bypass

Then execute:

npm install

This does not permanently change system settings.

### Option 3 — Change execution policy for current user (permanent)

Run PowerShell as Administrator:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned