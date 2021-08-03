# Abstract Algebra

A Python implementation of **Finite Algebras**: Magma, Semigroup, Monoid, Group, Ring, and Field

## Summary

The ``finite_algebras`` module contains class definitions, methods, and functions for working with algebras that only have a **finite number of elements**.

* The primary constructor of algebras is the function, **``make_finite_algebra``**, which examines the properties of the input table and returns the appropriate instance of an algebra.
* Algebras can be input from, or output to, JSON files/strings or Python dictionaries.
* Each algebra is defined by a list of *element names* (``str``) and a *multiplication table* ("Cayley Table"). A *name* and *description* can also be provided.
* Each algebra has methods for examining its properties (e.g., ``is_associative()``, ``is_commutative()``)
* Each algebra has a binary operation, defined by its table.
* Rings & Fields have two binary operations, defined by a second table.
* Algebraic elements can be "multiplied" via their binary operations (e.g., ``v4.op('h','v') ==> 'r'``).
* Inverses & identities can be obtained, if the algebra supports them (e.g., ``z3.inv('a') = 'a^2'``, ``z3.identity ==> 'e'``).
* Direct products of two or more algebras can be computed using Python's multiplication operator (e.g., ``z4 * v4``).
* If two algebras are isomorphic, the mapping between their elements can be determined (e.g., ``v4.isomorphic(z2 * z2) ==> {'h': 'e:a', 'v': 'a:e', 'r': 'a:a', 'e': 'e:e'}``)
* Autogeneration of some types of algebras, of arbitrary order, is supported (e.g., symmetric, cyclic).
* Subalgebras (e.g., subgroups) can be determined, along with related functionality (e.g, ``sg.is_normal()``).

## Installation

This module runs under Python 3.7+ and requires **NumPy**.

Clone the github repository to install:
$ git clone https://github.com/alreich/abstract_algebra.git
## Documentation

See full documentation at [ReadTheDocs](https://abstract-algebra.readthedocs.io/en/latest/index.html).

## Examples

The function, ``make_finite_algebra``, analyzes the input table and outputs the appropriate type of algebra.

In the following example, a Magma is output.


```python
>>> from finite_algebras import make_finite_algebra

>>> make_finite_algebra('RPS',
                        'Rock, Paper, Scissors',
                        ['r', 'p', 's'],
                        [['r', 'p', 'r'],
                         ['p', 'p', 's'],
                         ['r', 's', 's']])
```




    Magma(
    'RPS',
    'Rock, Paper, Scissors',
    ['r', 'p', 's'],
    [[0, 1, 0], [1, 1, 2], [0, 2, 2]]
    )



The method, ``about``, prints out information about an algebra.


```python
>>> v4 = make_finite_algebra('V4',
                             'Klein-4 group',
                             ['e', 'h', 'v', 'r'],
                             [[0, 1, 2, 3],
                              [1, 0, 3, 2],
                              [2, 3, 0, 1],
                              [3, 2, 1, 0]])

>>> v4.about(use_table_names=True)
```

    
    Group: V4
    Description: Klein-4 group
    Identity: e
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       h       h       2
          2       v       v       2
          3       r       r       2
    Cayley Table (showing names):
    [['e', 'h', 'v', 'r'],
     ['h', 'e', 'r', 'v'],
     ['v', 'r', 'e', 'h'],
     ['r', 'v', 'h', 'e']]

