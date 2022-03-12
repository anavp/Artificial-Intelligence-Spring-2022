import io_helper

def assert_correct_args(args):
    assert args.mode == "cnf" or args.mode == "solver" or args.mode == "dpll"

def check_for_empty_lines(given_list) -> bool:
    for ele in given_list:
        if len(ele) == 0:
            return True
    return False

def assign_remaining(state, verbose):
    for sym in state.keys():
        if state[sym] is None:
            if verbose:
                io_helper.print_func("unbound " + sym + "=false")
            state[sym] = False
    return state

def find_pure_literal(all_sym):
    selected_syms = []
    for sym in all_sym.keys():
        if all_sym[sym] is not None:
            selected_syms.append(sym)
    if len(selected_syms) == 0:
        return None
    selected_syms.sort()
    return (selected_syms[0], all_sym[selected_syms[0]], True)

def find_unit_literal(lines):
    for line in lines:
        if len(line) == 1:
            neg = True
            choice = line[0]
            if line[0][0] == '!':
                neg = False
                choice = choice[1:]
            return (choice, neg, False)
    return None

def find_easy_choice(lines, all_sym):
    choice = find_pure_literal(all_sym)
    if choice is not None:
        return choice
    return find_unit_literal(lines)

def reevaluate_add(reevaluate, line, cur, neg = False):
    if neg:
        neg_cur = cur[1:]
    else:
        neg_cur = "!" + cur
    line.remove(cur)
    for i in range(len(line) - 1, -1, -1):
        sym = line[i]
        if sym[0] == '!':
            sym = sym[1:]
            line[i] = sym
        if sym == cur or sym == neg_cur or sym in reevaluate:
            line.pop(i)
    return line

def reevaluation(sym, lines):
    neg_sym = "!" + sym
    value = None
    for line in lines:
        if sym in line:
            if value is None:
                value = True
                continue
            elif not value:
                return None
        elif neg_sym in line:
            if value is None:
                value = False
                continue
            elif value:
                return None
    return value

def update(lines, all_sym, selection, verbose):
    choice, value = selection
    neg_choice = "!" + choice
    length = len(lines)
    reevaluate = []
    to_print = []

    # Filtering based on selection
    for i in range(length - 1, -1, -1):
        line = lines[i]
        appended = False
        if choice in line and value:
            reevaluate = reevaluate + reevaluate_add(reevaluate, line, choice)
            lines.pop(i)
            continue
        elif choice in line:
            if len(line) == 1 and verbose:
                to_print.append(io_helper.get_line_for_print(line, " contradiction"))
                appended = True
            while choice in line:
                line.remove(choice)
            lines[i] = line
        if neg_choice in line and value:
            if len(line) == 1 and verbose:
                io_helper.print_func(io_helper.get_line_for_print(line, " contradiction"))
                appended = True
            while neg_choice in line:
                line.remove(neg_choice)
            lines[i] = line
        elif neg_choice in line:
            reevaluate = reevaluate + reevaluate_add(reevaluate, line, neg_choice, True)
            lines.pop(i)
            continue
        if not appended:
            to_print.append(io_helper.get_line_for_print(line, end = ""))

    # Updating all_sym:
    all_sym.pop(choice)
    for sym in reevaluate:
        all_sym[sym] = reevaluation(sym, lines)
    
    # Print if verbose:
    if verbose:
        to_print.reverse()
        for line in to_print:
            io_helper.print_func(line)
    return lines, all_sym

def make_hard_choice(state):
    syms = list(state)
    syms.sort()
    for sym in syms:
        if state[sym] is None:
            return sym

def init_all_sym(lines, all_sym):
    for sym in all_sym.keys():
        all_sym[sym] = reevaluation(sym, lines)
    return all_sym