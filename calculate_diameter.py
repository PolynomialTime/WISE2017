import networkx as nx

def diam(network):
    neighbors = []
    for i in nx.all_neighbors(network,'newcomer'):
        neighbors.append(('newcomer',i))
    Gc = max(nx.connected_component_subgraphs(network), key=len)
    diam_before = nx.diameter(Gc)
    network.remove_node('newcomer')
    Gc = max(nx.connected_component_subgraphs(network), key=len)
    diam_after = nx.diameter(Gc)
    network.add_node('newcomer')
    network.add_edges_from(neighbors)
    return [diam_before,diam_after]