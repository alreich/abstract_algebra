User Guide
==========

Class Hierarchy
---------------

:math:`\langle FiniteAlgebra \rangle \rightarrow` Magma
:math:`\rightarrow` Semigroup :math:`\rightarrow` Monoid
:math:`\rightarrow` Group :math:`\rightarrow` Ring :math:`\rightarrow`
Field

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

-  **Ring** – :math:`\langle S, +, \times \rangle`, where
   :math:`\langle S, + \rangle` is a commutative Group,
   :math:`\langle S, \times \rangle` is a Semigroup, and :math:`\times`
   distributes over :math:`+`

-  **Field** – a Ring :math:`\langle S, +, \times \rangle`, where
   :math:`\langle S\setminus{\{0\}}, \times \rangle` is a commutative
   Group.

Finite Algebra: Internal Representation
---------------------------------------

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

Algebra Constuction Examples
----------------------------

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
   corresponding to the individual values, described above.
3. Enter the **path to a JSON file** (``str``) that corresponds to the
   dictionary, described above.

``make_finite_algebra`` uses the table(s) to determine what type of
algebra it supports and returns the appropriate algebra.

In the following examples, the only algebra constructor used is
``make_finite_algebra``.

Group
~~~~~

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



Printing an algebra converts it to a string containing its class name,
algebra name, and the unique ID of the algebra instance:

.. code:: ipython3

    >>> print(z3)


.. parsed-literal::

    <Group:Z3, ID:140310561986768>


Group Properties
~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> z3.is_associative()  # Only Magmas are non-associative




.. parsed-literal::

    True



.. code:: ipython3

    >>> z3.is_commutative()




.. parsed-literal::

    True



.. code:: ipython3

    >>> z3.is_abelian()




.. parsed-literal::

    True



The ``identity`` method (property) returns the algebra’s identity
element, if it exists.

If the identity doesn’t exist, then ``None`` is returned.

.. code:: ipython3

    >>> z3.identity




.. parsed-literal::

    'e'



Internal to algebras, tables are stored as instances of the
``CayleyTable`` class:

.. code:: ipython3

    >>> z3.table




.. parsed-literal::

    CayleyTable([[0, 1, 2], [1, 2, 0], [2, 0, 1]])



.. code:: ipython3

    >>> z3.inv('a')  # Get an element's inverse, if it exists




.. parsed-literal::

    'a^2'



Binary Operation
~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> z3.op()  # zero arguments returns the identity, if it exists




.. parsed-literal::

    'e'



If only one argument is given to the binary operation, then that
argument is simply returned; unless it is not a valid element of the
algebra, in which case an exception is raised.

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



“Subtraction” in Groups
~~~~~~~~~~~~~~~~~~~~~~~

The method, ``sub``, is a convenience method for computing
“:math:`\alpha - \beta`”, that is, :math:`\alpha \circ \beta^{-1}` where
:math:`\alpha, \beta \in \langle G, \circ \rangle`.

.. code:: ipython3

    >>> a = 'a'
    >>> b = 'a^2'
    >>> print(f"For example, \"{a} - {b}\" = {a} * {z3.inv(b)} = {z3.op(a, z3.inv(b))}")


.. parsed-literal::

    For example, "a - a^2" = a * a = a^2


.. code:: ipython3

    >>> z3.sub(a, b)




.. parsed-literal::

    'a^2'



The ``about`` Method
~~~~~~~~~~~~~~~~~~~~

``about`` prints information about an algebra.

.. code:: ipython3

    >>> z3.about()


.. parsed-literal::

    
    Group: Z3
    Instance ID: 140310561986768
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


Magma
~~~~~

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
    Instance ID: 140310566620496
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
    Instance ID: 140310566620496
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

    >>> if rps.identity is None:
        print("RPS does not have an identity element")


.. parsed-literal::

    RPS does not have an identity element


Magma with Identity Element
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    Instance ID: 140310566603024
    Description: Magma with Identity
    Elements: ['e', 'a', 'b']
    Identity: e
    Associative? No
    Commutative? No
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 1, 2], [1, 0, 1], [2, 2, 1]]


Semigroup
~~~~~~~~~

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
    Instance ID: 140310566547088
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


Since the element in the 0,1 position of the table is 3, it follows
that, :math:`a \circ b = d`:

.. code:: ipython3

    >>> sg.op('a', 'b')




.. parsed-literal::

    'd'



.. code:: ipython3

    >>> if sg.identity is None:
        print("There is no identity element")


.. parsed-literal::

    There is no identity element


