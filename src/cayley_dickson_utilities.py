import re


def scalar_mult(scalar_name, elem_name, algebra):
    """ Scalar multiplication. 'a' * 'c:d' = 'a*c:a*d'
    Example: scalar_mult('2', '1:2', F3) ==> '2:1'
    """
    delimiter = algebra.direct_product_delimiter()
    components = elem_name.split(delimiter)
    return delimiter.join(map(lambda x: algebra.mult(scalar_name, x), components))


def negate(elem_name, algebra):
    """ Negation:  -'a:b' = '-a:-b'
    Example: negate('1:2', F3) ==> '2:1'
    """
    delimiter = algebra.direct_product_delimiter()
    components = elem_name.split(delimiter)
    return delimiter.join(map(lambda x: algebra.inv(x), components))


def conjugate(elem_name, algebra):
    """ Conjugation: conj('a:b') = 'a:-b'
    Example: conjugate('0:1', F3) ==> '0:2'
    """
    delimiter = algebra.direct_product_delimiter()
    components = elem_name.split(delimiter)
    head = components[0]
    tail = components[1:]
    tail_negated = list(map(lambda x: algebra.inv(x), tail))
    new_components = list(head) + tail_negated
    return delimiter.join(new_components)


def split_element(element, delimiter=':'):
    if delimiter in element:
        matches = list(re.finditer(delimiter, element))
        mid = matches[len(matches) // 2]
        return element[:mid.start()], element[mid.end():]
    else:
        return element


def multiply(x, y, rng, mu=None):
    if mu is None:
        mu = rng.inv(rng.one)  # The additive inverse of the Ring's multiplicative identity
    delim = rng.direct_product_delimiter()
    if delim in x:
        a, b = split_element(x, delim)
        c, d = split_element(y, delim)
        return delim.join((rng.add(rng.mult(a, c), rng.mult(mu, d, conjugate(b, rng))),
                           rng.add(rng.mult(conjugate(a, rng), d), rng.mult(c, b))))
    else:
        return rng.mult(x, y)


def norm(elem_name, algebra, alg_sqr):
    """Squared Absolute Value: 'a:b'^2 = 'a:b' * conj('a:b')
    Example: sqr_abs_val('1:2', F3, F3sqr) ==> '2'
    """
    delimiter = algebra.direct_product_delimiter()
    if delimiter in elem_name:
        # elem_name is not a scalar
        val = alg_sqr.mult(elem_name, conjugate(elem_name, algebra))
    else:
        # elem_name is a scalar
        val = algebra.mult(elem_name, elem_name)
    comp = val.split(delimiter)
    return comp[0]


# NOTE: The inverse function below is just for comparison/verification.
# The Field method, mult_inv, is the better way to compute the inverse of an element.

def inverse(elem_name, algebra, alg_sqr):
    """ Inversion: inv('a:b') = conj('a:b') / sqr_abs_val('a:b')
    Only works for Fields, not Rings.
    Example: inverse('1:1', F3, F3sqr) ==> '2:1'
    """
    if elem_name == alg_sqr.zero:
        raise ValueError(f"The additive identity element, {elem_name}, does not have an inverse.")
    else:
        # delimiter = algebra.direct_product_delimiter()
        absvalsqr = norm(elem_name, algebra, alg_sqr)
        absvalsqrinv = algebra.mult_inv(absvalsqr)
        return scalar_mult(absvalsqrinv, conjugate(elem_name, algebra), algebra)