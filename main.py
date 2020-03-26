import argparse
import os
import sys
from importlib import import_module

from grader.Grader import ConfigGrader, Grader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("score", nargs="+", help="input score")
    parser.add_argument("-g", "--grader", help="Name of grader (sakul, json)")
    parser.add_argument("-v", "--verbose", help="output verbosity", action="store_true")
    parser.add_argument("-c", "--config", help="JSON file", type=str)
    args = parser.parse_args()
    try:
        # if --grader option enable, dynamically import the grader
        # otherwise load default grader "SakulGrader"
        if args.grader and len(args.grader) > 0:
            grader_name = args.grader + "Grader"
        elif args.config and os.path.splitext(args.config)[1].lower() == '.json':
            grader_name = "JsonGrader"
        else:
            grader_name = "SakulGrader"
        if (args.verbose):
            print(f"-- use: {grader_name}")
        
        import_grader = import_module("grader." + grader_name)
        MyGrader = getattr(import_grader, grader_name)
        # check the loaded grader is a subclass of Grader
        if not issubclass(MyGrader, Grader):
            raise NotImplementedError()
        
        
        if issubclass(MyGrader, ConfigGrader):
            grader = MyGrader(args.config)
        else:
            grader = MyGrader()
        grades = grader.evaluate_list(args.score)
        for grade in grades:
            print(grade)
    except:
        print("Unexpected error:", sys.exc_info()[0])
