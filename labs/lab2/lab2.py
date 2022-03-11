from helper import *
import copy

# TODO: Figure what exactly to print in verbose mode and what not to print when not

def read_cnf_file(cnf_file):
    cnf_file = open(cnf_file, 'r')
    cnf_file = cnf_file.readlines()
    all_symbols_dict = dict()
    cnf_lines = []
    for line in cnf_file:
        atoms = line.strip('\n').split(' ', -1)
        cnf_lines.append(atoms)
        for atom in atoms:
            assert len(atom) > 0
            neg = False
            if atom[0] == '!':
                neg = True
                atom = atom[1:]
            assert len(atom) > 0
            if atom not in all_symbols_dict.keys():
                all_symbols_dict[atom] = neg
            elif all_symbols_dict[atom] != neg:
                all_symbols_dict[atom] = None
    return (cnf_lines, all_symbols_dict)


def recursive_dpll(lines, all_sym, cur_state, verbose = False):
    # Check if done
    if len(lines) == 0:
        cur_state = assign_remaining(cur_state)
        return cur_state
    
    # Check for empty lines
    if check_for_empty_lines(lines):
        return None
    # if DEBUG_MODE:
    #     print("Checkpt 1")
    # Check for easy-choice
    selection = find_easy_choice(lines, all_sym)

    # if DEBUG_MODE:
    #     print("Checkpt 2")
    if selection is not None:
        choice, value = selection
        if DEBUG_MODE:
            print_func("trying easy choice: " + str(selection))
        assert choice in cur_state.keys()
        assert cur_state[choice] is None
        cur_state[choice] = value
        lines, all_sym = update(lines, all_sym, selection, verbose)
        if verbose:
            print_func("easyCase " + choice + " = " + str_bool(value))
            print_lines(lines)
            if DEBUG_MODE:
                print_func(str(cur_state))
        return recursive_dpll(lines, all_sym, cur_state, verbose)
        
    
    # Make Hard Choice
    selection = make_hard_choice(cur_state)
    assert selection is not None and selection in cur_state.keys()
    cur_state_copy = copy.deepcopy(cur_state)
    all_sym_copy = copy.deepcopy(all_sym)
    lines_copy = copy.deepcopy(lines)
    cur_state_copy[selection] = True
    lines_copy, all_sym_copy = update(lines_copy, all_sym_copy, (selection, True), verbose)
    # TODO: Handle the contradiction printing here somehow
    if verbose:
        print_func("hard case, guess: " + selection + "=true")
        print_lines(lines_copy)
    cur_state_copy = recursive_dpll(lines_copy, all_sym_copy, cur_state_copy, verbose)
    if cur_state_copy is None:
        cur_state[selection] = False
        lines, all_sym = update(lines, all_sym, (selection, False), verbose)
        if verbose:
            print_func("hard case, guess: " + selection + "=false")
            print_lines(lines)
        return recursive_dpll(lines, all_sym, cur_state, verbose)
    else:
        return cur_state_copy

def dpll_solver(cnf_data, verbose):
    lines, all_sym = cnf_data
    init_state = dict()
    for sym in all_sym.keys():
        init_state[sym] = None
    all_sym = init_all_sym(lines, all_sym)
    print_lines(lines)
    ans = recursive_dpll(lines, all_sym, init_state, verbose)
    if ans is None:
        print_func('NO VALID ASSIGNMENT')
    else:
        # print_func(str(ans))
        print_state(ans)


def mode_eval_and_running(args):
    if args.mode == 'dpll':
        cnf_data = read_cnf_file(args.mode_file)
        # if DEBUG_MODE:
        #     lines, all_sym = cnf_data
        #     print(lines)
        #     print("\nAll Symbols:")
        #     print(all_sym)
        dpll_solver(cnf_data, args.v)

if __name__ == '__main__':
    args = parse_args()
    if args.w:
        print_func("", "", "./output.out")
    assert_correct_args(args)
    mode_eval_and_running(args)