Monoid
~~~~~~

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
    Instance ID: 140310566617808
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


By the way, the Monoid, above, and others like it of different orders,
can be automatically generated using the function,
``generate_commutative_monoid``. It is based on integer multiplication
modulo the desired order.

.. code:: ipython3

    >>> m4.identity  # Returns the identity element




.. parsed-literal::

    'b'



.. code:: ipython3

    >>> m4.op('c', 'b')  # since 'b' is the identity element




.. parsed-literal::

    'c'



Rings
-----

Ring Based on Powerset of a Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    Instance ID: 140310561999504
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


Ring Addition and Multiplication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ring addition, ``add``, is the same as the operation, ``op``, inherited
from its superclass, Group.

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



Zero Divisors of a Ring
~~~~~~~~~~~~~~~~~~~~~~~

The Ring just created has two zero divisors:

.. code:: ipython3

    >>> rng.zero_divisors()




.. parsed-literal::

    ['{0}', '{1}']



Autogeneration of a Powerset Ring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    Instance ID: 140309738792528
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


Ring Based on 2x2 Matrices
~~~~~~~~~~~~~~~~~~~~~~~~~~

See Example 6 in this reference:
http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html

Example 6 is a Ring based on the following matrices, where arithmetic is
done modulo 2:

:math:`0 = \begin{bmatrix} 0 & 0 \\ 0 & 0 \end{bmatrix}, a = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}, b = \begin{bmatrix} 0 & 1 \\ 0 & 1 \end{bmatrix}, c = \begin{bmatrix} 0 & 0 \\ 0 & 1 \end{bmatrix}`

.. code:: ipython3

    >>> addtbl = [['0', 'a', 'b', 'c'],
                  ['a', '0', 'c', 'b'],
                  ['b', 'c', '0', 'a'],
                  ['c', 'b', 'a', '0']]
    
    >>> multbl = [['0', '0', '0', '0'],
                  ['0', '0', 'a', 'a'],
                  ['0', '0', 'b', 'b'],
                  ['0', '0', 'c', 'c']]
    
    >>> ex6 = make_finite_algebra(
        'Ex6',
        'Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html',
        ['0', 'a', 'b', 'c'],
        addtbl,
        multbl)
    
    >>> ex6




.. parsed-literal::

    Ring(
    'Ex6',
    'Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html',
    ['0', 'a', 'b', 'c'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 2, 2], [0, 0, 3, 3]]
    )



.. code:: ipython3

    >>> ex6.about(use_table_names=True)


.. parsed-literal::

    
    Ring: Ex6
    Instance ID: 140309738833872
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the beginning of this User Guide, in the *Algebra Definitions*
section, a Ring is described as being a combination of a commutative
Group, under addition, and a Semigroup, under multiplication (with
distributivity of multiplication over addition). This section shows how
those algebraic components of a Ring can be extracted.

**NOTE**: The implementation of the two extraction methods, illustrated
below, operates by calling ``make_finite_algebra`` using the relevant
portions of the Ring. That way, the appropriate algebras are returned: a
commutative Group for the additive portion, and, at a minimum, a
Semigroup for the multiplicative portion.

.. code:: ipython3

    >>> ex6




.. parsed-literal::

    Ring(
    'Ex6',
    'Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html',
    ['0', 'a', 'b', 'c'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 2, 2], [0, 0, 3, 3]]
    )



The **additive portion** of this example ring is a commutative Group, as
expected:

.. code:: ipython3

    >>> ex6_add = ex6.extract_additive_algebra()
    >>> ex6_add.about()


.. parsed-literal::

    
    Group: Ex6.Add
    Instance ID: 140309738818768
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


And, the **multiplicative portion** is a Semigroup:

.. code:: ipython3

    >>> ex6_mult = ex6.extract_multiplicative_algebra()
    >>> ex6_mult




.. parsed-literal::

    Semigroup(
    'Ex6.Mult',
    'Multiplicative-only portion of Ex6',
    ['0', 'a', 'b', 'c'],
    [[0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 2, 2], [0, 0, 3, 3]]
    )



Autogenerating a Commutative Ring
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function, ``generate_algebra_mod_n``, is based on `example 2
here <http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html>`__
and in `Wikipedia
here <https://en.wikipedia.org/wiki/Finite_field#Field_with_four_elements>`__.
The :math:`+` and :math:`\times` operations are the usual integer
addition and multiplication modulo the order (n), resp.

As long as the order (n) is not prime the function
``generate_algebra_mod_n`` will produce a Ring, but for a prime order,
it will produce a Field.

