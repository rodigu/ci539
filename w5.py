import pandas as pd
import math
from dataclasses import dataclass


def mae(r):
    pass


def rmse():
    pass


@dataclass
class ConfusionMatrix():
    true_positive: int
    true_negative: int
    false_positive: int
    false_negative: int

    def total_actual_positive(self):
        return self.true_positive + self.false_negative

    def total_actual_negative(self):
        return self.true_negative + self.false_positive


def kappa():
    pass
