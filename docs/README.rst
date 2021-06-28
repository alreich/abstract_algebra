Abstract Algebra
================

An experimental implementation of finite groups.

For API documentation see:
https://abstract-algebra.readthedocs.io/en/latest/index.html

.. code:: ipython3

    import algebras as alg
    import json
    import os

.. code:: ipython3

    # Path to this repo
    aa_path = os.path.join(os.getenv('PYPROJ'), 'abstract_algebra')
    
    # Path to a directory containing Algebra definitions in JSON
    alg_dir = os.path.join(aa_path, "Algebras")

Groups
------

Store Group in JSON format
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  The mult_table must reference group elements according to their index
   (position) in the element_names list.
-  0 must always refer to the identity element.
-  The first row and first column must be the integers in order, (0, 1,
   2, …, n-1), where n is the number of elements

.. code:: ipython3

    # Path to a JSON file that defines the group V4
    v4_json = os.path.join(alg_dir, "v4_klein_4_group.json")
    
    !cat {v4_json}


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


Read JSON Definition to Instantiate a Group Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    v4 = alg.Group(v4_json)
    v4




.. parsed-literal::

    Group('V4',
    'Klein-4 group',
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]) 



The group can also be created using the Group constuctor.

.. code:: ipython3

    alg.Group('V4',
              'Another way to construct V4',
              ['e',  'h',  'v', 'hv'],
              [[0, 1, 2, 3],
               [1, 0, 3, 2],
               [2, 3, 0, 1],
               [3, 2, 1, 0]]
             )




.. parsed-literal::

    Group('V4',
    'Another way to construct V4',
    ['e', 'h', 'v', 'hv'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]) 



And the group can be created from a Python dictionary:

