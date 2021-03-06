import networkx as nx
import matplotlib.pyplot as plt
import network_trade_wars_5 as trade


def draw(network):
    nodes_isolated = []
    for node in network.nodes():  # find the ndoes without edges
        if network.degree(node) == 0:
            nodes_isolated.append(node)
    network.remove_nodes_from(nodes_isolated)  # remove the nodes without edges
    centrality = nx.closeness_centrality(network)  # show the network colored according the the centrality of nodes
    nx.draw(network, with_labels=True, pos=nx.spring_layout(network), node_color=centrality.values(), alpha=0.5, node_size=60)
    plt.show()


g = trade.n1989()
draw(g)