"""
@author: Alfred J. Reich

"""

# My math functions

# They are fairly standard, why aren't they in the standard math library?

import math


def is_prime(n):
    """Returns True if n is a positive, prime integer; otherwise, False is returned."""
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
    """Return the number of relative primes less than n."""
    return len(relative_primes(n))


def divisors(n, non_trivial=False):
    """Return the set of divisors of n.  Setting non_trivial=True, returns all
    divisors except for 1 & n."""
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


# def xgcd(a, b):
#     """An implementation of the Extended Euclidean Algorithm.
#     Returns gcd, x, & y, such that gcd == a * x + b * y, where
#     gcd is the Greatest Common Divisor,
#     x & y are called Bézout's coefficients.
#     Reference: https://anh.cs.luc.edu/331/notes/xgcd.pdf
#     """
#     prev_x, x = 1, 0
#     prev_y, y = 0, 1
#     while b:
#         q = a // b
#         x, prev_x = prev_x - q * x, x
#         y, prev_y = prev_y - q * y, y
#         a, b = b, a % b
#     return a, prev_x, prev_y


def xgcd(a, b):
    """An implementation of the Extended Euclidean Algorithm.
    Returns gcd, x, & y, such that gcd == a * x + b * y, where
    gcd is the Greatest Common Divisor of a & b.
    x & y are called Bézout's coefficients.
    Reference: https://anh.cs.luc.edu/331/notes/xgcd.pdf
    """
    x, next_x = 1, 0
    y, next_y = 0, 1
    while b:
        q = a // b
        next_x, x = x - q * next_x, next_x
        next_y, y = y - q * next_y, next_y
        a, b = b, a % b
    return a, x, y
