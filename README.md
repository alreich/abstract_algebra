# Abstract Algebra

This is an implementation of **Finite Algebras** in Python: Groups, Rings, Fields, Vector Spaces, Modules, Monoids, Semigroups, Magmas (Groupoids), regular (matrix) representations, abstract matrices, and Cayley-Dickson algebras.

The representation of an algebra here depends on being able to explicitely represent its multiplication/addition table (Cayley table). Large finite algebras--more than a few hundred elements--are possible, but may take a significant amount of time to process.  Also, all algebraic elements here are represented as strings ("symbols").

**NOTE: This Python module is a work-in-progress. Corrections and comments are welcome and appreciated. -- Al Reich, March 2024**

## Summary

The ``finite_algebras`` module contains class definitions, methods, and functions for working with algebras that  have a **finite number of elements**.

* The primary constructor of a finite algebra is the function, ``make_finite_algebra``. It examines the properties of the input table(s) and returns the appropriate instance of an algebra.
* Algebras can be input from, or output to, JSON files/strings or Python dictionaries.
* Each algebra is defined by:
  * A name (``str``),
  * A description (``str``),
  * A list of *element names* (``list`` of ``str``),
    * **All elements must be represented by strings**,
  * One or two square, 2-dimensional tables that define binary operations (``list`` of ``lists`` of ``int``),
    * The <i>ints</i> in a table represent indices in the list of element names,
    * Magmas, Semigroups, Monoids, & Groups have one table; Rings & Fields have two.
* Each algebra has methods for examining its properties (e.g., ``is_associative``, ``is_commutative``, ``center``, ``commutators``, etc.).
* Algebraic elements can be "added" (or "multiplied") via their binary operations (e.g., ``v4.op('h','v')`` $\Rightarrow$ ``'r'``).
* Inverses & identities can be obtained, if the algebra supports them (e.g., ``z3.inv('a')`` $\Rightarrow$ ``'a^2'``, ``z3.identity`` $\Rightarrow$ ``'e'``).
* Direct products of two or more algebras can be computed using Python's multiplication operator (e.g., ``z4 * v4``), and using Python's power operator (e.g., ``v4**3 == v4 * v4 * v4``).
* A Quotient Group is returned when a group, ``g``, is divided by one of it's normal subgroups, ``h``, using Python's true division operator (e.g., ``g / h``).
* Infix arithmetic of algebraic elements is supported for the operators, +, -, *, /, and \*\*, by using the context manager, ``InfixNotation`` (e.g., ``with InfixNotation(v4) as v; hr = v['h'] * v['r']``)
* If two algebras are isomorphic, the mapping between their elements can be found and returned as a Python dictionary (e.g., ``v4.isomorphic(z2 * z2)`` $\Rightarrow$ ``{'h': 'e:a', 'v': 'a:e', 'r': 'a:a', 'e': 'e:e'}``)
* Autogeneration of some types of algebras, of arbitrary order, is supported (e.g., symmetric, cyclic).
* Subalgebras (e.g., subgroups) can be determined, along with related functionality (e.g, ``is_normal()``).
* Groups, Rings, and Fields can be used to construct Modules and Vector Spaces, including n-dimensional Modules and Vector Spaces using the direct products of Rings and Fields, resp.
* Rings and Fields can be used to construct Cayley-Dickson algebras (i.e., abstractions of the complex numbers, as well as quaternions, octonions, etc.)
* The Regular Representation of a Monoid, Group, or the additive abelian Group of a Ring or Field, can be computed in either dense or sparse matrix form.
* Abstract Matrices over Rings/Fields can be represented and used in operations similar to numeric matrices (e.g., $+$, $-$, $\times$, determinant, inverse, etc.)

## Installation

This module runs under Python 3.11+ and requires **numpy**.  The sparse matrix <b>option</b> for Regular Representations requires **scipy.sparse**.

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


```python
>>> from finite_algebras import *
```

### Create an Algebra

As mentioned above, the integers in the 4x4 table, below, are indices of the 4 elements in the element list, ``['e', 'h', 'v', 'r']``.


