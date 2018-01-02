from typing import List

from ape.feaquencer.check_order import OrderingCondition


class MultipleFirstConditionsError(Exception):
    def __init__(self, msg: str, occ1: str, occ2: OrderingCondition) -> None:
        super(MultipleFirstConditionsError, self).__init__(msg)
        self.occurences = [occ1, occ2]


class MultipleLastConditionsError(Exception):
    def __init__(self, msg: str, occ1: str, occ2: OrderingCondition) -> None:
        super(MultipleLastConditionsError, self).__init__(msg)
        self.occurences = [occ1, occ2]


class AfterConditionToLastError(Exception):
    pass


class GraphCycleError(Exception):
    def __init__(self, cycle: List[str]) -> None:
        msg = "Cycle was detected in dependency graph: \n \t"
        for idx, feature in enumerate(cycle):
            msg += " {feature}".format(feature=feature)
            if idx != (len(cycle) - 1):
                msg += " =>"
        super(GraphCycleError, self).__init__(msg)
