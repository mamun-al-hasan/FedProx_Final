import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

def iid_divide(l, g):
    num_elems = len(l)
    group_size = int(len(l)/g)
    num_big_groups = num_elems - g * group_size
    num_small_groups = g - num_big_groups
    glist = []
    for i in range(num_small_groups):
        glist.append(l[group_size*i:group_size*(i+1)])
    bi = group_size*num_small_groups
    group_size += 1
    for i in range(num_big_groups):
        glist.append(l[bi+group_size*i:bi+group_size*(i+1)])
    return glist


# def test_iid_divide():
#     # Test case 1: Even division
#     l1 = list(range(10))  # List with 10 elements
#     g1 = 2  # Divide into 2 groups
#     divided_list1 = iid_divide(l1, g1)
#
#     print(f"Original list: {l1}")
#     print(f"Divided into {g1} groups: {divided_list1}")
#     assert len(divided_list1) == g1
#     assert all(len(group) == len(l1) // g1 for group in divided_list1)
#
#     # Test case 2: Uneven division
#     l2 = list(range(10))  # List with 10 elements
#     g2 = 3  # Divide into 3 groups
#     divided_list2 = iid_divide(l2, g2)
#
#     print(f"Original list: {l2}")
#     print(f"Divided into {g2} groups: {divided_list2}")
#     assert len(divided_list2) == g2
#     assert sum(len(group) for group in divided_list2) == len(l2)  # Total elements match original list
#
#     # Test case 3: One group
#     l3 = list(range(5))
#     g3 = 1  # Divide into 1 group
#     divided_list3 = iid_divide(l3, g3)
#
#     print(f"Original list: {l3}")
#     print(f"Divided into {g3} group: {divided_list3}")
#     assert len(divided_list3) == g3
#     assert divided_list3[0] == l3  # All elements should be in one group
#
#     # Test case 4: Group number exceeds list size
#     l4 = list(range(4))  # List with 4 elements
#     g4 = 5  # Trying to divide into 5 groups (more than the elements)
#     divided_list4 = iid_divide(l4, g4)
#
#     print(f"Original list: {l4}")
#     print(f"Divided into {g4} groups: {divided_list4}")
#     assert len(divided_list4) == len(l4)  # Each group will have at most one element
#     assert all(len(group) <= 1 for group in divided_list4)
#
#
# if __name__ == "__main__":
#     test_iid_divide()
