import itertools as it
from finite_algebras import partition_into_isomorphic_lists

def isomorphic_mapping(alg, other, mapping):
    """Returns True if the input mapping from this algebra to the other algebra is isomorphic."""
    return all([mapping[alg.op(x, y)] == other.op(mapping[x], mapping[y])
                for x in alg.elements for y in alg.elements])


def select_subalgebras(alg0, alg1):
    """Return a subalgebra, of highest order possible, from
    each of the two input algebras."""
    if alg0.order != alg1.order:
        print("Algebra orders do not match")
        return None, None

    subs0 = alg0.proper_subalgebras()
    subs1 = alg1.proper_subalgebras()
    if len(subs0) != len(subs1):
        print(f"Total number of subalgebras do not match, {len(subs0)} != {len(subs1)}")
        return None, None

    parts0 = partition_into_isomorphic_lists(subs0)
    parts1 = partition_into_isomorphic_lists(subs1)
    parts0.sort(key=lambda part: part[0].order, reverse=True)
    parts1.sort(key=lambda part: part[0].order, reverse=True)
    len_parts0 = [len(p) for p in parts0]
    len_parts1 = [len(q) for q in parts1]
    if len_parts0 != len_parts1:
        print(f"Number of subalgebras by order do not match, {len_parts0} != {len_parts1}")

    return parts0[0][0], parts1[0][0]


def isomorphisms_from_subalgebras(alg0, alg1):
    """Return a list of isomorphisms (dictionaries) between
    the two input algebras"""

    if alg0.order != alg1.order:
        return None

    sub0, sub1 = select_subalgebras(alg0, alg1)

    # Get the isomorphism between the two subalgebras
    subs_iso = sub0.isomorphic(sub1)

    # Get remainder elements (those not part of the subalgebra isomorphism)
    rem0 = list(set(alg0.elements) - set(sub0.elements))
    rem1 = list(set(alg1.elements) - set(sub1.elements))

    # List all the ways remainder elements can be mapped to each other
    rem_dicts = [dict(zip(rem0, perm)) for perm in it.permutations(rem1)]

    # Append the subalgebra isomorphism (mapping) to each mapping
    isos = [subs_iso | rem for rem in rem_dicts]

    # Return mappings that represent isomorphisms between the algebras
    return [iso for iso in isos if isomorphic_mapping(alg0, alg1, iso)]
