Vector Spaces & Modules
=======================

Vector Spaces and Modules are defined using Groups, Rings, and Fields.

Vector Space
------------

A **Vector Space**,
:math:`\mathscr{V} = \langle \mathscr{G}, \mathscr{F}, \circ \rangle`,
consists of the following:

-  an **abelian Group**, :math:`\mathscr{G} = \langle V, \oplus \rangle`
   (i.e., the *“vectors”*)
-  a **field**, :math:`\mathscr{F} = \langle S, +, \times \rangle`
   (i.e., the *“scalars”*)
-  and a **binary operator**, :math:`\circ : S \times V \to V`

where the following conditions hold:

1. Scaled Vectors: For all :math:`s \in S` and
   :math:`v \in V \Rightarrow s \circ v \in V`
2. Scaling by One: If :math:`\underline{1} \in S` is the multiplicative
   identity element of :math:`\mathscr{F}`, then
   :math:`\underline{1} \circ v = v`
3. Distributivity of Scalars Over Vector Addition:
   :math:`s \circ (v_1 \oplus v_2) = (s \circ v_1) \oplus (s \circ v_2)`
4. Distributivity of Vectors Over Scalar Addition:
   :math:`(s_1 + s_2) \circ v = (s_1 \circ v) \oplus (s_2 \circ v)`
5. Associativity:
   :math:`s_1 \circ (s_2 \circ v) = (s_1 \times s_2) \circ v`

A **Module**,
:math:`\mathscr{M} = \langle \mathscr{G}, \mathscr{R}, \circ \rangle`,
has the same conditions as a Vector Space, except that the Field is
replaced by a **Ring**,
:math:`\mathscr{R} = \langle S, +, \times \rangle`.

Internal Representation of Vector Spaces & Modules
--------------------------------------------------

Unlike Groups, Monoids, … , and Magmas, Vector Spaces and Modules have
more than one set of elements and more than one or two binary
operations. Within the ``finite_algebra`` implementation, the internal
representation is as shown below. The five elements listed must be input
to the function, ``make_finite_algebra``, in the order shown, to
construct a Module or VectorSpace.

-  **name**: (``str``) A short name for the algebra;
-  **description**: (``str``) Any additional, useful information about
   the algebra;
-  **scalars**: A ``Ring`` or a ``Field``. The Ring or Field elements
   are called *scalars* and the scalar addition and multiplication
   operations are those of the Ring or Field;
-  **vectors**: An abelian ``Group``. Its elements are *vectors* and its
   operation is *vector addition*;
-  **sv_op**: A scalar-vector binary operation,
   :math:`\circ : S \times V \to V`, for “scaling vectors”

If the scalars are a Field, then ``make_finite_algebra`` will construct
a VectorSpace. Otherwise, if the scalars are a Ring, then a Module will
be constructed.

Examples
--------

:math:`\mathbb{R}^n`
~~~~~~~~~~~~~~~~~~~~

Perhaps the most well-known example of a vector space is
:math:`\mathbb{R}^n`, the n-dimensional vector space over the real
numbers. Of course, :math:`\mathbb{R}^n` satisfies all of the conditions
listed in the definition above. The scalar field of :math:`\mathbb{R}^n`
is :math:`\mathbb{R}` itself, and the abelian group of
:math:`\mathbb{R}^n` is the direct product,
:math:`\mathscr{G} = \mathbb{R} \times \dots \times \mathbb{R} \equiv \times^n \mathbb{R}`,
where the group operation is component-wise addition in
:math:`\mathbb{R}`.

