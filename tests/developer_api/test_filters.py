import pytest

from starter_project.developer_api.filters import Filter, Relation


class TestFilters:
    TEST_KEY = "some-key"
    TEST_VALUE = "some-value"

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.test_filter = Filter(self.TEST_KEY)

    def test_construct_eq_relation(self):
        equals_filter = self.test_filter.eq(self.TEST_VALUE)
        assert equals_filter.key == self.TEST_KEY
        assert equals_filter.relation == Relation.EQ
        assert equals_filter.value == self.TEST_VALUE

    def test_construct_gt_relation(self):
        greater_than_filter = self.test_filter.gt(self.TEST_VALUE)
        assert greater_than_filter.key == self.TEST_KEY
        assert greater_than_filter.relation == Relation.GT
        assert greater_than_filter.value == self.TEST_VALUE

    def test_construct_lt_relation(self):
        less_than_filter = self.test_filter.lt(self.TEST_VALUE)
        assert less_than_filter.key == self.TEST_KEY
        assert less_than_filter.relation == Relation.LT
        assert less_than_filter.value == self.TEST_VALUE

    def test_construct_gte_relation(self):
        greater_than_or_equal_filter = self.test_filter.ge(self.TEST_VALUE)
        assert greater_than_or_equal_filter.key == self.TEST_KEY
        assert greater_than_or_equal_filter.relation == Relation.GE
        assert greater_than_or_equal_filter.value == self.TEST_VALUE

    def test_construct_lte_relation(self):
        less_than_or_equal_filter = self.test_filter.le(self.TEST_VALUE)
        assert less_than_or_equal_filter.key == self.TEST_KEY
        assert less_than_or_equal_filter.relation == Relation.LE
        assert less_than_or_equal_filter.value == self.TEST_VALUE
