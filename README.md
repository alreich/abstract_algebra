# Abstract Algebra

This is an implementation of **Finite Algebras** in Python: Groups, Rings, Fields, Vector Spaces, Modules, Monoids, Semigroups, and Magmas (Groupoids).

The representation of an algebra here depends on being able to explicitely represent its multiplication/addition table (Cayley table). Large finite algebras--more than a few hundred elements--are possible, but may take a significant amount of time to process.

## Summary

The ``finite_algebras`` module contains class definitions, methods, and functions for working with algebras that  have a **finite number of elements**.

* The primary constructor of a finite algebra is the function, ``make_finite_algebra``. It examines the properties of the input table(s) and returns the appropriate instance of an algebra.
* Algebras can be input from, or output to, JSON files/strings or Python dictionaries.
* Each algebra is defined by:
  * A name (``str``),
  * A description (``str``),
  * A list of *element names* (``list`` of ``str``),
    * All elements must be represented by strings,
  * One or two square, 2-dimensional tables that define binary operations (``list`` of ``lists`` of ``int``),
    * The <i>ints</i> in a table represent indices in the list of element names,
    * Magmas, Semigroups, Monoids, & Groups have one table; Rings & Fields have two.
* Each algebra has methods for examining its properties (e.g., ``is_associative``, ``is_commutative``, ``center``, ``commutators``, etc.).
* Algebraic elements can be "added" (or "multiplied") via their binary operations (e.g., ``v4.op('h','v')`` $\Rightarrow$ ``'r'``).
* Inverses & identities can be obtained, if the algebra supports them (e.g., ``z3.inv('a')`` $\Rightarrow$ ``'a^2'``, ``z3.identity`` $\Rightarrow$ ``'e'``).
* Direct products of two or more algebras can be computed using Python's multiplication operator (e.g., ``z4 * v4``), and using Python's power operator (e.g., ``v4**3 == v4 * v4 * v4``).
* If two algebras are isomorphic, the mapping between their elements can be found and returned as a Python dictionary (e.g., ``v4.isomorphic(z2 * z2)`` $\Rightarrow$ ``{'h': 'e:a', 'v': 'a:e', 'r': 'a:a', 'e': 'e:e'}``)
* Autogeneration of some types of algebras, of arbitrary order, is supported (e.g., symmetric, cyclic).
* Subalgebras (e.g., subgroups) can be determined, along with related functionality (e.g, ``is_normal()``).
* Groups, Rings, and Fields can be used to construct Modules and Vector Spaces, including n-dimensional Modules and Vector Spaces using the direct products of Rings and Fields, resp.
* The Regular Representation of a Monoid, Group, or the additive abelian Group of a Ring or Field, can be computed in either dense or sparse matrix form.
* Abstract Matrices over Rings/Fields can be represented and used in operations similar to numeric matrices (e.g., $+$, $-$, $\times$, determinant, inverse, etc.)

## Installation

This module runs under Python 3.7+ and requires **numpy**.  The sparse matrix <b>option</b> for Regular Representations requires **scipy.sparse**.

Clone the github repository to install:
$ git clone https://github.com/alreich/abstract_algebra.git
Once installed, you can follow along the examples here by setting an <b>environment variable</b>, that "points" to the parent directory of the <i>abstract_algebra</i> directory.

For example, if you clone this module into the directory, '/Users/myname/myrepos', then you can do the following to create an environment variable, PYPROJ, like the one used here.

>import os
> <p> os.environ['PYPROJ'] = '/Users/myname/myrepos'</p>

An environment variable constructed like this only lasts for the duration of the Python session. Consult your implementation of Python to find out how to make the environment variable more "durable".

## Documentation

See full documentation at <i>ReadTheDocs</i>: [https://abstract-algebra.readthedocs.io/](https://abstract-algebra.readthedocs.io/en/latest/index.html)

## Quick Look

### Create an Algebra

As mentioned above, the integers in the 4x4 table, below, are indices of the 4 elements in the element list, ``['e', 'h', 'v', 'r']``.


```python
>>> from finite_algebras import make_finite_algebra

>>> V4 = make_finite_algebra('V4',
                             'Klein-4 group',
                             ['e', 'h', 'v', 'r'],
                             [[0, 1, 2, 3],
                              [1, 0, 3, 2],
                              [2, 3, 0, 1],
                              [3, 2, 1, 0]])
>>> V4
```




    Group(
    'V4',
    'Klein-4 group',
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )



### Look at the Algebra's Properties

All of the information, provided by the ``about`` method, below, is derived from the table, input above, including the identity element, if it exists.


```python
>>> V4.about(use_table_names=True)
```

    
    ** Group **
    Name: V4
    Instance ID: 4597746640
    Description: Klein-4 group
    Order: 4
    Identity: 'e'
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0     'e'     'e'       1
          1     'h'     'h'       2
          2     'v'     'v'       2
          3     'r'     'r'       2
    Cayley Table (showing names):
    [['e', 'h', 'v', 'r'],
     ['h', 'e', 'r', 'v'],
     ['v', 'r', 'e', 'h'],
     ['r', 'v', 'h', 'e']]


### Autogenerate a Small Cyclic Group


```python
>>> from finite_algebras import generate_cyclic_group

>>> Z2 = generate_cyclic_group(2)

>>> Z2.about()
```

    
    ** Group **
    Name: Z2
    Instance ID: 4372024528
    Description: Autogenerated cyclic Group of order 2
    Order: 2
    Identity: 'e'
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a']
    Elements:
       Index   Name   Inverse  Order
          0     'e'     'e'       1
          1     'a'     'a'       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]


