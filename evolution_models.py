import networkx as nx
import selection_probability
import math
import random

def B_A(graph, internal_link_factor, links_added_per_step, add_percentage, del_percentage, time_step):
    # parameters initialization
    network = graph
    f = internal_link_factor
    m = links_added_per_step
    num_add = int(add_percentage * nx.number_of_nodes(network))
    num_del = int(del_percentage * nx.number_of_nodes(network))
    time = time_step
    probability = []
    probability_temp = []
    total_probability = 0
    nodes_pre_step = []
    nodes_added_this_step = []
    nodes_pair_without_edge = []
    nodes_for_del = []

    # calculate how many nodes should be added in this time step
    '''if n >=math.log10(t) and n <= math.log10(t+1):
        num_add = int (n * nx.number_of_nodes(network) / 100)
        num_del = num_add
        #print 'num_add',num_add
    else:
        num_add = int(math.log10(t) * nx.number_of_nodes(network) / 100)
        num_del = int((n * (t-1) / (pow(10,n) - 1)) * nx.number_of_nodes(network) / 100)
        #print 'num_add', num_add
        #print 'num_del', num_del'''


    # calculate the probability of each node to be linked according to whose degree
    for node in nx.nodes_iter(network):
        #print 'degree',network.degree(node)
        nodes_pre_step.append(node)
        probability_temp.append(network.degree(node))
        total_probability += network.degree(node)
    for prob in probability_temp:
        probability.append(float(prob) / total_probability)
    #print 'prob_temp',probability
    #print 'prob',probability

    # add num_add nodes to the network
    i = 1
    while i <= num_add:
        nodes_added_this_step.append('%d' % time + '_' + '%d' % i)
        i += 1
    network.add_nodes_from(nodes_added_this_step)

    # create m links for each node added in this time dtep according to the probability
    #print 'nodes_pre_step',nodes_pre_step
    for node_added in nodes_added_this_step:
        selected_nodes = selection_probability.select(nodes_pre_step,probability,m)
        #print 'selected_nodes', selected_nodes
        for node in selected_nodes:
            network.add_edge(node_added,node)

    # add f % internal links according to the production of each pair of nodes' degrees
    probability = []
    probability_temp = []
    total_probability = 0
    for i, elei in enumerate(nx.nodes_iter(network)):
        for j, elej in enumerate(nx.nodes_iter(network)):
            if i >= j:
                continue
            if not network.has_edge(elei, elej):
                nodes_pair_without_edge.append((elei,elej))
                probability_temp.append(network.degree(elei) * network.degree(elej))
                total_probability += network.degree(elei) * network.degree(elej)
    for prob in probability:
        probability.append(float(prob) / total_probability)
    selected_pairs = selection_probability.select(nodes_pair_without_edge,probability,int(f*nx.number_of_nodes(network)))
    for nodei,nodej in selected_pairs:
        network.add_edge(nodei,nodej)

    # delete num_del nodes according to whose degree
    probability = []
    probability_temp = []
    total_probability = 0.0
    for node in nx.nodes_iter(network):
        nodes_for_del.append(node)
        if network.degree(node) == 0:# if the degree is 0, let it to be 0.1, to avoid errors in probability calculation
            node_degree = 0.1
        else:
            node_degree = network.degree(node)
        probability_temp.append(1.0/node_degree)
        total_probability += 1.0/node_degree
    for prob in probability_temp:
        probability.append(prob/total_probability)
    selected_del = selection_probability.select(nodes_for_del,probability,num_del)
    for node in selected_del:
        network.remove_node(node)
        #print 'del',node

