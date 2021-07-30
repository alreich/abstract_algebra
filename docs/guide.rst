User Guide
==========

Algebra Definitions
-------------------

This is a Python module that contains the following implementations of
**finite algebras**:

**Magma** – a set with a binary operation:
:math:`\langle S, \circ \rangle`, where :math:`S` is a finite set and
:math:`\circ: S \times S \to S`

**Semigroup** – an associative Magma: for any
:math:`a,b,c \in S \Rightarrow a \circ (b \circ c) = (a \circ b) \circ c`

**Monoid** – a Semigroup with identity element: :math:`\exists e \in S`,
such that, for all :math:`a \in S, a \circ e = e \circ a = a`

**Group** – a Monoid with inverse elements:
:math:`\forall a \in S, \exists a^{-1} \in S`, such that,
:math:`a \circ a^{-1} = a^{-1} \circ a = e`

**Ring** – :math:`\langle S, +, \cdot \rangle`, where
:math:`\langle S, + \rangle` is a commutative Group,
:math:`\langle S, \cdot \rangle` is a Semigroup, and :math:`+`
distributes over :math:`\cdot`

**Field** – a Ring :math:`\langle S, +, \cdot \rangle`, where
:math:`\langle S\setminus{\{0\}}, \cdot \rangle` is a commutative Group.

Class Hierarchy
---------------

FiniteAlgebra :math:`\rightarrow` Magma :math:`\rightarrow` Semigroup
:math:`\rightarrow` Monoid :math:`\rightarrow` Group :math:`\rightarrow`
Ring :math:`\rightarrow` Field

where, :math:`A \rightarrow B` denotes “A is a superclass of B”.

**NOTE**: The *FiniteAlgbra* class is not intended to be instantiated.

Internal Representation
-----------------------

Internally, a ``FiniteAlgebra`` consists of the following quantities:

-  **name**: (``str``) A short name for the algebra;
-  **description**: (``str``) Any additional, useful information about
   the algebra;
-  **elements**: (``list`` of ``str``) Names of the algebras’s elements.
-  **table**: (``list`` of ``list`` of ``int``) The algebra’s
   multiplication table, where each list in the list represents a row of
   the table, and each integer represents the position of an element in
   ‘element_names’. Optionally, element names (``str``) may be used in
   the table, rather than integers.
-  **table2**: (OPTIONAL) Similar to *table*, above. Required when
   defining a Ring or Field.

**NOTE**: The type of table required here is known as a `Cayley
Table <https://en.wikipedia.org/wiki/Cayley_table>`__. All of the
properties of a finite algebra can be derived from its Cayley Table. For
this reason, this module includes a ``CayleyTable`` class for storing
the table and methods associated with it.

Group Constuction
-----------------

**``make_finite_algebra``**: Although individual algebras (Magma,
Semigroup, etc.) have their own individual constructors, requiring the
quantities described above, the **recommended** way to construct an
algebra is to use the function, ``make_finite_algebra``, using one of
the following three approaches to inputs:

1. Enter **individual values** corresponding to the quantities in its
   Internal Representation, described above.
2. Enter a **Python dictionary** (``dict``), with keys and values
   corresponding to either the four values, described above.
3. Enter the **path to a JSON file** (``str``) that corresponds to the
   dictionary, described above.

``make_finite_algebra`` uses the table(s) to determine what type of
algebra it supports and returns the appropriate algebra.

In the following examples, the only algebra constructor used is
``make_finite_algebra``.

**EXAMPLE: Group**

.. code:: ipython3

    >>> from finite_algebras import make_finite_algebra
    
    >>> z3 = make_finite_algebra('Z3',
                                 'Cyclic group of order 3',
                                 ['e', 'a', 'a^2'],
                                 [[ 'e' ,  'a' , 'a^2'],
                                  [ 'a' , 'a^2',  'e' ],
                                  ['a^2',  'e' ,  'a' ]]
                                )
    >>> z3




