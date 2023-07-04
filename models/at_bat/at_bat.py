from enum import Enum
from pydantic import BaseModel


class AtBatResult(Enum):
    HOMERUN = 0
    TRIPLE = 1
    DOUBLE = 2
    SINGLE = 3
    WALK = 4
    OUT = 5


result_mapping = {
    range(0, 14): AtBatResult.HOMERUN,
    range(15, 20): AtBatResult.TRIPLE,
    range(21, 46): AtBatResult.DOUBLE,
    range(47, 118): AtBatResult.SINGLE,
    range(119, 147): AtBatResult.WALK,
    range(148, 500): AtBatResult.OUT,
}


class AtBatRequest(BaseModel):
    batterGuess: int
    pitcherGuess: int


class AtBat(BaseModel):
    # will eventually need pitcher and batter attributes
    batter_guess: int
    pitcher_guess: int

    def pitch(self) -> AtBatResult:
        difference = self.__calculateDifference(self.pitcher_guess, self.batter_guess)

        for key in result_mapping:
            if difference in key:
                return result_mapping[key]

    @staticmethod
    def __calculateDifference(pitcher_guess: int, batter_guess: int) -> int:
        abs_difference = abs(pitcher_guess - batter_guess)
        if abs_difference > 500:
            return 1000 - abs_difference
        else:
            return abs_difference
