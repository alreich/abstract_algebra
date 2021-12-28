Rings and Fields
================

Rings and Fields have a single set of elements, but have two binary
operations on those elements. This section provides examples of Ring and
Field construction. See the section, “Definitions”, for definitions of
these algebraic structures

Internal Representation of Rings & Fields
-----------------------------------------

Internally, a ``FiniteAlgebra`` can take several different forms. For
algebras that have only one set of elements and two binary operations,
such as Rings and Fields, the internal representation is as shown below.
The first four components are the same as for Groups, Monoids, etc. The
only difference is the addition of **table2**. It defines Ring
multiplication.

-  **name**: (``str``) A short name for the algebra;
-  **description**: (``str``) Any additional, useful information about
   the algebra;
-  **elements**: (``list`` of ``str``) Names of the algebras’s elements.
-  **table**: (``list`` of ``list`` of ``int``) The algebra’s
   multiplication table, where each list in the list represents a row of
   the table, and each integer represents the position of an element in
   ‘element_names’. Optionally, element names (``str``) may be used in
   the table, rather than integers.
-  **table2**: Similar to *table*, above. Required when defining a Ring
   or Field.

Ring
----

**Ring** - :math:`\langle S, +, \times \rangle`, where
:math:`\langle S, + \rangle` is a commutative Group,
:math:`\langle S, \times \rangle` is a Semigroup, and :math:`\times`
distributes over :math:`+`

Ring Based on Powerset of a Set
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this ring, *“addition”* is symmetric difference,
:math:`\bigtriangleup`, and *“multiplication”* is intersection,
:math:`\cap`.

.. code:: ipython3

    >>> from finite_algebras import make_finite_algebra
    
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

    
    ** Ring **
    Name: Powerset Ring 2
    Instance ID: 140492681947344
    Description: Ring on powerset of {0, 1}
    Order: 4
    Identity: {}
    Commutative? Yes
    Cyclic?: No
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
    Zero Divisors: ['{0}', '{1}']
    Multiplicative Cayley Table (showing names):
    [['{}', '{}', '{}', '{}'],
     ['{}', '{0}', '{}', '{0}'],
     ['{}', '{}', '{1}', '{1}'],
     ['{}', '{0}', '{1}', '{0, 1}']]


Additive & Multiplicative Identity Elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A Ring’s additive and multiplicative identity elements can be obtained
as follows:

.. code:: ipython3

    rng.add_identity




.. parsed-literal::

    '{}'



.. code:: ipython3

    rng.mult_identity




.. parsed-literal::

    '{0, 1}'



Or, perhaps more suggestively as follows:

.. code:: ipython3

    rng.zero




.. parsed-literal::

    '{}'



.. code:: ipython3

    rng.one




.. parsed-literal::

    '{0, 1}'



Ring Addition and Multiplication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ring addition, ``add``, is the same as the operation, ``op``, inherited
from its superclass, Group.

Recall that, in this module, all elements are represented by strings
(names). So, even though the actual elements of a powerset Ring are sets
(e.g., {0, 1}), those elements are represented as strings (e.g., “{0,
1}”). The two examples below show “addition” and “multiplication”
operations in set notation, along with the same operations as performed
by the Ring’s ``add`` and ``mult`` operators.

Ring “addition” using set notation:
:math:`\{1\} \bigtriangleup \{0,1\} = \{0\}`

.. code:: ipython3

    >>> rng.add("{1}", "{0, 1}")




.. parsed-literal::

    '{0}'



Ring “multiplication” using set notation:
:math:`\{1\} \cap \{0,1\} = \{1\}`

.. code:: ipython3

    >>> rng.mult("{1}", "{0, 1}")




.. parsed-literal::

    '{1}'



Zero Divisors of a Ring
~~~~~~~~~~~~~~~~~~~~~~~

**This section needs more work**

Suppose :math:`\alpha \ne 0 \in S`, where :math:`0` is the additive
identity element of the Ring, :math:`\langle S, +, \times \rangle`.