.. parsed-literal::

    Group(
    Z3,
    Cyclic group of order 3,
    ['e', 'a', 'a^2'],
    [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
    )



**Associativity, Commutativity, Identity Elements, and Inverses**

.. code:: ipython3

    >>> z3.is_associative()  # Only Magmas are non-associative




.. parsed-literal::

    True



.. code:: ipython3

    >>> z3.is_commutative()  # Same as below




.. parsed-literal::

    True



.. code:: ipython3

    >>> z3.is_abelian()  # Same as above




.. parsed-literal::

    True



.. code:: ipython3

    >>> z3.identity  # Get the algebra's identity element, if it exists




.. parsed-literal::

    'e'



.. code:: ipython3

    >>> z3.table




.. parsed-literal::

    CayleyTable([[0, 1, 2], [1, 2, 0], [2, 0, 1]])



.. code:: ipython3

    >>> z3.inv('a')  # Get an element's inverse, if it exists




.. parsed-literal::

    'a^2'



**Binary Operation**

.. code:: ipython3

    >>> z3.op()  # zero arguments returns the identity, if it exists




.. parsed-literal::

    'e'



.. code:: ipython3

    >>> z3.op('a')




.. parsed-literal::

    'a'



.. code:: ipython3

    >>> z3.op('a', 'a')




.. parsed-literal::

    'a^2'



.. code:: ipython3

    >>> z3.op('a', 'a', 'a')




.. parsed-literal::

    'e'



**The ``about`` Method**

``about`` prints information about an algebra.

.. code:: ipython3

    >>> z3.about()


.. parsed-literal::

    
    Group: Z3
    Description: Cyclic group of order 3
    Identity: e
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       a     a^2       3
          2     a^2       a       3
    Cayley Table (showing indices):
    [[0, 1, 2], [1, 2, 0], [2, 0, 1]]


**EXAMPLE: Magma**

**Rock-Paper-Scissors**

See https://en.wikipedia.org/wiki/Commutative_magma

-  :math:`\langle S, \circ \rangle`, where :math:`S = \{r,p,s\}`
-  For all :math:`x, y \in S`, if :math:`x` *beats* :math:`y`, then
   :math:`x \circ y = y \circ x = x`
-  Also, for all :math:`x \in S`, :math:`xx = x`

From the rule in the second bullet, above, this algebra is obviously
commutative.

.. code:: ipython3

    >>> rps = make_finite_algebra('RPS',
                                  'Rock, Paper, Scissors Magma',
                                  ['r', 'p', 's'],
                                  [['r', 'p', 'r'],
                                   ['p', 'p', 's'],
                                   ['r', 's', 's']])
    
    >>> rps.about()


.. parsed-literal::

    
    Magma: RPS
    Description: Rock, Paper, Scissors Magma
    Elements: ['r', 'p', 's']
    Identity: None
    Associative? No
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 1, 0], [1, 1, 2], [0, 2, 2]]


By default, the ``about`` method prints the table using element
positions, but it can also printout a table using element names:

.. code:: ipython3

    >>> rps.about(use_table_names=True)


.. parsed-literal::

    
    Magma: RPS
    Description: Rock, Paper, Scissors Magma
    Elements: ['r', 'p', 's']
    Identity: None
    Associative? No
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing names):
    [['r', 'p', 'r'], ['p', 'p', 's'], ['r', 's', 's']]


**EXAMPLE (Magma with Identity)**

.. code:: ipython3

    >>> mag = make_finite_algebra('Whatever',
                                  'Magma with Identity',
                                  ['e', 'a', 'b'],
                                  [['e', 'a', 'b'],
                                   ['a', 'e', 'a'],
                                   ['b', 'b', 'a']])
    
    >>> mag.about()


.. parsed-literal::

    
    Magma: Whatever
    Description: Magma with Identity
    Elements: ['e', 'a', 'b']
    Identity: e
    Associative? No
    Commutative? No
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 1, 2], [1, 0, 1], [2, 2, 1]]


**EXAMPLE: Semigroup**

Reference: `Groupoids and Smarandache
Groupoids <https://arxiv.org/ftp/math/papers/0304/0304490.pdf>`__ by W.
B. Vasantha Kandasamy

