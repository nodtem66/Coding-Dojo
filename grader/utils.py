""" rounding number to target precision
round(0.4, 0) = 0
round(0.5, 0) = 1
"""
from decimal import Decimal, ROUND_HALF_UP

def round(x, precision: int = 0):
    y = Decimal(1) if precision == 0 else Decimal(str(1/10**precision))
    return Decimal(x).quantize(y, rounding=ROUND_HALF_UP)