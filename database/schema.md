# Database Schema (MongoDB)

## Collection: `complaints`

```json
{
  "id": "uuid-string",
  "user_id": "user_1001",
  "description": "Overflowing dustbin near bus stop",
  "location": {
    "latitude": 28.6139,
    "longitude": 77.2090,
    "address": "Connaught Place"
  },
  "image_url": "uploads/<filename>.jpg",
  "predicted_class": "Plastic",
  "status": "Pending",
  "assigned_worker_id": "worker_01",
  "created_at": "2026-03-31T10:15:00Z",
  "updated_at": "2026-03-31T10:20:00Z"
}
```

## Suggested Indexes

- `id` (unique)
- `status`
- `assigned_worker_id`
- `created_at`
- `location.latitude + location.longitude` (compound for geospatial analytics)
