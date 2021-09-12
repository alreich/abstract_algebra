Vector Spaces & Modules
=======================

Vector Spaces and Modules can be implemented using Finite Algebra
components, such as Groups, Rings, and Fields. See the previous section,
“Definitions”, for definitions of these algebraic structures.

Internal Representation of Vector Spaces & Modules
--------------------------------------------------

Internally, a ``FiniteAlgebra`` can take several different forms. For
algebras that have more than one set of elements and multiple binary
operations, such as Vector Spaces and Modules, the internal
representation is as shown below.

-  **name**: (``str``) A short name for the algebra;
-  **description**: (``str``) Any additional, useful information about
   the algebra;
-  **scalars**: A ``Ring`` (Module) or a ``Field`` (VectorSpace). Its
   elements are *scalars* and its operations are *scalar addition and
   multiplication*;
-  **vectors**: An abelian ``Group``. Its elements are *vectors* and its
   operation is *vector addition*;
-  **sv_op**: A scalar-vector binary operation,
   :math:`\circ : S \times V \to V`, for “scaling vectors”

Examples
--------

The following example demonstrates the construction of an n-dimensional
Vector Space that is similar to the type of vector space most students
are familiar with, i.e., vectors consist of components made out of the
same field elements (e.g., Real numbers) as the scalar field (e.g., also
Real numbers).

If you would rather skip this demonstration, then jump to the bottom of
this page to find the function, ``generate_n_dim_module``. It puts
everything about to be demonstrated into one tidy package for easy use.

So, to begin, we’ll use a Field, :math:`F`, and the abelian Group,
:math:`F_2 = F \times F`, created by computing the direct product of
:math:`F` with itself. This will create a “two-dimensional” Vector
Space. (This generalizes, by the way, to n-dimensions by using the
Group, :math:`F_n = F \times \dots \times F \equiv \times^n F`.)

First, we’ll load the built-in examples to obtain the “Field with 4
elements (from Wikipedia)”.

.. code:: ipython3

    >>> import os
    >>> aa_path = os.path.join(os.getenv("PYPROJ"), "abstract_algebra")
    >>> alg_dir = os.path.join(aa_path, "Algebras")

.. code:: ipython3

    >>> from finite_algebras import *
    #>>> import modules_and_vector_spaces as mvs

.. code:: ipython3

    >>> ex = Examples(alg_dir)


.. parsed-literal::

    ======================================================================
                               Example Algebras
    ----------------------------------------------------------------------
      15 example algebras are available.
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
    13: Q8 -- Quaternion Group
    14: SD16 -- Semidihedral group of order 16
    ======================================================================


The “field with 4 elements” will be the scalars.

.. code:: ipython3

    >>> F4 = ex.get_example(9)
    >>> F4.about(use_table_names=True)


.. parsed-literal::

    
    Field: F4
    Instance ID: 140652267961104
    Description: Field with 4 elements (from Wikipedia)
    Order: 4
    Identity: 0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0       0       0       1
          1       1       1       2
          2       a       a       2
          3     1+a     1+a       2
    Cayley Table (showing names):
    [['0', '1', 'a', '1+a'],
     ['1', '0', '1+a', 'a'],
     ['a', '1+a', '0', '1'],
     ['1+a', 'a', '1', '0']]
    Mult. Identity: 1
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing names):
    [['0', '0', '0', '0'],
     ['0', '1', 'a', '1+a'],
     ['0', 'a', '1+a', '1'],
     ['0', '1+a', '1', 'a']]


The “field with 4 elements” will also be used to generate an abelian
Group, as follows:

.. code:: ipython3

    >>> F4_2 = F4 * F4
    >>> F4_2.about(max_size=16)


.. parsed-literal::

    
    Group: F4_x_F4
    Instance ID: 140652267936016
    Description: Direct product of F4 & F4
    Order: 16
    Identity: 0:0
    Associative? Yes
    Commutative? Yes
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


The name of the function, ``make_dp_sv_op``, is shorthand for **Make a
Direct-Product-based Scalar-Vector Binary Operator**.

As input, it takes the Field (or Ring), the Direct Product of which,
will be used to create a Group (the Vectors).

The binary operator (function) it returns is used to scale a vector. It
takes two inputs, a scalar element and a vector element, and returns a
vector element.

