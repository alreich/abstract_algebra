User Guide
==========

Algebra Definitions
-------------------

This is a Python module that contains the following implementations of
**finite algebras**:

-  **Magma** – a set with a binary operation:
   :math:`\langle S, \circ \rangle`, where :math:`S` is a finite set and
   :math:`\circ: S \times S \to S`

-  **Semigroup** – an associative Magma: for any
   :math:`a,b,c \in S \Rightarrow a \circ (b \circ c) = (a \circ b) \circ c`

-  **Monoid** – a Semigroup with identity element:
   :math:`\exists e \in S`, such that, for all
   :math:`a \in S, a \circ e = e \circ a = a`

-  **Group** – a Monoid with inverse elements:
   :math:`\forall a \in S, \exists a^{-1} \in S`, such that,
   :math:`a \circ a^{-1} = a^{-1} \circ a = e`

-  **Ring** – :math:`\langle S, +, \cdot \rangle`, where
   :math:`\langle S, + \rangle` is a commutative Group,
   :math:`\langle S, \cdot \rangle` is a Semigroup, and :math:`+`
   distributes over :math:`\cdot`

-  **Field** – a Ring :math:`\langle S, +, \cdot \rangle`, where
   :math:`\langle S\setminus{\{0\}}, \cdot \rangle` is a commutative
   Group.

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

Algebra Constuction
-------------------

In a nutshell, use the function, ``make_finite_algebra`` for all algebra
construction.

Although individual algebras (Magma, Semigroup, etc.) have their own
individual constructors, requiring the quantities described above, the
**recommended** way to construct an algebra is to use the function,
``make_finite_algebra``, using one of the following three approaches to
inputs:

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

EXAMPLE: Group
~~~~~~~~~~~~~~

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
    'Z3',
    'Cyclic group of order 3',
    ['e', 'a', 'a^2'],
    [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
    )



Printing an algebra converts the algebra to string containing the unique
id of the algebra instance:

.. code:: ipython3

    >>> print(z3)


.. parsed-literal::

    <Group:Z3, ID:140209749411920>


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



The ``about`` Method
~~~~~~~~~~~~~~~~~~~~

``about`` prints information about an algebra.

.. code:: ipython3

    >>> z3.about()


.. parsed-literal::

    
    Group: Z3
    Instance ID: 140209749411920
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


EXAMPLE: Magma
~~~~~~~~~~~~~~

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
    Instance ID: 140210554229584
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
    Instance ID: 140210554229584
    Description: Rock, Paper, Scissors Magma
    Elements: ['r', 'p', 's']
    Identity: None
    Associative? No
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing names):
    [['r', 'p', 'r'], ['p', 'p', 's'], ['r', 's', 's']]


Paper beats Rock:

.. code:: ipython3

    >>> rps.op('r', 'p')




.. parsed-literal::

    'p'



.. code:: ipython3

    >>> if rps.op() is None:
        print("RPS does not have an identity element")


.. parsed-literal::

    RPS does not have an identity element


**EXAMPLE: Magma with Identity**

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
    Instance ID: 140210554272272
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
    Instance ID: 140210554149968
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


Since the element in the 0,1 position of the table is 3:

‘a’ \* ‘b’ = ‘d’

.. code:: ipython3

    >>> sg.op('a', 'b')




.. parsed-literal::

    'd'



.. code:: ipython3

    >>> if sg.op() is None:
        print("There is no identity element")


.. parsed-literal::

    There is no identity element


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
    Instance ID: 140210554271440
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


.. code:: ipython3

    >>> m4.op()  # Returns the identity element




.. parsed-literal::

    'b'



.. code:: ipython3

    >>> m4.op('c', 'b')  # since 'b' is the identity element




.. parsed-literal::

    'c'



**EXAMPLE: Ring based on powerset of a set**

In this ring, *“addition”* is symmetric difference and
*“multiplication”* is intersection.

.. code:: ipython3

    >>> rng = make_finite_algebra('Powerset Ring 2',
                                  'Ring on powerset of {0, 1}',
                                  ['{}', '{0}', '{1}', '{0, 1}'],
                                  [[0, 1, 2, 3],
                                   [1, 0, 3, 2],
                                   [2, 3, 0, 1],
                                   [3, 2, 1, 0]],
                                  [[0, 0, 0, 0],
                                   [0, 1, 0, 1],
                                   [0, 0, 2, 2],
                                   [0, 1, 2, 3]]
                                 )
    >>> rng




