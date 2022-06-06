from enum import Enum


class StrategyName(Enum):
    average = 'average'
    # another_strategy = ...


DEDUCTIBLE = 'deductible'
STOP_LOSS = 'stop_loss'
OOP_MAX = 'oop_max'


class BaseStrategy(object):

    def __init__(self):
        self.deductibles = 0
        self.stop_losses = 0
        self.oop_maxs = 0

    def process(self, responses: list):
        raise NotImplementedError


class AverageStrategy(BaseStrategy):

    def process(self, responses: list):
        for r in responses:
            self.deductibles += int(r.get(DEDUCTIBLE, 0))
            self.stop_losses += int(r.get(STOP_LOSS, 0))
            self.oop_maxs += int(r.get(OOP_MAX, 0))

        qty = len(responses)
        response = {
            DEDUCTIBLE: int(self.deductibles / qty),
            STOP_LOSS: int(self.stop_losses  / qty),
            OOP_MAX: int(self.oop_maxs  / qty),
        }
        return response
