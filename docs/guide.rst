User Guide
==========

Installation
------------

This module runs under Python 3.7+ and requires **numpy**.

Clone the github repository to install:

$ git clone https://github.com/alreich/abstract_algebra.git

Add the *abstract_algebra* directory to your *PYTHONPATH*.

Note: In the examples, below, an environment variable, *PYPROJ*, points
to the directory containing the *abstract_algebra* directory.

Internal Representation of a Finite Group
-----------------------------------------

Internally, the finite Group object consists of four quantities:

-  **name**: (``str``) A short name for the Group;

-  **description**: (``str``) Any additional, useful information about
   the Group;

-  **element_names**: (``list`` of ``str``) The Group’s element names,
   where the first element in the list is the Group’s identity element
   (usually denoted by ``e``);

-  **mult_table**: (``list`` of ``list`` of ``int``) The Group’s
   multiplication table, where each list in the list represents a row of
   the table, and each integer represents the position of an element in
   ‘element_names’. The table must be:

   -  Square. The row & column length equal the number of elements, say,
      n;
   -  The first row and first column should be the [0, 1, 2, …, n-1], in
      that exact order;
   -  Every row and column should contain the same integers, in a
      different order, so that no row or column contains the same
      integer twice. This is a consequence of the fact that every
      element in a group is unique and has an inverse that is also in
      the group.
   -  Capable of supporting associativity of the multiplication
      operator. This last requirement is automatically checked by the
      group constructor.

Group Constuction
-----------------

A Group object can be instantiated in several ways:

1. Enter **four values** corresponding to the quantities described
   above, in the order shown above.
2. Enter **three values** corresponding to ``name``, ``description``,
   and ``mult_table``, where ``mult_table`` uses element names (``str``)
   instead of ``int`` positions. The string-based ``mult_table`` must
   follow rules, similar to those described above:

   -  The identity element comes first in the first row and first
      column;
   -  The order of names in the first row and first column should be
      identical;
   -  No row or column contains the same element name twice.

3. Enter a **Python dictionary**, with keys and values corresponding to
   either the four value or three value input schemes, described above.
4. Enter the **path to a JSON file** (``str``) that corresponds to the
   dictionary described above.

Usage
-----

.. code:: ipython3

    >>> import algebras as alg
    
    >>> z3 = alg.Group('Z3',
                       'Cyclic group of order 3',
                       [[ 'e' ,  'a' , 'a^2'],
                        [ 'a' , 'a^2',  'e' ],
                        ['a^2',  'e' ,  'a' ]]
                      )
    >>> z3




.. parsed-literal::

    Group('Z3',
    'Cyclic group of order 3',
    ['e', 'a', 'a^2'],
    [[0, 1, 2], [1, 2, 0], [2, 0, 1]]) 



Below, we setup some useful path variables, one the points to the
abstract_algebra directory, and the other pointing to a subdirectory
containing algebra definitions in JSON format.

**Note**: The code here assumes that there is an environment variable,
``PYPROJ``, that points to the directory containing the abstract_algebra
directory.

.. code:: ipython3

    >>> import os
    >>> aa_path = os.path.join(os.getenv("PYPROJ"), "abstract_algebra")
    >>> alg_dir = os.path.join(aa_path, "Algebras")

Here’s a look at the Klein-4 Group in JSON format

.. code:: ipython3

    >>> v4_json = os.path.join(alg_dir, "v4_klein_4_group.json")
    >>> !cat {v4_json}


.. parsed-literal::

    {"type": "Group",
     "name": "V4",
     "description": "Klein-4 group",
     "element_names": ["e", "h", "v", "r"],
     "mult_table": [[0, 1, 2, 3],
                    [1, 0, 3, 2],
                    [2, 3, 0, 1],
                    [3, 2, 1, 0]]
    }


The JSON definition of a group can be used to instantiate a Group
object:

.. code:: ipython3

    >>> v4 = alg.Group(v4_json)
    >>> v4




.. parsed-literal::

    Group('V4',
    'Klein-4 group',
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]) 



Pretty print, ``pprint``, tries to print the table in human-readable
form. Calling it with its single argument set to ``True`` will print the
multiplication table using element names, rather than the positions of
element names in the element name list:

.. code:: ipython3

    >>> v4.pprint(True)


.. parsed-literal::

    Group('V4',
    'Klein-4 group',
    [['e', 'h', 'v', 'r'],
     ['h', 'e', 'r', 'v'],
     ['v', 'r', 'e', 'h'],
     ['r', 'v', 'h', 'e']]
    )


An element’s inverse can be obtained using the ``inverse`` method.

**NOTE**: Every element in the Klein-4 group is its own inverse.

.. code:: ipython3

    >>> h_inv = v4.inv('h')
    >>> h_inv




.. parsed-literal::

    'h'



Algebra elements can be *multiplied* using the Group method, ``mult``.

.. code:: ipython3

    >>> v4.mult('h', 'v')  # h * v = hv




.. parsed-literal::

    'r'



``mult`` can be called with zero or more arguments.

Calling ``mult`` without any arguments will return the identity element
for the group.

.. code:: ipython3

    >>> v4.mult()




.. parsed-literal::

    'e'



Calling ``mult`` with only one argument will simply return that
argument.

.. code:: ipython3

    >>> v4.mult('h')




.. parsed-literal::

    'h'



Calling ``mult`` with more than two arguments will return the product of
all of the arguments.

e.g., :math:`h \times v \times h^{-1} = v`

.. code:: ipython3

    >>> v4.mult('h', 'v', h_inv)




.. parsed-literal::

    'v'



