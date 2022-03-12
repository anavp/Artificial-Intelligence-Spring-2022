# from io_helper import *
# from io_helper import print_func
import io_helper
DEBUG_MODE = False

def assert_correct_args(args):
    assert args.mode == "cnf" or args.mode == "solver" or args.mode == "dpll"

def check_for_empty_lines(given_list) -> bool:
    for ele in given_list:
        if len(ele) == 0:
            return True
    return False

def assign_remaining(state, verbose):
    # TODO: Write "unbound: " here; in verbose mode??
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
    assert all_sym[selected_syms[0]] is not None
    return (selected_syms[0], all_sym[selected_syms[0]], True)

def find_unit_literal(lines):
    for line in lines:
        if len(line) == 1:
            neg = True
            choice = line[0]
            assert len(line[0]) > 0
            if line[0][0] == '!':
                neg = False
                choice = choice[1:]
            return (choice, neg, False)
    return None

def find_easy_choice(lines, all_sym):
    choice = find_pure_literal(all_sym)
    if choice is not None:
        # if DEBUG_MODE:
        #     io_helper.print_func("found pure literal")
        return choice
    return find_unit_literal(lines)

def reevaluate_add(reevaluate, line, cur, neg = False):
    if neg:
        neg_cur = cur[1:]
        assert len(neg_cur) > 0
    else:
        neg_cur = "!" + cur
    line.remove(cur)
    # assert cur not in line and neg_cur not in line
    for i in range(len(line) - 1, -1, -1):
        sym = line[i]
        assert sym is not None and len(sym) > 0
        if sym[0] == '!':
            sym = sym[1:]
            line[i] = sym
        if sym == cur or sym == neg_cur or sym in reevaluate:
            line.pop(i)
    return line

def reevaluation(sym, lines):
    assert sym is not None and len(sym) > 0 and sym[0] != '!'
    neg_sym = "!" + sym
    value = None
    for line in lines:
        if sym in line:
            # assert neg_sym not in line
            if value is None:
                value = True
                continue
            elif not value:
                return None
        elif neg_sym in line:
            # assert sym not in line
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
        assert len(line) > 0
        appended = False
        if choice in line and value:
            reevaluate = reevaluate + reevaluate_add(reevaluate, line, choice)
            lines.pop(i)
            continue
        elif choice in line:
            assert not value
            # if len(line) > 1:
            if len(line) == 1 and verbose:
                to_print.append(io_helper.get_line_for_print(line, " contradiction"))
                appended = True
            while choice in line:
                line.remove(choice)
            # assert choice not in line
            lines[i] = line
            # else:
            #     lines.pop(i)
            #     continue
        assert choice not in line
        if neg_choice in line and value:
            # if len(line) > 1:
            if len(line) == 1 and verbose:
                io_helper.print_func(io_helper.get_line_for_print(line, " contradiction"))
                appended = True
            while neg_choice in line:
                line.remove(neg_choice)
            # if len(line) > 1 and verbose:
            #     io_helper.print_func(io_helper.get_line_for_print(line))
            lines[i] = line
            # else:
            #     lines.pop(i)
            #     continue
        elif neg_choice in line:
            assert not value
            reevaluate = reevaluate + reevaluate_add(reevaluate, line, neg_choice, True)
            lines.pop(i)
            continue
        if not appended:
            to_print.append(io_helper.get_line_for_print(line, end = ""))
        assert neg_choice not in line
    
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
    assert False


def init_all_sym(lines, all_sym):
    for sym in all_sym.keys():
        all_sym[sym] = reevaluation(sym, lines)
    return all_sym