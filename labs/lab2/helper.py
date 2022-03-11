import argparse

DEBUG_MODE = False

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

def assert_correct_args(args):
    assert args.mode == "cnf" or args.mode == "bnf" or args.mode == "dpll"

def check_for_empty_lines(given_list) -> bool:
    for ele in given_list:
        if len(ele) == 0:
            return True
    return False

def assign_remaining(state):
    for sym in state.keys():
        if state[sym] is None:
            state[sym] = True
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
    return (selected_syms[0], all_sym[selected_syms[0]])

def find_unit_literal(lines):
    for line in lines:
        if len(line) == 1:
            neg = True
            choice = line[0]
            assert len(line[0]) > 0
            if line[0][0] == '!':
                neg = False
                choice = choice[1:]
            return (choice, neg)
    return None

def find_easy_choice(lines, all_sym):
    choice = find_pure_literal(all_sym)
    if choice is not None:
        if DEBUG_MODE:
            print_func("found pure literal")
        return choice
    return find_unit_literal(lines)

def reevaluate_add(reevaluate, line, cur, neg = False):
    if neg:
        neg_cur = cur[1:]
        assert len(neg_cur) > 0
    else:
        neg_cur = "!" + cur
    line.remove(cur)
    assert cur not in line and neg_cur not in line
    for i in range(len(line) - 1, -1, -1):
        sym = line[i]
        assert sym is not None and len(sym) > 0
        if sym[0] == '!':
            sym = sym[1:]
            line[i] = sym
        if sym in reevaluate:
            line.pop(i)
    return line

def reevaluation(sym, lines):
    assert sym is not None and len(sym) > 0 and sym[0] != '!'
    neg_sym = "!" + sym
    value = None
    for line in lines:
        if sym in line:
            assert neg_sym not in line
            if value is None:
                value = True
                continue
            elif not value:
                return None
        elif neg_sym in line:
            assert sym not in line
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

    # Filtering based on selection
    for i in range(length - 1, -1, -1):
        line = lines[i]
        assert len(line) > 0
        if choice in line and value:
            reevaluate = reevaluate + reevaluate_add(reevaluate, line, choice)
            lines.pop(i)
            continue
        elif choice in line:
            assert not value
            if len(line) > 1:
                line.remove(choice)
                assert choice not in line
                lines[i] = line
            else:

                lines.pop(i)
                continue
        assert choice not in line
        if neg_choice in line and value:
            # if len(line) > 1:
            line.remove(neg_choice)
            assert neg_choice not in line
            lines[i] = line
            # else:
            #     lines.pop(i)
            #     continue
        elif neg_choice in line:
            assert not value
            reevaluate = reevaluate + reevaluate_add(reevaluate, line, neg_choice, True)
            lines.pop(i)
        assert neg_choice not in line
    
    # Updating all_sym:
    all_sym.pop(choice)
    for sym in reevaluate:
        all_sym[sym] = reevaluation(sym, lines)
    
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

def print_lines(lines):
    for line in lines:
        # assert len(line) > 0
        if len(line) == 0:
            print_func("")
            continue
        for sym in line[:-1]:
            print_func(sym, end = " ")
        print_func(line[-1])

def print_state(state):
    syms = list(state)
    syms.sort()
    for sym in syms:
        print_func(sym + " = " + str_bool(state[sym]))

def str_bool(val):
    if val:
        return "true"
    return "false"

@static_vars(outFile=None)
def print_func(message, end = "\n", init = None):
    if init is not None:
        print_func.outFile = open(init, 'w')
        return
    if print_func.outFile is not None:
        print_func.outFile.write(message + end)
    else:
        print(message, end)
    

def parse_args(args = None):
    parser = argparse.ArgumentParser(description="CSCI-GA.2560 Artificial Intelligence Lab2 BNF to CNF and DPLL solver code")
    parser.add_argument("-v", required = False, default = False, action = 'store_true',\
        help = "use this tag to generate the verbose output")
    parser.add_argument("-mode", type = str, required = True, default = -1,\
        help = "the number of queens in the N-Queens problem")
    parser.add_argument("mode_file", metavar = 'mode_file_path', type = str,\
        help = "pass the path of the mode's input file")
    parser.add_argument("-w", required = False, default = False, action = 'store_true',\
        help = "use this tag to write the output to file called 'output.out' in the same directory")
    return parser.parse_args()