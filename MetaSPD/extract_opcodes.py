import glob


def get_opcode_set(path):
    """
    extracts all opcodes in program files
    :param path: a path which contains all program files
    :return: opcode set
    """
    opcode_set = set()
    input_files = glob.glob(path + "\\**\\*.txt", recursive=True)
    for input_file in input_files:
        with open(input_file) as file_handler:
            for opcode in [line.rstrip('\n') for line in file_handler.readlines()]:
                opcode_set.add(opcode)
    return opcode_set


def write_opcodes(path, opcodes):
    """
    writes opcode set to a file
    :param path: output path
    :param opcodes: opcode set
    """
    with open(path, "w") as file_handler:
        for opcode in opcodes:
            file_handler.write(opcode + "\n")


if __name__ == "__main__":
    write_opcodes(".\\opcode_set\\MySQL\\pirated_opcode_set.txt", get_opcode_set(".\\data\\MySQL\\pirated"))
    write_opcodes(".\\opcode_set\\MySQL\\innocent_opcode_set.txt", get_opcode_set(".\\data\\MySQL\\innocent"))
