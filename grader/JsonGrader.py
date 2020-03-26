""" From Sakul's criteria: https://github.com/saladpuk/Coding-Dojo """
""" We implemented the JSON-based logic file """
from .Grader import ConfigGrader
import os
import json
from . import utils

class JsonGrader(ConfigGrader):
    
    _params = {"default": "X", "round": 0}
    _is_checked_config = False

    def __init__(self, config_file=""):
        if config_file:
            self.parse_config(config_file)
            
    def parse_config(self, config):
        params = {}
        if os.path.exists(config) and os.path.isfile(config):
            with open(config, "r") as f:
                params = json.load(f)
        else:
            params = json.loads(config)
        self.check_config(params)
        self._params = params
        if not "default" in params:
            self._params["default"] = "X"
        if not "round" in params:
            self._params["round"] = 0
        self._is_checked_config = True

    def check_config(self, params):
        if len(params) == 0:
            raise IOError("Missing JSON data")
        if not "criterias" in params:
            raise IOError("Missing criterias key")
        else:
            if not isinstance(params["criterias"], list):
                raise IOError("criterias key must be list")
            for c in params["criterias"]:
                if not isinstance(c, dict):
                    raise IOError("criterias must be list of object")
                if not "grade" in c:
                    raise IOError("criteria must have grade key")
        if "round" in params and not isinstance(params["round"], int):
            raise IOError("round key must be int")
        self._is_checked_config = True

    def evaluate(self, score):
        if not self._is_checked_config:
            raise IOError("run parse_config() before evaluate()")
        return super().evaluate(score)

    def _before(self, raw):
        return utils.round(raw, self._params["round"])

    def grading(self, score):
        for c in self._params["criterias"]:
            success = True
            if success and "from" in c:
                success = (score >= float(c["from"]))
            if success and "to" in c:
                success = (score <= float(c["to"]))
            if success:
                return c.get("grade")
        return None

    def _after(self, grade):
        if grade:
            return grade
        return self._params["default"]