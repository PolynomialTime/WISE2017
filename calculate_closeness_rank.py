import networkx as nx


def rank(network, target_node):
    conponents = nx.connected_component_subgraphs(network)
    x =0
    for i in conponents:
        if target_node in i.nodes():
            x = i
            break
    num = 0.0
    for node in nx.nodes(x):
        try:
            if nx.closeness_centrality(x, target_node) < nx.closeness_centrality(x, node):
                num += 1
        except:
            num += 1
    centrality_percentage_rank = float(num) / x.number_of_nodes()
    return centrality_percentage_rank + 0.0000001