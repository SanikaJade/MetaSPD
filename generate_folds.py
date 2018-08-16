import glob
import os
import random

from MetaSPD import convert_opcodes


def programs_to_gspan(programs, output, opcode_set):
    """
    convert programs to gspan format
    :param programs: list of program paths
    :param output: output path
    :param opcode_set: opcode set for matrix initialization
    """
    if not os.path.exists(os.path.dirname(output)):
        os.makedirs(os.path.dirname(output))
    with open(output, 'w') as file_handler:
        for index, program in enumerate(programs):
            matrix = convert_opcodes.opcode_to_matrix(program, opcode_set)
            file_handler.write(convert_opcodes.matrix_to_gspan(matrix, index) + '\n')


def generate_pirated_folds():
    # generate 10 folds for pirated programs
    pirated_directory = '.\\data\\MySQL\\pirated'
    pirated_opcode_set = open('.\\opcode_set\\MySQL\\pirated_opcode_set.txt').read().splitlines()
    obfuscation_levels = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400']
    for level in obfuscation_levels:
        pirated_files = glob.glob(os.path.join(pirated_directory, level) + "\\**\\*.txt", recursive=True)
        random.shuffle(pirated_files)
        base = 0
        for fold in range(1, 11):
            r = len(pirated_files) % 10
            if fold <= r:
                step = int(len(pirated_files) / 10) + 1
            else:
                step = int(len(pirated_files) / 10)
            training_set = set(pirated_files) - set(pirated_files[base:base + step])
            test_set = set(pirated_files[base:base + step])
            output_path = '.\\data\\MySQL\\folds\\pirated\\%s\\%s' % (level, fold)
            programs_to_gspan(training_set, os.path.join(output_path, 'train_set.txt'), pirated_opcode_set)
            programs_to_gspan(test_set, os.path.join(output_path, 'test_set.txt'), pirated_opcode_set)
            base += step


def generate_innocent_folds():
    # generate 10 folds for innocent programs
    innocent_directory = '.\\data\\MySQL\\innocent'
    innocent_opcode_set = open('.\\opcode_set\\MySQL\\innocent_opcode_set.txt').read().splitlines()
    innocent_files = glob.glob(innocent_directory + "\\**\\*.txt", recursive=True)
    random.shuffle(innocent_files)
    base = 0
    for fold in range(1, 11):
        r = len(innocent_files) % 10
        if fold <= r:
            step = int(len(innocent_files) / 10) + 1
        else:
            step = int(len(innocent_files) / 10)
        training_set = set(innocent_files) - set(innocent_files[base:base + step])
        test_set = set(innocent_files[base:base + step])
        output_path = '.\\data\\MySQL\\folds\\innocent\\%s' % fold
        programs_to_gspan(training_set, os.path.join(output_path, 'train_set.txt'), innocent_opcode_set)
        programs_to_gspan(test_set, os.path.join(output_path, 'test_set.txt'), innocent_opcode_set)
        base += step


if __name__ == "__main__":
    generate_innocent_folds()
    generate_pirated_folds()
