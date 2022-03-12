# from io_helper import print_func

NEGATION = '!'
AND = '&'
OR = '|'
IMPLIES = '=>'
DOUBLE_IMPLIES = '<=>'
ALL_OPERATORS = [NEGATION, AND, OR, IMPLIES, DOUBLE_IMPLIES]

def is_atom(token: str) -> bool:
    assert " " not in token
    return all(char.isalnum() or char == '_' for char in token)

def is_operator(token: str) -> bool:
    assert " " not in token
    return token in ALL_OPERATORS

def is_bracket(token: str) -> bool:
    assert " " not in token
    return token in [")", "("]

def higher_precedence(operator1: str, operator2: str) -> bool:
    return ALL_OPERATORS.index(operator1) < ALL_OPERATORS.index(operator2)

def get_precedence(operator: str) -> int:
    return len(ALL_OPERATORS) - ALL_OPERATORS.index(operator)