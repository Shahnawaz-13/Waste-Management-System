from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from app.core.database import database
from app.models.enums import ComplaintStatus


def _complaint_collection():
    return database["complaints"]


async def create_complaint(document: dict[str, Any]) -> dict[str, Any]:
    await _complaint_collection().insert_one(document)
    return document


async def list_complaints() -> list[dict[str, Any]]:
    cursor = _complaint_collection().find().sort("created_at", -1)
    return await cursor.to_list(length=500)


async def assign_worker(complaint_id: str, worker_id: str) -> dict[str, Any] | None:
    updated_at = datetime.now(timezone.utc)
    await _complaint_collection().update_one(
        {"id": complaint_id},
        {
            "$set": {
                "assigned_worker_id": worker_id,
                "status": ComplaintStatus.IN_PROGRESS.value,
                "updated_at": updated_at,
            }
        },
    )
    return await _complaint_collection().find_one({"id": complaint_id})


async def update_status(complaint_id: str, status: str) -> dict[str, Any] | None:
    updated_at = datetime.now(timezone.utc)
    await _complaint_collection().update_one(
        {"id": complaint_id}, {"$set": {"status": status, "updated_at": updated_at}}
    )
    return await _complaint_collection().find_one({"id": complaint_id})


async def list_worker_tasks(worker_id: str) -> list[dict[str, Any]]:
    cursor = _complaint_collection().find({"assigned_worker_id": worker_id})
    return await cursor.to_list(length=200)


async def seed_demo_data_if_empty():
    count = await _complaint_collection().count_documents({})
    if count > 0:
        return

    now = datetime.now(timezone.utc)
    seed_docs = [
        {
            "id": str(uuid4()),
            "user_id": "user_1001",
            "description": "Overflowing street bin near market entrance.",
            "location": {"latitude": 28.6139, "longitude": 77.2090, "address": "Central Market"},
            "image_url": "uploads/demo1.jpg",
            "predicted_class": "Plastic",
            "status": "Pending",
            "assigned_worker_id": None,
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": str(uuid4()),
            "user_id": "user_1002",
            "description": "Metal scraps dumped beside bus stop.",
            "location": {"latitude": 28.5355, "longitude": 77.3910, "address": "Sector 18"},
            "image_url": "uploads/demo2.jpg",
            "predicted_class": "Metal",
            "status": "In Progress",
            "assigned_worker_id": "worker_01",
            "created_at": now,
            "updated_at": now,
        },
    ]
    await _complaint_collection().insert_many(seed_docs)
