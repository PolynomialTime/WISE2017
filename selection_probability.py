# select num items according to probabilities
import random


def select(node_list, probability, num):
    selected = []
    i = 0
    while i < num:
        x = random.uniform(0,1)
        cumulative_probability = 0.0
        for item, item_probability in zip(node_list,probability):
            cumulative_probability += item_probability
            if x < cumulative_probability:
                selected.append(item)
                break
        i += 1

    selected_list = list(set(selected))  # remove repeated items
    return selected_list
