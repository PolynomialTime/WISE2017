import networkx as nx
import draw_network
import remove_isolated_part
import calculate_closeness_rank
import networks
import calculate_diameter
import evolution_models
import math
import csv

node_dict_WS_100 = {0:79,1:46,2:15,3:59,4:5,5:20,6:45,7:91,8:37,9:26}
node_dict_WS_200 = {0:141,1:63,2:167,3:18,4:192,5:84,6:91,7:47,8:44,9:113}
node_dict_WS_500 = {0:278,1:347,2:401,3:321,4:407,5:208,6:47,7:264,8:158,9:196}
node_dict_WS_1000 = {0:327,1:75,2:560,3:372,4:893,5:460,6:848,7:998,8:807,9:423}
node_dict_BA_100={0:2,1:5,2:71,3:96,4:53,5:64,6:79,7:77,8:20,9:74}
node_dict_BA_200 = {0:1,1:89,2:51,3:183,4:76,5:39,6:106,7:142,8:187,9:136}
node_dict_BA_500 = {0:5,1:41,2:116,3:270,4:294,5:111,6:421,7:262,8:490,9:345}
node_dict_BA_1000 = {0:723,1:835,2:518,3:369,4:141,5:315,6:557,7:641,8:830,9:999}
node_dict_ER_100 = {0:81,1:49,2:38,3:66,4:34,5:20,6:0,7:94,8:93,9:28}
node_dict_ER_200 = {0:49,1:88,2:72,3:136,4:17,5:185,6:7,7:174,8:41,9:188}
node_dict_ER_500 = {0:82,1:317,2:173,3:341,4:143,5:4,6:264,7:420,8:455,9:429}
node_dict_ER_1000 = {0:240,1:510,2:230,3:151,4:53,5:487,6:660,7:727,8:295,9:528}

def embed(network, newcomer):
    return nx.clustering(network,newcomer) * network.degree(newcomer) * (network.degree(newcomer)-1) / (2*nx.number_of_nodes(network)*(nx.number_of_nodes(network)-1 ))

def cluster_coefficient(network,newcomer):
    return nx.clustering(network,newcomer)

def local(network, newcomer, heuristic):
    if heuristic == 'cls':
        remove_isolated_part.remove(network)
        depth = 2
        radius = 2
        max_closeness_node = 0
        max_closeness = 0
        distance = 0
        while depth <= radius:
            for node in nx.nodes_iter(network):
                try:
                    if nx.dijkstra_path_length(network, node, newcomer) == depth and (
                            not network.has_edge(newcomer, node)):
                        a = nx.closeness_centrality(network, node)
                        if a >= max_closeness:
                            max_closeness = a
                            max_closeness_node = node
                            distance = depth
                except:
                    continue
            depth += 1
        network.add_edge(newcomer, max_closeness_node)
        return distance # distance*1 is the cost
    elif heuristic=='deg':
        # remove_isolated_part.remove(network)
        depth = 2
        radius = 2
        max_degree_node = 0
        max_degree = 0
        distance = 0
        while depth <= radius:
            for node in nx.nodes_iter(network):
                try:
                    if nx.dijkstra_path_length(network, node, newcomer) == depth and (
                    not network.has_edge(newcomer, node)):
                        a = network.degree(node)
                        if a >= max_degree:
                            max_degree = a
                            max_degree_node = node
                            distance = depth
                except:
                    continue
            depth += 1
        network.add_edge(newcomer, max_degree_node)
        return distance # distance*1 is the cost
    elif heuristic=='btw':
        remove_isolated_part.remove(network)
        depth = 2
        radius = 2
        max_btw_node = 0
        max_btw = 0
        distance = 0
        btw = nx.betweenness_centrality(network)
        while depth <= radius:
            for node in nx.nodes_iter(network):
                try:
                    if nx.dijkstra_path_length(network, node, newcomer) == depth and (
                    not network.has_edge(newcomer, node)):
                        if btw[node] >= max_btw:
                            # print node,btw[node]
                            max_btw = btw[node]
                            max_btw_node = node
                            distance = depth
                except:
                    continue
            depth += 1
        network.add_edge(newcomer, max_btw_node)
        return distance  # distance*1 is the cost

