from enum import Enum
from pydantic import BaseModel

from models.player.batter import Batter
from models.player.pitcher import Pitcher


class AtBatResult(Enum):
    HOMERUN = 0
    TRIPLE = 1
    DOUBLE = 2
    SINGLE = 3
    WALK = 4
    FLYOUT = 5
    POPOUT = 6
    GROUNDOUT = 7
    STRIKEOUT = 8
    INFIELD_SINGLE = 9
    OUT = 10


hitProb = [107, 109, 113, 116, 119, 129, 137, 146, 152]
hrProb = [5, 7, 9, 12, 15, 23, 28, 33, 38]
doubleProb = [17, 18, 20, 22, 26, 29, 30, 32, 33]
tripleProb = [1, 2, 3, 4, 6, 7, 8, 9, 10]
walkProb = [5, 9, 15, 21, 29, 35, 44, 53, 64]
infieldSingleProb = [1, 1, 3, 4, 6, 11, 15, 20, 24]
# taken off the spreadsheet, but apparently they just proportion out the outs by percentage. For now, just going to have an out.
flyOutProb = [130, 126, 118, 110, 100, 94, 89, 83, 80]
popOutProb = [170, 160, 150, 140, 130, 120, 110, 100, 90]
groundballProb = [177, 167, 156, 146, 131, 114, 96, 80, 67, 57]
strikeoutProb = [158, 146, 133, 120, 103, 90, 72, 60, 43]


class AtBatRequest(BaseModel):
    batterGuess: int
    pitcherGuess: int
    batter: Batter
    pitcher: Pitcher


class AtBat(BaseModel):
    batter_guess: int
    pitcher_guess: int
    batter: Batter
    pitcher: Pitcher

    def pitch(self) -> AtBatResult:
        difference = self.__calculateDifference(self.pitcher_guess, self.batter_guess)

        result_mapping = AtBat.__rangeBuilder(self.batter, self.pitcher)
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

    @staticmethod
    def __rangeBuilder(batter: Batter, pitcher: Pitcher):
        ARRAY_SHIFT = 4  # probability lists are zero indexed while pitcher batter comparisons range from -4 to 4
        hrRangeTop = hrProb[batter.power - pitcher.velocity + ARRAY_SHIFT] - 1
        tripleRangeTop = (
            hrRangeTop + tripleProb[batter.speed - pitcher.awareness + ARRAY_SHIFT]
        )
        doubleRangeTop = (
            tripleRangeTop + doubleProb[batter.speed - pitcher.awareness + ARRAY_SHIFT]
        )
        singleRangeTop = (
            hitProb[batter.contact - pitcher.movement + ARRAY_SHIFT] + 5 - 1
        )  # need to figure out why they added 5
        infieldSingleRangeTop = (
            singleRangeTop
            + infieldSingleProb[batter.speed - pitcher.awareness + ARRAY_SHIFT]
        )
        walkRangeTop = (
            infieldSingleRangeTop + walkProb[batter.eye - pitcher.command + ARRAY_SHIFT]
        )
        # flyOutRangeTop = (
        #     walkRangeTop + flyOutProb[batter.power - pitcher.velocity + ARRAY_SHIFT] - 1
        # )
        # popOutRangeTop = (
        #     flyOutRangeTop
        #     + popOutProb[batter.power - pitcher.velocity + ARRAY_SHIFT]
        #     - 1
        # )
        # gbOutRangeTop = (
        #     popOutRangeTop
        #     + groundballProb[batter.speed - pitcher.awareness + ARRAY_SHIFT]
        #     - 1
        # )
        # strikeoutRangeTop = (
        #     gbOutRangeTop
        #     + strikeoutProb[batter.contact - pitcher.movement + ARRAY_SHIFT]
        #     - 1
        # )

        return {
            range(0, hrRangeTop): AtBatResult.HOMERUN,
            range(hrRangeTop + 1, tripleRangeTop): AtBatResult.TRIPLE,
            range(tripleRangeTop + 1, doubleRangeTop): AtBatResult.DOUBLE,
            range(doubleRangeTop + 1, singleRangeTop): AtBatResult.SINGLE,
            range(
                singleRangeTop + 1, infieldSingleRangeTop
            ): AtBatResult.INFIELD_SINGLE,
            range(infieldSingleRangeTop + 1, walkRangeTop): AtBatResult.WALK,
            range(walkRangeTop + 1, 500): AtBatResult.OUT
            # range(walkRangeTop + 1, flyOutRangeTop): AtBatResult.FLYOUT,
            # range(flyOutRangeTop + 1, popOutRangeTop): AtBatResult.POPOUT,
            # range(popOutRangeTop + 1, gbOutRangeTop): AtBatResult.GROUNDOUT,
            # range(gbOutRangeTop + 1, strikeoutRangeTop): AtBatResult.STRIKEOUT,
        }
