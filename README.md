# Task Manager App

A simple 3-tier web app: **HTML/CSS frontend** + **FastAPI backend** (in-memory storage, no database).

---

## Project Structure

```
crud/
├── backend/
│   ├── main.py          # FastAPI app — data stored in a Python dict
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

## 1. Run the Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload --port 8000
```

> ⚠️ Data is stored in memory — it resets every time you restart the server.

API docs: **http://localhost:8000/docs**

---

## 2. Open the Frontend

Double-click `frontend/index.html` in your browser.

---

## API Endpoints

| Method | URL | Action |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create task |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

---

## AWS Mapping (for learning)

```
User → ALB (Public Subnet)
         ↓
    EC2/ECS  ← FastAPI app  (Private Subnet)
```

| Local | AWS |
|---|---|
| `uvicorn` on port 8000 | EC2 / ECS in Private Subnet |
| Open HTML in browser | S3 + CloudFront or EC2 in Public Subnet |
| ALB replaces direct port access | ALB routes traffic to backend |
