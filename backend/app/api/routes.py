from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.config import settings
from app.schemas.complaint import ComplaintStatusUpdate, TaskAssignRequest
from app.services.analytics_service import get_dashboard_analytics
from app.services.complaint_service import (
    assign_worker,
    create_complaint,
    list_complaints,
    list_worker_tasks,
    seed_demo_data_if_empty,
    update_status,
)
from app.services.ml_service import predict_waste_class
from app.utils.route_optimization import CityGraph

router = APIRouter()


@router.on_event("startup")
async def startup_seed_data():
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
    await seed_demo_data_if_empty()


@router.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.app_name}


@router.post("/complaints")
async def create_new_complaint(
    user_id: str = Form(...),
    description: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    address: str = Form(""),
    image: UploadFile = File(...),
):
    image_bytes = await image.read()
    waste_class = predict_waste_class(image_bytes)
    complaint_id = str(uuid4())

    image_path = Path(settings.upload_dir) / f"{complaint_id}_{image.filename}"
    image_path.write_bytes(image_bytes)

    now = datetime.now(timezone.utc)
    document = {
        "id": complaint_id,
        "user_id": user_id,
        "description": description,
        "location": {"latitude": latitude, "longitude": longitude, "address": address},
        "image_url": str(image_path),
        "predicted_class": waste_class.value,
        "status": "Pending",
        "assigned_worker_id": None,
        "created_at": now,
        "updated_at": now,
    }

    return await create_complaint(document)


@router.get("/complaints")
async def get_all_complaints():
    return await list_complaints()


@router.patch("/complaints/{complaint_id}/assign")
async def assign_task(complaint_id: str, payload: TaskAssignRequest):
    updated = await assign_worker(complaint_id, payload.worker_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return updated


@router.patch("/complaints/{complaint_id}/status")
async def update_task_status(complaint_id: str, payload: ComplaintStatusUpdate):
    updated = await update_status(complaint_id, payload.status.value)
    if not updated:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return updated


@router.get("/workers/{worker_id}/tasks")
async def get_worker_tasks(worker_id: str):
    return await list_worker_tasks(worker_id)


@router.get("/analytics/dashboard")
async def dashboard_analytics():
    return await get_dashboard_analytics()


@router.post("/optimize-route")
async def optimize_route(start: str = Form(...), end: str = Form(...)):
    graph = CityGraph()
    roads = [
        ("Depot", "Zone-A", 3.0),
        ("Depot", "Zone-B", 2.5),
        ("Zone-A", "Zone-C", 2.0),
        ("Zone-B", "Zone-C", 1.5),
        ("Zone-C", "Landfill", 4.0),
    ]
    for src, dst, dist in roads:
        graph.add_road(src, dst, dist)

    result = graph.shortest_path(start, end)
    if not result["path"]:
        raise HTTPException(status_code=404, detail="No route found")
    return result