def W_S(graph,beta,edges_rewired):
    network = graph
    edges_add = []
    edges_removed = []
    for edge in edges_rewired:
        x = random.uniform(0, 1)
        if x <= beta:
            node_random_selected = random.randint(0, nx.number_of_nodes(network)-1)
            #print 'node_random_selected',node_random_selected
            #print network.nodes()[node_random_selected]
            if node_random_selected != edge[0] and node_random_selected != edge[1] \
                    and (not ((edge[0], network.nodes()[node_random_selected]) in edges_add))\
                    and (not ((edge[0], network.nodes()[node_random_selected]) in network.edges())):
                edges_add.append((edge[0],network.nodes()[node_random_selected]))
                edges_removed.append(edge)
    network.remove_edges_from(edges_removed)
    network.add_edges_from(edges_add)
    for i in edges_removed:
        edges_rewired.remove(i)
    for j in edges_add:
        edges_rewired.append(j)
    #print edges_rewired

def E_R(network,p,rate,time):
    num_add = int(rate*nx.number_of_nodes(network))
    nodes_added_this_step = []
    i = 1
    nodes_del = []
    while True:
        nodes_del = random.sample(network.nodes(), num_add)
        if not('newcomer' in nodes_del):
            break
    network.remove_nodes_from(nodes_del)
    while i <= num_add:
        nodes_added_this_step.append('%d' % time + '_' + '%d' % i)
        i += 1
    network.add_nodes_from(nodes_added_this_step)
    for i in nodes_added_this_step:
        for j in nx.nodes_iter(network):
            if j == 'newcomer':
                continue
            x = random.uniform(0, 1)
            if x<=p:
                network.add_edge(i,j)

def L_P(graph, threshold_add, threshold_del, time):
    # parameters initialization
    network = graph
    #print nx.number_of_edges(network)
    num_add = int(threshold_add * nx.number_of_edges(network))  # the number of egdes to be added
    #num_del = int(threshold_del * nx.number_of_edges(network))  # the number of edges to be deleted
    nodes_pair_with_edge = []  # the pairs of nodes with edges
    nodes_pair_without_edge = []  # the pairs of nodes without edges
    probability_add = []  # the probabilities of the pairs of nodes to be added
    #probability_del = []  # the probabilities of the pairs of nodes to be deleted
    u = 0  # node i
    v = 0  # node j
    score = 0  # the score of each pair of nodes in link prediction model
    #total_score_with_edge = 0.0  # the sum of scores of pairs of nodes with edge
    total_score_without_edge = 0.0  # the sum of scores of pairs of nodes without edge

    #  calculate the score of each pair of nodes
    for i, elei in enumerate(nx.nodes_iter(network)):
        for j, elej in enumerate(nx.nodes_iter(network)):

            if i >= j:
                continue
            if not network.has_edge(elei, elej):
                try:
                    pre = nx.adamic_adar_index(network, [(elei, elej)])
                    for u, v, s in pre:
                        score = s
                except ZeroDivisionError:
                    score = 5
                total_score_without_edge += score
                nodes_pair_without_edge.append((u, v, score))

    for a, b, c in nodes_pair_without_edge:
        probability_add.append(c / total_score_without_edge)  # calculate the probabilities of edges to be added
    # select edges to be added according to probabilities
    edges_add = selection_probability.select(nodes_pair_without_edge, probability_add, num_add)
    for a, b, c in edges_add:
        network.add_edge(a, b)  # add selected edges

    #print 'del', num_del,',', 'add', num_add,',','edges:', nx.number_of_edges(network)
    #print 'del', edges_del
    #print 'add', edges_add



