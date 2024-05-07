def sortAndFilter(in_list, filter_index):
    if filter_index > len(in_list):
        raise ValueError("Invalid index for list")
    # Sanity check of list
    if in_list[0][-1] < in_list[0][-2]:
        raise ValueError("List may be have own/max reversed")
    sortable_map = {}
    for item in in_list:
        if item[filter_index] not in sortable_map:
            sortable_map[item[filter_index]] = [0, 0]
        sortable_map[item[filter_index]][0] += item[-2]
        sortable_map[item[filter_index]][1] += item[-1]
    item_sorter = []
    for key in sortable_map:
        item_sorter.append((key, sortable_map[key][0]/sortable_map[key][1], sortable_map[key][1] - sortable_map[key][0]))
    item_sorter = sorteditem_sorter, key=lambda x:(x[1], -x[2], x[0]))
    returned_value = item_sorter[0][0]
    ret_list = []
    for item in in_list:
        if item[filter_index] == returned_value:
            ret_list.append(item)
    return (returned_value, ret_list)
   