def globl(network, newcomer, heuristic):
    if heuristic=='cls':
        remove_isolated_part.remove(network)
        gamma = 0
        r = 2
        nodes_uncover = []
        while len(nodes_uncover) == 0:
            for node in nx.nodes_iter(network):
                if nx.dijkstra_path_length(network, node, newcomer) > r - gamma:
                    nodes_uncover.append(node)
            gamma += 1

        max_cls_node = 'a'
        max_cls = -1
        for node in nodes_uncover:
            x = nx.closeness_centrality(network, node)
            if x > max_cls:
                max_cls_node = node
                max_cls = x
        # print 'node',max_deg_node
        if max_cls_node != 'a':
            cost = nx.dijkstra_path_length(network, max_cls_node, newcomer)
            network.add_edge(newcomer, max_cls_node)
            return cost
    elif heuristic=='deg':
        remove_isolated_part.remove(network)
        gamma = 0
        r = 2
        nodes_uncover = []
        while len(nodes_uncover) == 0:
            for node in nx.nodes_iter(network):
                if nx.dijkstra_path_length(network, node, newcomer) > r - gamma:
                    nodes_uncover.append(node)
            gamma += 1

        max_deg_node = 'a'
        max_degree = -1
        for node in nodes_uncover:
            x = network.degree(node)
            if x > max_degree:
                max_deg_node = node
                max_degree = x
        # print 'node',max_deg_node
        if max_deg_node != 'a':
            cost = nx.dijkstra_path_length(network, max_deg_node, newcomer)
            network.add_edge(newcomer, max_deg_node)
            return cost
    elif heuristic=='btw':
        remove_isolated_part.remove(network)
        gamma = 0
        r = 2
        nodes_uncover = []
        while len(nodes_uncover) == 0:
            for node in nx.nodes_iter(network):
                if nx.dijkstra_path_length(network, node, 'newcomer') > r - gamma:
                    nodes_uncover.append(node)
            gamma += 1

        Gc = max(nx.connected_component_subgraphs(network), key=len)
        max_btw_node = 'a'
        max_btw = -1
        btw = nx.betweenness_centrality(Gc)
        for node in nodes_uncover:
            x = btw[node]
            if x > max_btw:
                max_btw_node = node
                max_btw = x
        # print 'node',max_deg_node
        if max_btw_node != 'a':
            cost = nx.dijkstra_path_length(network, max_btw_node, 'newcomer')
            network.add_edge('newcomer', max_btw_node)
            return cost

