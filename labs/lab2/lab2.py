import dpll_helper
import io_helper
import cnf_helper
import copy
# TODO: Figure what exactly to print in verbose mode and what not to print when not

def bnf_to_cnf(bnf_data, verbose):
    # io_helper.print_func("beginning: ")
    # io_helper.print_lines(bnf_data)
    verbose_outputs = {}
    for i in range(len(bnf_data)):
        verbose_outputs[i] = []
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)
    # Step 1:
    bnf_data = cnf_helper.remove_double_implies(bnf_data)
    # io_helper.print_func("after step 1: ")
    # io_helper.print_lines(bnf_data)
    # io_helper.print_infixes(bnf_data)
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)

    # Step 2:
    bnf_data = cnf_helper.remove_implies(bnf_data)
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)
    # io_helper.print_func("\nafter step 2: ")
    # io_helper.print_lines(bnf_data)
    # io_helper.print_infixes(bnf_data)

    # Step 3:
    bnf_data = cnf_helper.update_negation(bnf_data)
    if verbose:
        verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)
    # io_helper.print_func("\nafter step 3: ")
    # io_helper.print_lines(bnf_data)
    # io_helper.print_infixes(bnf_data)

    # Step 4:
    # bnf_data = cnf_helper.update_and_or(bnf_data)
    bnf_data = cnf_helper.overall_update_and_or(bnf_data)
    # if verbose:
    #     verbose_outputs = io_helper.to_store_infixes(bnf_data, verbose_outputs)
    #     io_helper.print_verbose_dict(verbose_outputs)
    # io_helper.print_func("\nafter step 4: ")
    # io_helper.print_lines(bnf_data)
    # io_helper.print_infixes(bnf_data)

    if verbose:
        io_helper.print_verbose_dict(verbose_outputs)
    # Step 5:
    cnf_data = cnf_helper.split_into_cnf(bnf_data)
    # io_helper.print_func("\nafter step 5: ")
    return cnf_data

def recursive_dpll(lines, all_sym, cur_state, verbose = False):
    # Check if done
    if len(lines) == 0:
        cur_state = dpll_helper.assign_remaining(cur_state)
        return cur_state
    
    # Check for empty lines
    if dpll_helper.check_for_empty_lines(lines):
        return None
    selection = dpll_helper.find_easy_choice(lines, all_sym)

    if selection is not None:
        choice, value = selection
        if dpll_helper.DEBUG_MODE:
            io_helper.print_func("trying easy choice: " + str(selection))
        assert choice in cur_state.keys()
        assert cur_state[choice] is None
        cur_state[choice] = value
        lines, all_sym = dpll_helper.update(lines, all_sym, selection, verbose)
        if verbose:
            io_helper.print_func("easyCase " + choice + " = " + io_helper.str_bool(value))
            io_helper.print_lines(lines)
            if dpll_helper.DEBUG_MODE:
                io_helper.print_func(str(cur_state))
        return recursive_dpll(lines, all_sym, cur_state, verbose)
        
    
    # Make Hard Choice
    selection = dpll_helper.make_hard_choice(cur_state)
    assert selection is not None and selection in cur_state.keys()
    cur_state_copy = copy.deepcopy(cur_state)
    all_sym_copy = copy.deepcopy(all_sym)
    lines_copy = copy.deepcopy(lines)
    cur_state_copy[selection] = True
    lines_copy, all_sym_copy = dpll_helper.update(lines_copy, all_sym_copy, (selection, True), verbose)
    # TODO: Handle the contradiction printing here somehow
    if verbose:
        io_helper.print_func("hard case, guess: " + selection + "=true")
        io_helper.print_lines(lines_copy)
    cur_state_copy = recursive_dpll(lines_copy, all_sym_copy, cur_state_copy, verbose)
    if cur_state_copy is None:
        cur_state[selection] = False
        lines, all_sym = dpll_helper.update(lines, all_sym, (selection, False), verbose)
        if verbose:
            io_helper.print_func("hard case, guess: " + selection + "=false")
            io_helper.print_lines(lines)
        return recursive_dpll(lines, all_sym, cur_state, verbose)
    else:
        return cur_state_copy

def dpll_solver(cnf_data, verbose):
    lines, all_sym = cnf_data
    init_state = dict()
    for sym in all_sym.keys():
        init_state[sym] = None
    all_sym = dpll_helper.init_all_sym(lines, all_sym)
    io_helper.print_lines(lines)
    ans = recursive_dpll(lines, all_sym, init_state, verbose)
    if ans is None:
        io_helper.print_func('NO VALID ASSIGNMENT')
    else:
        # print_func(str(ans))
        io_helper.print_state(ans)

def mode_eval_and_running(args):
    args.mode = args.mode.lower()
    if args.mode == 'dpll':
        cnf_data = io_helper.read_cnf_file(args.mode_file)
        dpll_solver(cnf_data, args.v)
    elif args.mode == 'cnf' or args.mode == 'solver':
        bnf_data = io_helper.read_bnf_file(args.mode_file)
        cnf_data = bnf_to_cnf(bnf_data, args.v)
        all_sym = io_helper.generate_all_syms_dict(cnf_data)
        # cnf_data = (cnf_data, all_sym)
    if args.mode == 'cnf':
        # TODO: Print cnf output
        io_helper.print_lines(cnf_data)
        pass
    elif args.mode == 'solver':
        dpll_solver((cnf_data, all_sym), args.v)

if __name__ == '__main__':
    args = io_helper.parse_args()
    if args.w:
        io_helper.print_func("", "", "./output.out")
    dpll_helper.assert_correct_args(args)
    mode_eval_and_running(args)