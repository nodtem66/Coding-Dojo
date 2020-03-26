""" Grader base class """
class Grader:
    """ process the raw score before grading"""
    def _before(self, raw_score):
        return raw_score
    """ process the result grade after grading """
    def _after(self, grade):
        return grade
    """ Evaluate the input score and return string """
    def grading(self, score):
        raise NotImplementedError()
    """ prepare the score, grading, post-processing the result """
    def evaluate(self, raw):
        score = self._before(raw)
        grade = self.grading(score)
        return self._after(grade)
    """ Evaluate the score list and return grades """
    def evaluate_list(self, scores: list) -> list:
        if isinstance(scores, list):
            return [self.evaluate(float(x)) for x in scores]
        return []

class ConfigGrader(Grader):
    """ Add the config file parameter """
    def __init__(self, config_file):
        pass