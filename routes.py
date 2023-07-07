from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models.at_bat.at_bat import AtBat, AtBatRequest

from models.game.game import Game, SimpleGame


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new game",
    status_code=status.HTTP_201_CREATED,
    response_model=Game,
)
def create_game(request: Request, game: Game = Body(...)):
    game = jsonable_encoder(game)
    new_game = request.app.database["games"].insert_one(game)
    created_game = request.app.database["games"].find_one({"_id": new_game.inserted_id})

    return created_game


@router.get("/", response_description="List all games", response_model=List[Game])
def list_games(request: Request):
    games = list(request.app.database["games"].find(limit=100))
    return games


@router.get(
    "/{id}", response_description="Get a single game by id", response_model=Game
)
def find_game(id: str, request: Request):
    if (game := request.app.database["games"].find_one({"_id": id})) is not None:
        return game
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Game with ID {id} not found"
    )


@router.post(
    "/{id}/at-bat",
    response_description="Create an at bat",
    status_code=status.HTTP_201_CREATED,
    response_model=Game,
)
def initiate_at_bat(id: str, request: Request, at_bat_body: AtBatRequest = Body(...)):
    # will build this with entire pitcher and batter objects being passed in. will eventually store the players in the db and retreive them here
    if (game := request.app.database["games"].find_one({"_id": id})) is not None:
        game = Game(**game)
        at_bat = AtBat(
            batter_guess=at_bat_body.batterGuess,
            pitcher_guess=at_bat_body.pitcherGuess,
            batter=at_bat_body.batter,
            pitcher=at_bat_body.pitcher,
        )
        at_bat_result = at_bat.pitch()
        game = game.updateGameAfterPitch(at_bat_result)

        request.app.database["games"].replace_one(
            {"_id": id},
            game.dict(by_alias=True) | {"batting_team": game.batting_team.value},
        )
        if (
            existing_game := request.app.database["games"].find_one({"_id": id})
        ) is not None:
            return existing_game
        return game
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Game with ID {id} not found"
    )