.. code:: ipython3

    >>> from finite_algebras import generate_algebra_mod_n

.. code:: ipython3

    >>> r6 = generate_algebra_mod_n(6)
    >>> r6




.. parsed-literal::

    Ring(
    'R6',
    'Autogenerated Ring of integers mod 6',
    ['a0', 'a1', 'a2', 'a3', 'a4', 'a5'],
    [[0, 1, 2, 3, 4, 5], [1, 2, 3, 4, 5, 0], [2, 3, 4, 5, 0, 1], [3, 4, 5, 0, 1, 2], [4, 5, 0, 1, 2, 3], [5, 0, 1, 2, 3, 4]],
    [[0, 0, 0, 0, 0, 0], [0, 1, 2, 3, 4, 5], [0, 2, 4, 0, 2, 4], [0, 3, 0, 3, 0, 3], [0, 4, 2, 0, 4, 2], [0, 5, 4, 3, 2, 1]]
    )



.. code:: ipython3

    >>> r6.about(use_table_names=True)


.. parsed-literal::

    
    Ring: R6
    Instance ID: 140309738853712
    Description: Autogenerated Ring of integers mod 6
    Identity: a0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      a0      a0       1
          1      a1      a5       6
          2      a2      a4       3
          3      a3      a3       2
          4      a4      a2       3
          5      a5      a1       6
    Cayley Table (showing names):
    [['a0', 'a1', 'a2', 'a3', 'a4', 'a5'],
     ['a1', 'a2', 'a3', 'a4', 'a5', 'a0'],
     ['a2', 'a3', 'a4', 'a5', 'a0', 'a1'],
     ['a3', 'a4', 'a5', 'a0', 'a1', 'a2'],
     ['a4', 'a5', 'a0', 'a1', 'a2', 'a3'],
     ['a5', 'a0', 'a1', 'a2', 'a3', 'a4']]
    Mult. Identity: a1
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing names):
    [['a0', 'a0', 'a0', 'a0', 'a0', 'a0'],
     ['a0', 'a1', 'a2', 'a3', 'a4', 'a5'],
     ['a0', 'a2', 'a4', 'a0', 'a2', 'a4'],
     ['a0', 'a3', 'a0', 'a3', 'a0', 'a3'],
     ['a0', 'a4', 'a2', 'a0', 'a4', 'a2'],
     ['a0', 'a5', 'a4', 'a3', 'a2', 'a1']]


**Extracting it’s component algebras**

In the following, we extract the component algebras of this Ring as a
commutative Group and a Monoid.

The Monoid occurs since this Ring’s multiplicative portion includes a
multiplicative identity element (‘a1’), but does not include inverses of
all elements.

.. code:: ipython3

    >>> r6add = r6.extract_additive_algebra()
    >>> r6add.about()


.. parsed-literal::

    
    Group: R6.Add
    Instance ID: 140309738856080
    Description: Additive-only portion of R6
    Identity: a0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      a0      a0       1
          1      a1      a5       6
          2      a2      a4       3
          3      a3      a3       2
          4      a4      a2       3
          5      a5      a1       6
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5],
     [1, 2, 3, 4, 5, 0],
     [2, 3, 4, 5, 0, 1],
     [3, 4, 5, 0, 1, 2],
     [4, 5, 0, 1, 2, 3],
     [5, 0, 1, 2, 3, 4]]


.. code:: ipython3

    >>> r6mult = r6.extract_multiplicative_algebra()
    >>> r6mult.about()


.. parsed-literal::

    
    Monoid: R6.Mult
    Instance ID: 140309738867408
    Description: Multiplicative-only portion of R6
    Elements: ['a0', 'a1', 'a2', 'a3', 'a4', 'a5']
    Identity: a1
    Associative? Yes
    Commutative? Yes
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0],
     [0, 1, 2, 3, 4, 5],
     [0, 2, 4, 0, 2, 4],
     [0, 3, 0, 3, 0, 3],
     [0, 4, 2, 0, 4, 2],
     [0, 5, 4, 3, 2, 1]]


Fields
------

Field with four elements
~~~~~~~~~~~~~~~~~~~~~~~~

**Reference**: See Wikipedia: `“Field with four
elements” <https://en.wikipedia.org/wiki/Finite_field#Field_with_four_elements>`__