A Finite, n-Dimensional Vector Space (similar to :math:`\mathbb{R}^n`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given a finite Field (or finite Ring) and a positive integer dimension,
the function, ``generate_n_dim_module``, constructs an n-dimensional
Vector Space (or Module) similar to how :math:`\mathbb{R}^n` is
constructed.

This will be demonstrated using the following `“field with 4 elements”
(see
Wikipedia) <https://en.wikipedia.org/wiki/Finite_field#Field_with_four_elements>`__:

.. code:: ipython3

    >>> from finite_algebras import make_finite_algebra, generate_n_dim_module

.. code:: ipython3

    >>> f4 = make_finite_algebra('F4',
                                 'Field with 4 elements (from Wikipedia)',
                                 ['0', '1', 'a', '1+a'],
                                 [['0', '1', 'a', '1+a'],
                                  ['1', '0', '1+a', 'a'],
                                  ['a', '1+a', '0', '1'],
                                  ['1+a', 'a', '1', '0']],
                                 [['0', '0', '0', '0'],
                                  ['0', '1', 'a', '1+a'],
                                  ['0', 'a', '1+a', '1'],
                                  ['0', '1+a', '1', 'a']]
                                )
    
    >>> f4




.. parsed-literal::

    Field(
    'F4',
    'Field with 4 elements (from Wikipedia)',
    ['0', '1', 'a', '1+a'],
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    )



f4 is used, below, to create a finite, n-dimensional VectorSpace.

NOTE: ``generate_n_dim_module`` is a convenience function. Within it,
the requisite Field (or Ring), Group, and scalar-vector operation are
constructed and then fed to the all-purpose algebra construction
function, ``make_finite_algebra``, to create a VectorSpace or Module.
The five conditions, listed in the definition above, are also checked.
If any of them fail, then an exception will be raised.

.. code:: ipython3

    n = 2  # using small dimension to limit the amount of printout below
    
    vs4 = generate_n_dim_module(f4, n)
    
    vs4.about(max_size=16)


.. parsed-literal::

    
    VectorSpace: VS2-F4
    Instance ID: 140501808710352
    Description: 2-dimensional Vector Space over F4
    
    SCALARS:
    
    ** Field **
    Name: F4
    Instance ID: 140501806720912
    Description: Field with 4 elements (from Wikipedia)
    Order: 4
    Identity: 0
    Associative? Yes
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
    
    VECTORS:
    
    ** Group **
    Name: F4_x_F4
    Instance ID: 140501808763344
    Description: Direct product of F4 & F4
    Order: 16
    Identity: 0:0
    Associative? Yes
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


The scalar and vector elements of the VectorSpace can be obtained as
follows:

.. code:: ipython3

    >>> vs4.scalar.elements




.. parsed-literal::

    ['0', '1', 'a', '1+a']



.. code:: ipython3

    >>> vs4.vector.elements




.. parsed-literal::

    ['0:0',
     '0:1',
     '0:a',
     '0:1+a',
     '1:0',
     '1:1',
     '1:a',
     '1:1+a',
     'a:0',
     'a:1',
     'a:a',
     'a:1+a',
     '1+a:0',
     '1+a:1',
     '1+a:a',
     '1+a:1+a']



Scalar addition and multiplication is just the addition and
multiplication operations of the Field (Scalars) used to create the
VectorSpace (or Module)

.. code:: ipython3

    >>> vs4.scalar.add('1', 'a')




.. parsed-literal::

    '1+a'



.. code:: ipython3

    >>> vs4.scalar.mult('a', 'a')




.. parsed-literal::

    '1+a'



Vector addition is just the binary operation of the Group (Vectors) used
to create the Vector Space (or Module)

.. code:: ipython3

    >>> vs4.vector_add('1+a:1', '1:a')  # Same as vs4.vector.op('1+a:1', '1:a')




.. parsed-literal::

    'a:1+a'



And, since the *scalar* part of a VectorSpace is a Field, we can obtain
it’s identity elements as follows:

.. code:: ipython3

    >>> vs4.scalar.zero




.. parsed-literal::

    '0'



.. code:: ipython3

    >>> vs4.scalar.one




.. parsed-literal::

    '1'



The scalar-vector operation for scaling Vectors (or Modules) is the
method, ``sv_op``, and takes two inputs: a scalar and vector, resp.

.. code:: ipython3

    vs4.sv_op('a', '1+a:1')




.. parsed-literal::

    '1:a'



Checking the Five VectorSpace/Module Conditions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Scaling by 1**

If :math:`\mathscr{1} \in S` is the multiplicative identity element of
:math:`\mathscr{F}`, then :math:`\mathscr{1} \circ v = v`

.. code:: ipython3

    >>> print(vs4.sv_op(vs4.scalar.one, 'a:1+a'))


.. parsed-literal::

    a:1+a


**Distributivity of scalars over vector addition**

:math:`s \circ (v_1 \oplus v_2) = (s \circ v_1) \oplus (s \circ v_2)`

.. code:: ipython3

    >>> # Example
    >>> 
    >>> s = 'a'
    >>> v1 = 'a:1+a'
    >>> v2 = 'a:1'
    >>> print(vs4.sv_op(s, vs4.vector_add(v1, v2)))
    >>> print(vs4.vector_add(vs4.sv_op(s, v1), vs4.sv_op(s, v2)))


.. parsed-literal::

    0:1+a
    0:1+a


**Distributivity of vectors over scalar addition**

:math:`(s_1 + s_2) \circ v = (s_1 \circ v) \oplus (s_2 \circ v)`

.. code:: ipython3

    >>> # Example
    >>> 
    >>> s1 = 'a'
    >>> s2 = '1+a'
    >>> v = 'a:1'
    >>> print(vs4.sv_op(vs4.scalar.add(s1, s2), v))
    >>> print(vs4.vector_add(vs4.sv_op(s1, v), vs4.sv_op(s2, v)))


.. parsed-literal::

    a:1
    a:1


**Associativity**

:math:`s_1 \circ (s_2 \circ v) = (s_1 \times s_2) \circ v`

.. code:: ipython3

    >>> # Example
    >>> 
    >>> s1 = 'a'
    >>> s2 = '1+a'
    >>> v = 'a:1'
    >>> print(vs4.sv_op(s1, vs4.sv_op(s2, v)))
    >>> print(vs4.sv_op(vs4.scalar.mult(s1, s2), v))


.. parsed-literal::

    a:1
    a:1


Module based on a Ring
----------------------

Another example, using the technique presented above, but this time with
a Ring, instead of a Field.

.. code:: ipython3

    >>> from finite_algebras import generate_powerset_ring
    >>> psr2 = generate_powerset_ring(2)
    >>> psr2.about()


.. parsed-literal::

    
    ** Ring **
    Name: PSRing2
    Instance ID: 140502879843728
    Description: Autogenerated Ring on powerset of {0, 1} w/ symm. diff. (add) & intersection (mult)
    Order: 4
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {0}     {0}       2
          2     {1}     {1}       2
          3  {0, 1}  {0, 1}       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    Mult. Identity: {0, 1}
    Mult. Commutative? Yes
    Zero Divisors: ['{0}', '{1}']
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 2, 2], [0, 1, 2, 3]]