```python
>>> V4 = make_finite_algebra('V4',
>>>                          'Klein-4 group',
>>>                          ['e', 'h', 'v', 'r'],
>>>                          [[0, 1, 2, 3],
>>>                           [1, 0, 3, 2],
>>>                           [2, 3, 0, 1],
>>>                           [3, 2, 1, 0]])
>>> V4
```




    Group(
    'V4',
    'Klein-4 group',
    ('e', 'h', 'v', 'r'),
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )



The output above is the algebra's **repr**, and can be copied-and-pasted to produce another instance of the algebra.

The **str** form, printed below, is more succinct and cannot be copied-and-pasted.


```python
>>> print(V4)
```

    <Group:V4, ID:5077832032>


### Perform Arithmetic

Using postfix or infix notation (e.g., $h + v - r = e$)


```python
>>> x = V4.op('h', 'v', V4.inv('r'))
>>> x
```




    'e'




```python
>>> with InfixNotation(V4) as v:
>>>     x = v['h'] + v['v'] - v['r']
>>> x
```




    'e'



### Look at the Algebra's Properties

All of the information, provided by the ``about`` method, below, is derived from the table, input above, including the identity element, if it exists.


```python
>>> _ = V4.about(use_table_names=True)  # 'about' prints info, but also returns the algebra itself
```

    
    ** Group **
    Name: V4
    Instance ID: 5077832032
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


### Summarize an Algebra's Proper Subalgebras

Get all proper subalgebras of an algebra.


```python
>>> V4.proper_subalgebras()
```




    [Group(
     'V4_subalgebra_0',
     'Subalgebra of: Klein-4 group',
     ('e', 'h'),
     [[0, 1], [1, 0]]
     ),
     Group(
     'V4_subalgebra_1',
     'Subalgebra of: Klein-4 group',
     ('e', 'r'),
     [[0, 1], [1, 0]]
     ),
     Group(
     'V4_subalgebra_2',
     'Subalgebra of: Klein-4 group',
     ('e', 'v'),
     [[0, 1], [1, 0]]
     )]



Or, summarize the subalgebras by isomorphism.


```python
>>> _ = about_subalgebras(V4)  # Returns a list of lists of proper subalgebras (ignored here)
```

    
    Subalgebras of <Group:V4, ID:5077832032>
      There is 1 unique proper subalgebra, up to isomorphism, out of 3 total subalgebras.
      as shown by the partitions below:
    
    3 Isomorphic Commutative Normal Groups of order 2 with identity 'e':
          Group: V4_subalgebra_0: ('e', 'h')
          Group: V4_subalgebra_1: ('e', 'r')
          Group: V4_subalgebra_2: ('e', 'v')
    


### Autogenerate an Algebra


```python
>>> Z2 = generate_cyclic_group(2)  # Generates a cyclic group of order 2

>>> _ = Z2.about()
```

    
    ** Group **
    Name: Z2
    Instance ID: 5077882800
    Description: Autogenerated cyclic Group of order 2
    Order: 2
    Identity: '0'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['1']
    Elements:
       Index   Name   Inverse  Order
          0     '0'     '0'       1
          1     '1'     '1'       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]


### Compute a Direct Product

If A & B are finite algebras, then A * B and A\*\*3 will also be Direct Products of the algebras. NOTE: A\*\*3 == A * A * A.


```python
>>> Z2_sqr = Z2 * Z2  # NOTE: Z2**2 will also do the same thing

>>> _ = Z2_sqr.about(use_table_names=True)
```

    
    ** Group **
    Name: Z2_x_Z2
    Instance ID: 5077965904
    Description: Direct product of Z2 & Z2
    Order: 4
    Identity: '0:0'
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0   '0:0'   '0:0'       1
          1   '0:1'   '0:1'       2
          2   '1:0'   '1:0'       2
          3   '1:1'   '1:1'       2
    Cayley Table (showing names):
    [['0:0', '0:1', '1:0', '1:1'],
     ['0:1', '0:0', '1:1', '1:0'],
     ['1:0', '1:1', '0:0', '0:1'],
     ['1:1', '1:0', '0:1', '0:0']]