.. code:: ipython3

    >>> elems = ['0', '1', 'a', '1+a']
    
    >>> add_table = [[ '0' ,  '1' ,  'a' , '1+a'],
                     [ '1' ,  '0' , '1+a',  'a' ],
                     [ 'a' , '1+a',  '0' ,  '1' ],
                     ['1+a',  'a' ,  '1' ,  '0' ]]
    
    >>> mult_table = [['0',  '0' ,  '0' ,  '0' ],
                      ['0',  '1' ,  'a' , '1+a'],
                      ['0',  'a' , '1+a',  '1' ],
                      ['0', '1+a',  '1' ,  'a' ]]
    
    >>> f4 = make_finite_algebra('F4',
                                 'Field with 4 elements',
                                 elems,
                                 add_table,
                                 mult_table
                                )
    >>> f4.about()


.. parsed-literal::

    
    Field: F4
    Instance ID: 140309738791824
    Description: Field with 4 elements
    Identity: 0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       0       0       1
          1       1       1       2
          2       a       a       2
          3     1+a     1+a       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    Mult. Identity: 1
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]


Addition & Multiplication in Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Field’s addition and multiplication operations are inherited from its
superclass, Ring.

.. code:: ipython3

    >>> f4.add('a', '1')




.. parsed-literal::

    '1+a'



.. code:: ipython3

    >>> f4.mult('a', 'a')




.. parsed-literal::

    '1+a'



Division in Fields
~~~~~~~~~~~~~~~~~~

The method, ``div``, is a convenience method in Fields for computing
“:math:`\alpha \div \beta, \beta \ne 0`”, that is,
:math:`\alpha \times \beta^{-1}` where
:math:`\alpha, \beta \in \langle F, +, \times \rangle`.

.. code:: ipython3

    >>> a = 'a'
    >>> b = '1+a'
    >>> print(f"For example, \"{a} / {b}\" = {a} * {f4.mult_inv(b)} = {f4.mult(a, f4.mult_inv(b))}")


.. parsed-literal::

    For example, "a / 1+a" = a * a = 1+a


.. code:: ipython3

    >>> f4.div(a, b)




.. parsed-literal::

    '1+a'



Recall the definition of a Field, given at the beginning of this User
Guide:

**Field** – a Ring :math:`\langle S, +, \times \rangle`, where
:math:`\langle S\setminus{\{0\}}, \times \rangle` is a commutative
Group.

During Field construction, the commutative Group, mentioned in the
definition, is also constructed and stored inside the Field instance. It
is used to obtain multiplicative inverses and to define a *division*
method, ``div``.

The ``div`` method, for example, can be used to construct the “Division”
table shown in the Wikipedia entry, `“Field with four
elements” <https://en.wikipedia.org/wiki/Finite_field#Field_with_four_elements>`__:

.. code:: ipython3

    >>> div_table = [[f4.div(x, y) for y in f4.elements] for x in f4.elements]
    >>> div_table




.. parsed-literal::

    [[None, '0', '0', '0'],
     [None, '1', '1+a', 'a'],
     [None, 'a', '1', '1+a'],
     [None, '1+a', 'a', '1']]



Autogenerated Prime Field
~~~~~~~~~~~~~~~~~~~~~~~~~

The example here uses the function, ``generate_algebra_mod_n``,
described above. As noted above, if the order, n, is prime, then it will
produce a Field.

.. code:: ipython3

    >>> from finite_algebras import generate_algebra_mod_n
    
    >>> f7 = generate_algebra_mod_n(7)
    >>> f7.about()


.. parsed-literal::

    
    Field: F7
    Instance ID: 140309738724112
    Description: Autogenerated Field of integers mod 7
    Identity: a0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      a0      a0       1
          1      a1      a6       7
          2      a2      a5       7
          3      a3      a4       7
          4      a4      a3       7
          5      a5      a2       7
          6      a6      a1       7
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5, 6],
     [1, 2, 3, 4, 5, 6, 0],
     [2, 3, 4, 5, 6, 0, 1],
     [3, 4, 5, 6, 0, 1, 2],
     [4, 5, 6, 0, 1, 2, 3],
     [5, 6, 0, 1, 2, 3, 4],
     [6, 0, 1, 2, 3, 4, 5]]
    Mult. Identity: a1
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0, 0],
     [0, 1, 2, 3, 4, 5, 6],
     [0, 2, 4, 6, 1, 3, 5],
     [0, 3, 6, 2, 5, 1, 4],
     [0, 4, 1, 5, 2, 6, 3],
     [0, 5, 3, 1, 6, 4, 2],
     [0, 6, 5, 4, 3, 2, 1]]


Serialization
-------------

Algebras can be converted to and from JSON strings/files and Python
dictionaries.

Instantiate Algebra from JSON File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First setup some path variables:

