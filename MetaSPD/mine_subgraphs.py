import sys
import os
from gspan_mining import gSpan


def mine_subgraphs(directory, support):
    """
    mines frequent subgraphs with specified minimum support
    :param directory: a directory which contains 10 folds for both training set and test set
    :param support: support value for frequent subgraph mining
    :return: gspan output file for each fold
    """
    for fold in range(1, 11):
        print("Fold %s" % fold)
        orig_stdout = sys.stdout
        output_path = os.path.join(directory, str(fold), 'subgraph_set.txt')
        output_file = open(output_path, 'w')
        sys.stdout = output_file
        file_path = os.path.join(directory, str(fold), 'train_set.txt')
        support_value = get_support(file_path, support)
        subgraph_miner = gSpan(file_path, support_value, where=True, min_num_vertices=2, max_num_vertices=6)
        subgraph_miner.run()
        sys.stdout = orig_stdout
        output_file.close()


def get_support(path, support):
    """
    converts relative support to absolute support
    :param path: programs input file
    :param support: relative support
    :type support: float
    :return: absolute support
    """
    with open(path, 'r') as file_handler:
        return int(file_handler.read().count('#') * support)


def mine_pirated_subgraphs():
    # mines frequent subgraphs in training set of pirated folds
    pirated_directory = '.\\data\\MySQL\\folds\\pirated'
    obfuscation_levels = ['10', '20', '30', '40', '50', '60', '70', '80', '90', '100', '200', '300', '400']
    print('Mining Pirated...')
    for level in obfuscation_levels:
        print("Obfuscation Level %s" % level)
        mine_subgraphs(os.path.join(pirated_directory, str(level)), 1)


def mine_innocent_subgraphs():
    # mines frequent subgraphs in training set of innocent folds
    innocent_directory = '.\\data\\MySQL\\folds\\innocent'
    print('Mining Innocent...')
    mine_subgraphs(innocent_directory, 0.5)


if __name__ == "__main__":
    mine_innocent_subgraphs()
    mine_pirated_subgraphs()