.. parsed-literal::

    Ring(
    'Powerset Ring 2',
    'Ring on powerset of {0, 1}',
    ['{}', '{0}', '{1}', '{0, 1}'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 2, 2], [0, 1, 2, 3]]
    )



.. code:: ipython3

    >>> rng.about(use_table_names=True)


.. parsed-literal::

    
    Ring: Powerset Ring 2
    Instance ID: 140210554194128
    Description: Ring on powerset of {0, 1}
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {0}     {0}       2
          2     {1}     {1}       2
          3  {0, 1}  {0, 1}       2
    Cayley Table (showing names):
    [['{}', '{0}', '{1}', '{0, 1}'],
     ['{0}', '{}', '{0, 1}', '{1}'],
     ['{1}', '{0, 1}', '{}', '{0}'],
     ['{0, 1}', '{1}', '{0}', '{}']]
    Mult. Identity: {0, 1}
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing names):
    [['{}', '{}', '{}', '{}'],
     ['{}', '{0}', '{}', '{0}'],
     ['{}', '{}', '{1}', '{1}'],
     ['{}', '{0}', '{1}', '{0, 1}']]


.. code:: ipython3

    >>> {1} ^ {0,1}  # Symmetric Difference using actual sets




.. parsed-literal::

    {0}



.. code:: ipython3

    >>> rng.add("{1}", "{0, 1}")




.. parsed-literal::

    '{0}'



.. code:: ipython3

    >>> {1} & {0,1}  # Intersection using actual sets




.. parsed-literal::

    {1}



.. code:: ipython3

    >>> rng.mult("{1}", "{0, 1}")




.. parsed-literal::

    '{1}'



**EXAMPLE: Zero Divisors of a Ring**

The Ring just created has two zero divisors:

.. code:: ipython3

    rng.zero_divisors()




.. parsed-literal::

    ['{0}', '{1}']



**EXAMPLE: Autogeneration of a Powerset Ring**

.. code:: ipython3

    >>> from finite_algebras import generate_powerset_ring
    
    >>> psr3 = generate_powerset_ring(3)  # Ring order will be 3!
    
    >>> psr3




.. parsed-literal::

    Ring(
    'PSRing3',
    'Autogenerated Ring on powerset of {0, 1, 2} w/ symm. diff. (add) & intersection (mult)',
    ['{}', '{0}', '{1}', '{2}', '{0, 1}', '{0, 2}', '{1, 2}', '{0, 1, 2}'],
    [[0, 1, 2, 3, 4, 5, 6, 7], [1, 0, 4, 5, 2, 3, 7, 6], [2, 4, 0, 6, 1, 7, 3, 5], [3, 5, 6, 0, 7, 1, 2, 4], [4, 2, 1, 7, 0, 6, 5, 3], [5, 3, 7, 1, 6, 0, 4, 2], [6, 7, 3, 2, 5, 4, 0, 1], [7, 6, 5, 4, 3, 2, 1, 0]],
    [[0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 1, 1, 0, 1], [0, 0, 2, 0, 2, 0, 2, 2], [0, 0, 0, 3, 0, 3, 3, 3], [0, 1, 2, 0, 4, 1, 2, 4], [0, 1, 0, 3, 1, 5, 3, 5], [0, 0, 2, 3, 2, 3, 6, 6], [0, 1, 2, 3, 4, 5, 6, 7]]
    )



.. code:: ipython3

    >>> psr3.about(use_table_names=True)