### Find an Isomorphism

It is well known that z2_sqr & v4 are isomorphic. The method ``isomorphic`` confirms this by finding the following mapping between their elements.

If an isomorphism between two algebras does not exist, then ``False`` is returned.


```python
>>> V4.isomorphic(Z2_sqr)
```




    {'e': '0:0', 'h': '0:1', 'v': '1:0', 'r': '1:1'}



### Compute a Quotient Group

V4 is "divided" by one of its normal subgroups, V4sub.

The element list of the quotient group, computed below, is made up of representative elements from each coset, prefixed with "~".


```python
>>> V4sub = Group('V4sub',
>>>                'Subgroup of: Klein-4 group',
>>>                ['e', 'r'],
>>>                [[0, 1],
>>>                 [1, 0]])
>>> 
>>> quotient_group = V4 / V4sub
>>> 
>>> _ = quotient_group.about()
```

    
    ** Group **
    Name: V4/V4sub
    Instance ID: 5078156784
    Description: Group V4 modulo subgroup V4sub
    Order: 2
    Identity: '~e'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['~h']
    Elements:
       Index   Name   Inverse  Order
          0    '~e'    '~e'       1
          1    '~h'    '~h'       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]


Here is the list of left cosets.


```python
>>> list(V4.left_cosets(V4sub))
```




    [['e', 'r'], ['h', 'v']]



Note that if we create the direct product of the subgroup, ``V4sub``, and ``quotient_group``, we obtain an algebra that is isomorphic to the original group, ``V4``.

That is, V4sub $\times$ (V4 / V4sub) $\cong$ V4.


```python
>>> prod = V4sub * quotient_group
>>> _ = prod.about()
```

    
    ** Group **
    Name: V4sub_x_V4/V4sub
    Instance ID: 4380610384
    Description: Direct product of V4sub & V4/V4sub
    Order: 4
    Identity: 'e:~e'
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0  'e:~e'  'e:~e'       1
          1  'e:~h'  'e:~h'       2
          2  'r:~e'  'r:~e'       2
          3  'r:~h'  'r:~h'       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]



```python
>>> V4.isomorphic(prod)
```




    {'e': 'e:~e', 'h': 'e:~h', 'v': 'r:~e', 'r': 'r:~h'}



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

