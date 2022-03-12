# from io_helper import print_func
import copy

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

def remove_double_implies(bnf_lines):
    for ind, line in enumerate(bnf_lines):
        begun = False
        first, second = None, None
        curcount = -1
        index = len(line) - 1
        end_index = -1
        mid_index = -1
        while index >= 0:
            if not begun and line[index] != DOUBLE_IMPLIES:
                index -= 1
                continue
            if not begun:
                end_index = index
                index -= 1
                begun = True
                curcount = 1
                continue
            assert begun and curcount > 0 and not is_bracket(line[index])
            if is_atom(line[index]):
                curcount -= 1
            elif is_bracket(line[index]):
                pass
            elif is_operator(line[index]):
                if line[index] == NEGATION:
                    curcount += 0
                else:
                    curcount += 1
            if curcount == 0 and second is None:
                assert end_index != -1 and mid_index == -1
                second = copy.deepcopy(line[index : end_index])
                curcount = 1
                mid_index = index
            elif curcount == 0:
                assert end_index != -1 and mid_index != -1 and first is None and second is not None
                first = copy.deepcopy(line[index:mid_index])
                curcount = -1
                begun = False
                # line = line[:index] + first + [NEGATION] + second + [OR] + copy.deepcopy(second) + [NEGATION] + copy.deepcopy(first) + [OR, AND] + line[end_index + 1:]
                line = line[:index] + first + second + [IMPLIES] + copy.deepcopy(second) + copy.deepcopy(first) + [IMPLIES, AND] + line[end_index + 1:]
                index += 2 * len(first) + 2 * len(second) + 3
                end_index, mid_index = -1, -1
                first, second = None, None
            index -= 1
        bnf_lines[ind] = line
    return bnf_lines

def remove_implies(bnf_lines):
    for ind, line in enumerate(bnf_lines):
        index = len(line) - 1
        begun = False
        curcount = -1
        end_index = -1
        while index >= 0:
            if not begun and line[index] != IMPLIES:
                index -= 1
                continue
            if not begun:
                line[index] = OR
                end_index = index
                index -= 1
                begun = True
                curcount = 1
                continue
            assert begun and curcount > 0
            if is_atom(line[index]):
                curcount -= 1
            elif is_bracket(line[index]):
                pass
            elif is_operator(line[index]):
                if line[index] == NEGATION:
                    curcount += 0
                else:
                    curcount += 1
            if curcount == 0:
                line.insert(index, NEGATION)
                index = end_index + 1
                end_index = -1
                begun = False
                curcount = -1
            index -= 1
        bnf_lines[ind] = line
        assert not begun
    return bnf_lines

def update_negation(bnf_lines):
    for ind, line in enumerate(bnf_lines):
        begun = False
        first, second = None, None
        curcount = -1
        index = len(line) - 1
        end_index, mid_index = -1, -1
        while index >= 0:
            if not begun and line[index] != NEGATION:
                index -= 1
                continue
            if not begun:
                assert index > 0
                if line[index - 1] == NEGATION:
                    line.pop(index)
                    line.pop(index - 1)
                    index -= 2
                    begun = False
                    continue
                if is_operator(line[index - 1]):
                    assert curcount == -1
                    assert line[index - 1] == OR or line[index - 1] == AND
                    if line[index - 1] == OR:
                        line[index - 1] = AND
                    else:
                        line[index - 1] = OR
                    line.pop(index)
                    end_index = index - 1
                    index -= 2
                    begun = True
                    curcount = 1
                else:
                    index -= 2
                continue
            assert begun and curcount > 0 and not is_bracket(line[index])
            if is_atom(line[index]):
                curcount -= 1
            elif is_bracket(line[index]):
                pass
            elif is_operator(line[index]):
                if line[index] == NEGATION:
                    curcount += 0
                else:
                    curcount += 1
            if curcount == 0 and second is None:
                assert end_index != -1 and mid_index == -1
                second = copy.deepcopy(line[index : end_index])
                curcount = 1
                mid_index = index
            elif curcount == 0:
                assert end_index != -1 and mid_index != -1 and first is None and second is not None
                first = copy.deepcopy(line[index:mid_index])
                curcount = -1
                begun = False
                line = line[:index] + first + [NEGATION] + second + [NEGATION] + line[end_index:]
                index += len(first) + len(second) + 2
                end_index, mid_index = -1, -1
                first, second = None, None
            index -= 1
        bnf_lines[ind] = line
    return bnf_lines

def update_and_or(bnf_data):
    pass