.. parsed-literal::

    
    Ring: PSRing3
    Instance ID: 140210554304720
    Description: Autogenerated Ring on powerset of {0, 1, 2} w/ symm. diff. (add) & intersection (mult)
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
    Cayley Table (showing names):
    [['{}', '{0}', '{1}', '{2}', '{0, 1}', '{0, 2}', '{1, 2}', '{0, 1, 2}'],
     ['{0}', '{}', '{0, 1}', '{0, 2}', '{1}', '{2}', '{0, 1, 2}', '{1, 2}'],
     ['{1}', '{0, 1}', '{}', '{1, 2}', '{0}', '{0, 1, 2}', '{2}', '{0, 2}'],
     ['{2}', '{0, 2}', '{1, 2}', '{}', '{0, 1, 2}', '{0}', '{1}', '{0, 1}'],
     ['{0, 1}', '{1}', '{0}', '{0, 1, 2}', '{}', '{1, 2}', '{0, 2}', '{2}'],
     ['{0, 2}', '{2}', '{0, 1, 2}', '{0}', '{1, 2}', '{}', '{0, 1}', '{1}'],
     ['{1, 2}', '{0, 1, 2}', '{2}', '{1}', '{0, 2}', '{0, 1}', '{}', '{0}'],
     ['{0, 1, 2}', '{1, 2}', '{0, 2}', '{0, 1}', '{2}', '{1}', '{0}', '{}']]
    Mult. Identity: {0, 1, 2}
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing names):
    [['{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'],
     ['{}', '{0}', '{}', '{}', '{0}', '{0}', '{}', '{0}'],
     ['{}', '{}', '{1}', '{}', '{1}', '{}', '{1}', '{1}'],
     ['{}', '{}', '{}', '{2}', '{}', '{2}', '{2}', '{2}'],
     ['{}', '{0}', '{1}', '{}', '{0, 1}', '{0}', '{1}', '{0, 1}'],
     ['{}', '{0}', '{}', '{2}', '{0}', '{0, 2}', '{2}', '{0, 2}'],
     ['{}', '{}', '{1}', '{2}', '{1}', '{2}', '{1, 2}', '{1, 2}'],
     ['{}', '{0}', '{1}', '{2}', '{0, 1}', '{0, 2}', '{1, 2}', '{0, 1, 2}']]


**EXAMPLE: Ring based on 2x2 Matrices**

This is example 6 here:
http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html

.. code:: ipython3

    addtbl = [['0', 'a', 'b', 'c'],
              ['a', '0', 'c', 'b'],
              ['b', 'c', '0', 'a'],
              ['c', 'b', 'a', '0']]

.. code:: ipython3

    multbl = [['0', '0', '0', '0'],
              ['0', '0', 'a', 'a'],
              ['0', '0', 'b', 'b'],
              ['0', '0', 'c', 'c']]

.. code:: ipython3

    ex6 = make_finite_algebra('Ex6',
                              'Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html',
                              ['0', 'a', 'b', 'c'],
                              addtbl,
                              multbl)
    
    ex6




.. parsed-literal::

    Ring(
    'Ex6',
    'Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html',
    ['0', 'a', 'b', 'c'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 2, 2], [0, 0, 3, 3]]
    )



.. code:: ipython3

    ex6.about(use_table_names=True)


.. parsed-literal::

    
    Ring: Ex6
    Instance ID: 140211627060432
    Description: Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html
    Identity: 0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       0       0       1
          1       a       a       2
          2       b       b       2
          3       c       c       2
    Cayley Table (showing names):
    [['0', 'a', 'b', 'c'],
     ['a', '0', 'c', 'b'],
     ['b', 'c', '0', 'a'],
     ['c', 'b', 'a', '0']]
    Mult. Identity: None
    Mult. Commutative? No
    Multiplicative Cayley Table (showing names):
    [['0', '0', '0', '0'],
     ['0', '0', 'a', 'a'],
     ['0', '0', 'b', 'b'],
     ['0', '0', 'c', 'c']]


Extracting a Ring’s Additive & Multiplicative “Subalgebras”
-----------------------------------------------------------

At the very beginning of this guide document, in the *Algebra
Definitions* section, a Ring is describes as being a combination of a
commutative Group, under addition, and a Semigroup, under
multiplication.

This section shows how the algebraic components of a Ring can be
extracted.

**NOTE**: The implementation of the two extraction methods, illustrated
below, operates by calling ``make_finite_algebra`` using the relevant
portions of the Ring. That way, the appropriate algebras are returned: a
commutative Group for the additive portion, and, at a minimum, a
Semigroup for the multiplicative portion.

.. code:: ipython3

    ex6




.. parsed-literal::

    Ring(
    'Ex6',
    'Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html',
    ['0', 'a', 'b', 'c'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 2, 2], [0, 0, 3, 3]]
    )



The **Additive portion** is a commutative Group, as expected:

.. code:: ipython3

    ex6_add = ex6.extract_additive_algebra()
    ex6_add.about()


.. parsed-literal::

    
    Group: Ex6.Add
    Instance ID: 140209749635728
    Description: Additive-only portion of Ex6
    Identity: 0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       0       0       1
          1       a       a       2
          2       b       b       2
          3       c       c       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]