.. code:: ipython3

    >>> op = make_dp_sv_op(F4)

The function, ``make_finite_algebra``, checks the inputs and then
outputs the most specific algebraic structure supported by the inputs,
which in this case are either a Module or a Vector Space.

.. code:: ipython3

    >>> vs = make_finite_algebra('VS4_2D', '4 Element 2D Vector Space', F4, F4_2, op)
    >>> vs




.. parsed-literal::

    <VectorSpace:VS4_2D, ID:140652267934608, Scalars:F4, Vectors:F4_x_F4>



The elements of a Direct Product are constructed from the elements of
the component algebras (Field or Ring in this case), separated by a
colon (‘:’). So, where one might think of a vector as something like,
(0, 1), here it would be, 0:1. This is convenient, because Direct
Products can be “stacked” onto Direct Products any number of times,
yielding something elements like, a:1:0:1+a.

.. code:: ipython3

    >>> print(vs.vector.elements)


.. parsed-literal::

    ['0:0', '0:1', '0:a', '0:1+a', '1:0', '1:1', '1:a', '1:1+a', 'a:0', 'a:1', 'a:a', 'a:1+a', '1+a:0', '1+a:1', '1+a:a', '1+a:1+a']


.. code:: ipython3

    >>> print(vs.scalar.elements)


.. parsed-literal::

    ['0', '1', 'a', '1+a']


Scalar addition and multiplication is just the addition and
multiplication operations of the Field (Scalars) used to create the
Vector Space (or Module)

.. code:: ipython3

    >>> vs.scalar.add('1', 'a')




.. parsed-literal::

    '1+a'



.. code:: ipython3

    >>> vs.scalar.mult('a', 'a')




.. parsed-literal::

    '1+a'



Vector addition is just the binary operation of the Group (Vectors) used
to create the Vector Space (or Module)

.. code:: ipython3

    >>> vs.vector_add('1:a', 'a:a')  # Same as vs.vector.op('1:a', 'a:a')




.. parsed-literal::

    '1+a:0'



The method, ``sv_op``, below, is the result of the function,
``make_dp_sv_op``, described above.

.. code:: ipython3

    >>> vs.sv_op('a', 'a:a')




.. parsed-literal::

    '1+a:1+a'



.. code:: ipython3

    >>> vs.scalar.zero




.. parsed-literal::

    '0'



.. code:: ipython3

    >>> vs.scalar.one




.. parsed-literal::

    '1'



Check: Scaling by 1
~~~~~~~~~~~~~~~~~~~

If :math:`\mathscr{1} \in S` is the multiplicative identity element of
:math:`\mathscr{F}`, then :math:`\mathscr{1} \circ v = v`

.. code:: ipython3

    >>> check_scaling_by_one(F4, F4_2, op)




.. parsed-literal::

    True



Check: Distributivity of scalars over vector addition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`s \circ (v_1 \oplus v_2) = (s \circ v_1) \oplus (s \circ v_2)`

.. code:: ipython3

    >>> # Example
    >>> 
    >>> s = 'a'
    >>> v1 = 'a:1+a'
    >>> v2 = 'a:1'
    >>> print(vs.sv_op(s, vs.vector_add(v1, v2)))
    >>> print(vs.vector_add(vs.sv_op(s, v1), vs.sv_op(s, v2)))


.. parsed-literal::

    0:1+a
    0:1+a


.. code:: ipython3

    >>> check_dist_of_scalars_over_vec_add(F4, F4_2, op)




.. parsed-literal::

    True



Check: Distributivity of vectors over scalar addition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`(s_1 + s_2) \circ v = (s_1 \circ v) \oplus (s_2 \circ v)`

.. code:: ipython3

    >>> # Example
    >>> 
    >>> s1 = 'a'
    >>> s2 = '1+a'
    >>> v = 'a:1'
    >>> print(vs.sv_op(vs.scalar.add(s1, s2), v))
    >>> print(vs.vector_add(vs.sv_op(s1, v), vs.sv_op(s2, v)))


.. parsed-literal::

    a:1
    a:1


.. code:: ipython3

    >>> check_dist_of_vec_over_scalar_add(F4, F4_2, op)




.. parsed-literal::

    True



Check: Associativity
~~~~~~~~~~~~~~~~~~~~

