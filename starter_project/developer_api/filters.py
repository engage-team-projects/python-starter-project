from enum import Enum
from typing import Union


class Relation(Enum):
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    GE = "gte"
    LE = "lte"


class FilterRelation:
    def __init__(self, key: str, relation: Relation, value: str):
        self.key = key
        self.relation = relation
        self.value = value


class Equals(FilterRelation):
    def __init__(self, key: str, value: str):
        super().__init__(key, Relation.EQ, value)


class GreaterThan(FilterRelation):
    def __init__(self, key: str, value: str):
        super().__init__(key, Relation.GT, value)


class LessThan(FilterRelation):
    def __init__(self, key: str, value: str):
        super().__init__(key, Relation.LT, value)


class GreaterThanOrEqual(FilterRelation):
    def __init__(self, key: str, value: str):
        super().__init__(key, Relation.GE, value)


class LessThanOrEqual(FilterRelation):
    def __init__(self, key: str, value: str):
        super().__init__(key, Relation.LE, value)


class Filter:
    def __init__(self, key: str):
        self.key = key

    def eq(self, value: Union[int, str]):
        """Creates a filter there the attribute is equal to the value

        :param value: The value that the attribute should be equal to
        :return:
        """
        return Equals(self.key, value)

    def gt(self, value: int):
        """Creates a filter there the attribute is greater than the value

        :param value: The value that the attribute should be greater than
        :return:
        """
        return GreaterThan(self.key, value)

    def lt(self, value: int):
        """Creates a filter there the attribute is less than the value

        :param value: The value that the attribute should be less than
        :return:
        """
        return LessThan(self.key, value)

    def ge(self, value: int):
        """Creates a filter there the attribute is greater than or equal to the value

        :param value: The value that the attribute should be greater than or equal to
        :return:
        """
        return GreaterThanOrEqual(self.key, value)

    def le(self, value: int):
        """Creates a filter there the attribute is less than or equal to the value

        :param value: The value that the attribute should be less than or equal to
        :return:
        """
        return LessThanOrEqual(self.key, value)