-  one that points to the abstract_algebra directory
-  and the other points to a subdirectory containing algebra definitions
   in JSON format

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



Convert Algebra to Python Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The examples, below, show a Magma, Group, & Field, being converted into
dictionaries.

.. code:: ipython3

    >>> rps.to_dict()




.. parsed-literal::

    {'name': 'RPS',
     'description': 'Rock, Paper, Scissors Magma',
     'elements': ['r', 'p', 's'],
     'table': [[0, 1, 0], [1, 1, 2], [0, 2, 2]]}



The **type** of algebra (e.g., Magma) can be included in the dictionary
for readability, however, the *type* field is ignored when
``make_finite_algebra`` reads a dictionary or JSON file.

.. code:: ipython3

    >>> rps_dict = rps.to_dict(include_classname=True)
    
    >>> rps_dict




.. parsed-literal::

    {'name': 'RPS',
     'description': 'Rock, Paper, Scissors Magma',
     'elements': ['r', 'p', 's'],
     'table': [[0, 1, 0], [1, 1, 2], [0, 2, 2]],
     'type': 'Magma'}



.. code:: ipython3

    >>> v4_dict = v4.to_dict()
    
    >>> v4_dict




.. parsed-literal::

    {'name': 'V4',
     'description': 'Klein-4 group',
     'elements': ['e', 'h', 'v', 'r'],
     'table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}



.. code:: ipython3

    >>> f4_dict = f4.to_dict()
    
    >>> f4_dict




.. parsed-literal::

    {'name': 'F4',
     'description': 'Field with 4 elements',
     'elements': ['0', '1', 'a', '1+a'],
     'table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
     'table2': [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]}



Instantiate Algebra from Python Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> rps_from_dict = make_finite_algebra(rps_dict)
    
    >>> rps_from_dict




.. parsed-literal::

    Magma(
    'RPS',
    'Rock, Paper, Scissors Magma',
    ['r', 'p', 's'],
    [[0, 1, 0], [1, 1, 2], [0, 2, 2]]
    )



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



.. code:: ipython3

    >>> f4_from_dict = make_finite_algebra(f4_dict)
    
    >>> f4_from_dict




.. parsed-literal::

    Field(
    'F4',
    'Field with 4 elements',
    ['0', '1', 'a', '1+a'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    )



Convert Algebra to JSON String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> v4_json_string = v4.dumps()
    
    >>> v4_json_string




.. parsed-literal::

    '{"name": "V4", "description": "Klein-4 group", "elements": ["e", "h", "v", "r"], "table": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]}'



**WARNING**: Although an algebra can be constructed by loading its
definition from a JSON file, it cannot be constructed directly from a
JSON string, because ``make_finite_algebra`` interprets a single string
input as a JSON file name. To load an algebra from a JSON string, first
convert the string to a Python dictionary, then input that to
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

There are several functions for autogenerating finite algebras of
specified size:

**Groups**

-  ``generate_cyclic_group(n)``: :math:`Z_n`, where
   :math:`a \circ b \equiv a+b` mod :math:`n`, where
   :math:`a,b \in \{0,1,...,n-1\}`
-  ``generate_symmetric_group(n)``: :math:`S_n`, where :math:`\circ` is
   composition of permutations of :math:`(0, 1, ..., n-1)`
-  ``generate_powerset_group(n)``:
   :math:`A \circ B \equiv A \bigtriangleup B`, where
   :math:`A,B \in P(\{0, 1, ..., n-1\})`; order is :math:`2^n`

**Monoid**

-  ``generate_commutative_monoid(n)``: :math:`a \circ b \equiv ab` mod
   :math:`n`, where :math:`a,b \in \{0,1,...,n-1\}`

**Rings & Fields**

-  ``generate_powerset_ring``: :math:`A+B \equiv A \bigtriangleup B` and
   :math:`A \times B \equiv A \cap B`, where
   :math:`A,B \in P(\{0, 1, ..., n-1\})`
-  ``generate_algebra_mod_n``: Combination of generate_cyclic_group
   (:math:`+`) and generate_commutative_monoid (:math:`\times`)

   -  If n is prime, then this will be a Field, otherwise it will be a
      Ring

Autogenerated Cyclic Group
~~~~~~~~~~~~~~~~~~~~~~~~~~

A cyclic group of any desired order can be generated as follows:

.. code:: ipython3

    >>> from finite_algebras import generate_cyclic_group
    
    >>> z2 = generate_cyclic_group(2)
    
    >>> z2.about()


.. parsed-literal::

    
    Group: Z2
    Instance ID: 140309738725328
    Description: Autogenerated cyclic Group of order 2
    Identity: e
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       a       a       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]


Autogenerated Symmetric Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    Instance ID: 140310566723024
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


Autogenerated Powerset Group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function, ``generate_powerset_group``, will generate a group on the
powerset of {0, 1, 2, …, n-1} with **symmetric difference** as the
group’s binary operation. This group is useful because it can be used to
form a ring with set intersection as the second operator.

This means that the order of the autogenerated powerset group will be
:math:`2^n`, so the same WARNING as above applies with regard to large
values of n.

.. code:: ipython3

    >>> from finite_algebras import generate_powerset_group
    
    >>> ps3 = generate_powerset_group(3)
    
    >>> ps3.about()


.. parsed-literal::

    
    Group: PS3
    Instance ID: 140310566743120
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


Autogenerated Monoid
~~~~~~~~~~~~~~~~~~~~

The function, ``generate_commutative_monoid``, is based on integer
multiplication modulo the desired order.

.. code:: ipython3

    >>> from finite_algebras import generate_commutative_monoid
    
    >>> m7 = generate_commutative_monoid(7)
    
    >>> m7.about()


.. parsed-literal::

    
    Monoid: M7
    Instance ID: 140310566679824
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

Direct Product of Multiple Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> z2_cubed = z2 * z2 * z2
    
    >>> z2_cubed.about()


.. parsed-literal::

    
    Group: Z2_x_Z2_x_Z2
    Instance ID: 140309738854736
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


Direct Product of Monoids
~~~~~~~~~~~~~~~~~~~~~~~~~

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
    Instance ID: 140310566715792
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

Group Isomorphism
~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> z2_sqr = z2 * z2
    
    >>> v4.isomorphic(z2_sqr)




.. parsed-literal::

    {'e': 'e:e', 'h': 'e:a', 'v': 'a:e', 'r': 'a:a'}



If two groups are not isomorphic, then ``False`` is returned.

.. code:: ipython3

    >>> z4 = generate_cyclic_group(4)
    
    >>> z4.isomorphic(z2_sqr)




.. parsed-literal::

    False



Magma Isomorphism
~~~~~~~~~~~~~~~~~

**Water, Fire, Stick Magma**

A made-up Magma, similar to Rock, Paper, Scissors:

-  Water quenches Fire
-  Fire burns Stick
-  Stick floats on Water

.. code:: ipython3

    >>> wfs = make_finite_algebra('WFS',
                                  'Water, Fire, Stick Magma',
                                  ['water', 'fire', 'stick'],
                                  [[0, 0, 2],
                                   [0, 1, 1],
                                   [2, 1, 2]])
    >>> wfs




.. parsed-literal::

    Magma(
    'WFS',
    'Water, Fire, Stick Magma',
    ['water', 'fire', 'stick'],
    [[0, 0, 2], [0, 1, 1], [2, 1, 2]]
    )



Here’s the isomorphism between rps and wfs:

.. code:: ipython3

    >>> rps.isomorphic(wfs)




.. parsed-literal::

    {'r': 'water', 'p': 'stick', 's': 'fire'}



Subalgebras (Subgroups)
-----------------------

A Group can contain subgroups, submonoids, subsemigroups, or submagmas.
In general, all of these are referred to here as *subalgebras*.

The method, ``proper_subalgebras``, extracts all possible subalgebras
that exist within an algebra, regardless of whether they are isomorphic
to each other or not, or even of the same algebraic class as the parent
algebra.

Proper Subgroups
~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> z8 = generate_cyclic_group(8)
    
    >>> z8_proper_subs = z8.proper_subalgebras(True)
    >>> z8_proper_subs




.. parsed-literal::

    [Group(
     'Z8_subalgebra_0',
     'Subalgebra of: Autogenerated cyclic Group of order 8',
     ['e', 'a^4'],
     [[0, 1], [1, 0]]
     ),
     Group(
     'Z8_subalgebra_1',
     'Subalgebra of: Autogenerated cyclic Group of order 8',
     ['e', 'a^2', 'a^4', 'a^6'],
     [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
     )]



Normal Subgroups
~~~~~~~~~~~~~~~~

Both of the subgroups of Z8, derived above, are **normal**:

.. code:: ipython3

    >>> [z8.is_normal(g) for g in z8_proper_subs]




.. parsed-literal::

    [True, True]



Proper Subalgebras up to Isomorphism
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example, below, uses the autogenerated powerset group, **ps3**, that
was created earlier.

.. code:: ipython3

    >>> from finite_algebras import partition_into_isomorphic_lists
    
    >>> ps3_proper_subalgebras = ps3.proper_subalgebras(True)
    
    >>> print(f"{ps3.name} has {len(ps3_proper_subalgebras)} proper subalgebras.")
    
    >>> unique_subalgebras = partition_into_isomorphic_lists(ps3_proper_subalgebras)
    
    >>> print(f"But, up to isomorphisms, only {len(unique_subalgebras)} are proper and unique.")


.. parsed-literal::

    PS3 has 14 proper subalgebras.
    But, up to isomorphisms, only 2 are proper and unique.


The function, ``partition_into_isomorphic_lists``, does just that; it
partitions a list of algebras (subgroups in this case) into a list of
lists, where each sublist contains subalgebras that are all isomophic to
each other. In this example, all of the subalgebras are subgroups.

So, in the following, the ``about`` method is called on the first group
of each sublist:

.. code:: ipython3

    >>> _ = [subalg[0].about() for subalg in unique_subalgebras]


.. parsed-literal::

    
    Group: PS3_subalgebra_0
    Instance ID: 140310566566224
    Description: Subalgebra of: Autogenerated Group on the powerset of 3 elements, with symmetric difference operator
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1  {0, 2}  {0, 2}       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]
    
    Group: PS3_subalgebra_2
    Instance ID: 140309738677712
    Description: Subalgebra of: Autogenerated Group on the powerset of 3 elements, with symmetric difference operator
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {0}     {0}       2
          2     {2}     {2}       2
          3  {0, 2}  {0, 2}       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]