And, the **Multiplicative portion** is a Semigroup:

.. code:: ipython3

    ex6_mult = ex6.extract_multiplicative_algebra()
    ex6_mult




.. parsed-literal::

    Semigroup(
    'Ex6.Mult',
    'Multiplicative-only portion of Ex6',
    ['0', 'a', 'b', 'c'],
    [[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 2, 2], [0, 0, 3, 3]]
    )



Autogenerate a Commutative Ring
-------------------------------

This Ring autogeneration function is based on example 2 here:
http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html

.. code:: ipython3

    from finite_algebras import generate_commutative_ring

.. code:: ipython3

    r5 = generate_commutative_ring(5)
    r5




.. parsed-literal::

    Ring(
    'R5',
    'Autogenerated commutative Ring of order 5',
    ['a0', 'a1', 'a2', 'a3', 'a4'],
    [[0, 1, 2, 3, 4], [1, 2, 3, 4, 0], [2, 3, 4, 0, 1], [3, 4, 0, 1, 2], [4, 0, 1, 2, 3]],
    [[0, 0, 0, 0, 0], [0, 1, 2, 3, 4], [0, 2, 4, 1, 3], [0, 3, 1, 4, 2], [0, 4, 3, 2, 1]]
    )



.. code:: ipython3

    r5.about(use_table_names=True)


.. parsed-literal::

    
    Ring: R5
    Instance ID: 140209749681616
    Description: Autogenerated commutative Ring of order 5
    Identity: a0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      a0      a0       1
          1      a1      a4       5
          2      a2      a3       5
          3      a3      a2       5
          4      a4      a1       5
    Cayley Table (showing names):
    [['a0', 'a1', 'a2', 'a3', 'a4'],
     ['a1', 'a2', 'a3', 'a4', 'a0'],
     ['a2', 'a3', 'a4', 'a0', 'a1'],
     ['a3', 'a4', 'a0', 'a1', 'a2'],
     ['a4', 'a0', 'a1', 'a2', 'a3']]
    Mult. Identity: a1
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing names):
    [['a0', 'a0', 'a0', 'a0', 'a0'],
     ['a0', 'a1', 'a2', 'a3', 'a4'],
     ['a0', 'a2', 'a4', 'a1', 'a3'],
     ['a0', 'a3', 'a1', 'a4', 'a2'],
     ['a0', 'a4', 'a3', 'a2', 'a1']]


**Extracting it’s component algebras**

In the following, we extract the component algebras of this Ring as a
commutative Group and a Monoid.

The Monoid occurs since this Ring’s multiplicative portion includes a
multiplicative identity element (‘a1’).

.. code:: ipython3

    r5add = r5.extract_additive_algebra()
    r5add.about()


.. parsed-literal::

    
    Group: R5.Add
    Instance ID: 140209749680912
    Description: Additive-only portion of R5
    Identity: a0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      a0      a0       1
          1      a1      a4       5
          2      a2      a3       5
          3      a3      a2       5
          4      a4      a1       5
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4],
     [1, 2, 3, 4, 0],
     [2, 3, 4, 0, 1],
     [3, 4, 0, 1, 2],
     [4, 0, 1, 2, 3]]


.. code:: ipython3

    r5mult = r5.extract_multiplicative_algebra()
    r5mult.about()


.. parsed-literal::

    
    Monoid: R5.Mult
    Instance ID: 140209749637264
    Description: Multiplicative-only portion of R5
    Elements: ['a0', 'a1', 'a2', 'a3', 'a4']
    Identity: a1
    Associative? Yes
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 0, 0, 0, 0],
     [0, 1, 2, 3, 4],
     [0, 2, 4, 1, 3],
     [0, 3, 1, 4, 2],
     [0, 4, 3, 2, 1]]


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
    'V4',
    'Klein-4 group',
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
    'V4',
    'Klein-4 group',
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
input as a JSON file name. To load an algebra from a JSON string,
convert the string to a Python dictionary and then input that to
``make_finite_algebra``, as shown below:

.. code:: ipython3

    >>> import json
    
    >>> make_finite_algebra(json.loads(v4_json_string))




