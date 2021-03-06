import networkx as nx


def remove(network):
    nodes_isolated = []
    for node in nx.nodes_iter(network):  # find the ndoes without edges
        try:
            nx.dijkstra_path_length(network, node, 'newcomer')
        except:
            nodes_isolated.append(node)
    network.remove_nodes_from(nodes_isolated)