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


def test_multiple_operators():
    ts = types("+ - * / % ** == != < > <= >=\n")
    assert T.PLUS in ts and T.MINUS in ts and T.STAR in ts
    assert T.SLASH in ts and T.DOUBLESTAR in ts


def test_logical_operators():
    ts = types("and or not\n")
    assert T.AND in ts and T.OR in ts and T.NOT in ts


def test_identifiers():
    toks = Lexer("x y _var var123\n").tokenize()
    assert toks[0].type == T.NAME and toks[0].value == "x"
    assert toks[1].type == T.NAME and toks[1].value == "y"
    assert toks[2].type == T.NAME and toks[2].value == "_var"
    assert toks[3].type == T.NAME and toks[3].value == "var123"


def test_zero_and_negative_numbers():
    toks = Lexer("0 -5 0.0\n").tokenize()
    assert toks[0].type == T.INT and toks[0].value == 0


def test_string_with_quotes():
    toks = Lexer('"hello world"\n').tokenize()
    assert toks[0].type == T.STRING and toks[0].value == "hello world"


def test_string_empty():
    toks = Lexer('""\n').tokenize()
    assert toks[0].type == T.STRING and toks[0].value == ""


def test_colon_and_parens():
    ts = types("() : = \n")
    assert T.LPAREN in ts and T.RPAREN in ts
    assert T.COLON in ts and T.ASSIGN in ts


def test_elif_keyword():
    ts = types("elif\n")
    assert T.ELIF in ts


def test_multiple_indents():
    src = "if True:\n    if True:\n        x = 1\n"
    ts = types(src)
    indent_count = ts.count(T.INDENT)
    assert indent_count == 2


def test_mixed_indent_dedent():
    src = "if True:\n    x = 1\ny = 2\n"
    ts = types(src)
    assert T.INDENT in ts
    assert T.DEDENT in ts


def test_float_with_leading_zero():
    toks = Lexer("0.5\n").tokenize()
    assert toks[0].type == T.FLOAT and toks[0].value == 0.5


def test_string_with_escape_sequences():
    toks = Lexer(r'"a\tb\n"' + "\n").tokenize()
    assert toks[0].type == T.STRING
    assert "\t" in toks[0].value or "\\t" in repr(toks[0].value)


def test_operators_sequence():
    toks = Lexer("1 + 2 - 3 * 4 / 5\n").tokenize()
    ops = [t for t in toks if t.type in (T.PLUS, T.MINUS, T.STAR, T.SLASH)]
    assert len(ops) == 4


def test_keywords_are_not_names():
    toks = Lexer("while if def return\n").tokenize()
    assert toks[0].type == T.WHILE
    assert toks[1].type == T.IF
    assert toks[2].type == T.DEF
    assert toks[3].type == T.RETURN


def test_comparison_operators():
    ts = types("< > <= >= == !=\n")
    assert T.LT in ts and T.GT in ts
    assert T.LE in ts and T.GE in ts
    assert T.EQ in ts and T.NE in ts
