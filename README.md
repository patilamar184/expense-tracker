# Mini Expense Tracker 💰

A simple FastAPI project to learn **Authentication, Authorization & JWT**.

Every user has their own expenses. Nobody can see other's expenses. Admin can see all.

## Tech Stack
- FastAPI + SQLAlchemy + SQLite
- JWT for Auth
- Bcrypt for Password Hashing

## Setup

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload