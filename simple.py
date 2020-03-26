import sys

from grader.SakulGrader import SakulGrader

if __name__ == "__main__":
    try:
        score = float(input("Input score: "))
        grader = SakulGrader()
        print(grader.evaluate(score))
    except:
        print("Nice! try again:", sys.exc_info()[0])
