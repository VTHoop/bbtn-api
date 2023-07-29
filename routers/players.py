from fastapi import APIRouter, Body, Request, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models.player.batter import Batter
from models.player.pitcher import Pitcher


router = APIRouter()


@router.post(
    "/player/batter",
    response_description="Create a new batter",
    status_code=status.HTTP_201_CREATED,
    response_model=Batter,
)
def create_batter(request: Request, batter: Batter = Body(...)):
    batter = jsonable_encoder(batter)
    new_batter = request.app.database["players"].insert_one(batter)
    created_batter = request.app.database["players"].find_one(
        {"_id": new_batter.inserted_id}
    )

    return created_batter


@router.post(
    "/player/pitcher",
    response_description="Create a new pitcher",
    status_code=status.HTTP_201_CREATED,
    response_model=Pitcher,
)
def create_pitcher(request: Request, pitcher: Pitcher = Body(...)):
    pitcher = jsonable_encoder(pitcher)
    new_pitcher = request.app.database["players"].insert_one(pitcher)
    created_pitcher = request.app.database["players"].find_one(
        {"_id": new_pitcher.inserted_id}
    )

    return created_pitcher


@router.get(
    "/player",
    response_description="List all players",
    response_model=List[Pitcher | Batter],
)
def list_players(request: Request, team: str | None = None):
    if team:
        return list(request.app.database["players"].find({"team": team}, limit=1000))
    return list(request.app.database["players"].find(limit=1000))