The following small, [finite field with four elements](https://en.wikipedia.org/wiki/Finite_field#Field_with_four_elements) comes from Wikipedia.


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
>>> _ = f4.about(use_table_names=True)
```

    
    ** Field **
    Name: F4
    Instance ID: 5077270016
    Description: Field with 4 elements (from Wikipedia)
    Order: 4
    Identity: '0'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['a', '1+a']
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



### Cayley-Dickson Algebra (CDA)

The following method constructs an abstraction of the complex numbers based on the field, f4, created above.

The CDA constructed from f4 does **not** keep a copy of f4, so conjugates must be stored in a dictionary within the CDA. Note also that the equivalent of "minus one" in f4 is the element '1'.


```python
>>> f4cda = f4.make_cayley_dickson_algebra(version=2)

>>> _ = f4cda.about(max_size=16, show_conjugates=True)
```

    
    ** Ring **
    Name: F4_CDA_1966
    Instance ID: 5077831360
    Description: Cayley-Dickson algebra based on F4, where mu = 1, Schafer 1966 version.
    Order: 16
    Identity: '0:0'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['0:a', '1+a:1', 'a:1', '1:1+a', '0:1+a', '1:a']
    Elements:
       Index   Name   Inverse  Order
          0   '0:0'   '0:0'       1
          1   '0:1'   '0:1'       2
          2   '0:a'   '0:a'       2
          3 '0:1+a' '0:1+a'       2
          4   '1:0'   '1:0'       2
          5   '1:1'   '1:1'       2
          6   '1:a'   '1:a'       2
          7 '1:1+a' '1:1+a'       2
          8   'a:0'   'a:0'       2
          9   'a:1'   'a:1'       2
         10   'a:a'   'a:a'       2
         11 'a:1+a' 'a:1+a'       2
         12 '1+a:0' '1+a:0'       2
         13 '1+a:1' '1+a:1'       2
         14 '1+a:a' '1+a:a'       2
         15 '1+a:1+a' '1+a:1+a'       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
     [1, 0, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12, 15, 14],
     [2, 3, 0, 1, 6, 7, 4, 5, 10, 11, 8, 9, 14, 15, 12, 13],
     [3, 2, 1, 0, 7, 6, 5, 4, 11, 10, 9, 8, 15, 14, 13, 12],
     [4, 5, 6, 7, 0, 1, 2, 3, 12, 13, 14, 15, 8, 9, 10, 11],
     [5, 4, 7, 6, 1, 0, 3, 2, 13, 12, 15, 14, 9, 8, 11, 10],
     [6, 7, 4, 5, 2, 3, 0, 1, 14, 15, 12, 13, 10, 11, 8, 9],
     [7, 6, 5, 4, 3, 2, 1, 0, 15, 14, 13, 12, 11, 10, 9, 8],
     [8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7],
     [9, 8, 11, 10, 13, 12, 15, 14, 1, 0, 3, 2, 5, 4, 7, 6],
     [10, 11, 8, 9, 14, 15, 12, 13, 2, 3, 0, 1, 6, 7, 4, 5],
     [11, 10, 9, 8, 15, 14, 13, 12, 3, 2, 1, 0, 7, 6, 5, 4],
     [12, 13, 14, 15, 8, 9, 10, 11, 4, 5, 6, 7, 0, 1, 2, 3],
     [13, 12, 15, 14, 9, 8, 11, 10, 5, 4, 7, 6, 1, 0, 3, 2],
     [14, 15, 12, 13, 10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 0, 1],
     [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
    Mult. Identity: '1:0'
    Mult. Commutative? Yes
    Zero Divisors: ['1:1', 'a:a', '1+a:1+a']
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15],
     [0, 8, 12, 4, 2, 10, 14, 6, 3, 11, 15, 7, 1, 9, 13, 5],
     [0, 12, 4, 8, 3, 15, 7, 11, 1, 13, 5, 9, 2, 14, 6, 10],
     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
     [0, 5, 10, 15, 5, 0, 15, 10, 10, 15, 0, 5, 15, 10, 5, 0],
     [0, 9, 14, 7, 6, 15, 8, 1, 11, 2, 5, 12, 13, 4, 3, 10],
     [0, 13, 6, 11, 7, 10, 1, 12, 9, 4, 15, 2, 14, 3, 8, 5],
     [0, 2, 3, 1, 8, 10, 11, 9, 12, 14, 15, 13, 4, 6, 7, 5],
     [0, 6, 11, 13, 9, 15, 2, 4, 14, 8, 5, 3, 7, 1, 12, 10],
     [0, 10, 15, 5, 10, 0, 5, 15, 15, 5, 0, 10, 5, 15, 10, 0],
     [0, 14, 7, 9, 11, 5, 12, 2, 13, 3, 10, 4, 6, 8, 1, 15],
     [0, 3, 1, 2, 12, 15, 13, 14, 4, 7, 5, 6, 8, 11, 9, 10],
     [0, 7, 9, 14, 13, 10, 4, 3, 6, 1, 15, 8, 11, 12, 2, 5],
     [0, 11, 13, 6, 14, 5, 3, 8, 7, 12, 10, 1, 9, 2, 4, 15],
     [0, 15, 5, 10, 15, 0, 10, 5, 5, 10, 0, 15, 10, 5, 15, 0]]
    Conjugate Mapping: {'0:0': '0:0', '0:1': '0:1', '0:a': '0:a', '0:1+a': '0:1+a', '1:0': '1:0', '1:1': '1:1', '1:a': '1:a', '1:1+a': '1:1+a', 'a:0': 'a:0', 'a:1': 'a:1', 'a:a': 'a:a', 'a:1+a': 'a:1+a', '1+a:0': '1+a:0', '1+a:1': '1+a:1', '1+a:a': '1+a:a', '1+a:1+a': '1+a:1+a'}