.. code:: ipython3

    >>> sg = make_finite_algebra('Example 1.4.1',
                             'See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy',
                             ['a', 'b', 'c', 'd', 'e', 'f'],
                             [[0, 3, 0, 3, 0, 3],
                              [1, 4, 1, 4, 1, 4],
                              [2, 5, 2, 5, 2, 5],
                              [3, 0, 3, 0, 3, 0],
                              [4, 1, 4, 1, 4, 1],
                              [5, 2, 5, 2, 5, 2]]
                            )
    >>> sg.about()


.. parsed-literal::

    
    Semigroup: Example 1.4.1
    Description: See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    Elements: ['a', 'b', 'c', 'd', 'e', 'f']
    Identity: None
    Associative? Yes
    Commutative? No
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 3, 0, 3, 0, 3],
     [1, 4, 1, 4, 1, 4],
     [2, 5, 2, 5, 2, 5],
     [3, 0, 3, 0, 3, 0],
     [4, 1, 4, 1, 4, 1],
     [5, 2, 5, 2, 5, 2]]


**EXAMPLE: Monoid**

.. code:: ipython3

    >>> m4 = make_finite_algebra('M4',
                                 'Example of a commutative monoid',
                                 ['a', 'b', 'c', 'd'],
                                 [[0, 0, 0, 0],
                                  [0, 1, 2, 3],
                                  [0, 2, 0, 2],
                                  [0, 3, 2, 1]])
    
    >>> m4.about(use_table_names=True)


.. parsed-literal::

    
    Monoid: M4
    Description: Example of a commutative monoid
    Elements: ['a', 'b', 'c', 'd']
    Identity: b
    Associative? Yes
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing names):
    [['a', 'a', 'a', 'a'],
     ['a', 'b', 'c', 'd'],
     ['a', 'c', 'a', 'c'],
     ['a', 'd', 'c', 'b']]


Serialization
-------------

Algebras can be converted to and from JSON strings/files and Python
dictionaries.

**EXAMPLE: Load from JSON File**

First setup some path variables: \* one that points to the
abstract_algebra directory \* and the other points to a subdirectory
containing algebra definitions in JSON format

Also, the code here assumes that there is an environment variable,
``PYPROJ``, that points to the parent directory of the abstract_algebra
directory.

.. code:: ipython3

    >>> import os
    >>> aa_path = os.path.join(os.getenv("PYPROJ"), "abstract_algebra")
    >>> alg_dir = os.path.join(aa_path, "Algebras")

Here’s the **JSON file**:

.. code:: ipython3

    >>> v4_json = os.path.join(alg_dir, "v4_klein_4_group.json")
    
    >>> !cat {v4_json}


.. parsed-literal::

    {"name": "V4",
     "description": "Klein-4 group",
     "elements": ["e", "h", "v", "r"],
     "table": [[0, 1, 2, 3],
               [1, 0, 3, 2],
               [2, 3, 0, 1],
               [3, 2, 1, 0]]
    }


And, here’s the **algebra**:

.. code:: ipython3

    >>> v4 = make_finite_algebra(v4_json)
    
    >>> v4




.. parsed-literal::

    Group(
    V4,
    Klein-4 group,
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )



**EXAMPLE (Convert to Dictionary)**

.. code:: ipython3

    >>> v4_dict = v4.to_dict()
    
    >>> v4_dict




