import dpll_helper
import io_helper
import cnf_helper
import copy

def bnf_to_cnf(bnf_data, verbose):
    verbose_outputs = {}
    for i in range(len(bnf_data)):
        verbose_outputs[i] = []
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)
    # Step 1:
    bnf_data = cnf_helper.remove_double_implies(bnf_data)
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)

    # Step 2:
    bnf_data = cnf_helper.remove_implies(bnf_data)
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)

    # Step 3:
    bnf_data = cnf_helper.update_negation(bnf_data)
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)

    # Step 4:
    bnf_data = cnf_helper.overall_update_and_or(bnf_data)

    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)
        io_helper.print_verbose_dict(verbose_outputs)
    
    # Step 5:
    cnf_data = cnf_helper.split_into_cnf(bnf_data)

    return cnf_data

def recursive_dpll(lines, all_sym, cur_state, verbose):
    # Check if done
    if len(lines) == 0:
        cur_state = dpll_helper.assign_remaining(cur_state, verbose)
        return cur_state
    
    # Check for empty lines
    if dpll_helper.check_for_empty_lines(lines):
        return None
    selection = dpll_helper.find_easy_choice(lines, all_sym)

    if selection is not None:
        choice, value, pure_literal = selection
        cur_state[choice] = value
        if verbose:
            if pure_literal:
                io_helper.print_func("easy case: pure literal " + choice + " = " + io_helper.str_bool(value))
            else:
                io_helper.print_func("easy case: unit literal " + choice + " = " + io_helper.str_bool(value))
        lines, all_sym = dpll_helper.update(lines, all_sym, (choice, value), verbose)
        return recursive_dpll(lines, all_sym, cur_state, verbose)
    
    # Make Hard Choice
    selection = dpll_helper.make_hard_choice(cur_state)
    cur_state_copy = copy.deepcopy(cur_state)
    all_sym_copy = copy.deepcopy(all_sym)
    lines_copy = copy.deepcopy(lines)
    cur_state_copy[selection] = True
    if verbose:
        io_helper.print_func("hard case, guess: " + selection + "=true")
    lines_copy, all_sym_copy = dpll_helper.update(lines_copy, all_sym_copy, (selection, True), verbose)
    cur_state_copy = recursive_dpll(lines_copy, all_sym_copy, cur_state_copy, verbose)
    if cur_state_copy is None:
        cur_state[selection] = False
        if verbose:
            io_helper.print_func("fail", end = "|")
            io_helper.print_func("hard case, try: " + selection + "=false")
        lines, all_sym = dpll_helper.update(lines, all_sym, (selection, False), verbose)
        return recursive_dpll(lines, all_sym, cur_state, verbose)
    else:
        return cur_state_copy

def dpll_solver(cnf_data, verbose):
    lines, all_sym = cnf_data
    init_state = dict()
    for sym in all_sym.keys():
        init_state[sym] = None
    all_sym = dpll_helper.init_all_sym(lines, all_sym)
    if verbose:
        io_helper.print_lines(lines)
    ans = recursive_dpll(lines, all_sym, init_state, verbose)
    if ans is None:
        io_helper.print_func('NO VALID ASSIGNMENT')
    else:
        io_helper.print_state(ans)

def mode_eval_and_run(args):
    args.mode = args.mode.lower()
    if args.mode == 'dpll':
        cnf_data, all_sym = io_helper.read_cnf_file(args.mode_file)
    elif args.mode == 'cnf' or args.mode == 'solver':
        bnf_data = io_helper.read_bnf_file(args.mode_file)
        cnf_data = bnf_to_cnf(bnf_data, args.v)
        all_sym = io_helper.generate_all_syms_dict(cnf_data)

    if args.mode == 'cnf':
        io_helper.print_lines(cnf_data)
    elif args.mode == 'dpll' or args.mode == 'solver':
        if args.mode == 'solver' and args.v:
            io_helper.print_func("")
        dpll_solver((cnf_data, all_sym), args.v)

if __name__ == '__main__':
    args = io_helper.init()
    dpll_helper.assert_correct_args(args)
    mode_eval_and_run(args)