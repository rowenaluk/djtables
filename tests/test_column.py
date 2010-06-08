#!/usr/bin/env python
# vim: et ts=4 sw=4


from fudge import Fake
from nose.tools import assert_raises
from tables.column import Column, WrappedColumn


def test_sortable_by_order_of_creation():
    a, b, c = Column(), Column(), Column()
    assert sorted([b, a, c]) == [a, b, c]


def test_can_be_bound():
    table  = Fake()
    column = Column()

    column.bind_to(table, "alpha")

    assert column.is_bound == True
    assert column.bound_to == (table, "alpha")


def test_raises_if_rebound():
    table_a = Fake()
    table_b = Fake()
    column = Column()

    column.bind_to(table_a, "beta")

    assert_raises(AttributeError,
        column.bind_to, table_b, "gamma")


def test_can_be_explicitly_named():
    column = Column(name="delta")
    assert column.name == "delta"


def test_can_be_named_by_binding():
    table  = Fake()
    column = Column()

    column.bind_to(table, "epsilon")

    assert column.name == "epsilon"


def test_renders_values_to_unicode():
    assert Column().render(True) == u"True"
    assert Column().render(123) == u"123"


def test_renders_name_to_unicode():
    assert unicode(Column('zeta')) == u"zeta"


def test_wrapped_column_wraps_column_attrs():
    table  = Fake()
    column = Fake().has_attr(eta=123).provides("__unicode__").returns("theta")

    wrapped_column = WrappedColumn(table, column)
    wrapped_column.iota = 456

    assert wrapped_column.eta == 123
    assert wrapped_column.iota == 456

    assert unicode(column) == "theta"
    assert unicode(wrapped_column) == "theta"


def test_wrapped_column_is_sorted_via_table():
    meta     = Fake().has_attr(order_by="kappa")
    table    = Fake().has_attr(_meta=meta)
    column_a = Fake().has_attr(name="kappa")
    column_b = Fake().has_attr(name="mu")

    wrapped_column_a = WrappedColumn(table, column_a) # sorted
    wrapped_column_b = WrappedColumn(table, column_b) # unsorted

    assert wrapped_column_a.is_sorted == True
    assert wrapped_column_b.is_sorted == False
    assert wrapped_column_a.sort_direction == "asc"
    assert wrapped_column_b.sort_direction == None


def test_wrapped_column_has_sort_url():
    table  = Fake().provides("get_url").calls(
        lambda order_by: ["nu", order_by])
    column = Fake().has_attr(name="xi")

    wrapped_column = WrappedColumn(table, column)

    assert wrapped_column.sort_url == ["nu", "xi"]