.. parsed-literal::

    {'type': 'Group',
     'name': 'V4',
     'description': 'Klein-4 group',
     'elements': ['e', 'h', 'v', 'r'],
     'table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}



**EXAMPLE (Construct from Dictionary)**

.. code:: ipython3

    >>> v4_from_dict = make_finite_algebra(v4_dict)
    
    >>> v4_from_dict




.. parsed-literal::

    Group(
    V4,
    Klein-4 group,
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )



**EXAMPLE (Convert to JSON String)**

.. code:: ipython3

    >>> v4_json_string = v4.dumps()
    
    >>> v4_json_string




.. parsed-literal::

    '{"type": "Group", "name": "V4", "description": "Klein-4 group", "elements": ["e", "h", "v", "r"], "table": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}'



**WARNING**: Although an algebra can be constructed by loading its
definition from a JSON file, it cannot be constructed directly from a
JSON string, because ``make_finite_algebra`` interprets a single string
input as a JSON file name. To load an algebra from a JSON string one
first has to convert the string to a Python dictionary and then input
that to ``make_finite_algebra``, as shown below:

.. code:: ipython3

    >>> import json
    
    >>> make_finite_algebra(json.loads(v4_json_string))




.. parsed-literal::

    Group(
    V4,
    Klein-4 group,
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )



Autogeneration of Finite Algebras
---------------------------------

There are three functions for autogenerating a group of a specified
order: \* ``autogenerate_cyclic_group(order)`` \*
``autogenerate_symmetric_group(order)`` \*
``autogenerate_powerset_group(order)``

And one function for autogenerating a monoid of a specified order: \*
``autogenerate_commutative_monoid(order)``

**EXAMPLE: Autogenerated Cyclic Group**

A cyclic group of any desired order can be generated as follows:

.. code:: ipython3

    >>> from finite_algebras import generate_cyclic_group
    
    >>> z2 = generate_cyclic_group(2)
    
    >>> z2




.. parsed-literal::

    Group(
    Z2,
    Autogenerated cyclic group of order 2,
    ['e', 'a'],
    [[0, 1], [1, 0]]
    )



**EXAMPLE: Autogenerated Symmetric Group**

The symmetric group, based on the permutations of n elements, (1, 2, 3,
…, n), can be generated as follows:

**WARNING**: Since the order of an autogenerated symmetric group is
**n!**, even a small value of **n** can result in a very large group.

.. code:: ipython3

    >>> from finite_algebras import generate_symmetric_group
    
    >>> s3 = generate_symmetric_group(3)
    
    >>> s3.about()


.. parsed-literal::

    
    Group: S3
    Description: Autogenerated symmetric group on 3 elements
    Identity: (1, 2, 3)
    Associative? Yes
    Commutative? No
    Elements:
       Index   Name   Inverse  Order
          0 (1, 2, 3) (1, 2, 3)       1
          1 (1, 3, 2) (1, 3, 2)       2
          2 (2, 1, 3) (2, 1, 3)       2
          3 (2, 3, 1) (3, 1, 2)       3
          4 (3, 1, 2) (2, 3, 1)       3
          5 (3, 2, 1) (3, 2, 1)       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5],
     [1, 0, 4, 5, 2, 3],
     [2, 3, 0, 1, 5, 4],
     [3, 2, 5, 4, 0, 1],
     [4, 5, 1, 0, 3, 2],
     [5, 4, 3, 2, 1, 0]]


**EXAMPLE: Autogenerated Powerset Group**

The function, ``autogenerate_powerset_group``, will generate a group on
the powerset of {0, 1, 2, …, n} with **symmetric difference** as the
group’s binary operation. This group is useful because it can be used to
form a ring with set intersection as the second operator.

This means that the order of the autogenerated powerset group will be
:math:`2^n`, so the same WARNING as above applies.

.. code:: ipython3

    >>> from finite_algebras import generate_powerset_group
    
    >>> ps3 = generate_powerset_group(3)
    
    >>> ps3.about()


.. parsed-literal::

    
    Group: PS3
    Description: Autogenerated group on the powerset of 3 elements, with symmetric difference operator
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {0}     {0}       2
          2     {1}     {1}       2
          3     {2}     {2}       2
          4  {0, 1}  {0, 1}       2
          5  {0, 2}  {0, 2}       2
          6  {1, 2}  {1, 2}       2
          7 {0, 1, 2} {0, 1, 2}       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5, 6, 7],
     [1, 0, 4, 5, 2, 3, 7, 6],
     [2, 4, 0, 6, 1, 7, 3, 5],
     [3, 5, 6, 0, 7, 1, 2, 4],
     [4, 2, 1, 7, 0, 6, 5, 3],
     [5, 3, 7, 1, 6, 0, 4, 2],
     [6, 7, 3, 2, 5, 4, 0, 1],
     [7, 6, 5, 4, 3, 2, 1, 0]]


**EXAMPLE: Autogenerated Monoid**

.. code:: ipython3

    >>> from finite_algebras import generate_commutative_monoid
    
    >>> m7 = generate_commutative_monoid(7)
    
    >>> m7.about()


