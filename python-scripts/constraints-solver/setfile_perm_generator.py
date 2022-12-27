import os
from Configurations.const_solver import CG_constraint_solver


def get_hex_zero_padding(value):
    if value <= 0xff:
        return 2
    elif value <= 0xffff:
        return 4


if __name__ == "__main__":
    output_dir = "setfiles"         # Arg
    config_dir = "configuration"    # Arg
    cs = CG_constraint_solver()
    solutions = cs.get_solution(config_dir, "root.json")
    perm_count = len(solutions)
    if perm_count == 0:
        print("No permutations created ...")
        exit(0)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    file_index = 0
    file_padding = len(str(perm_count))
    for solution in solutions:
        f = open(os.path.join(output_dir, f"config_perm{file_index:0{file_padding}}.tset"), "w")
        for register in solution.keys():
            hex_value_str = format(solution[register], 'x')
            hex_padding = get_hex_zero_padding(solution[register])
            f.write(f"WRITE #{register} {hex_value_str.rjust(hex_padding, '0')}\n")
        f.close()
        file_index += 1
        # print(solution)
