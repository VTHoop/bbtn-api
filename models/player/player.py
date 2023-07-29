from typing import Optional
import uuid
from pydantic import BaseModel, Field


class Player(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    number: int = Field(...)
    position: str = Field(...)
    team: Optional[str]
