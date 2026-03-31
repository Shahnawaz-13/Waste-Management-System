from pydantic import BaseModel


class TrendPoint(BaseModel):
    day: str
    complaints: int


class AreaPoint(BaseModel):
    area: str
    complaints: int


class DashboardAnalytics(BaseModel):
    total_complaints: int
    pending: int
    in_progress: int
    completed: int
    trend: list[TrendPoint]
    area_wise: list[AreaPoint]