def run(model,size,alg,heuristic,limit_of_initial_cost,initial_connection,rank_expected):
    # Set
    cost_per_time_step = 1.0
    cost_per_depth = 2
    upper_limit_of_time_steps = 300
    # CONSTANT
    time_step = 1
    total_cost = 0.0
    # PARAMETERS ABOUT network
    network = None
    node_connected = None
    edges_rewired =None
    if model=='BA':
        if size==100:
            network = networks.B_A_100()
            node_connected = node_dict_BA_100[limit_of_initial_cost]
        elif size==200:
            network = networks.B_A_200()
            node_connected = node_dict_BA_200[limit_of_initial_cost]
        elif size==500:
            network = networks.B_A_500()
            node_connected = node_dict_BA_500[limit_of_initial_cost]
        elif size==1000:
            network = networks.B_A_1000()
            node_connected = node_dict_BA_1000[limit_of_initial_cost]
    elif model=='ER':
        if size==100:
            network = networks.E_R_100()
            node_connected = node_dict_ER_100[limit_of_initial_cost]
        elif size==200:
            network = networks.E_R_200()
            node_connected = node_dict_ER_200[limit_of_initial_cost]
        elif size==500:
            network = networks.E_R_500()
            node_connected = node_dict_ER_500[limit_of_initial_cost]
        elif size==1000:
            network = networks.E_R_1000()
            node_connected = node_dict_ER_1000[limit_of_initial_cost]
    elif model=='WS':
        if size==100:
            g=networks.W_S_100()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_100[limit_of_initial_cost]
        elif size == 200:
            g = networks.W_S_200()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_200[limit_of_initial_cost]
        elif size == 500:
            g = networks.W_S_500()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_500[limit_of_initial_cost]
        elif size==1000:
            g = networks.W_S_1000()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_1000[limit_of_initial_cost]
    # PARAMETERS ABOUT newcomer
    network.add_node('newcomer')  # add the newcomer to the network
    network.add_edge('newcomer',node_connected)


    # loop : newcomer's decision making, while time is lower than the upper limit and centrality of newcomer in rank is lower than expected
    while True:
        if model=='BA':
            evolution_models.B_A(network, 0.01, 2, 0.05, 0.02, time_step)
        elif model=='ER':
            evolution_models.E_R(network, 0.004, 0.05, time_step)
        elif model=='WS':
            evolution_models.W_S(network, 0.2, edges_rewired)
        elif model=='LP':
            evolution_models.L_P_jaccard_coefficient(network, 0.005, 5, time_step)

        if (not network.has_node('newcomer')) or network.degree('newcomer') == 0:
            print 'Exit, Newcomer Eliminated!'
            print 'Time Steps Used:', time_step
            return ['/','/']
        # search the neighbors of the newcomer, search depth is determined by the parameter search_depth_factor
        if alg=='l':
            total_cost += local(network, 'newcomer', heuristic)
        elif alg=='g':
            total_cost += globl(network, 'newcomer', heuristic)

        # calculate the rank of newcomer
        remove_isolated_part.remove(network)
        centrality_percentage_rank = calculate_closeness_rank.rank(network,'newcomer')
        print centrality_percentage_rank
        print total_cost
        print '///////////'
        #diam = calculate_diameter.diam(network)
        #print diam[0],',',diam[1]
        #csv_row.append(diam[0])
        #csv_row.append(diam[1])
        #writer.writerow(csv_row)
        #csv_row=[]
        '''
        if time_step > upper_limit_of_time_steps:
            print 'End, Time Out!'
            print 'Centrality of Newcomer:', float(nx.closeness_centrality(network, 'newcomer')), \
                'Top', '%.2f%%' % (centrality_percentage_rank * 100)
            print 'Total Cost:', total_cost
            print 'Time Steps Used:', time_step
            break

        if  nx.closeness_centrality(network,'newcomer') / centrality_percentage_rank> 25:
            print 'End, Centrality of Newcomer Reaches the Level Expected!'
            print 'Centrality of Newcomer:', float(nx.closeness_centrality(network, 'newcomer')), \
                'Top', '%.2f%%' % (centrality_percentage_rank * 100)
            print 'Total Cost:', total_cost
            print 'Time Steps Used:', time_step
            break
        '''
        time_step += 1
        if time_step == 10:
            break
    #draw_network.draw(network)
    return [total_cost,time_step]

