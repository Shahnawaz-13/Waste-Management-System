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
│   └── requirements.txt
├── frontend/                # Streamlit UI
│   ├── app.py
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

### Run Backend
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

### Run Frontend
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

## Deployability Notes
- **Backend**: deploy on Render/Railway
- **Frontend**: deploy on Streamlit Community Cloud
- **Database**: MongoDB Atlas
- Add environment variables in deployment settings:
  - `MONGO_URI`
  - `MONGO_DB_NAME`
  - `API_BASE` (frontend)

## Suggested Enhancements
- Real model inference endpoint using TorchScript/ONNX
- JWT authentication + RBAC
- Notifications (email/SMS)
- GeoJSON-based route graph with live traffic data
