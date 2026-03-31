from collections import Counter, defaultdict

from app.services.complaint_service import list_complaints


async def get_dashboard_analytics() -> dict:
    complaints = await list_complaints()
    status_counter = Counter([item.get("status", "Pending") for item in complaints])

    trend_map = defaultdict(int)
    for item in complaints:
        date_key = item["created_at"].strftime("%Y-%m-%d")
        trend_map[date_key] += 1

    area_counter = Counter([
        item.get("location", {}).get("address", "Unknown") for item in complaints
    ])

    trend = [
        {"day": key, "complaints": value}
        for key, value in sorted(trend_map.items(), key=lambda x: x[0])
    ]

    area_wise = [{"area": key, "complaints": value} for key, value in area_counter.items()]

    return {
        "total_complaints": len(complaints),
        "pending": status_counter.get("Pending", 0),
        "in_progress": status_counter.get("In Progress", 0),
        "completed": status_counter.get("Completed", 0),
        "trend": trend,
        "area_wise": area_wise,
    }
