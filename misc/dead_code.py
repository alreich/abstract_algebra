# def permutation_mapping(perm, base=0):
#     """Return a mapping of the consecutive integers, starting at the base value,
#     to the integers in the permutation, perm.
#
#     Examples:
#
#     >>> permutation_mapping((0, 1, 2, 3))  # (default) base = 0
#     {0: 0, 1: 1, 2: 2, 3: 3}
#
#     >>> permutation_mapping((3,1,2), 1)
#     {1: 3, 2: 1, 3: 2}
#
#     """
#     return {i: perm[i - base] for i in range(base, len(perm) + base)}


# def compose_perms(q, p, base=0):
#     """Apply permutation q to permutation p.  That is q o p = q(p(id),
#     where id is the identity permutation, e.g., (0,1,2,...) or (1,2,3,...).
#
#     Example: from Pinter, page 71
#
#     >>> alpha = (1, 3, 2)
#     >>> beta = (3, 1, 2)
#     >>> compose_perms(alpha, beta, 1)  # base = 1
#     (2, 1, 3)
#     # i.e., alpha(beta(1,2,3)) = alpha(3,1,2) = (2,1,3)
#
#     """
#     qmap = permutation_mapping(q, base)
#     pmap = permutation_mapping(p, base)
#     return tuple([qmap[pmap[i]] for i in range(base, len(q) + base)])


# def swap_list_items(lst, item1, item2):
#     a, b = lst.index(item1), lst.index(item2)
#     lst[b], lst[a] = lst[a], lst[b]
#     return None

# def swap_rows(arr, i, j):
#     """Swap the i_th and j_th rows of a numpy array.
#
#     This function is not used yet."""
#     arr[[i, j], :] = arr[[j, i], :]
#     return arr


# def swap_cols(arr, i, j):
#     """Swap the i_th and j_th columns of a numpy array.
#
#     This function is not used yet."""
#     arr[:, [i, j]] = arr[:, [j, i]]
#     return arr


# def swap_rows_cols(arr, i, j):
#     """Swap the i_th and j_th rows and columns of a numpy array.
#
#     This function is not used yet."""
#     arr0 = swap_rows(arr, i, j)
#     return swap_cols(arr0, i, j)


# def remove_items(tup, items):
#     """Return a copy of the tuple, tup, with 'items' removed."""
#     lst_copy = list(copy.copy(tup))
#     for item in items:
#         lst_copy.remove(item)
#     return tuple(lst_copy)


    # def element_orders(self, reverse=False):
    #     """Return a dictionary where the keys are element names and the values are their orders.
    #
    #     Parameters
    #     ----------
    #     reverse : boolean
    #       If True, then the dict has orders for keys and sets of elements for values.
    #       The default is False.
    #
    #     Returns
    #     -------
    #     dict
    #       A dictionary to look up element order by element name; or, if reversed, then to look up
    #       sets of elements with a given order.
    #     """
    #     order_dict = {elem: self.element_order(elem) for elem in self.element_names}
    #     if reverse:
    #         reverse_dict = {}
    #         for key, val in order_dict.items():
    #             reverse_dict.setdefault(val, []).append(key)
    #         return reverse_dict
    #     else:
    #         return order_dict