def L_P_common_neighbors(graph, threshold_add, threshold_del, time):
    # parameters initialization
    network = graph
    #print nx.number_of_edges(network)
    num_add = int(threshold_add * nx.number_of_edges(network))  # the number of egdes to be added
    #num_del = int(threshold_del * nx.number_of_edges(network))  # the number of edges to be deleted
    nodes_pair_with_edge = []  # the pairs of nodes with edges
    nodes_pair_without_edge = []  # the pairs of nodes without edges
    probability_add = []  # the probabilities of the pairs of nodes to be added
    #probability_del = []  # the probabilities of the pairs of nodes to be deleted
    u = 0  # node i
    v = 0  # node j
    score = 0  # the score of each pair of nodes in link prediction model
    #total_score_with_edge = 0.0  # the sum of scores of pairs of nodes with edge
    total_score_without_edge = 0.0  # the sum of scores of pairs of nodes without edge

    #  calculate the score of each pair of nodes
    for i, elei in enumerate(nx.nodes_iter(network)):
        for j, elej in enumerate(nx.nodes_iter(network)):

            if i >= j:
                continue
            if not network.has_edge(elei, elej):
                try:
                    score = len(nx.common_neighbors(network, elei, elej))
                except :
                    continue
                total_score_without_edge += score
                nodes_pair_without_edge.append((elei, elej, score))

    for a, b, c in nodes_pair_without_edge:
        probability_add.append(c / total_score_without_edge)  # calculate the probabilities of edges to be added
    # select edges to be added according to probabilities
    edges_add = selection_probability.select(nodes_pair_without_edge, probability_add, num_add)
    for a, b, c in edges_add:
        network.add_edge(a, b)  # add selected edges

    #print 'del', num_del,',', 'add', num_add,',','edges:', nx.number_of_edges(network)
    #print 'del', edges_del
    #print 'add', edges_add

def L_P_jaccard_coefficient(graph, threshold_add, threshold_del, time):
    # parameters initialization
    network = graph
    # print nx.number_of_edges(network)
    num_add = int(threshold_add * nx.number_of_edges(network))  # the number of egdes to be added
    # num_del = int(threshold_del * nx.number_of_edges(network))  # the number of edges to be deleted
    nodes_pair_with_edge = []  # the pairs of nodes with edges
    nodes_pair_without_edge = []  # the pairs of nodes without edges
    probability_add = []  # the probabilities of the pairs of nodes to be added
    # probability_del = []  # the probabilities of the pairs of nodes to be deleted
    u = 0  # node i
    v = 0  # node j
    score = 0  # the score of each pair of nodes in link prediction model
    # total_score_with_edge = 0.0  # the sum of scores of pairs of nodes with edge
    total_score_without_edge = 0.0  # the sum of scores of pairs of nodes without edge

    #  calculate the score of each pair of nodes
    for i, elei in enumerate(nx.nodes_iter(network)):
        for j, elej in enumerate(nx.nodes_iter(network)):

            if i >= j:
                continue
            if not network.has_edge(elei, elej):
                try:
                    pre = nx.jaccard_coefficient(network, [(elei, elej)])
                    for u, v, s in pre:
                        score = s
                except :
                    continue
                total_score_without_edge += score
                nodes_pair_without_edge.append((elei, elej, score))

    for a, b, c in nodes_pair_without_edge:
        probability_add.append(c / total_score_without_edge)  # calculate the probabilities of edges to be added
    # select edges to be added according to probabilities
    edges_add = selection_probability.select(nodes_pair_without_edge, probability_add, num_add)
    for a, b, c in edges_add:
        network.add_edge(a, b)  # add selected edges

        # print 'del', num_del,',', 'add', num_add,',','edges:', nx.number_of_edges(network)
        # print 'del', edges_del
        # print 'add', edges_add


def N_W_S(graph,beta,nodes_add_rate):
    network = graph
    edges_add = []
    num_of_nodes_add = int(nx.number_of_nodes(network)*nodes_add_rate)
    num = 1
    i=0
    j=0
    num = 1
    while num <= num_of_nodes_add:
        node_selected = random.randint(0, nx.number_of_nodes(network)-1)
        node_1 = node_selected - 1
        node_2 = node_selected + 1
        node_3 = node_selected +2


    for edge in nx.edges_iter(network):
        x = random.uniform(0, 1)
        if x < beta:
            node_random_selected = random.randint(0, nx.number_of_nodes(network)-1)
            #print 'node_random_selected',node_random_selected
            #print network.nodes()[node_random_selected]
            if node_random_selected != edge[0] and node_random_selected != edge[1] \
                    and (not ((edge[0], network.nodes()[node_random_selected]) in edges_add))\
                    and (not ((edge[0], network.nodes()[node_random_selected]) in network.edges())):
                edges_add.append((edge[0],network.nodes()[node_random_selected]))
    network.add_edges_from(edges_add)
    #draw_network.draw(network)

