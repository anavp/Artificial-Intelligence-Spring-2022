import argparse
from infix_postfix_helper import infix_to_postfix, postfix_to_infix

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

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

def print_infixes(postfixes):
    for postfix in postfixes:
        print_func(postfix_to_infix(postfix))

def to_store_infixes(postfixes, outputs):
    for index, postfix in enumerate(postfixes):
        assert index in list(outputs)
        outputs[index].append(postfix_to_infix(postfix))
    return outputs

def print_verbose_dict(outputs):
    for key in outputs:
        print_list(outputs[key])
        # print_func("")

@static_vars(outFile=None)
def print_func(message, end = "\n", init = None):
    if init is not None:
        print_func.outFile = open(init, 'w')
        return
    if print_func.outFile is not None:
        try:
            print_func.outFile.write(message + end)
        except TypeError:
            print("TypeError")
            print("given message: " + str(message))
            exit(0)
    else:
        print(message, end)
    
def print_list(given_list):
    for ele in given_list:
        print_func(str(ele))

def open_file(filename, mode = 'r'):
    try:
        file = open(filename, mode)
        return file
    except FileNotFoundError:
        print_func(f'The file {filename} was not found. Exiting from the program.')
        exit(0)

def read_bnf_file(bnf_file):
    bnf_file = open_file(bnf_file, 'r')
    bnf_data = bnf_file.readlines()
    bnf_data = [line.strip("\n") for line in bnf_data]
    # print_list(bnf_data)
    # print_func("done")
    bnf_file.close()
    postfix_exprs = []
    for line in bnf_data:
        # line = line.strip("\n")
        postfix_exprs.append(infix_to_postfix(line))
        # print_func("current postfix line: ", end = "")
        # print_func(str(postfix_exprs[-1]))
    return postfix_exprs

def generate_all_syms_dict(cnf_data):
    all_symbols_dict = dict()
    for line in cnf_data:
        # atoms = line.strip('\n').split(' ', -1)
        # cnf_lines.append(atoms)
        for atom in line:
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
    return all_symbols_dict

def read_cnf_file(cnf_file):
    cnf_file = open_file(cnf_file, 'r')
    cnf_data = cnf_file.readlines()
    cnf_file.close()
    cnf_lines = []
    for line in cnf_data:
        atoms = line.strip('\n').split(' ', -1)
        cnf_lines.append(atoms)
        # for atom in atoms:
        #     assert len(atom) > 0
        #     neg = False
        #     if atom[0] == '!':
        #         neg = True
        #         atom = atom[1:]
        #     assert len(atom) > 0
        #     if atom not in all_symbols_dict.keys():
        #         all_symbols_dict[atom] = neg
        #     elif all_symbols_dict[atom] != neg:
        #         all_symbols_dict[atom] = None
    all_symbols_dict = generate_all_syms_dict(cnf_lines)
    return (cnf_lines, all_symbols_dict)

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