def joint_run(model,size,alg,heuristic,limit_of_initial_cost,initial_connection,rank_expected):
    # Set
    cost_per_time_step = 1.0
    cost_per_depth = 2
    upper_limit_of_time_steps = 300
    # parameters of joint
    benefit_l=[]
    benefit_g=[]
    benefit_l.append(1.0)
    benefit_g.append(1.0)
    rank_last_step = 1.0
    # CONSTANT
    time_step = 1
    total_cost = 0.0
    # PARAMETERS ABOUT network
    network = None
    node_connected = None
    edges_rewired = None
    if model == 'BA':
        if size == 100:
            network = networks.B_A_100()
            node_connected = node_dict_BA_100[limit_of_initial_cost]
        elif size == 200:
            network = networks.B_A_200()
            node_connected = node_dict_BA_200[limit_of_initial_cost]
        elif size == 500:
            network = networks.B_A_500()
            node_connected = node_dict_BA_500[limit_of_initial_cost]
        elif size == 1000:
            network = networks.B_A_1000()
            node_connected = node_dict_BA_1000[limit_of_initial_cost]
    elif model == 'ER':
        if size == 100:
            network = networks.E_R_100()
            node_connected = node_dict_ER_100[limit_of_initial_cost]
        elif size == 200:
            network = networks.E_R_200()
            node_connected = node_dict_ER_200[limit_of_initial_cost]
        elif size == 500:
            network = networks.E_R_500()
            node_connected = node_dict_ER_500[limit_of_initial_cost]
        elif size == 1000:
            network = networks.E_R_1000()
            node_connected = node_dict_ER_1000[limit_of_initial_cost]
    elif model == 'WS':
        if size == 100:
            g = networks.W_S_100()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_100[limit_of_initial_cost]
        elif size == 200:
            g = networks.W_S_200()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_200[limit_of_initial_cost]
        elif size == 500:
            g = networks.W_S_500()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_500[limit_of_initial_cost]
        elif size == 1000:
            g = networks.W_S_1000()
            network = g[0]
            edges_rewired = g[1]
            node_connected = node_dict_WS_1000[limit_of_initial_cost]
    # PARAMETERS ABOUT newcomer
    network.add_node('newcomer')  # add the newcomer to the network
    network.add_edge('newcomer', node_connected)

    # try each algorithm at the beginning
    total_cost += local(network,'newcomer',heuristic)
    benefit_l.append(rank_last_step - calculate_closeness_rank.rank(network,'newcomer'))
    rank_last_step = calculate_closeness_rank.rank(network,'newcomer')
    print rank_last_step * 100
    print total_cost
    print embed(network,'newcomer')
    print '///////////'

    total_cost += globl(network, 'newcomer', heuristic)
    benefit_g.append(rank_last_step - calculate_closeness_rank.rank(network,'newcomer'))
    rank_last_step = calculate_closeness_rank.rank(network,'newcomer')
    print rank_last_step * 100
    print total_cost
    print embed(network, 'newcomer')
    print '///////////'
    time_step=2
    while True:
        if model == 'BA':
            evolution_models.B_A(network, 0.01, 2, 0.05, 0.02, time_step)
        elif model == 'ER':
            evolution_models.E_R(network, 0.004, 0.05, time_step)
        elif model == 'WS':
            evolution_models.W_S(network, 0.2, edges_rewired)
        elif model == 'LP':
            evolution_models.L_P_jaccard_coefficient(network, 0.005, 5, time_step)

        joint_score_l = float(sum(benefit_l)) / len(benefit_l) + math.sqrt(2*math.log(time_step,math.e)/len(benefit_l))
        joint_score_g = float(sum(benefit_g)) / len(benefit_g) + math.sqrt(2 * math.log(time_step, math.e) / len(benefit_g))
        time_step += 1
        if joint_score_l >= joint_score_g:
            total_cost += local(network, 'newcomer', heuristic)
            benefit_l.append(rank_last_step - calculate_closeness_rank.rank(network, 'newcomer'))
            rank_last_step = calculate_closeness_rank.rank(network, 'newcomer')
            print '---chose local---'
        else:
            total_cost += globl(network, 'newcomer', heuristic)
            benefit_g.append(rank_last_step - calculate_closeness_rank.rank(network, 'newcomer'))
            rank_last_step = calculate_closeness_rank.rank(network, 'newcomer')
            print '---chose global---'

        remove_isolated_part.remove(network)
        centrality_percentage_rank = calculate_closeness_rank.rank(network, 'newcomer')
        print rank_last_step * 100
        print total_cost
        #print embed(network, 'newcomer')
        # print '///////////'
        if time_step == 50:
            break
