pytest_plugins = 'pytester'


test_str = """
import pytest

def test_add():
    assert 1 + 2 == 3

def test_add_fail():
    assert 1 + 2 == 4

    
@pytest.mark.xfail(reason='This test is expected to fail')
def test_subtract():
    assert 2 - 1 == 0


@pytest.mark.skipif(True, reason='This test is skipped')
def test_multiply():
    assert 2 * 2 == 5
"""


def test_base(pytester):
    pytester.makepyfile(test_str)
    result = pytester.runpytest()
    assert any('passed' in x and '1' in x for x in result.outlines)
    assert any('failed' in x and '1' in x for x in result.outlines)
    assert any('skipped' in x and '1' in x for x in result.outlines)
    assert any('xfailed' in x and '1' in x for x in result.outlines)

def test_fixture(pytester_pretty):
    pytester_pretty.makepyfile(test_str)
    result = pytester_pretty.runpytest()
    result.assert_outcomes(passed=1, failed=1, skipped=1, xfailed=1)
    lines = result.outlines
    # Look for the table row with function name, function line, and error line
    assert any('test_add_fail' in line and '6' in line and '7' in line and "AssertionError" in line for line in lines)

def test_fixture_short(pytester_pretty):
    pytester_pretty.makepyfile(test_str)
    result = pytester_pretty.runpytest("--tb=short")
    result.assert_outcomes(passed=1, failed=1, skipped=1, xfailed=1)
    lines = result.outlines
    assert any('test_add_fail' in line and '6' in line and '7' in line and "assert (1 + 2) == 4" in line for line in lines)

def test_fixture_line(pytester_pretty):
    pytester_pretty.makepyfile(test_str)
    result = pytester_pretty.runpytest("--tb=line")
    result.assert_outcomes(passed=1, failed=1, skipped=1, xfailed=1)
    lines = result.outlines
    assert any('test_add_fail' in line and '6' in line and '7' in line and "assert (1 + 2) == 4" in line for line in lines)

