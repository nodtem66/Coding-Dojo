""" From Sakul's criteria: https://github.com/saladpuk/Coding-Dojo """
from .Grader import Grader
from . import utils

class SakulGrader(Grader):
    def grading(self, score):
        if score >= 91 and score <= 100:
            return "A"
        elif score >= 81 and score <= 90:
            return "B"
        elif score >= 71 and score <= 80:
            return "C"
        elif score >= 61 and score <= 70:
            return "D"
        elif score >= 0 and score <= 60:
            return "F"
        return ""

class ExtendedSakulGrader(SakulGrader):
    def _before(self, raw_score):
        return utils.round(raw_score)
    def _after(self, grade):
        if not grade:
            return "X"
        return grade