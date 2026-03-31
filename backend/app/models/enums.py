from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"
    WORKER = "worker"


class ComplaintStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class WasteClass(str, Enum):
    PLASTIC = "Plastic"
    METAL = "Metal"
    ORGANIC = "Organic"