.. code:: ipython3

    >>> n = 2
    >>> psr_mod = generate_n_dim_module(psr2, n)
    >>> psr_mod.about(max_size=16)


.. parsed-literal::

    
    Module: Mod2-PSRing2
    Instance ID: 140501808829008
    Description: 2-dimensional Module over PSRing2
    
    SCALARS:
    
    ** Ring **
    Name: PSRing2
    Instance ID: 140502879843728
    Description: Autogenerated Ring on powerset of {0, 1} w/ symm. diff. (add) & intersection (mult)
    Order: 4
    Identity: {}
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0      {}      {}       1
          1     {0}     {0}       2
          2     {1}     {1}       2
          3  {0, 1}  {0, 1}       2
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    Mult. Identity: {0, 1}
    Mult. Commutative? Yes
    Zero Divisors: ['{0}', '{1}']
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 2, 2], [0, 1, 2, 3]]
    
    VECTORS:
    
    ** Group **
    Name: PSRing2_x_PSRing2
    Instance ID: 140502879845904
    Description: Direct product of PSRing2 & PSRing2
    Order: 16
    Identity: {}:{}
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0   {}:{}   {}:{}       1
          1  {}:{0}  {}:{0}       2
          2  {}:{1}  {}:{1}       2
          3 {}:{0, 1} {}:{0, 1}       2
          4  {0}:{}  {0}:{}       2
          5 {0}:{0} {0}:{0}       2
          6 {0}:{1} {0}:{1}       2
          7 {0}:{0, 1} {0}:{0, 1}       2
          8  {1}:{}  {1}:{}       2
          9 {1}:{0} {1}:{0}       2
         10 {1}:{1} {1}:{1}       2
         11 {1}:{0, 1} {1}:{0, 1}       2
         12 {0, 1}:{} {0, 1}:{}       2
         13 {0, 1}:{0} {0, 1}:{0}       2
         14 {0, 1}:{1} {0, 1}:{1}       2
         15 {0, 1}:{0, 1} {0, 1}:{0, 1}       2
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

