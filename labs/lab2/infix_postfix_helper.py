import cnf_helper
import io_helper
import re
def add_required_spaces(bnf_string: str) -> str:
    """
        Add spaces around brackets and operators
    """
    for operator in cnf_helper.ALL_OPERATORS[1:]:
        if operator == cnf_helper.IMPLIES:
            continue
        bnf_string = bnf_string.replace(operator, " " + operator + " ")
    occurrences = [m.start() for m in re.finditer(cnf_helper.IMPLIES, bnf_string)]
    occurrences.sort()
    num = 0
    for index in occurrences:
        index += num
        assert index != 0
        if bnf_string[index - 1] == '<':
            continue
        bnf_string = bnf_string[:index] + " " + bnf_string[index:]
        num += 1
    bnf_string = bnf_string.replace(" " + cnf_helper.IMPLIES, " " + cnf_helper.IMPLIES + " ")
    bnf_string = bnf_string.replace("(", " ( " )
    bnf_string = bnf_string.replace(")", " ) ")
    return bnf_string


def infix_to_postfix(infix: str):
    # Add spaces around operators and brackets
    infix = add_required_spaces(infix)
    # io_helper.print_func("after adding spaces")
    # io_helper.print_func(str(infix))
    # Split the string into tokens
    infix = infix.strip().split()
    # io_helper.print_func("after splitting: ")
    # io_helper.print_func(str(infix))
    conversion_stack = list()
    postfix = list()
    for token in infix:
        if token == '(':
            conversion_stack.append(token)
        elif token == ')':
            while len(conversion_stack) > 0 and conversion_stack[-1] != '(':
                postfix.append(conversion_stack.pop())
            conversion_stack.pop()
        elif cnf_helper.is_atom(token):
            postfix.append(token)
            continue
        else:
            while len(conversion_stack) > 0 and conversion_stack[-1] != '(' and not cnf_helper.higher_precedence(token, conversion_stack[-1]):
                postfix.append(conversion_stack.pop())
            conversion_stack.append(token)
    while not len(conversion_stack) == 0:
        postfix.append(conversion_stack.pop())
    return postfix