:math:`s_1 \circ (s_2 \circ v) = (s_1 \times s_2) \circ v`

.. code:: ipython3

    >>> # Example
    >>> 
    >>> s1 = 'a'
    >>> s2 = '1+a'
    >>> v = 'a:1'
    >>> print(vs.sv_op(s1, vs.sv_op(s2, v)))
    >>> print(vs.sv_op(vs.scalar.mult(s1, s2), v))


.. parsed-literal::

    a:1
    a:1


.. code:: ipython3

    >>> check_associativity(F4, F4_2, op)




.. parsed-literal::

    True



3D Vector Space
~~~~~~~~~~~~~~~

Here is another, similar example, except that the abelian Group is the
direct product, :math:`F_4 \times F_4 \times F_4`, which can be
calculated for any Finite Algebra using the method, ``power``.

.. code:: ipython3

    >>> F4_3 = F4.power(3)
    >>> F4_3.about()


.. parsed-literal::

    
    Group: F4_x_F4_x_F4
    Instance ID: 140653340679248
    Description: Direct product of F4_x_F4 & F4
    Order: 64
    Identity: 0:0:0
    Associative? Yes
    Commutative? Yes
    Elements:
       Index   Name   Inverse  Order
          0   0:0:0   0:0:0       1
          1   0:0:1   0:0:1       2
          2   0:0:a   0:0:a       2
          3 0:0:1+a 0:0:1+a       2
          4   0:1:0   0:1:0       2
          5   0:1:1   0:1:1       2
          6   0:1:a   0:1:a       2
          7 0:1:1+a 0:1:1+a       2
          8   0:a:0   0:a:0       2
          9   0:a:1   0:a:1       2
         10   0:a:a   0:a:a       2
         11 0:a:1+a 0:a:1+a       2
         12 0:1+a:0 0:1+a:0       2
         13 0:1+a:1 0:1+a:1       2
         14 0:1+a:a 0:1+a:a       2
         15 0:1+a:1+a 0:1+a:1+a       2
         16   1:0:0   1:0:0       2
         17   1:0:1   1:0:1       2
         18   1:0:a   1:0:a       2
         19 1:0:1+a 1:0:1+a       2
         20   1:1:0   1:1:0       2
         21   1:1:1   1:1:1       2
         22   1:1:a   1:1:a       2
         23 1:1:1+a 1:1:1+a       2
         24   1:a:0   1:a:0       2
         25   1:a:1   1:a:1       2
         26   1:a:a   1:a:a       2
         27 1:a:1+a 1:a:1+a       2
         28 1:1+a:0 1:1+a:0       2
         29 1:1+a:1 1:1+a:1       2
         30 1:1+a:a 1:1+a:a       2
         31 1:1+a:1+a 1:1+a:1+a       2
         32   a:0:0   a:0:0       2
         33   a:0:1   a:0:1       2
         34   a:0:a   a:0:a       2
         35 a:0:1+a a:0:1+a       2
         36   a:1:0   a:1:0       2
         37   a:1:1   a:1:1       2
         38   a:1:a   a:1:a       2
         39 a:1:1+a a:1:1+a       2
         40   a:a:0   a:a:0       2
         41   a:a:1   a:a:1       2
         42   a:a:a   a:a:a       2
         43 a:a:1+a a:a:1+a       2
         44 a:1+a:0 a:1+a:0       2
         45 a:1+a:1 a:1+a:1       2
         46 a:1+a:a a:1+a:a       2
         47 a:1+a:1+a a:1+a:1+a       2
         48 1+a:0:0 1+a:0:0       2
         49 1+a:0:1 1+a:0:1       2
         50 1+a:0:a 1+a:0:a       2
         51 1+a:0:1+a 1+a:0:1+a       2
         52 1+a:1:0 1+a:1:0       2
         53 1+a:1:1 1+a:1:1       2
         54 1+a:1:a 1+a:1:a       2
         55 1+a:1:1+a 1+a:1:1+a       2
         56 1+a:a:0 1+a:a:0       2
         57 1+a:a:1 1+a:a:1       2
         58 1+a:a:a 1+a:a:a       2
         59 1+a:a:1+a 1+a:a:1+a       2
         60 1+a:1+a:0 1+a:1+a:0       2
         61 1+a:1+a:1 1+a:1+a:1       2
         62 1+a:1+a:a 1+a:1+a:a       2
         63 1+a:1+a:1+a 1+a:1+a:1+a       2
    Group order is 64 > 12, so no further info calculated/printed.