.. parsed-literal::

    Group(
    'V4',
    'Klein-4 group',
    ['e', 'h', 'v', 'r'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    )



Autogeneration of Finite Algebras
---------------------------------

There are three functions for autogenerating a group of a specified
order:

-  ``autogenerate_cyclic_group(order)``
-  ``autogenerate_symmetric_group(order)``
-  ``autogenerate_powerset_group(order)``

And one function for autogenerating a monoid of a specified order:

-  ``autogenerate_commutative_monoid(order)``

**EXAMPLE: Autogenerated Cyclic Group**

A cyclic group of any desired order can be generated as follows:

.. code:: ipython3

    >>> from finite_algebras import generate_cyclic_group
    
    >>> z2 = generate_cyclic_group(2)
    
    >>> z2




.. parsed-literal::

    Group(
    'Z2',
    'Autogenerated cyclic Group of order 2',
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
    Instance ID: 140209749683280
    Description: Autogenerated symmetric Group on 3 elements
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
    Instance ID: 140209749713552
    Description: Autogenerated Group on the powerset of 3 elements, with symmetric difference operator
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
    Instance ID: 140209749746704
    Description: Autogenerated commutative Monoid of order 7
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
    Instance ID: 140209749772112
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
    'M3',
    'Autogenerated commutative Monoid of order 3',
    ['a0', 'a1', 'a2'],
    [[0, 0, 0], [0, 1, 2], [0, 2, 1]]
    )



.. code:: ipython3

    >>> m3_sqr = mon3 * mon3
    >>> m3_sqr.about()


.. parsed-literal::

    
    Monoid: M3_x_M3
    Instance ID: 140210292664784
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

**EXAMPLE: Group Isomorphism**

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



**EXAMPLE: Magma Isomorphism**

**Water, Fire, Stick Magma**

A made-up Magma, similar to Rock, Paper, Scissors:

-  Water quenches Fire
-  Fire burns Stick
-  Stick floats on Water

.. code:: ipython3

    wfs = make_finite_algebra('WFS',
                              'Water, Fire, Stick Magma',
                              ['water', 'fire', 'stick'],
                              [[0, 0, 2],
                               [0, 1, 1],
                               [2, 1, 2]])
    wfs




.. parsed-literal::

    Magma(
    'WFS',
    'Water, Fire, Stick Magma',
    ['water', 'fire', 'stick'],
    [[0, 0, 2], [0, 1, 1], [2, 1, 2]]
    )



Here’s the isomorphism between rps and wfs:

.. code:: ipython3

    rps.isomorphic(wfs)




.. parsed-literal::

    {'r': 'water', 'p': 'stick', 's': 'fire'}



Subalgebras (Subgroups)
-----------------------

**EXAMPLE: Proper Subgroups**

.. code:: ipython3

    >>> z8 = generate_cyclic_group(8)
    
    >>> z8.proper_subgroups()




.. parsed-literal::

    [Group(
     'Z8_subgroup_0',
     'Subgroup of: Autogenerated cyclic Group of order 8',
     ['e', 'a^2', 'a^4', 'a^6'],
     [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
     ),
     Group(
     'Z8_subgroup_1',
     'Subgroup of: Autogenerated cyclic Group of order 8',
     ['e', 'a^4'],
     [[0, 1], [1, 0]]
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
    Instance ID: 140209749558288
    Description: Subgroup of: Autogenerated Group on the powerset of 3 elements, with symmetric difference operator
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {1}     {1}       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]
    
    Group: PS3_subgroup_1
    Instance ID: 140209749558672
    Description: Subgroup of: Autogenerated Group on the powerset of 3 elements, with symmetric difference operator
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {1}     {1}       2
          2  {0, 2}  {0, 2}       2
          3 {0, 1, 2} {0, 1, 2}       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]


Loading Examples
----------------

``Examples`` is a convenience class for accessing some of the example
algebras in the algebras directory. To add or subtract algebras to its
default list, see the file, ‘examples.json’, in the algebras directory.

.. code:: ipython3

    from finite_algebras import Examples
    
    ex = Examples(alg_dir)


.. parsed-literal::

    ======================================================================
                               Example Algebras
    ----------------------------------------------------------------------
      9 example algebras are available.
      Use "get_example(INDEX)" to get a specific example,
      where INDEX is the first number on each line below:
    ----------------------------------------------------------------------
    0: A4 -- Alternating group on 4 letters (AKA Tetrahedral group)
    1: D3 -- https://en.wikipedia.org/wiki/Dihedral_group_of_order_6
    2: D4 -- Dihedral group on four vertices
    3: Pinter29 -- Non-abelian group, p.29, 'A Book of Abstract Algebra' by Charles C. Pinter
    4: RPS -- Rock, Paper, Scissors Magma
    5: S3 -- Symmetric group on 3 letters
    6: S3X -- Another version of the symmetric group on 3 letters
    7: V4 -- Klein-4 group
    8: Z4 -- Cyclic group of order 4
    ======================================================================


.. code:: ipython3

    grp = ex.get_example(3)
    grp.about()


.. parsed-literal::

    
    Group: Pinter29
    Instance ID: 140210292723024
    Description: Non-abelian group, p.29, 'A Book of Abstract Algebra' by Charles C. Pinter
    Identity: I
    Associative? Yes
    Commutative? No
    Elements:
       Index   Name   Inverse  Order
          0       I       I       1
          1       A       A       2
          2       B       D       3
          3       C       C       2
          4       D       B       3
          5       K       K       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5],
     [1, 0, 3, 2, 5, 4],
     [2, 5, 4, 1, 0, 3],
     [3, 4, 5, 0, 1, 2],
     [4, 3, 0, 5, 2, 1],
     [5, 2, 1, 4, 3, 0]]


