import pandas as pd
import numpy as np


def opcode_to_matrix(program_path, opcode_set):
    """
    converts program file to adjacency matrix
    :param program_path: program file path
    :param opcode_set: all possible opcodes
    :return: upper triangle of adjacency matrix
    """
    matrix = __init_matrix(opcode_set)
    with open(program_path) as file_handler:
        opcodes = file_handler.read().splitlines()
        for index in range(0, len(opcodes) - 1):
            matrix.loc[opcodes[index], opcodes[index + 1]] += 1
    # calculate row-normalized matrix
    return __upper_triangle(matrix.div(matrix.sum(axis=1), axis=0).fillna(0))


def matrix_to_gspan(matrix, index):
    """
    converts adjacency matrix to gspan format
    :param matrix: adjacency matrix
    :param index: output graph index
    :return: graph in gspan format
    """
    subset = matrix[['Row', 'Column', 'Value']]
    vertices = set(matrix.loc[:, 'Row'].tolist() + matrix.loc[:, 'Column'].tolist())
    edges = [tuple(x) for x in subset.values]
    gspan = ["t # %s" % index]
    gspan.extend(["v %s %s" % (vertex, vertex) for vertex in vertices])
    gspan.extend(["e %s %s %s" % (source, target, weight) for (source, target, weight) in edges])
    return "\n".join(gspan)


def __init_matrix(opcode_set):
    """
    creates an empty matrix from opcode_set
    :param opcode_set: all possible opcodes
    :return: an empty matrix
    """
    index = pd.Index(opcode_set, name="rows")
    column = pd.Index(opcode_set, name="columns")
    matrix = pd.DataFrame(data=0, index=index, columns=column)
    return matrix


def __upper_triangle(matrix):
    """
    extracts upper triangle from input matrix
    :param matrix: adjacency matrix
    :return: upper triangle
    """
    matrix = matrix.where(np.triu(np.ones(matrix.shape)).astype(np.bool))
    matrix = matrix.stack().reset_index()
    matrix.columns = ['Row', 'Column', 'Value']
    return matrix[matrix.Value > 0]