Subalgebras of Semigroups, Etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recall the Semigroup example from above:

.. code:: ipython3

    >>> sg.about()


.. parsed-literal::

    
    Semigroup: Example 1.4.1
    Instance ID: 140310566547088
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


It contains 10 proper subalgebras, including 7 Semigroups and 3 Groups,
as shown below:

.. code:: ipython3

    >>> sg_subs = sg.proper_subalgebras(False)
    >>> _ = [print(f"{sub}\n   Order: {sub.order}\n   Elements: {sub.elements}")
             for sub in sg_subs]


.. parsed-literal::

    <Semigroup:Example 1.4.1_subalgebra_0, ID:140310566601488>
       Order: 2
       Elements: ['a', 'e']
    <Semigroup:Example 1.4.1_subalgebra_1, ID:140310566604432>
       Order: 4
       Elements: ['a', 'b', 'd', 'e']
    <Semigroup:Example 1.4.1_subalgebra_2, ID:140309738854544>
       Order: 4
       Elements: ['a', 'c', 'd', 'f']
    <Semigroup:Example 1.4.1_subalgebra_3, ID:140309738854288>
       Order: 2
       Elements: ['c', 'e']
    <Group:Example 1.4.1_subalgebra_4, ID:140310566492048>
       Order: 2
       Elements: ['a', 'd']
    <Semigroup:Example 1.4.1_subalgebra_5, ID:140309738794576>
       Order: 4
       Elements: ['b', 'c', 'e', 'f']
    <Group:Example 1.4.1_subalgebra_6, ID:140309738791312>
       Order: 2
       Elements: ['c', 'f']
    <Semigroup:Example 1.4.1_subalgebra_7, ID:140309738793936>
       Order: 3
       Elements: ['a', 'c', 'e']
    <Semigroup:Example 1.4.1_subalgebra_8, ID:140310566723408>
       Order: 2
       Elements: ['a', 'c']
    <Group:Example 1.4.1_subalgebra_9, ID:140310566723536>
       Order: 2
       Elements: ['b', 'e']


