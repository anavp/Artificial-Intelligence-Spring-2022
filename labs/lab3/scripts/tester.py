import os
import subprocess as sp

def open_file(file, mode = 'r'):
    try:
        file = open(file, mode)
        return file
    except FileNotFoundError:
        print(f'filename {file} does not seem to exist. Exiting from the program now')
        exit(0)

def check_if_files_match(file1_name, file2_name) -> bool:
    file1 = open_file(file1_name)
    file2 = open_file(file2_name)
    lines1 = file1.readlines()
    lines2 = file2.readlines()
    if len(lines1) != len(lines2):
        return False

    for index, line1 in enumerate(lines1):
        line2 = lines2[index]
        if len(line1) != len(line2):
            return False
        if len(line1.strip("\n")) == 0:
            continue
        if '->' in line1:
            if os.path.basename(file1_name) == 'hw8.out' and line1.strip('\n') == 'F -> E':
                continue
            if line1 != line2:
                return False
            continue
        assert '=' in line1 and '=' in line2, line1
        split1 = line1.split()
        split2 = line2.split()
        for ind2, valuation1 in enumerate(split1):
            valuation2 = split2[ind2]
            valuation1 = valuation1.split('=')
            valuation2 = valuation2.split('=')
            assert len(valuation1) == len(valuation2) and len(valuation1) == 2
            if valuation1[0] != valuation2[0]:
                return False
            valuation1 = float(valuation1[1])
            valuation2 = float(valuation2[1])
            if round(abs(valuation1 - valuation2),3) <= 0.01:
                continue
            return False
    return True

if __name__ == '__main__':
    os.system("rm -f ../outputs/output.out")
    reference_outputs = sp.getoutput("ls ../reference_outputs/*.out")
    reference_outputs = reference_outputs.split('\n', -1)
    outputs = sp.getoutput("ls ../outputs/*.out")
    outputs = outputs.split('\n', -1)
    reference_outputs.sort()
    outputs.sort()
    os.system("rm -f ../outputs/LOG.txt")
    for index, ref_out in enumerate(reference_outputs):
        print(os.path.basename(ref_out) + ": ", end = "")
        matches = check_if_files_match(ref_out, outputs[index])
        if matches:
            print("match")
            continue
        basename = os.path.basename(ref_out)
        os.system(f"echo '{basename} log begins:' >> ../outputs/LOG.txt")
        os.system(f"diff -b -B {ref_out} {outputs[index]} >> ../outputs/LOG.txt")
        os.system(f"echo '{basename} log ends\n\n\n' >> ../outputs/LOG.txt")
        print("does not match")