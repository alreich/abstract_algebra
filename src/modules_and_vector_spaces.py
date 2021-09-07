from finite_algebras import Group, Ring, Field, yes_or_no


def make_dp_sv_op(alg):
    """Return a scalar-vector operator based on the direct product of a Ring or
    Field with itself.  That is, op:SxV-->V
    """
    delimiter = alg.direct_product_delimiter()
    return lambda s, v: delimiter.join([alg.mult(s, x) for x in v.split(delimiter)])


def make_module(name, description, ring, group, operator):
    """The primary function for creating Vector Spaces or Modules."""
    if isinstance(group, Group):
        if isinstance(ring, Field):
            result = VectorSpace(name, description, ring, group, operator)
        elif isinstance(ring, Ring):
            result = Module(name, description, ring, group, operator)
        else:
            raise ValueError(f"{ring} must be a Ring or a Field")
    else:
        raise ValueError(f"{group} must be a Group")
    return result


class Module:

    def __init__(self, name, description, ring, group, operator):
        self.name = name
        self.description = description
        self.scalar = ring
        self.vector = group
        self.sv_op = operator  # scalar-vector operator
        if not isinstance(ring, Ring):
            raise ValueError(f"{ring} is not a Ring.")
        if not isinstance(group, Group) and group.is_abelian():
            raise ValueError(f"{group} is not an abelian Group.")
        if not check_module_conditions(ring, group, operator):
            raise ValueError("Inputs don't meet requirements for a Module.")

    def __repr__(self):
        sname = self.scalar.name
        vname = self.vector.name
        cname = self.__class__.__name__
        return f"<{cname}:{self.name}, ID:{id(self)}, Scalars:{sname}, Vectors:{vname}>"

    def vector_add(self, v1, v2):
        """Return the sum of two vectors using the Group operation, op."""
        return self.vector.op(v1, v2)

    def about(self, max_size=12, use_table_names=False):
        """Print information about the Module or Vector Space."""
        print(f"\n{self.__class__.__name__}: {self.name}")
        print(f"Instance ID: {id(self)}")
        print(f"Description: {self.description}")
        print(f"Order: {self.scalar.order}")
        print(f"\nSCALARS:")
        self.scalar.about(max_size, use_table_names)
        print(f"\nVECTORS:")
        self.vector.about(max_size, use_table_names)
        return None


class VectorSpace(Module):

    def __init__(self, name, description, field, group, operator):
        super().__init__(name, description, field, group, operator)
        if not isinstance(field, Field):
            raise ValueError(f"{field} must be a Field.")


def generate_n_dim_module(alg, n):
    """Return a Module or Vector Space over the input algebra (field or ring),
    where the vectors are the n-times direct product of the input algebra"""
    if isinstance(alg, Field):
        prefix = "VS"
        kind = "Vector Space"
    elif isinstance(alg, Ring):
        prefix = "Mod"
        kind = "Module"
    else:
        raise ValueError(f"{alg} is not a Ring or a Field")
    name = f"{prefix}{n}-{alg.name}"
    desc = f"{n}-dimensional {kind} over {alg}"
    group = alg.power(n)
    op = make_dp_sv_op(alg)
    return make_module(name, desc, alg, group, op)


def check_module_conditions(ring, group, sv_op, verbose=False):
    """Check all four conditions required of a Module."""

    check1 = check_scaling_by_one(ring, group, sv_op, verbose)
    if verbose:
        print(f"* Scaling by 1 OK? {yes_or_no(check1)}")

    check2 = check_dist_of_scalars_over_vec_add(ring, group, sv_op, verbose)
    if verbose:
        print(f"* Distributivity of scalars over vector addition OK? {yes_or_no(check2)}")

    check3 = check_dist_of_vec_over_scalar_add(ring, group, sv_op, verbose)
    if verbose:
        print(f"* Distributivity of vectors over scalar addition OK? {yes_or_no(check3)}")

    check4 = check_associativity(ring, group, sv_op, verbose)
    if verbose:
        print(f"* Scaling by 1 OK? {yes_or_no(check4)}")

    return check1 & check2 & check3 & check4


def check_scaling_by_one(ring, group, sv_op, verbose=False):
    is_ok = True
    one = ring.one
    for v in group:
        if v != sv_op(one, v):
            is_ok = False
            if verbose:
                print(f"{one} x {v} = {sv_op(one, v)}")
    return is_ok


def check_dist_of_scalars_over_vec_add(ring, group, sv_op, verbose=False):
    is_ok = True
    for s in ring:
        for v1 in group:
            for v2 in group:
                a = sv_op(s, group.op(v1, v2))
                b = group.op(sv_op(s, v1), sv_op(s, v2))
                if a != b:
                    is_ok = False
                    if verbose:
                        print(f"{a} != {b}")
    return is_ok


def check_dist_of_vec_over_scalar_add(ring, group, sv_op, verbose=False):
    is_ok = True
    for s1 in ring:
        for s2 in ring:
            for v in group:
                a = sv_op(ring.add(s1, s2), v)
                b = group.op(sv_op(s1, v), sv_op(s2, v))
                if a != b:
                    is_ok = False
                    if verbose:
                        print(f"{a} != {b}")
    return is_ok


def check_associativity(ring, group, sv_op, verbose=False):
    is_ok = True
    for s1 in ring:
        for s2 in ring:
            for v in group:
                a = sv_op(ring.add(s1, s2), v)
                b = group.op(sv_op(s1, v), sv_op(s2, v))
                if a != b:
                    is_ok = False
                    if verbose:
                        print(f"{a} != {b}")
    return is_ok
