from typing import List, Optional
import uuid

from flask import current_app
from pydantic import BaseModel, Field
from models.at_bat.at_bat import AtBatResult
import models.game.constants as GameConstants
from models.team.team import Team
from enum import Enum


class BattingTeam(Enum):
    AWAY = 0
    HOME = 1


class SimpleGame(BaseModel):
    game: str


class Game(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    home_team: Team
    away_team: Team
    field: List[bool] = [False, False, False]
    inning: int = 1
    outs: int = 0
    batting_team: BattingTeam = BattingTeam.AWAY
    home_score: int = 0
    away_score: int = 0
    is_over: bool = False
    last_play_result: Optional[str]

    def __str__(self) -> str:
        return f"The home team is {self.home_team.name} and the away team is {self.away_team.name}. It is the {self.inning} inning and the score is {self.home_score}-{self.away_score}."

    @staticmethod
    def calculateRunsBattedIn(bases: List[bool], basesAdvanced: int) -> int:
        print(
            "filtered bases are:",
            list(filter(lambda base: base, bases[:basesAdvanced])),
        )
        return len(list(filter(lambda base: base, bases[:basesAdvanced])))

    def updateGameAfterPitch(self, pitch: AtBatResult):
        self.last_play_result = pitch.name
        self = self.updateBatter()
        if pitch == AtBatResult.OUT:
            self.recordOut()
        elif pitch == AtBatResult.WALK:
            if self.field == [True, True, True]:
                self.addRuns(1)
            self.field[0] = True if self.field[1] and self.field[2] else False
            self.field[1] = True if self.field[2] else False
            self.field[2] = True
        else:
            if pitch == AtBatResult.SINGLE:
                self.addRuns(self.calculateRunsBattedIn(self.field, 1))
                self.field[2], self.field[1], self.field[0] = (
                    True,
                    self.field[2],
                    self.field[1],
                )
            elif pitch == AtBatResult.DOUBLE:
                self.addRuns(Game.calculateRunsBattedIn(self.field, 2))
                self.field[2], self.field[1], self.field[0] = False, True, self.field[2]
            elif pitch == AtBatResult.TRIPLE:
                self.addRuns(Game.calculateRunsBattedIn(self.field, 3))
                self.field = [False, False, True]
            elif pitch == AtBatResult.HOMERUN:
                self.addRuns(Game.calculateRunsBattedIn(self.field, 3) + 1)
                self.field = [False, False, False]
        return self

    def recordOut(self):
        if self.outs == 2:
            self.outs = 0
            self.clearField()
            self.is_over = self.isGameOver()
            if self.batting_team == BattingTeam.AWAY:
                self.batting_team = BattingTeam.HOME
            else:
                self.batting_team = BattingTeam.AWAY
                self.inning = self.inning + 1
        else:
            self.outs = self.outs + 1
        return self

    def updateBatter(self):
        if self.batting_team == BattingTeam.AWAY:
            self.away_team.at_bat = (self.away_team.at_bat + 1) % 9
        else:
            self.home_team.at_bat = (self.home_team.at_bat + 1) % 9
        return self

    def addRuns(self, runs: int):
        if self.batting_team == BattingTeam.AWAY:
            self.away_score += runs
        else:
            self.home_score += runs

    def clearField(self):
        self.field = [False, False, False]
        return self

    def isGameOver(self) -> bool:
        if self.batting_team == BattingTeam.AWAY:
            return (
                True
                if self.home_score > self.away_score
                and self.inning >= GameConstants.STANDARD_INNINGS_IN_GAME
                else False
            )
        # this only checks for home team; need to check for away team
        return (
            True
            if self.home_score != self.away_score
            and self.inning == GameConstants.STANDARD_INNINGS_IN_GAME
            else False
        )

    @classmethod
    def get_games(cls) -> list:
        for elem in current_app.db.games.find({}):
            print({**elem["home_team"]})
        # print(cls(**elem).json()) for elem in current_app.db.games.find({})
        return []
        # return [cls(**elem) for elem in current_app.db.games.find({})]
