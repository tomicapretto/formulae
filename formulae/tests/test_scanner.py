import pytest

from formulae.scanner import Scanner, ScanError
from formulae.token import Token


def compare_two_lists(l1, l2):
    return all([True if i == j else False for i, j in zip(l1, l2)])


def test_scan_empty():
    with pytest.raises(ScanError):
        Scanner("").scan()


def test_scan_literal():
    sc = Scanner("'A'").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("STRING", "'A'", "A"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("1").scan()
    comp = [Token("NUMBER", "1", 1), Token("PLUS", "+"), Token("NUMBER", "1", 1), Token("EOF", "")]
    assert compare_two_lists(sc, comp)

    sc = Scanner("1.132").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("NUMBER", "1.132", 1.132),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)


def test_scan_quoted_name():
    sc = Scanner("`$$##!!`").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("BQNAME", "`$$##!!`"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)


def test_scan_variable():
    sc = Scanner("x").scan()
    comp = [Token("NUMBER", "1", 1), Token("PLUS", "+"), Token("IDENTIFIER", "x"), Token("EOF", "")]
    assert compare_two_lists(sc, comp)


def test_scan_call():
    sc = Scanner("f(x)").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "f"),
        Token("LEFT_PAREN", "("),
        Token("IDENTIFIER", "x"),
        Token("RIGHT_PAREN", ")"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("module.f(x)").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "module.f"),
        Token("LEFT_PAREN", "("),
        Token("IDENTIFIER", "x"),
        Token("RIGHT_PAREN", ")"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("{x + y}").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("LEFT_BRACE", "{"),
        Token("IDENTIFIER", "x"),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "y"),
        Token("RIGHT_BRACE", "}"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)


def test_scan_binary():
    sc = Scanner("x + y").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x - y").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("MINUS", "-"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x * y").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("STAR", "*"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x / y").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("SLASH", "/"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x : y").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("COLON", ":"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x ** 2").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("STAR_STAR", "**"),
        Token("NUMBER", "2", 2),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x | y").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("PIPE", "|"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x ~ y").scan()
    comp = [
        Token("IDENTIFIER", "x"),
        Token("TILDE", "~"),
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)


def test_scan_grouping():
    sc = Scanner("(x + z)").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("LEFT_PAREN", "("),
        Token("IDENTIFIER", "x"),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "z"),
        Token("RIGHT_PAREN", ")"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)


def test_scan_assign():
    sc = Scanner("x = z").scan()
    comp = [
        Token("NUMBER", "1", 1),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "x"),
        Token("EQUAL", "="),
        Token("IDENTIFIER", "z"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)


def test_scan_intercept_disabled():
    sc = Scanner("x + y").scan(add_intercept=False)
    comp = [
        Token("IDENTIFIER", "x"),
        Token("PLUS", "+"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)

    sc = Scanner("x ~ y").scan(add_intercept=False)
    comp = [
        Token("IDENTIFIER", "x"),
        Token("TILDE", "~"),
        Token("IDENTIFIER", "y"),
        Token("EOF", ""),
    ]
    assert compare_two_lists(sc, comp)