.. code:: ipython3

    v4_dict = {'type': 'Group',
               'name': 'V4',
               'description': 'Yet another way to define V4',
               'element_names': ['e', 'h', 'v', 'hv'],
               'mult_table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}
    
    alg.Group(v4_dict)




.. parsed-literal::

    Group('V4',
    'Yet another way to define V4',
    ['e', 'h', 'v', 'hv'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]) 



For other ways to create groups, see the Jupyter Notebook,
ways_to_create_a_group.

Pretty Printing a Group
-----------------------

A group can be pretty printed in two ways:

The default way prints the table as it is represented internally using
element indices.

.. code:: ipython3

    v4.pprint()


.. parsed-literal::

    Group('V4',
    'Klein-4 group',
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )


Or it can be printed using element names in the multiplication table.

Note that, here, the element names list is omitted, since it is
redundant to the first row of the table.

.. code:: ipython3

    v4.pprint(True)


.. parsed-literal::

    Group('V4',
    'Klein-4 group',
    [['e', 'h', 'v', 'r'],
     ['h', 'e', 'r', 'v'],
     ['v', 'r', 'e', 'h'],
     ['r', 'v', 'h', 'e']]
    )


In either of the methods, above, the printed output can be evaluated to
create a duplicate of the group.

For example, copying the printout immediately above we obtain the
following:

.. code:: ipython3

    alg.Group('V4',
    'Klein-4 group',
    [['e', 'h', 'v', 'hv'],
     ['h', 'e', 'hv', 'v'],
     ['v', 'hv', 'e', 'h'],
     ['hv', 'v', 'h', 'e']]
    )




.. parsed-literal::

    Group('V4',
    'Klein-4 group',
    ['e', 'h', 'v', 'hv'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]) 



Multiply Group Elements
-----------------------

Group multiplication operation takes zero or more arguments and returns
the product according to the group’s multiplication table (mult_table).

If no argument is provided, then the group’s identity element is
returned

.. code:: ipython3

    v4.mult()




.. parsed-literal::

    'e'



If one argument is provided, then that argument is returned, assuming
it’s a valid element name.

.. code:: ipython3

    v4.mult('h')




.. parsed-literal::

    'h'



If the one argument is not a valid element name, then an exception is
raised.

.. code:: ipython3

    try:
        v4.mult('FOO')
    except ValueError as err:
        print("Caught Error:")
        print(f"  {err}")


.. parsed-literal::

    Caught Error:
      FOO is not a valid Group element name


If two or more arguments are provided, then their combined product is
returned:

.. code:: ipython3

    v4.mult('h','v')  # h * v




.. parsed-literal::

    'r'



.. code:: ipython3

    v4.mult('h', 'v', 'r')  # h * v * hv




.. parsed-literal::

    'e'



Inverse Elements
~~~~~~~~~~~~~~~~

.. code:: ipython3

    v4.inv('h')




.. parsed-literal::

    'h'



That is, :math:`h * h^{-1} = e`

.. code:: ipython3

    v4.mult('h', v4.inv('h'))




.. parsed-literal::

    'e'



Check if Abelian
~~~~~~~~~~~~~~~~

.. code:: ipython3

    v4.is_abelian()




.. parsed-literal::

    True



Check if Associative
~~~~~~~~~~~~~~~~~~~~

NOTE: A group must be is_associative, so this check is done
automatically when a group object is instantiated.

.. code:: ipython3

    v4.is_associative()




.. parsed-literal::

    True



Group Generators
~~~~~~~~~~~~~~~~

For now, there is only one group generator, for cyclic groups of any
finite order:

.. code:: ipython3

    z7 = alg.generate_cyclic_group(7)
    z7.pprint()


.. parsed-literal::

    Group('Z7',
    'Autogenerated cyclic group of order 7',
    ['e', 'a', 'a^2', 'a^3', 'a^4', 'a^5', 'a^6'],
    [[0, 1, 2, 3, 4, 5, 6],
     [1, 2, 3, 4, 5, 6, 0],
     [2, 3, 4, 5, 6, 0, 1],
     [3, 4, 5, 6, 0, 1, 2],
     [4, 5, 6, 0, 1, 2, 3],
     [5, 6, 0, 1, 2, 3, 4],
     [6, 0, 1, 2, 3, 4, 5]]
    )


Derive Direct Product
~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    v4.direct_product_delimiter('-')  # Default delimiter is ':'
    v4_x_v4 = v4 * v4
    v4_x_v4.pprint()


.. parsed-literal::

    Group('V4_x_V4',
    'Direct product of V4 & V4',
    ['e-e', 'e-h', 'e-v', 'e-r', 'h-e', 'h-h', 'h-v', 'h-r', 'v-e', 'v-h', 'v-v', 'v-r', 'r-e', 'r-h', 'r-v', 'r-r'],
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
    )


Convert to Dictionary or JSON string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    v4.to_dict()




.. parsed-literal::

    {'type': 'Group',
     'name': 'V4',
     'description': 'Klein-4 group',
     'element_names': ['e', 'h', 'v', 'r'],
     'mult_table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}



.. code:: ipython3

    v4.dumps()




.. parsed-literal::

    '{"type": "Group", "name": "V4", "description": "Klein-4 group", "element_names": ["e", "h", "v", "r"], "mult_table": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}'



Proper Subgroups
~~~~~~~~~~~~~~~~

.. code:: ipython3

    subs = v4.proper_subgroups()
    
    print(f"\nAll {len(subs)} of these proper subgroups are, obviously, isomorphic to each other.\n")
    
    for sub in subs:
        sub.pprint()


.. parsed-literal::

    
    All 3 of these proper subgroups are, obviously, isomorphic to each other.
    
    Group('V4_subgroup_0',
    'Subgroup of: Klein-4 group',
    ['e', 'h'],
    [[0, 1], [1, 0]]
    )
    Group('V4_subgroup_1',
    'Subgroup of: Klein-4 group',
    ['e', 'v'],
    [[0, 1], [1, 0]]
    )
    Group('V4_subgroup_2',
    'Subgroup of: Klein-4 group',
    ['e', 'r'],
    [[0, 1], [1, 0]]
    )


Print Information about a Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    z7.about()


.. parsed-literal::

    
    Group: Z7
    Autogenerated cyclic group of order 7
    Abelian? True
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       a     a^6       7
          2     a^2     a^5       7
          3     a^3     a^4       7
          4     a^4     a^3       7
          5     a^5     a^2       7
          6     a^6       a       7
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5, 6],
     [1, 2, 3, 4, 5, 6, 0],
     [2, 3, 4, 5, 6, 0, 1],
     [3, 4, 5, 6, 0, 1, 2],
     [4, 5, 6, 0, 1, 2, 3],
     [5, 6, 0, 1, 2, 3, 4],
     [6, 0, 1, 2, 3, 4, 5]]


Resources
~~~~~~~~~

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
