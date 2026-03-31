# Smart Waste Management System using AI and Data Analytics

A production-ready final year project template with modular architecture, role-based workflow, analytics, and AI waste classification.

## 1) Project Architecture (Step 1)

```text
Waste-Management-System/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/             # REST routes
│   │   ├── core/            # config + DB connection
│   │   ├── models/          # enums/constants
│   │   ├── schemas/         # pydantic schemas
│   │   ├── services/        # business logic
│   │   └── utils/           # algorithms (Dijkstra)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # Streamlit UI
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── ml_model/                # CNN training + inference
│   ├── scripts/
│   │   ├── train.py
│   │   └── predict.py
│   └── requirements.txt
├── database/
│   └── schema.md
├── docs/
│   ├── ppt_content.md
│   └── viva_questions.md
├── docker-compose.yml
└── README.md
```

## 2) Backend Implementation (Step 2)

### Tech
- FastAPI
- MongoDB (Motor async driver)
- Modular service layer

### Key API Endpoints
- `POST /api/complaints` → User submits complaint (image + location)
- `GET /api/complaints` → Admin sees all complaints
- `PATCH /api/complaints/{id}/assign` → Admin assigns worker
- `PATCH /api/complaints/{id}/status` → Worker/Admin updates status
- `GET /api/workers/{worker_id}/tasks` → Worker tasks
- `GET /api/analytics/dashboard` → Charts data
- `POST /api/optimize-route` → Dijkstra shortest route

### Run Backend (Local)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

## 3) Frontend Implementation (Step 3)

### UI Modules
- **User Panel**: Complaint submission with image upload and coordinates
- **Admin Panel**: Complaint table, worker assignment, charts, heatmap
- **Worker Panel**: Assigned tasks and status update
- **Sidebar Tool**: Route optimization

### Run Frontend (Local)
```bash
cd frontend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Set backend URL if needed:
```bash
export API_BASE=http://localhost:8000/api
```

## 4) ML Model (Step 4)

### Dataset Suggestion
Use **TrashNet** dataset and map labels to 3 classes:
- Plastic
- Metal
- Organic

Expected folder structure:
```text
ml_model/data/trashnet/
├── train/
│   ├── plastic/
│   ├── metal/
│   └── organic/
└── val/
    ├── plastic/
    ├── metal/
    └── organic/
```

### Train
```bash
python ml_model/scripts/train.py --data-dir ml_model/data/trashnet --epochs 10
```

### Predict
```bash
python ml_model/scripts/predict.py --image-path sample.jpg
```

## 5) Integration Flow (Step 5)

1. User uploads complaint image + location from Streamlit.
2. Backend stores image and metadata in MongoDB.
3. Backend predicts waste class (service placeholder linked to ML script contract).
4. Admin assigns worker.
5. Worker updates status (`Pending → In Progress → Completed`).
6. Dashboard updates charts and map with latest complaint data.
7. Route optimization endpoint helps with efficient pickup planning.

## Advanced Features Included
- ✅ Route optimization using Dijkstra algorithm
- ✅ Heatmap visualization of complaint coordinates

---

# Deployment Guide (Beginner Friendly)

## Option A: One-command deployment locally using Docker Compose (Recommended first)

### Prerequisites
- Install Docker Desktop (Windows/Mac) or Docker Engine + Compose (Linux)
- Verify:
```bash
docker --version
docker compose version
```

### Start everything
From project root:
```bash
docker compose up --build -d
```

### Open apps
- Frontend (Streamlit): `http://localhost:8501`
- Backend docs (FastAPI): `http://localhost:8000/docs`

### Stop services
```bash
docker compose down
```

### Stop + remove volumes (full reset)
```bash
docker compose down -v
```

---

## Option B: Free cloud deployment (Render + Streamlit Cloud + MongoDB Atlas)

## 1) Deploy MongoDB (Atlas)
1. Create free cluster at MongoDB Atlas.
2. Create database user + password.
3. Add IP access (for testing: allow `0.0.0.0/0`, later restrict).
4. Copy connection string:
   - `mongodb+srv://<user>:<password>@<cluster-url>/...`

## 2) Deploy backend on Render
1. Push this repo to GitHub.
2. In Render: **New Web Service** → connect repo.
3. Configure:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables:
   - `APP_NAME=Smart Waste Management API`
   - `ENVIRONMENT=production`
   - `MONGO_URI=<atlas-connection-string>`
   - `MONGO_DB_NAME=smart_waste_db`
   - `UPLOAD_DIR=uploads`
5. Deploy and test `https://<your-backend>/api/health`

## 3) Deploy frontend on Streamlit Community Cloud
1. In Streamlit Cloud: **New app** → select repo.
2. Main file path: `frontend/app.py`
3. Set environment variable:
   - `API_BASE=https://<your-render-backend>/api`
4. Deploy and open app URL.

## 4) CORS + Connectivity checklist
- Backend CORS currently allows all origins (`*`) for easy student deployment.
- Make sure frontend uses correct API URL.
- Ensure Atlas network access allows Render IPs.

---

## Option C: Single VPS (Ubuntu) deployment

1. Install Docker + Compose on VPS.
2. Clone repo and run:
```bash
docker compose up --build -d
```
3. Put Nginx reverse proxy in front (HTTPS with Let’s Encrypt).
4. Map:
   - `/` → frontend `:8501`
   - `/api` → backend `:8000`

---

## Production hardening checklist (important)
- Add JWT authentication + role-based authorization.
- Restrict CORS to your frontend domain only.
- Use object storage (S3/Cloudinary) instead of local uploads for images.
- Add logging, monitoring, and error tracking.
- Add backups for MongoDB.
- Move route graph from demo data to real GIS/roads data.

## Suggested Enhancements
- Real model inference endpoint using TorchScript/ONNX
- Notifications (email/SMS)
- GeoJSON-based route graph with live traffic data
