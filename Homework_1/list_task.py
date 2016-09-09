# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]
def remove_adjacent(lst):
    res = list()
    for i in range(len(lst)):
        if i == 0 or lst[i] != lst[i - 1]:
            res.append(lst[i])
    return res

# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]
def linear_merge(lst1, lst2):
    pos1, pos2 = 0, 0
    res = list()
    while (pos1 != len(lst1) and pos2 != len(lst2)):
        if (lst1[pos1] < lst2[pos2]):
            res.append(lst1[pos1])
            pos1 += 1
        else:
            res.append(lst2[pos2])
            pos2 += 1
    if pos1 != len(lst1):
        res.extend(lst1[pos1:])
    if pos2 != len(lst2):
        res.extend(lst2[pos2:])
    return res

