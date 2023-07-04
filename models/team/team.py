from typing import List
import uuid

from pydantic import BaseModel, Field
from models.player.batter import Batter
from models.player.pitcher import Pitcher


class Team(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    lineup: List[Batter] = Field(...)
    pitcher: Pitcher = Field(...)
    at_bat: int = 0