### Compute a Direct Product

If A & B are finite algebras, then A * B and A\*\*3 will also be Direct Products of the algebras. NOTE: A\*\*3 == A * A * A.


```python
>>> Z2_sqr = Z2 * Z2  # NOTE: Z2**2 will also do the same thing

>>> Z2_sqr.about(use_table_names=True)
```

    
    ** Group **
    Name: Z2_x_Z2
    Instance ID: 4602714896
    Description: Direct product of Z2 & Z2
    Order: 4
    Identity: 'e:e'
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0   'e:e'   'e:e'       1
          1   'e:a'   'e:a'       2
          2   'a:e'   'a:e'       2
          3   'a:a'   'a:a'       2
    Cayley Table (showing names):
    [['e:e', 'e:a', 'a:e', 'a:a'],
     ['e:a', 'e:e', 'a:a', 'a:e'],
     ['a:e', 'a:a', 'e:e', 'e:a'],
     ['a:a', 'a:e', 'e:a', 'e:e']]


### Find an Isomorphism

It is well known that z2_sqr & v4 are isomorphic. The method ``isomorphic`` confirms this by finding the following mapping between their elements.

If an isomorphism between two algebras does not exist, then ``False`` is returned.


```python
>>> V4.isomorphic(Z2_sqr)
```




    {'e': 'e:e', 'h': 'e:a', 'v': 'a:e', 'r': 'a:a'}



### Regular Representation

The method, ``regular_representation``, constructs an isomorphic mapping between a group, or monoid, and a set of square matrices such that the group's identity element corresponds to the identity matrix.


```python
>>> mapping, _, _, _ = V4.regular_representation()
>>> for elem in mapping:
>>>     print(elem)
>>>     print(mapping[elem])
>>>     print()
```

    e
    [[1. 0. 0. 0.]
     [0. 1. 0. 0.]
     [0. 0. 1. 0.]
     [0. 0. 0. 1.]]
    
    h
    [[0. 1. 0. 0.]
     [1. 0. 0. 0.]
     [0. 0. 0. 1.]
     [0. 0. 1. 0.]]
    
    v
    [[0. 0. 1. 0.]
     [0. 0. 0. 1.]
     [1. 0. 0. 0.]
     [0. 1. 0. 0.]]
    
    r
    [[0. 0. 0. 1.]
     [0. 0. 1. 0.]
     [0. 1. 0. 0.]
     [1. 0. 0. 0.]]
    


### Create a Finite Field

The following small, finite field is used to illustrate Abstract Matrices, farther below.


```python
>>> f4 = make_finite_algebra('F4',
>>>                          'Field with 4 elements (from Wikipedia)',
>>>                          ['0', '1', 'a', '1+a'],
>>>                          [[0, 1, 2, 3],
>>>                           [1, 0, 3, 2],
>>>                           [2, 3, 0, 1],
>>>                           [3, 2, 1, 0]],
>>>                          [[0, 0, 0, 0],
>>>                           [0, 1, 2, 3],
>>>                           [0, 2, 3, 1],
>>>                           [0, 3, 1, 2]]
>>>                         )
```


```python
>>> f4.about(use_table_names=True)
```

    
    ** Field **
    Name: F4
    Instance ID: 4602473168
    Description: Field with 4 elements (from Wikipedia)
    Order: 4
    Identity: '0'
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['1+a', 'a']
    Elements:
       Index   Name   Inverse  Order
          0     '0'     '0'       1
          1     '1'     '1'       2
          2     'a'     'a'       2
          3   '1+a'   '1+a'       2
    Cayley Table (showing names):
    [['0', '1', 'a', '1+a'],
     ['1', '0', '1+a', 'a'],
     ['a', '1+a', '0', '1'],
     ['1+a', 'a', '1', '0']]
    Mult. Identity: '1'
    Mult. Commutative? Yes
    Zero Divisors: None
    Multiplicative Cayley Table (showing names):
    [['0', '0', '0', '0'],
     ['0', '1', 'a', '1+a'],
     ['0', 'a', '1+a', '1'],
     ['0', '1+a', '1', 'a']]


### Abstract Matrices over a Finite Field

Abstract Matrices can be constructed over a Ring or Field.  Abstract Matrices can be added, subtracted, multiplied, transposed, and inverted, if the inverse exists.


```python
>>> from abstract_matrix import AbstractMatrix

>>> arr = [[  '0', '1',   'a'],
>>>        [  '1', 'a', '1+a'],
>>>        ['1+a', '0',   '1']]

>>> mat = AbstractMatrix(arr, f4)
>>> mat
```




    [['0', '1', 'a'],
     ['1', 'a', '1+a'],
     ['1+a', '0', '1']]




```python
>>> mat.determinant()
```




    '1'




```python
>>> mat_inv = mat.inverse()
>>> mat_inv
```




    [['a', '1', '0'],
     ['1+a', '1', 'a'],
     ['1', '1+a', '1']]




```python
>>> mat * mat.inverse()
```




    [['1', '0', '0'],
     ['0', '1', '0'],
     ['0', '0', '1']]


