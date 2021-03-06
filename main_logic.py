import csv
import decision_making


# FILE DATA
csv_title = ['Cimax']
title_counter = 1
while title_counter <= 10:
    csv_title.append('Test'+'%d'%title_counter + '_Total Cost')
    csv_title.append('Test'+'%d'%title_counter + '_Time Steps')
    title_counter += 1
csv_file = file('experiment_data_1.csv', 'wb')
writer = csv.writer(csv_file)
writer.writerow(csv_title)
csv_row = []

# EXPERIMENTS
upper_limit_of_initial_cost_rank = 9
initial_connection = 1
rank_expected = 0.01
test_times = 1
while (upper_limit_of_initial_cost_rank <=9):
    csv_row.append(upper_limit_of_initial_cost_rank)
    test_times = 1
    print 'rank',upper_limit_of_initial_cost_rank
    while test_times <= 1:
        print upper_limit_of_initial_cost_rank
        l = decision_making.joint_run('BA',100,'l','cls',upper_limit_of_initial_cost_rank,initial_connection,rank_expected)
        csv_row.append(l[0])
        csv_row.append(l[1])
        test_times += 1
    writer.writerow(csv_row)
    csv_row = []
    upper_limit_of_initial_cost_rank += 10
