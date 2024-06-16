#!/usr/bin/python3

"""
Function for sorting and filtering of collection data
"""

def sort_and_filter(in_list:list, filter_index:int):
    """
    Function for sorting and filtering of collection data
    """
    if filter_index > len(in_list[0]):
        raise ValueError("Invalid index for list")
    # Sanity check of list
    if in_list[0][-1] < in_list[0][-2]:
        raise ValueError("List may have own/max reversed")
    is_list = False
    if type(in_list[0][filter_index]) is list or type(in_list[0][filter_index]) is tuple:
        is_list = True
    sortable_map = {}
    for item in in_list:
        if is_list:
            for sub_item in item[filter_index]:
                if sub_item not in sortable_map:
                    sortable_map[sub_item] = [0, 0]
                sortable_map[sub_item][0] += item[-2]
                sortable_map[sub_item][1] += item[-1]
        else:
            if item[filter_index] not in sortable_map:
                sortable_map[item[filter_index]] = [0, 0]
            sortable_map[item[filter_index]][0] += item[-2]
            sortable_map[item[filter_index]][1] += item[-1]
    item_sorter = []
    for item_name, sort_vals in sortable_map.items():
        item_sorter.append((item_name, sort_vals[0]/sort_vals[1], sort_vals[1] - sort_vals[0]))
    item_sorter = sorted(item_sorter, key=lambda x:(x[1], -x[2], x[0]))
    #print(item_sorter)

    returned_value = item_sorter[0][0]
    ret_list = []
    if is_list:
        for item in in_list:
            if returned_value in item[filter_index]:
                ret_list.append(item)
    else:
        for item in in_list:
            if item[filter_index] == returned_value:
                ret_list.append(item)
    return (returned_value, ret_list)
