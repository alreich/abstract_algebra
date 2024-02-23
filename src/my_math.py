"""
@author: Alfred J. Reich

"""

# My math functions

# These are fairly standard functions that are not in Python's standard math library.
#
# Some of the functionality here may be available in other large math-related packages
# like, NumPy, SymPy, and SciPy, but are here to reduce the dependency on such large
# packages for just one or two functions.
#
# NOTE: isprime, totient, & divisors are available in sympy.ntheory

import math


def isprime(n):
    """Returns True if n is a positive, prime integer; otherwise, False is returned.
    The same function exists in SymPy."""
    if isinstance(n, int):
        if n == 2:
            return True
        if n % 2 == 0 or n <= 1:
            return False
        root_n = int(math.sqrt(n)) + 1
        for val in range(3, root_n, 2):
            if n % val == 0:
                return False
        return True
    else:
        raise False


def is_relatively_prime(n, m):
    """Return True if n & m are relatively prime, otherwise return False."""
    if math.gcd(n, m) == 1:
        return True
    else:
        return False


def relative_primes(n):
    """Return the list of relative primes that are less than n."""
    return [x for x in range(n) if is_relatively_prime(x, n)]


def totient(n):
    """Return the number of relative primes less than n.
    The same function exists in SymPy."""
    return len(relative_primes(n))


def divisors(n, non_trivial=False):
    """Return the set of divisors of n.  Setting non_trivial=True, returns all
    divisors except for 1 & n. The same function exists in SymPy."""
    result = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        quot, rem = divmod(n, i)
        if rem == 0:
            result.update({i, quot})
    res = sorted(list(result))
    if non_trivial:
        return res[1:-1]
    else:
        return res


def divides(m, n):
    """Returns True if m divides n."""
    if m == 0:
        return False
    elif n == 0:
        return True
    elif (abs(m) <= abs(n)) and (n % m == 0):
        return True
    else:
        return False


# def xgcd(a, b):
#     """The extended Euclidean algorithm.
#
#     Returns gcd, x, & y, such that gcd = a * x + b * y,
#     where gcd is the Greatest Common Divisor of a & b.
#     x & y are called Bézout's coefficients.
#     """
#     x, next_x = 1, 0
#     y, next_y = 0, 1
#     while b:
#         q = a // b
#         # NOTE: Each of the next three lines performs two assignments
#         next_x, x = x - q * next_x, next_x
#         next_y, y = y - q * next_y, next_y
#         a, b = b, a % b
#     return a, x, y

def xgcd(alpha, beta):
    """The extended Euclidean algorithm.

    Returns gcd, x, & y, such that gcd = a * x + b * y,
    where gcd is the Greatest Common Divisor of a & b.
    x & y are called Bézout's coefficients.
    """
    # NOTE: Many of the lines below perform two assigment operations
    a, b = alpha, beta
    x, next_x = 1, 0
    y, next_y = 0, 1
    while b:
        q = a // b
        next_x, x = x - q * next_x, next_x
        next_y, y = y - q * next_y, next_y
        a, b = b, a % b
    return a, x, y
