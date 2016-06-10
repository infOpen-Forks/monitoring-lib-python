# -*- coding: utf-8 -*-

"""
ConnectionCount class tests
--------------------------

Tests for `ConnectionCount` class.
"""


from jsonpath_rw.jsonpath import DatumInContext
from nagiosplugin import Context, Metric, Ok, Critical
import pytest


from temelio_monitoring.context import StringEqualityFromJSON

@pytest.mark.parametrize('expected_string,result,do_cast,expected_output', [
    ('foo', 'bar', False,
     'Json output: bar (expected string: foo // do_str_cast: False)'),
    ('foo', 'foo', False,
     'Json output: foo (expected string: foo // do_str_cast: False)'),
    ('5', 5, True,
     'Json output: 5 (expected string: 5 // do_str_cast: True)'),
    ('5', 5, False,
     'Json output: 5 (expected string: 5 // do_str_cast: False)'),
])
def test_with_args(expected_string, result, do_cast, expected_output):
    """
    Check context output
    """

    context = StringEqualityFromJSON(
        'json_output',
        expected_string=expected_string,
        do_str_cast=do_cast)
    result_array = [DatumInContext(result)]
    metric = Metric('my_metric', result_array)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringEqualityFromJSON) is True
    assert context.describe(metric) == expected_output


def test_without_value():
    """
    Check if JSON path request not return result
    """

    context = StringEqualityFromJSON('json_output', 'foo', False)
    metric = Metric('my_metric', [])

    with pytest.raises(RuntimeError) as err:
        context.evaluate(metric, None)

        assert isinstance(context, Context) is True
        assert isinstance(context, StringEqualityFromJSON) is True
        assert str(err) == 'No value returned by probe'


@pytest.mark.parametrize('expected_string,result,do_cast,eval_result', [
    ('foo', 'bar', False, Critical),
    ('foo', 'foo', False, Ok),
    ('5', 5, True, Ok),
    ('5', 5, False, Critical)
])
def test_eval_with_cast(expected_string, result, do_cast, eval_result):
    """
    Check evaluate method, Rssource param not used, so set it to None
    """

    context = StringEqualityFromJSON(
        'json_output',
        expected_string=expected_string,
        do_str_cast=do_cast)
    result_array = [DatumInContext(result)]
    metric = Metric('my_metric', result_array)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringEqualityFromJSON) is True
    assert context.evaluate(metric, None).state == eval_result