Then, :math:`\alpha` is a **left zero divisor**, if
:math:`\exists \beta \in S, \beta \ne 0` such that
:math:`\alpha \times \beta = 0`.

Similarly, :math:`\alpha` is a **right zero divisor**, if
:math:`\exists \gamma \in S, \gamma \ne 0` such that
:math:`\gamma \times \alpha = 0`.

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

    
    ** Ring **
    Name: PSRing3
    Instance ID: 140492419016016
    Description: Autogenerated Ring on powerset of {0, 1, 2} w/ symm. diff. (add) & intersection (mult)
    Order: 8
    Identity: {}
    Commutative? Yes
    Cyclic?: No
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
    Zero Divisors: ['{0}', '{1}', '{2}', '{0, 1}', '{0, 2}', '{1, 2}']
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

    
    ** Ring **
    Name: Ex6
    Instance ID: 140492419058320
    Description: Example 6: http://www-groups.mcs.st-andrews.ac.uk/~john/MT4517/Lectures/L3.html
    Order: 4
    Identity: 0
    Commutative? Yes
    Cyclic?: No
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
    Zero Divisors: ['a', 'b', 'c']
    Multiplicative Cayley Table (showing names):
    [['0', '0', '0', '0'],
     ['0', '0', 'a', 'a'],
     ['0', '0', 'b', 'b'],
     ['0', '0', 'c', 'c']]


Extracting a Ring’s Additive & Multiplicative “Subalgebras”
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the Definitions section, a Ring is described as being a combination
of a commutative Group, under addition, and a Semigroup, under
multiplication (with distributivity of multiplication over addition).
This section shows how those algebraic components of a Ring can be
extracted.

The implementation of the two extraction methods, illustrated below,
operates by calling ``make_finite_algebra`` using the relevant portions
of the Ring. That way, the appropriate algebras are returned: a
commutative Group for the additive portion, and, at a minimum, a
Semigroup for the multiplicative portion.

The example to follow uses the Ring, ``ex6``, created above.

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

    
    ** Group **
    Name: Ex6.Add
    Instance ID: 140492419056720
    Description: Additive-only portion of Ex6
    Order: 4
    Identity: 0
    Commutative? Yes
    Cyclic?: No
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
and `Wikipedia
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

    
    ** Ring **
    Name: R6
    Instance ID: 140492419071120
    Description: Autogenerated Ring of integers mod 6
    Order: 6
    Identity: a0
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a1', 'a5']
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
    Zero Divisors: ['a2', 'a3', 'a4']
    Multiplicative Cayley Table (showing names):
    [['a0', 'a0', 'a0', 'a0', 'a0', 'a0'],
     ['a0', 'a1', 'a2', 'a3', 'a4', 'a5'],
     ['a0', 'a2', 'a4', 'a0', 'a2', 'a4'],
     ['a0', 'a3', 'a0', 'a3', 'a0', 'a3'],
     ['a0', 'a4', 'a2', 'a0', 'a4', 'a2'],
     ['a0', 'a5', 'a4', 'a3', 'a2', 'a1']]


Notice that there is a multiplicative identity in the Ring, above. So,
if we extract the multiplicative portion of that Ring we should expect
to obtain a Monoid, instead of a Semigroup, and we do, as shown below.

.. code:: ipython3

    >>> r6mult = r6.extract_multiplicative_algebra()
    >>> r6mult.about()


.. parsed-literal::

    
    ** Monoid **
    Name: R6.Mult
    Instance ID: 140492419019728
    Description: Multiplicative-only portion of R6
    Order: 6
    Identity: a1
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements: ['a0', 'a1', 'a2', 'a3', 'a4', 'a5']
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0],
     [0, 1, 2, 3, 4, 5],
     [0, 2, 4, 0, 2, 4],
     [0, 3, 0, 3, 0, 3],
     [0, 4, 2, 0, 4, 2],
     [0, 5, 4, 3, 2, 1]]


Field
-----

**Field** – a Ring :math:`\langle S, +, \times \rangle`, where
:math:`\langle S\setminus{\{0\}}, \times \rangle` is a commutative
Group.

:math:`S\setminus{\{0\}}` is the set :math:`S` with the additive
identity element removed.

Example: A field with four elements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Reference**: Wikipedia: `“Field with four
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

    
    ** Field **
    Name: F4
    Instance ID: 140492419166480
    Description: Field with 4 elements
    Order: 4
    Identity: 0
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['1+a', 'a']
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
    Zero Divisors: None
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
    >>> print(f"For example, \"{a} / {b}\" = {a} * inv({b}) = {a} * {f4.mult_inv(b)} = {f4.mult(a, f4.mult_inv(b))}")


