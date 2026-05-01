from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    content: str = Field(min_length=3, max_length=2000)


class TaskRead(BaseModel):
    id: str
    content: str
    status: str
    moderation_result: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)