.. parsed-literal::

    
    Monoid: M7
    Description: Autogenerated commutative monoid of order 7
    Elements: ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6']
    Identity: a1
    Associative? Yes
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0, 0],
     [0, 1, 2, 3, 4, 5, 6],
     [0, 2, 4, 6, 1, 3, 5],
     [0, 3, 6, 2, 5, 1, 4],
     [0, 4, 1, 5, 2, 6, 3],
     [0, 5, 3, 1, 6, 4, 2],
     [0, 6, 5, 4, 3, 2, 1]]


Direct Products
---------------

The **direct product** of two or more algebras can be generated using
Python’s multiplication operator, ``*``:

**EXAMPLE: Direct Product of 3 Groups**

.. code:: ipython3

    >>> z2_cubed = z2 * z2 * z2
    
    >>> z2_cubed.about()


.. parsed-literal::

    
    Group: Z2_x_Z2_x_Z2
    Description: Direct product of Z2_x_Z2 & Z2
    Identity: e:e:e
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0   e:e:e   e:e:e       1
          1   e:e:a   e:e:a       2
          2   e:a:e   e:a:e       2
          3   e:a:a   e:a:a       2
          4   a:e:e   a:e:e       2
          5   a:e:a   a:e:a       2
          6   a:a:e   a:a:e       2
          7   a:a:a   a:a:a       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5, 6, 7],
     [1, 0, 3, 2, 5, 4, 7, 6],
     [2, 3, 0, 1, 6, 7, 4, 5],
     [3, 2, 1, 0, 7, 6, 5, 4],
     [4, 5, 6, 7, 0, 1, 2, 3],
     [5, 4, 7, 6, 1, 0, 3, 2],
     [6, 7, 4, 5, 2, 3, 0, 1],
     [7, 6, 5, 4, 3, 2, 1, 0]]


**EXAMPLE: Direct Product of 2 Monoids**

.. code:: ipython3

    >>> mon3 = generate_commutative_monoid(3)
    
    >>> mon3




.. parsed-literal::

    Monoid(
    M3,
    Autogenerated commutative monoid of order 3,
    ['a0', 'a1', 'a2'],
    [[0, 0, 0], [0, 1, 2], [0, 2, 1]]
    )



.. code:: ipython3

    >>> m3_sqr = mon3 * mon3
    >>> m3_sqr.about()


.. parsed-literal::

    
    Monoid: M3_x_M3
    Description: Direct product of M3 & M3
    Elements: ['a0:a0', 'a0:a1', 'a0:a2', 'a1:a0', 'a1:a1', 'a1:a2', 'a2:a0', 'a2:a1', 'a2:a2']
    Identity: a1:a1
    Associative? Yes
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 2, 0, 1, 2, 0, 1, 2],
     [0, 2, 1, 0, 2, 1, 0, 2, 1],
     [0, 0, 0, 3, 3, 3, 6, 6, 6],
     [0, 1, 2, 3, 4, 5, 6, 7, 8],
     [0, 2, 1, 3, 5, 4, 6, 8, 7],
     [0, 0, 0, 6, 6, 6, 3, 3, 3],
     [0, 1, 2, 6, 7, 8, 3, 4, 5],
     [0, 2, 1, 6, 8, 7, 3, 5, 4]]


Isomorphisms
------------

If two groups are isomorphic, then the mapping between their elements is
returned as a Python dictionary.

Here’a a well-known example, using two small groups created above:

**EXAMPLE: Isomorphisms**

.. code:: ipython3

    >>> z2_sqr = z2 * z2
    
    >>> v4.isomorphic(z2_sqr)




.. parsed-literal::

    {'h': 'e:a', 'v': 'a:e', 'r': 'a:a', 'e': 'e:e'}



If two groups are not isomorphic, then ``False`` is returned.

.. code:: ipython3

    >>> z4 = generate_cyclic_group(4)
    
    >>> z4.isomorphic(z2_sqr)




.. parsed-literal::

    False



Subalgebras (Subgroups)
-----------------------

**EXAMPLE: Proper Subgroups**

.. code:: ipython3

    >>> z8 = generate_cyclic_group(8)
    
    >>> z8.proper_subgroups()




