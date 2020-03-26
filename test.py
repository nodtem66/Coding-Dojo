import unittest

import grader.utils as utils
from grader.Grader import ConfigGrader, Grader
from grader.JsonGrader import JsonGrader
from grader.SakulGrader import ExtendedSakulGrader, SakulGrader


class TestUtils(unittest.TestCase):
    def test_round(self):
        self.assertTrue(utils.round(0.5), 0)
        self.assertTrue(utils.round(0.5), 1)
        self.assertTrue(utils.round(1.5), 2)
        self.assertTrue(utils.round(60.45, 0), 60)
        self.assertTrue(utils.round(1.44, 1), 1.4)
        self.assertTrue(utils.round(1.45, 1), 1.5)
    
class TestCoverage(unittest.TestCase):
    def test_grader(self):
        grader = ConfigGrader('test')
        with self.assertRaises(NotImplementedError):
            grader.evaluate(0)
        self.assertEqual(grader.evaluate_list(0), [])
    def test_json_grader(self):
        with self.assertRaisesRegex(IOError, "Missing JSON data"):
            JsonGrader('{}')
        with self.assertRaisesRegex(IOError, "criterias key must be list"):
            JsonGrader('{"criterias": 1}')
        with self.assertRaisesRegex(IOError, "round key must be int"):
            JsonGrader('{"criterias": [], "round": 1.0}')
        with self.assertRaisesRegex(IOError, "criterias must be list of object"):
            JsonGrader('{"criterias": [1]}')
        with self.assertRaisesRegex(IOError, "criteria must have grade key"):
            JsonGrader('{"criterias": [{}]}')
        with self.assertRaisesRegex(IOError, "run parse_config\(\) before evaluate\(\)"):
            grader = JsonGrader()
            grader.evaluate(0)
        
        grader = JsonGrader('{"criterias": [{"grade": "A"}]}')
        self.assertEqual(grader.evaluate(0), "A")

        grader = JsonGrader('grader_config_example.json')
        self.assertGreater(len(grader._params), 0)

class TestSakulGrader(unittest.TestCase):
    def setUp(self):
        self.grader = SakulGrader()
    def test_init(self):
        self.assertTrue(isinstance(self.grader, SakulGrader))
        self.assertTrue(isinstance(self.grader, Grader))
    def test_evaluate(self):
        self.assertEqual(self.grader.evaluate(0), "F")
        self.assertEqual(self.grader.evaluate(60), "F")
        self.assertEqual(self.grader.evaluate(60.5), "")
        self.assertEqual(self.grader.evaluate(61), "D")
        self.assertEqual(self.grader.evaluate(62), "D")
        self.assertEqual(self.grader.evaluate(70), "D")
        self.assertEqual(self.grader.evaluate(70.5), "")
        self.assertEqual(self.grader.evaluate(71), "C")
        self.assertEqual(self.grader.evaluate(80.5), "")
        self.assertEqual(self.grader.evaluate(81), "B")
        self.assertEqual(self.grader.evaluate(90.5), "")
        self.assertEqual(self.grader.evaluate(100), "A")
    def test_evaluate_list(self):
        scores = [x for x in range(0, 101)]
        grades = list("F"*61 + "D"*10 + "C"*10 + "B"*10 + "A"*10)
        self.assertEqual(self.grader.evaluate_list(scores), grades)


class TestExtendedSakulGrader(unittest.TestCase):
    def setUp(self):
        self.grader = ExtendedSakulGrader()
    def test_init(self):
        self.assertTrue(isinstance(self.grader, ExtendedSakulGrader))
        self.assertTrue(isinstance(self.grader, Grader))
    def test_evaluate(self):
        self.assertEqual(self.grader.evaluate(-1), "X")
        self.assertEqual(self.grader.evaluate(0), "F")
        self.assertEqual(self.grader.evaluate(60), "F")
        self.assertEqual(self.grader.evaluate(60.45), "F")
        self.assertEqual(self.grader.evaluate(60.5), "D")
        self.assertEqual(self.grader.evaluate(61), "D")
        self.assertEqual(self.grader.evaluate(62), "D")
        self.assertEqual(self.grader.evaluate(70), "D")
        self.assertEqual(self.grader.evaluate(70.5), "C")
        self.assertEqual(self.grader.evaluate(71), "C")
        self.assertEqual(self.grader.evaluate(80.5), "B")
        self.assertEqual(self.grader.evaluate(81), "B")
        self.assertEqual(self.grader.evaluate(90.5), "A")
        self.assertEqual(self.grader.evaluate(100), "A")
        self.assertEqual(self.grader.evaluate(100.501), "X")
    def test_evaluate_list(self):
        scores = [x for x in range(0, 101)]
        grades = list("F"*61 + "D"*10 + "C"*10 + "B"*10 + "A"*10)
        self.assertEqual(self.grader.evaluate_list(scores), grades)