.. parsed-literal::

    For example, "a / 1+a" = a * inv(1+a) = a * a = 1+a


.. code:: ipython3

    >>> f4.div(a, b)




.. parsed-literal::

    '1+a'



Recall the definition of a Field, given in the Definition section:

**Field** – a Ring :math:`\langle S, +, \times \rangle`, where
:math:`\langle S\setminus{\{0\}}, \times \rangle` is a commutative
Group.

During Field construction, the commutative Group, mentioned in the
definition, is also constructed and stored inside the Field instance. It
is used to obtain multiplicative inverses and to define a *division*
method, ``div``.

The ``div`` method, for example, can be used to construct the “Division
x/y” table shown in the Wikipedia entry, `“Field with four
elements” <https://en.wikipedia.org/wiki/Finite_field#Field_with_four_elements>`__:

.. code:: ipython3

    >>> div_table = [[f4.div(x, y) for y in f4.elements if y != f4.zero] for x in f4.elements]
    
    >>> for row in div_table:
    >>>     print(row)


.. parsed-literal::

    ['0', '0', '0']
    ['1', '1+a', 'a']
    ['a', '1', '1+a']
    ['1+a', 'a', '1']


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

    
    ** Field **
    Name: F7
    Instance ID: 140492419124752
    Description: Autogenerated Field of integers mod 7
    Order: 7
    Identity: a0
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
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
    Zero Divisors: None
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

Rings and Fields can be converted to and from JSON strings/files and
Python dictionaries.

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

Here’s the path to the JSON file for the “field with four elements”, and
a listing of the file itself.

.. code:: ipython3

    >>> f4_json = os.path.join(alg_dir, "field_with_four_elements.json")
    
    >>> !cat {f4_json}


.. parsed-literal::

    {"name": "F4",
     "description": "Field with 4 elements (from Wikipedia)",
     "elements": ["0", "1", "a", "1+a"],
     "table": [[0, 1, 2, 3],
               [1, 0, 3, 2],
               [2, 3, 0, 1],
               [3, 2, 1, 0]],
     "table2": [[0, 0, 0, 0],
                [0, 1, 2, 3],
                [0, 2, 3, 1],
                [0, 3, 1, 2]]
    }


And here’s the field created from the JSON file.

.. code:: ipython3

    >>> f4 = make_finite_algebra(f4_json)
    
    >>> f4




