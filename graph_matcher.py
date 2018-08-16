import os
import sys
import tempfile

import networkx.algorithms.isomorphism as iso
from gspan_mining import gSpan

from MetaSPD.gspan_parser import *


def subgraph_is_isomorphic(graph, subgraph):
    """
    determines whether main graph contains a subgraph which is isomorphic to input subgraph
    :param graph: main graph
    :param subgraph: a subgraph to be searched in main graph
    :return: boolean
    """
    graph_gspan = networkx_to_gspan(graph, 0)
    subgraph_gspan = networkx_to_gspan(subgraph, 1)

    # create temporary files during gspan processing
    input_fd, input_filename = tempfile.mkstemp()
    output_fd, output_filename = tempfile.mkstemp()

    with os.fdopen(input_fd, 'w', encoding='utf-8') as input_handler:
        input_handler.write(graph_gspan + subgraph_gspan)
    orig_stdout = sys.stdout
    sys.stdout = os.fdopen(output_fd, 'w', encoding='utf-8')
    subgraph_miner = gSpan(input_filename, 2, where=True)
    subgraph_miner.run()
    sys.stdout = orig_stdout
    mined_subgraphs = parse_mined_gspan_file(output_filename)

    # remove temporary files
    os.remove(input_filename)
    os.remove(output_filename)

    em = iso.numerical_edge_match('weight', 0)
    nm = iso.categorical_node_match('name', None)
    for mined_subgraph in mined_subgraphs:
        graph_matcher = iso.GraphMatcher(mined_subgraph, subgraph, node_match=nm, edge_match=em)
        if graph_matcher.is_isomorphic():
            return True
    return False


def networkx_to_gspan(networkx_graph, index):
    """
    convert networkx object to gspan format
    :param networkx_graph: networkx graph
    :param index: index number
    :type index: int
    :return: gspan graph
    """
    gspan = "t # %s" % index
    for node, name in nx.get_node_attributes(networkx_graph, 'name').items():
        gspan += "\nv %s %s" % (name, name)
    for edge, weight in nx.get_edge_attributes(networkx_graph, 'weight').items():
        gspan += "\ne %s %s %s\n" % (edge[0], edge[1], weight)
    return gspan


if __name__ == "__main__":
    A = nx.Graph()
    B = nx.Graph()

    A.add_node('andl', name='andl')
    A.add_node('jmp', name='jmp')
    A.add_node('a', name='a')
    A.add_edge('andl', 'jmp', weight=0.17647058823529413)
    A.add_edge('jmp', 'a', weight=0.17647058823529413)
    A.add_edge('a', 'andl', weight=0.17647058823529413)

    B.add_node('andl', name='andl')
    B.add_node('jmp', name='jmp')
    B.add_edge('andl', 'jmp', weight=0.17647058823529413)

    # check whether B is isomorph to another subgraph in A
    print(subgraph_is_isomorphic(A, B))
