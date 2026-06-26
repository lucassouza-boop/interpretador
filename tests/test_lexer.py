from minipy.lexer import Lexer
from minipy.tokens import TokenType as T


def types(source):
    return [t.type for t in Lexer(source).tokenize()]


def test_numbers_and_ops():
    toks = Lexer("1 + 2 * 3\n").tokenize()
    assert toks[0].type == T.INT and toks[0].value == 1
    assert toks[1].type == T.PLUS
    assert toks[3].type == T.STAR


def test_float():
    toks = Lexer("3.14\n").tokenize()
    assert toks[0].type == T.FLOAT and toks[0].value == 3.14


def test_string_escape():
    toks = Lexer(r'"a\nb"' + "\n").tokenize()
    assert toks[0].type == T.STRING and toks[0].value == "a\nb"


def test_keywords():
    ts = types("def if else while return True False None\n")
    assert T.DEF in ts and T.IF in ts and T.WHILE in ts


def test_indent_dedent():
    src = "if True:\n    x = 1\n"
    ts = types(src)
    assert T.INDENT in ts
    assert T.DEDENT in ts


def test_comment_ignored():
    toks = Lexer("# comentário\n1\n").tokenize()
    assert toks[0].type == T.INT