The list subalgebras of **sg** can be partitioned into 4 sublists of
subalgebras, where within each sublist, the subalgebras are isomorphic
each other. The ``about`` info for the first subalgebra of each sublist
is below:

.. code:: ipython3

    >>> parts = partition_into_isomorphic_lists(sg_subs)
    
    >>> for part in parts:
    >>>     part[0].about()
    >>>     print("\n" + "="*60)


.. parsed-literal::

    
    Semigroup: Example 1.4.1_subalgebra_0
    Instance ID: 140310566601488
    Description: Subalgebra of: See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    Elements: ['a', 'e']
    Identity: None
    Associative? Yes
    Commutative? No
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 0], [1, 1]]
    
    ============================================================
    
    Semigroup: Example 1.4.1_subalgebra_1
    Instance ID: 140310566604432
    Description: Subalgebra of: See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    Elements: ['a', 'b', 'd', 'e']
    Identity: None
    Associative? Yes
    Commutative? No
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 2, 2, 0], [1, 3, 3, 1], [2, 0, 0, 2], [3, 1, 1, 3]]
    
    ============================================================
    
    Group: Example 1.4.1_subalgebra_4
    Instance ID: 140310566492048
    Description: Subalgebra of: See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    Identity: a
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       a       a       1
          1       d       d       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]
    
    ============================================================
    
    Semigroup: Example 1.4.1_subalgebra_7
    Instance ID: 140309738793936
    Description: Subalgebra of: See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    Elements: ['a', 'c', 'e']
    Identity: None
    Associative? Yes
    Commutative? No
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 0, 0], [1, 1, 1], [2, 2, 2]]
    
    ============================================================


