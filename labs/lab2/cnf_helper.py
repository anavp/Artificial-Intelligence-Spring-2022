import copy
NEGATION = '!'
AND = '&'
OR = '|'
IMPLIES = '=>'
DOUBLE_IMPLIES = '<=>'
ALL_OPERATORS = [NEGATION, AND, OR, IMPLIES, DOUBLE_IMPLIES]

def is_atom(token: str) -> bool:
    # assert " " not in token
    return all(char.isalnum() or char == '_' for char in token)

def is_operator(token: str) -> bool:
    # assert " " not in token
    return token in ALL_OPERATORS

def is_bracket(token: str) -> bool:
    # assert " " not in token
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
            # assert begun and curcount > 0 and not is_bracket(line[index])
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
                # assert end_index != -1 and mid_index == -1
                second = copy.deepcopy(line[index : end_index])
                curcount = 1
                mid_index = index
            elif curcount == 0:
                # assert end_index != -1 and mid_index != -1 and first is None and second is not None
                first = copy.deepcopy(line[index:mid_index])
                curcount = -1
                begun = False
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
            # assert begun and curcount > 0
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
        # assert not begun
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
                # assert index > 0
                if line[index - 1] == NEGATION:
                    line.pop(index)
                    line.pop(index - 1)
                    index -= 2
                    begun = False
                    continue
                if is_operator(line[index - 1]):
                    # assert curcount == -1
                    # assert line[index - 1] == OR or line[index - 1] == AND
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
            # assert begun and curcount > 0 and not is_bracket(line[index])
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
                # assert end_index != -1 and mid_index == -1
                second = copy.deepcopy(line[index : end_index])
                curcount = 1
                mid_index = index
            elif curcount == 0:
                # assert end_index != -1 and mid_index != -1 and first is None and second is not None
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

def update_and_or(bnf_data, first_iteration = True):
    change = False
    for ind, line in enumerate(bnf_data):
        if OR not in line or AND not in line:
            continue
        # assert OR in line and AND in line
        line_copy = copy.deepcopy(line)
        line_copy.reverse()
        if len(line) - line_copy.index(OR) - 1 < line.index(AND):
            continue
        conversion_stack = list()
        for index, token in enumerate(line):
            # assert not is_bracket(token)
            if is_atom(token):
                conversion_stack.append([token])
                continue
            # assert token == AND or token == NEGATION or token == OR
            if token == NEGATION:
                # assert index > 0 and is_atom(line[index - 1])
                top_element = conversion_stack.pop()
                # assert len(top_element) == 1 and top_element[0] == line[index - 1]
                cur_val = [top_element[0], NEGATION]
                conversion_stack.append(cur_val)
                continue
            # assert len(conversion_stack) > 1
            if token == OR:
                second = conversion_stack.pop()
                first = conversion_stack.pop()
                second_first, second_second, second_token = None, None, None
                first_first, first_second, first_token = None, None, None
                if len(second) == 3:
                    second_first = second[0]
                    second_second = second[1]
                    second_token = second[2]
                    second = second_first + second_second + [second_token]
                else:
                    # assert len(second) > 0
                    pass
                if len(first) == 3:
                    first_first = first[0]
                    first_second = first[1]
                    first_token = first[2]
                    first = first_first + first_second + [first_token]
                else:
                    # assert len(first) > 0
                    pass
                if AND in first or AND in second:
                    # assert first_iteration or ((first_token is None and second_token is not None and second_token == AND) or (second_token is None and first_token is not None and first_token == AND) or (first_token is not None and second_token is not None and (first_token == AND or second_token == AND)))
                    if first_token is not None and first_token == AND:
                        first_ans = first_first + second + [OR]
                        second_ans = first_second + second + [OR]
                        conversion_stack.append([first_ans, second_ans, AND])
                        change = True
                        continue
                    else:
                        # assert second_token is not None and second_token == AND
                        first_ans = first + second_first + [OR]
                        second_ans = first + second_second + [OR]
                        conversion_stack.append([first_ans, second_ans, AND])
                        change = True
                        continue
                else:
                    conversion_stack.append([first, second, token])
            else:
                # assert token == AND
                second = conversion_stack.pop()
                first = conversion_stack.pop()
                second_first, second_second, second_token = None, None, None
                first_first, first_second, first_token = None, None, None
                if len(second) == 3:
                    second_first = second[0]
                    second_second = second[1]
                    second_token = second[2]
                    second = second_first + second_second + [second_token]
                else:
                    # assert len(second) > 0
                    pass
                if len(first) == 3:
                    first_first = first[0]
                    first_second = first[1]
                    first_token = first[2]
                    first = first_first + first_second + [first_token]
                else:
                    # assert len(first) > 0
                    pass
                conversion_stack.append([first, second, token])
        # assert len(conversion_stack) == 1
        final = conversion_stack.pop()
        if len(final) == 1:
            bnf_data[ind] = final[0]
        else:
            bnf_data[ind] = final[0] + final[1] + final[2:]
    return bnf_data, change

def overall_update_and_or(bnf_lines):
    counter = 0
    while True:
        counter += 1
        if counter > 100:
            assert False, "counter break; should never happen"
        if counter == 1:
            bnf_lines, change = update_and_or(bnf_lines)
        else:
            bnf_lines, change = update_and_or(bnf_lines, False)
        if not change:
            break
    return bnf_lines

def postfix_to_infix_list(postfix: list) -> list:
    conversion_stack = list()
    for token in postfix:
        # assert not is_bracket(token)
        if is_atom(token):
            conversion_stack.append([token])
            continue
        # assert is_operator(token)
        if token == NEGATION:
            # assert len(conversion_stack) > 0
            top_val = conversion_stack.pop()
            # assert len(top_val) == 1
            top_val = top_val[0]
            cur_val = NEGATION + top_val
            conversion_stack.append([cur_val])
        else:
            # assert len(conversion_stack) > 1
            second = conversion_stack.pop()
            first = conversion_stack.pop()
            conversion_stack.append(first + [token] + second)
    # assert len(conversion_stack) == 1
    return conversion_stack.pop()

def split_into_cnf(bnf_lines):
    cnf_lines = []
    for line in bnf_lines:
        start = 0
        line = postfix_to_infix_list(line)
        for index, token in enumerate(line):
            if token == AND:
                cnf_lines.append(line[start:index])
                start = index + 1
        cnf_lines.append(line[start:])
    
    # Removing |
    for index, line in enumerate(cnf_lines):
        while OR in line:
            line.remove(OR)
        line.sort(key=lambda x: x if x[0] != '!' else x[1:])
        cnf_lines[index] = line
    cnf_lines.sort(key=lambda x: len(x))
    return cnf_lines