Cayley Tables
-------------

Under normal usage, there should be no need to directly create Cayley
Tables. This section, however, provides a brief glimse at the
``CayleyTable`` class.

All of the properties of a finite algebra are determined from its Cayley
Table, or in the case of this Python module, its ``CayleyTable``. That
functionality is passed through to the appropriate methods of the
various algebras. Below, is a demonstration of how **distributivity**
between two binary operations can be determined using their Cayley
Tables.

**EXAMPLE: Distributivity between Cayley Tables**

The two tables, below, were generated from the powerset of a 3 element
set, where “addition” is **symmetric difference** and “multiplication”
is **intersection**. Recall, the order of the powerset is :math:`2^n`,
where :math:`n` is the size of the set.

The element names are simply the string representations of the sets in
the powerset:

[‘{}’, ‘{0}’, ‘{1}’, ‘{2}’, ‘{0, 1}’, ‘{0, 2}’, ‘{1, 2}’, ‘{0, 1, 2}’]

And the tables, below, use the positions (indices) of the 8 elements in
the powerset:

.. code:: ipython3

    addtbl = [[0, 1, 2, 3, 4, 5, 6, 7],
              [1, 0, 4, 5, 2, 3, 7, 6],
              [2, 4, 0, 6, 1, 7, 3, 5],
              [3, 5, 6, 0, 7, 1, 2, 4],
              [4, 2, 1, 7, 0, 6, 5, 3],
              [5, 3, 7, 1, 6, 0, 4, 2],
              [6, 7, 3, 2, 5, 4, 0, 1],
              [7, 6, 5, 4, 3, 2, 1, 0]]

.. code:: ipython3

    multbl = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 1, 1, 0, 1],
              [0, 0, 2, 0, 2, 0, 2, 2],
              [0, 0, 0, 3, 0, 3, 3, 3],
              [0, 1, 2, 0, 4, 1, 2, 4],
              [0, 1, 0, 3, 1, 5, 3, 5],
              [0, 0, 2, 3, 2, 3, 6, 6],
              [0, 1, 2, 3, 4, 5, 6, 7]]

.. code:: ipython3

    from cayley_table import CayleyTable

.. code:: ipython3

    addct = CayleyTable(addtbl)
    addct.about(True)


.. parsed-literal::

      Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?
    -------------------------------------------------------------------------------------
         8        True         True            0         0          0       True


.. code:: ipython3

    mulct = CayleyTable(multbl)
    mulct.about(True)


.. parsed-literal::

      Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?
    -------------------------------------------------------------------------------------
         8        True         True            7         7          7      False


Checking Tables for Distributivity
----------------------------------

Multiplication distributes over addition.

.. code:: ipython3

    mulct.distributes_over(addct)




.. parsed-literal::

    True



But, addition does not distribute over multiplication.

.. code:: ipython3

    addct.distributes_over(mulct)




.. parsed-literal::

    False



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
-  `“Rings and
   Fields” <http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/index.html>`__,
   John O’Connor & Edmund Robertson, School of Math. & Stat., Univ. of
   St Andrews, Scotland