.. parsed-literal::

    [Group(
     Z8_subgroup_0,
     Subgroup of: Autogenerated cyclic group of order 8,
     ['e', 'a^4'],
     [[0, 1], [1, 0]]
     ),
     Group(
     Z8_subgroup_1,
     Subgroup of: Autogenerated cyclic group of order 8,
     ['e', 'a^2', 'a^4', 'a^6'],
     [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
     )]



**EXAMPLE: Proper Subgroups, up to Isomorphism**

.. code:: ipython3

    >>> from finite_algebras import partition_into_isomorphic_lists
    
    >>> ps3_proper_subgroups = ps3.proper_subgroups()
    
    >>> print(f"{ps3.name} has {len(ps3_proper_subgroups)} proper subgroups.")
    
    >>> unique_subgroups = partition_into_isomorphic_lists(ps3_proper_subgroups)
    
    >>> print(f"But, up to isomorphisms, only {len(unique_subgroups)} are proper and unique.")


.. parsed-literal::

    PS3 has 14 proper subgroups.
    But, up to isomorphisms, only 2 are proper and unique.


The function, ``partition_into_isomorphic_lists``, does just that; it
partitions a list of groups (subgroups in this case) into a list of
lists, where each sublist contains groups that are all isomophic to each
other.

So, in the following, the ``about`` method is called on the first group
of each sublist:

.. code:: ipython3

    >>> _ = [subgroup[0].about() for subgroup in unique_subgroups]


.. parsed-literal::

    
    Group: PS3_subgroup_0
    Description: Subgroup of: Autogenerated group on the powerset of 3 elements, with symmetric difference operator
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {0}     {0}       2
          2     {1}     {1}       2
          3  {0, 1}  {0, 1}       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    
    Group: PS3_subgroup_1
    Description: Subgroup of: Autogenerated group on the powerset of 3 elements, with symmetric difference operator
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1 {0, 1, 2} {0, 1, 2}       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]


Resources
---------

-  Book: `“Visual Group Theory” by Nathan
   Carter <https://bookstore.ams.org/clrm-32>`__
-  `Group
   Explorer <https://nathancarter.github.io/group-explorer/index.html>`__
   – Visualization software for the abstract algebra classroom
-  `Groupprops, The Group Properties Wiki
   (beta) <https://groupprops.subwiki.org/wiki/Main_Page>`__
-  `GroupNames <https://people.maths.bris.ac.uk/~matyd/GroupNames/index.html>`__
   – “A database, under construction, of names, extensions, properties
   and character tables of finite groups of small order.”
-  `GAP <https://www.gap-system.org/#:~:text=What%20is%20GAP%3F,data%20libraries%20of%20algebraic%20objects.>`__
   – “Groups, Algorithms, Programming - a System for Computational
   Discrete Algebra”
-  `Groups of small
   order <http://www.math.ucsd.edu/~atparris/small_groups.html>`__:
   Compiled by John Pedersen, Dept of Mathematics, University of South
   Florida
-  `List of small
   groups <https://en.wikipedia.org/wiki/List_of_small_groups>`__:
   Finite groups of small order up to group isomorphism
-  `Classification of Groups of Order n ≤ 8
   (PDF) <http://www2.lawrence.edu/fast/corrys/Math300/8Groups.pdf>`__
-  `Subgroups of Order 4
   (PDF) <http://newton.uor.edu/facultyfolder/beery/abstract_algebra/08_SbgrpsOrder4.pdf>`__
-  Klein four-group, V4

   -  `Wikipedia <https://en.wikipedia.org/wiki/Klein_four-group>`__
   -  `Group
      Explorer <https://github.com/nathancarter/group-explorer/blob/master/groups/V_4.group>`__

-  Cyclic group

   -  `Wikipedia <https://en.wikipedia.org/wiki/Cyclic_group>`__
   -  `Z4, cyclic group of order
      4 <https://github.com/nathancarter/group-explorer/blob/master/groups/Z_4.group>`__

-  Symmetric group

   -  `Symmetric group on 3
      letters <https://github.com/nathancarter/group-explorer/blob/master/groups/S_3.group>`__.
      Another name for this group is “Dihedral group on 3 vertices”

-  `Groupoids and Smarandache
   Groupoids <https://arxiv.org/ftp/math/papers/0304/0304490.pdf>`__ by
   W. B. Vasantha Kandasamy
