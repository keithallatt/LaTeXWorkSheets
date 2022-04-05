"""

"""
import abc


def _mask(length, shift):
    def mask_variable(var):
        return var & (((1 << length) - 1) << shift)

    return mask_variable


# PROBLEM LEVEL #

class GradeLevel:
    mask = _mask(4, 0)
    PreK = 0
    Kindergarten = 1
    Grade1 = 2
    Grade2 = 3
    Grade3 = 4
    Grade4 = 5
    Grade5 = 6
    Grade6 = 7
    Grade7 = 8
    Grade8 = 9
    Grade9 = 10
    Grade10 = 11
    Grade11 = 12
    Grade12 = 13
    University = 14


class Difficulty:
    mask = _mask(4, 4)
    Basic = 1 << 4
    Simple = 2 << 4
    Intermediate = 3 << 4
    Advanced = 4 << 4
    Expert = 5 << 4


class LaTeXPiece(abc.ABC):
    def __init__(self):
        self._on_new_page = False

    @abc.abstractmethod
    def __str__(self, solved=False):
        pass


class Problem(LaTeXPiece):
    def __init__(self, grade_level: int = GradeLevel.Grade1, difficulty: int = Difficulty.Basic):
        super().__init__()
        self.gd_encoded = grade_level | difficulty
        self._on_new_page = True

    @abc.abstractmethod
    def __str__(self, solved=False):
        pass


if __name__ == '__main__':
    pass