Built-In Examples
-----------------

``Examples`` is a convenience class for accessing some of the example
algebras in the algebras directory. To add or subtract algebras to its
default list, see the file, ‘examples.json’, in the algebras directory.

.. code:: ipython3

    >>> from finite_algebras import Examples
    
    >>> ex = Examples(alg_dir)  # Requires path to directory containing algebras' JSON files


.. parsed-literal::

    ======================================================================
                               Example Algebras
    ----------------------------------------------------------------------
      13 example algebras are available.
      Use "get_example(INDEX)" to retrieve a specific example,
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
    9: F4 -- Field with 4 elements (from Wikipedia)
    10: mag_id -- Magma with Identity
    11: Example 1.4.1 -- See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    12: Ex6 -- Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html
    ======================================================================


.. code:: ipython3

    >>> grp = ex.get_example(3)
    >>> grp.about()


.. parsed-literal::

    
    Group: Pinter29
    Instance ID: 140310566740368
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

All of the properties of a finite algebra can be determined from its
Cayley Table, or in the case of this Python module, its ``CayleyTable``.
That functionality is passed through to the appropriate methods of the
various algebras. Below, is a demonstration of how **distributivity**
between two binary operations can be determined using their Cayley
Tables.

The two tables, below, were generated from the powerset of a 3 element
set, where “addition” is **symmetric difference** and “multiplication”
is **intersection**. Recall, the order of the powerset is :math:`2^n`,
where :math:`n` is the size of the set.

The element names are simply the string representations of the sets in
the powerset:

[‘{}’, ‘{0}’, ‘{1}’, ‘{2}’, ‘{0, 1}’, ‘{0, 2}’, ‘{1, 2}’, ‘{0, 1, 2}’]

And the tables, below, contain the positions (indices) of the 8 elements
in the powerset:

.. code:: ipython3

    >>> addtbl = [[0, 1, 2, 3, 4, 5, 6, 7],
                  [1, 0, 4, 5, 2, 3, 7, 6],
                  [2, 4, 0, 6, 1, 7, 3, 5],
                  [3, 5, 6, 0, 7, 1, 2, 4],
                  [4, 2, 1, 7, 0, 6, 5, 3],
                  [5, 3, 7, 1, 6, 0, 4, 2],
                  [6, 7, 3, 2, 5, 4, 0, 1],
                  [7, 6, 5, 4, 3, 2, 1, 0]]

.. code:: ipython3

    >>> multbl = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 1, 1, 0, 1],
                  [0, 0, 2, 0, 2, 0, 2, 2],
                  [0, 0, 0, 3, 0, 3, 3, 3],
                  [0, 1, 2, 0, 4, 1, 2, 4],
                  [0, 1, 0, 3, 1, 5, 3, 5],
                  [0, 0, 2, 3, 2, 3, 6, 6],
                  [0, 1, 2, 3, 4, 5, 6, 7]]

.. code:: ipython3

    >>> from cayley_table import CayleyTable

.. code:: ipython3

    >>> addct = CayleyTable(addtbl)
    >>> addct.about(True)


.. parsed-literal::

      Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?
    -------------------------------------------------------------------------------------
         8        True         True            0         0          0       True


.. code:: ipython3

    >>> mulct = CayleyTable(multbl)
    >>> mulct.about(True)


.. parsed-literal::

      Order  Associative?  Commutative?  Left Id?  Right Id?  Identity?  Inverses?
    -------------------------------------------------------------------------------------
         8        True         True            7         7          7      False


Checking Tables for Distributivity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Multiplication distributes over addition.

.. code:: ipython3

    >>> mulct.distributes_over(addct)




.. parsed-literal::

    True



But, addition does not distribute over multiplication.

.. code:: ipython3

    >>> addct.distributes_over(mulct)




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
