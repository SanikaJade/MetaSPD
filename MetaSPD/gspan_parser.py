import re
import networkx as nx


def parse_mined_gspan_file(gspan_file, label=None):
    """
    parses mined gspan file for further processing
    :param gspan_file: input mined gspan file
    :param label: label to be set for mined subgraphs
    :return: list of networkx subgraphs
    """
    with open(gspan_file) as file_handler:
        gspan_data = file_handler.read()
        raw_subgraphs = [raw_subgraph.strip() for raw_subgraph in re.split('--*', gspan_data)[:-1]]
        subgraphs = []
        for raw_subgraph in raw_subgraphs:
            lines = raw_subgraph.split('\n')
            vertices = [tuple(line.split(' ')[1:3]) for line in lines if re.match('v .* .*', line)]
            edges = [tuple(line.split(' ')[1:4]) for line in lines if re.match('e .* .* .*', line)]
            parents = tuple(*[re.findall('\d+', line) for line in lines if 'where' in line])
            subgraphs.append(subgraph_to_networkx(vertices, edges, label, parents))
        return subgraphs


def parse_gspan_file(gspan_file, label):
    """
    parses gspan file for further processing
    :param gspan_file: gspan file path
    :param label: label to be set for graphs
    :return: list of networkx graphs
    """
    with open(gspan_file, 'r') as file_handler:
        raw_graphs = re.compile('t # \d+').split(file_handler.read())[1:]
        graphs = []
        for graph in raw_graphs:
            lines = graph.split('\n')
            vertices = [tuple(line.split(' ')[1:3]) for line in lines if re.match('v .* .*', line)]
            edges = [tuple(line.split(' ')[1:4]) for line in lines if re.match('e .* .* .*', line)]
            graphs.append(subgraph_to_networkx(vertices, edges, label))
    return graphs


def subgraph_to_networkx(vertices, edges, label, parents=None):
    """
    creates a networkx object for input subgraph or graph
    :param vertices: input vertices
    :param edges: input edges
    :param label: input label
    :param parents: graphs which contain input subgraph
    :return: networkx object
    """
    graph = nx.Graph(parents=parents, label=label)
    vertices_dict = dict()
    for vertex in vertices:
        vertices_dict[vertex[0]] = vertex[1]
        graph.add_node(vertex[1], name=vertex[1])
    for edge in edges:
        graph.add_edge(vertices_dict[edge[0]], vertices_dict[edge[1]], weight=float(edge[2]))
    return graph


def count_graphs(path):
    """
    counts graphs in gspan file
    :param path: gspan file path
    :return: graphs count
    """
    with open(path, 'r') as file_handler:
        return int(file_handler.read().count('#'))