.. parsed-literal::

    Field(
    'F4',
    'Field with 4 elements (from Wikipedia)',
    ['0', '1', 'a', '1+a'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    )



Convert Algebra to Python Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The example, below, shows a Field, being converted into dictionary.

.. code:: ipython3

    >>> f4_dict = f4.to_dict()
    
    >>> f4_dict




.. parsed-literal::

    {'name': 'F4',
     'description': 'Field with 4 elements (from Wikipedia)',
     'elements': ['0', '1', 'a', '1+a'],
     'table': [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
     'table2': [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]}



Instantiate Algebra from Python Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> f4_from_dict = make_finite_algebra(f4_dict)
    
    >>> f4_from_dict




.. parsed-literal::

    Field(
    'F4',
    'Field with 4 elements (from Wikipedia)',
    ['0', '1', 'a', '1+a'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    )



Convert Algebra to JSON String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> f4_json_string = f4.dumps()
    
    >>> f4_json_string




.. parsed-literal::

    '{"name": "F4", "description": "Field with 4 elements (from Wikipedia)", "elements": ["0", "1", "a", "1+a"], "table": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]], "table2": [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]}'



**WARNING**: Although an algebra can be constructed by loading its
definition from a JSON file, it cannot be constructed directly from a
JSON string, because ``make_finite_algebra`` interprets a single string
input as a JSON file name. To load an algebra from a JSON string, first
convert the string to a Python dictionary, then input that to
``make_finite_algebra``, as shown below:

.. code:: ipython3

    >>> import json
    
    >>> make_finite_algebra(json.loads(f4_json_string))




.. parsed-literal::

    Field(
    'F4',
    'Field with 4 elements (from Wikipedia)',
    ['0', '1', 'a', '1+a'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    )



Autogeneration of Rings & Fields
--------------------------------

There are several functions for autogenerating finite Rings and Fields
of specified size:

-  ``generate_powerset_ring``: :math:`A+B \equiv A \bigtriangleup B` and
   :math:`A \times B \equiv A \cap B`, where
   :math:`A,B \in P(\{0, 1, ..., n-1\})`
-  ``generate_algebra_mod_n``: Combination of generate_cyclic_group
   (:math:`+`) and generate_commutative_monoid (:math:`\times`)

   -  If n is prime, then this will be a Field, otherwise it will be a
      Ring

Direct Products
---------------

The **direct product** of two or more algebras can be generated using
Python’s multiplication operator, ``*``:

Direct Product of Multiple Fields
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The direct product of a finite Field with itself will produce a finite
abelian Group.

.. code:: ipython3

    >>> f4_sqr = f4 * f4
    
    >>> f4_sqr.about(max_size=16)


.. parsed-literal::

    
    ** Ring **
    Name: F4_x_F4
    Instance ID: 140492419042256
    Description: Direct product of F4 & F4
    Order: 16
    Identity: 0:0
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0     0:0     0:0       1
          1     0:1     0:1       2
          2     0:a     0:a       2
          3   0:1+a   0:1+a       2
          4     1:0     1:0       2
          5     1:1     1:1       2
          6     1:a     1:a       2
          7   1:1+a   1:1+a       2
          8     a:0     a:0       2
          9     a:1     a:1       2
         10     a:a     a:a       2
         11   a:1+a   a:1+a       2
         12   1+a:0   1+a:0       2
         13   1+a:1   1+a:1       2
         14   1+a:a   1+a:a       2
         15 1+a:1+a 1+a:1+a       2
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
    Mult. Identity: 1:1
    Mult. Commutative? Yes
    Zero Divisors: ['0:1', '0:a', '0:1+a', '1:0', 'a:0', '1+a:0']
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],
     [0, 2, 3, 1, 0, 2, 3, 1, 0, 2, 3, 1, 0, 2, 3, 1],
     [0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2, 0, 3, 1, 2],
     [0, 0, 0, 0, 4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12],
     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
     [0, 2, 3, 1, 4, 6, 7, 5, 8, 10, 11, 9, 12, 14, 15, 13],
     [0, 3, 1, 2, 4, 7, 5, 6, 8, 11, 9, 10, 12, 15, 13, 14],
     [0, 0, 0, 0, 8, 8, 8, 8, 12, 12, 12, 12, 4, 4, 4, 4],
     [0, 1, 2, 3, 8, 9, 10, 11, 12, 13, 14, 15, 4, 5, 6, 7],
     [0, 2, 3, 1, 8, 10, 11, 9, 12, 14, 15, 13, 4, 6, 7, 5],
     [0, 3, 1, 2, 8, 11, 9, 10, 12, 15, 13, 14, 4, 7, 5, 6],
     [0, 0, 0, 0, 12, 12, 12, 12, 4, 4, 4, 4, 8, 8, 8, 8],
     [0, 1, 2, 3, 12, 13, 14, 15, 4, 5, 6, 7, 8, 9, 10, 11],
     [0, 2, 3, 1, 12, 14, 15, 13, 4, 6, 7, 5, 8, 10, 11, 9],
     [0, 3, 1, 2, 12, 15, 13, 14, 4, 7, 5, 6, 8, 11, 9, 10]]


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