.. code:: ipython3

    >>> op = make_dp_sv_op(F4)

.. code:: ipython3

    >>> vs3 = make_finite_algebra('VS4_3D', '4 Element 3D Vector Space', F4, F4_3, op)
    >>> vs3




.. parsed-literal::

    <VectorSpace:VS4_3D, ID:140652395126096, Scalars:F4, Vectors:F4_x_F4_x_F4>



Rather than checking each of the Module/VectorSpace conditions
individually, they can be checked all at once using the function,
``check_module_conditions``.

Also, ``check_module_conditions`` is automatically called by the Module
and VectorSpace constructors. If it fails, then the constructor will
raise a ValueError exception.

.. code:: ipython3

    >>> check_module_conditions(F4, F4_3, op, verbose=True)


.. parsed-literal::

    * Scaling by 1 OK? Yes
    * Distributivity of scalars over vector addition OK? Yes
    * Distributivity of vectors over scalar addition OK? Yes
    * Scaling by 1 OK? Yes




.. parsed-literal::

    True



Module based on a Ring
----------------------

Another example, using the technique presented above, but this time with
a Ring, instead of a Field.

.. code:: ipython3

    >>> psr2 = generate_powerset_ring(2)
    >>> psr2.about()


.. parsed-literal::

    
    Ring: PSRing2
    Instance ID: 140652395139984
    Description: Autogenerated Ring on powerset of {0, 1} w/ symm. diff. (add) & intersection (mult)
    Order: 4
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
    Mult. Identity: {0, 1}
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 2, 2], [0, 1, 2, 3]]


.. code:: ipython3

    >>> psr2_2 = psr2 * psr2
    >>> psr2_2.about()


.. parsed-literal::

    
    Group: PSRing2_x_PSRing2
    Instance ID: 140652395168144
    Description: Direct product of PSRing2 & PSRing2
    Order: 16
    Identity: {}:{}
    Associative? Yes
    Commutative? Yes
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
    Group order is 16 > 12, so no further info calculated/printed.


.. code:: ipython3

    >>> psr_op = make_dp_sv_op(psr2)
    >>> 
    >>> psr_mod = make_finite_algebra("PSRmod", "2D Powerset Vector Space", psr2, psr2_2, psr_op)
    >>> psr_mod.about(max_size=16)


.. parsed-literal::

    
    Module: PSRmod
    Instance ID: 140652395171280
    Description: 2D Powerset Vector Space
    Order: 4
    
    SCALARS:
    
    Ring: PSRing2
    Instance ID: 140652395139984
    Description: Autogenerated Ring on powerset of {0, 1} w/ symm. diff. (add) & intersection (mult)
    Order: 4
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
    Mult. Identity: {0, 1}
    Mult. Commutative? Yes
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0], [0, 1, 0, 1], [0, 0, 2, 2], [0, 1, 2, 3]]
    
    VECTORS:
    
    Group: PSRing2_x_PSRing2
    Instance ID: 140652395168144
    Description: Direct product of PSRing2 & PSRing2
    Order: 16
    Identity: {}:{}
    Associative? Yes
    Commutative? Yes
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


Wrapping it All Up in One Function
----------------------------------

As mentioned at the beginning of this page, everything done above can be
accomplished with a single function call to ``generate_n_dim_module``.

Two inputs are required: a Field and an integer (number of dimensions)

.. code:: ipython3

    >>> F4_2X = generate_n_dim_module(F4, 2)
    >>> F4_2X.about(max_size=16)


.. parsed-literal::

    
    VectorSpace: VS2-F4
    Instance ID: 140652395171792
    Description: 2-dimensional Vector Space over <Field:F4, ID:140652267961104>
    Order: 4
    
    SCALARS:
    
    Field: F4
    Instance ID: 140652267961104
    Description: Field with 4 elements (from Wikipedia)
    Order: 4
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
    
    VECTORS:
    
    Group: F4_x_F4
    Instance ID: 140652395159824
    Description: Direct product of F4 & F4
    Order: 16
    Identity: 0:0
    Associative? Yes
    Commutative? Yes
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