A group can be tested to determine if it’s **abelian**:

.. code:: ipython3

    >>> v4.is_abelian()




.. parsed-literal::

    True



A **cyclic group** of any order can be automatically generated:

.. code:: ipython3

    >>> z4 = alg.generate_cyclic_group(4)
    >>> z4




.. parsed-literal::

    Group('Z4',
    'Autogenerated cyclic group of order 4',
    ['e', 'a', 'a^2', 'a^3'],
    [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]) 



The ``about`` method provides information about a group.

.. code:: ipython3

    z4.about(use_table_names=True)


.. parsed-literal::

    
    Group: Z4
    Autogenerated cyclic group of order 4
    Abelian? True
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       a     a^3       4
          2     a^2     a^2       2
          3     a^3       a       4
    Cayley Table (showing names):
    [['e', 'a', 'a^2', 'a^3'],
     ['a', 'a^2', 'a^3', 'e'],
     ['a^2', 'a^3', 'e', 'a'],
     ['a^3', 'e', 'a', 'a^2']]


The **direct product** of two or more groups can be generated using
Python’s multiplication operator, ``*``:

.. code:: ipython3

    >>> z2 = alg.generate_cyclic_group(2)
    >>> z2




.. parsed-literal::

    Group('Z2',
    'Autogenerated cyclic group of order 2',
    ['e', 'a'],
    [[0, 1], [1, 0]]) 



.. code:: ipython3

    >>> z2_x_z2 = z2 * z2
    >>> z2_x_z2




.. parsed-literal::

    Group('Z2_x_Z2',
    'Direct product of Z2 & Z2',
    ['e:e', 'e:a', 'a:e', 'a:a'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]) 



If two groups are isomorphic, then the mapping between their elements is
returned as a Python dictionary.

.. code:: ipython3

    >>> v4.isomorphic(z2_x_z2)




.. parsed-literal::

    {'h': 'e:a', 'v': 'a:e', 'r': 'a:a', 'e': 'e:e'}



If two groups are not isomorphic, then ``False`` is returned.

.. code:: ipython3

    >>> z4.isomorphic(z2_x_z2)




.. parsed-literal::

    False



The proper subgroups of a group can also be computed.

.. code:: ipython3

    >>> z8 = alg.generate_cyclic_group(8)
    >>> z8.proper_subgroups()




.. parsed-literal::

    [Group('Z8_subgroup_0',
     'Subgroup of: Autogenerated cyclic group of order 8',
     ['e', 'a^2', 'a^4', 'a^6'],
     [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]) ,
     Group('Z8_subgroup_1',
     'Subgroup of: Autogenerated cyclic group of order 8',
     ['e', 'a^4'],
     [[0, 1], [1, 0]]) ]



Autogeneration of Groups
------------------------

There are three functions for autogenerating groups: \*
``autogenerate_cyclic_group`` \* ``autogenerate_symmetric_group`` \*
``autogenerate_powerset_group``

The autogeneration of cyclic groups was demonstrated above. Usage of the
other two group autogenerators is illustrated below.

The symmetric group, based on the permutations of n elements, (1, 2, 3,
…, n), can be generated using ``autogenerate_symmetric_group``.

WARNING: Since the order of an autogenerated symmetric group is n!, even
small values of n can result in large groups, which, in turn, can result
in long runtimes associated with operations performed on them.

.. code:: ipython3

    s3 = alg.generate_symmetric_group(3)
    s3.about()


.. parsed-literal::

    
    Group: S3
    Autogenerated symmetric group on 3 elements
    Abelian? False
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


The function, ``autogenerate_powerset_group``, will generate a group on
the powerset of {0, 1, 2, …, n} with symmetric difference as the groups
binary operation. This group is useful because it can be used to form a
ring with set intersection as the second operator.

This means that the order of the autogenerated powerset group will be
:math:`2^n`, so the same WARNING as above applies.

Note that, in the powerset example below, tuples are used as elements,
rather than sets, because the implementation needs to index elements,
and you can’t do that with sets.

.. code:: ipython3

    ps3 = alg.generate_powerset_group(3)
    ps3.about()
    
    #print(f"\nIdentity Element: {ps3.identity}")
    #print(f"Abelian? {ps3.is_abelian()}\n")


.. parsed-literal::

    
    Group: PS3
    Autogenerated group on the powerset of 3 elements, with symmetric difference operator
    Abelian? True
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


.. code:: ipython3

    ps3_proper_subgroups = ps3.proper_subgroups()
    
    print(f"{ps3.name} has {len(ps3_proper_subgroups)} proper subgroups.")
    
    unique_subgroups = alg.divide_groups_into_isomorphic_sets(ps3_proper_subgroups)
    
    print(f"But, up to isomorphisms, only {len(unique_subgroups)} are proper subgroups.")


.. parsed-literal::

    PS3 has 14 proper subgroups.
    But, up to isomorphisms, only 2 are proper subgroups.


Here are the two unique, up to isomorphism, subgroups of PS3:

.. code:: ipython3

    _ = [subgroup[0].pprint() for subgroup in unique_subgroups]


.. parsed-literal::

    Group('PS3_subgroup_0',
    'Subgroup of: Autogenerated group on the powerset of 3 elements, with symmetric difference operator',
    ['{}', '{2}', '{0, 1}', '{0, 1, 2}'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )
    Group('PS3_subgroup_1',
    'Subgroup of: Autogenerated group on the powerset of 3 elements, with symmetric difference operator',
    ['{}', '{0, 2}'],
    [[0, 1], [1, 0]]
    )


