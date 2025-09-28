
# Cloud-Based Employee Management System (Beginner)

## Overview
A simple full-stack web application built with Flask (Python) that demonstrates:
- Employee CRUD (Add / Edit / Delete / List)
- Simple Attendance logging
- Leave request submission and approval
- Basic authentication (Admin & Employee)
- Analytics dashboard powered by Chart.js

This is a college-level project scaffold you can demo in interviews. It uses SQLite for simplicity but can be migrated to MySQL/Postgres and deployed to Azure or AWS.

## Stack
- Backend: Flask, SQLAlchemy
- Database: SQLite (for demo)
- Frontend: HTML, Bootstrap 5, Chart.js
- Optional: Deploy to Azure App Service or other cloud provider.

## How to run (locally)
1. Create and activate a Python virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the database (creates `app.db`):
   ```bash
   python init_db.py
   ```
4. Run the app:
   ```bash
   flask run
   ```
   or
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000/` in your browser.

## Default Admin
- email: admin@ondo.local
- password: admin123

## Notes for interview
- Explain how you can replace SQLite with Azure SQL / MySQL and store uploaded files in Azure Blob Storage.
- Show the dashboard and a sample employee add flow to demo features.

## Files included
- app.py (main Flask app)
- models.py (SQLAlchemy models)
- init_db.py (DB initialization with sample data)
- requirements.txt
- templates/ (HTML templates)
- static/ (CSS, JS)