class TestJsonGrader(unittest.TestCase):
    def setUp(self):
        self.grader = JsonGrader()
    def test_init(self):
        self.assertTrue(isinstance(self.grader, JsonGrader))
        self.assertTrue(isinstance(self.grader, ConfigGrader))
        self.assertTrue(isinstance(self.grader, Grader))
    def test_config(self):
        with self.assertRaisesRegex(IOError, "Missing criterias key"):
            self.grader.parse_config('{"round": 1}')
        with self.assertRaisesRegex(IOError, "Missing JSON data"):
            self.grader.parse_config('{}')
        with self.assertRaisesRegex(IOError, "Missing JSON data"):
            self.grader.parse_config('[]')
    def test_evaluate(self):
        self.grader.parse_config("""{
            "round": 0,
            "criterias": [
                { "from": 0, "to": 49, "grade": "F"},
                { "from": 50, "to": 54, "grade": "D"},
                { "from": 55, "to": 59, "grade": "D+"},
                { "from": 60, "to": 64, "grade": "C"},
                { "from": 65, "to": 69, "grade": "C+"},
                { "from": 70, "to": 74, "grade": "B"},
                { "from": 75, "to": 79, "grade": "B+"},
                { "from": 80, "to": 100, "grade": "A"},
                { "from": 100, "grade": "A+"}
            ],
            "default": "-"
        }
        """)
        self.assertEqual(self.grader.evaluate(-1), "-")
        self.assertEqual(self.grader.evaluate(0), "F")
        self.assertEqual(self.grader.evaluate(49), "F")
        self.assertEqual(self.grader.evaluate(49.5), "D")
        self.assertEqual(self.grader.evaluate(54.5), "D+")
        self.assertEqual(self.grader.evaluate(59.5), "C")
        self.assertEqual(self.grader.evaluate(64.5), "C+")
        self.assertEqual(self.grader.evaluate(69.5), "B")
        self.assertEqual(self.grader.evaluate(74.5), "B+")
        self.assertEqual(self.grader.evaluate(79.45), "B+")
        self.assertEqual(self.grader.evaluate(79.5), "A")
        self.assertEqual(self.grader.evaluate(90), "A")
        self.assertEqual(self.grader.evaluate(91), "A")
        self.assertEqual(self.grader.evaluate(100), "A")
        self.assertEqual(self.grader.evaluate(100.49), "A")
        self.assertEqual(self.grader.evaluate(100.5), "A+")
    def test_evaluate_list(self):
        self.grader.parse_config("""{
            "round": 0,
            "criterias": [
                { "from": 0, "to": 49, "grade": "F"},
                { "from": 50, "to": 54, "grade": "D"},
                { "from": 55, "to": 59, "grade": "D+"},
                { "from": 60, "to": 64, "grade": "C"},
                { "from": 65, "to": 69, "grade": "C+"},
                { "from": 70, "to": 74, "grade": "B"},
                { "from": 75, "to": 79, "grade": "B+"},
                { "from": 80, "to": 100, "grade": "A"},
                { "from": 100, "grade": "A+"}
            ],
            "default": "-"
        }
        """)
        self.maxDiff = None
        scores = [x for x in range(0, 102)]
        grades = ("F "*50 + "D "*5 + "D+ "*5 + "C "*5 + "C+ "*5 + "B "*5 + "B+ "*5 + "A "*21 + "A+ ").split()
        self.assertEqual(self.grader.evaluate_list(scores), grades)


if __name__ == "__main__":
    unittest.main()
