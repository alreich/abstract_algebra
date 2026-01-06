Cayley-Dickson Construction
===========================

References
----------

-  [Baez 2001] “The Octonions”, Baez, John C., Bull. Amer. Math. Soc. 39
   (2002), 145-205.
   (`PDF <https://www.ams.org/journals/bull/2002-39-02/S0273-0979-01-00934-X/S0273-0979-01-00934-X.pdf>`__)
-  [Reich 2024] This document. (I haven’t found another reference, yet,
   for the Theorem stated below, if there is one.)
-  [Schafer 1954] Schafer, R. D. “On the Algebras Formed by the
   Cayley-Dickson Process.” American Journal of Mathematics 76, no. 2
   (1954)
-  [Schafer 1966] “An Introduction to Nonassociative Algebras”, Schafer,
   R. D., Academic Press, 1966. (`or see the 1961
   version <https://www.gutenberg.org/ebooks/25156>`__)

Definitions
-----------

The `Cayley-Dickson
construction <https://en.wikipedia.org/wiki/Cayley%E2%80%93Dickson_construction>`__
begins with a base algebra, :math:`A`, usually a ring or field, from
which another algebra, :math:`\mathscr{C}(A)`, is derived, with compound
elements, identical to those found in the direct product of :math:`A`
with itself. And, like direct products, addition is defined
element-wise, but multiplication is defined **similar to complex number
multiplication**, as described in Definition 1, below. The description
is “simplified” because it does not use conjugation anywhere.
Conjugation is defined and used in the more general definitions that
follow this one.

   **Definition 1: Cayley-Dickson Algebra (CDA) - Simplified Version (no
   conjugation)**

   Let :math:`A = \langle S, +, \cdot \rangle` be a ring and let
   :math:`T = S \times S` (i.e., the cross-product of :math:`S` with
   itself).

   Then, define the algebra,
   :math:`\mathscr{C}(A) \equiv \langle T, \oplus, \odot \rangle`,

   where :math:`\forall (a,b),(c,d) \in T`,

   :math:`(a,b) \oplus (c,d) \equiv (a + c, b + d)`

   :math:`(a,b) \odot (c,d) \equiv (a \cdot c - b \cdot d, a \cdot d + b \cdot c)`

For example, if we apply the Cayley-Dickson construction to the field of
real numbers, :math:`\mathbb{R}`, we obtain the algebra of **complex
numbers**, :math:`\mathscr{C}(\mathbb{R}) \equiv \mathbb{C}`.

The Cayley-Dickson Algebra (CDA) constructor, :math:`\mathscr{C}`, can
be applied to another CDA, multiple times, as described in Definition 2.

   **Definition 2: CDA Constructor**

   Let :math:`k \in Z^+` and :math:`\mathscr{C}^0(A) \equiv A`,

   then
   :math:`\mathscr{C}^k(A) \equiv \mathscr{C}(\mathscr{C}^{k-1}(A))`,

For example,
:math:`\mathscr{C}^2(\mathbb{R}) \equiv \mathscr{C}(\mathbb{C}) \equiv \mathbb{H}`
is the algebra of **quaternions**, and
:math:`\mathscr{C}^3(\mathbb{R}) \equiv \mathbb{O}` is the algebra of
**octonions**.

In many papers on the subject, a generalization of complex
multiplication is used, instead of the multiplication described in
Definition 1. And, there are multiple, different versions of the
generalization.

All of the generalizations begin with a common, recursive definition of
conjugation, described in Definition 3.

   **Definition 3: Conjugation**

   The **conjugate** of an algebraic element, :math:`r`, is denoted by
   :math:`\overline{r}`, and defined recursively as follows:

   For :math:`a \in A`, the base algebra, let
   :math:`\overline{a} \equiv a`.

   Then, let :math:`k \in Z^+`; :math:`p,q \in \mathscr{C}^{k-1}(A)`;
   and :math:`(p,q) \in \mathscr{C}^k(A)`,

   and define :math:`\overline{(p, q)} \equiv (\overline{p}, -q)`

Three generalizations of multiplication are shown below in Definition 4
(versions A, B, & C):

   **Definition 4: CDA Multiplication**

   Let :math:`k \in Z^+`; :math:`a,b,c,d,\mu \in \mathscr{C}^{k-1}(A)`;
   and :math:`\mu \neq 0`,

   then define multiplication for
   :math:`(a,b), (c,d) \in \mathscr{C}^k(A)` according to **one** of the
   following definitions:

   **[Shafer 1966] Version 4-A**:

   :math:`(a, b) \odot (c, d) = (a \cdot c + \mu \cdot d \cdot \overline{b}, \overline{a} \cdot d + c \cdot b)`

   **[Shafer 1954] Version 4-B**:

   :math:`(a, b) \odot (c, d) = (a \cdot c + \mu \cdot \overline{d} \cdot b, d \cdot a + b \cdot \overline{c})`

   **[Baez 2001] Version 4-C**:

   :math:`(a,b) \odot (c,d) \equiv (a \cdot c - d \cdot \overline{b}, \overline{a} \cdot d + c \cdot b)`

   **[Reich 2024] Definition 1, again (for comparison)**

   :math:`(a,b) \odot (c,d) \equiv (a \cdot c - b \cdot d, a \cdot d + b \cdot c)`

Note that, if the base (“starting”) algebra, :math:`A`, is a field, then
multiplication is commutative and every element is it’s own conjugate.
And, if :math:`\mu = -1`, where :math:`-1` is the additive inverse of
:math:`A`\ ’s multiplicative identity element, then all of the
multiplication versions above produce the same algebra,
:math:`\mathscr{C}(A)`. But, when we start applying CDA constructions on
top of other CDA constructions, the different versions diverge. And, not
only that, even if we stick to a single multiplication version, each
subsequent application of the CDA construction process results in
increasingly “unstructured” algebras. As [Baez 2001] writes, “…each time
we apply the construction, our algebra gets a bit worse. First we lose
the fact that every element is its own conjugate, then we lose
commutativity, then we lose associativity, and finally we lose the
division algebra property.”

Finite Cayley-Dickson Algebras
------------------------------

The Cayley-Dickson constructor, :math:`\mathscr{C}`, defined above, can
also be applied to finite rings or fields.

An interesting result regarding the application of the Cayley-Dickson
construction to a finite field is stated in the Theorem below.

   **Theorem [Reich 2024]**

   Let :math:`F_n` be a finite field of order :math:`n`, where
   :math:`n \in \mathbb{Z}^+` and :math:`n > 1` is a `Gaussian
   prime <https://mathworld.wolfram.com/GaussianPrime.html>`__ (e.g., 3,
   7, 11, 19, 23, 31, 43, …),

   then :math:`\mathscr{C}(F_n)` will be a finite **field** of order
   :math:`n^2`,

   otherwise :math:`\mathscr{C}(F_n)` will be a finite ring.

Examples
--------

Since each application of the Cayley-Dickson construction doubles the
number of elements of its base algebra, repeated applications of the
construction can result in much larger algebras, so the examples in this
section will be restricted to small base rings & fields.

.. code:: ipython3

    import finite_algebras as alg

The ``finite_algebras`` function, ``generate_algebra_mod_n``, will
generate a ring or field based on integer addition and multiplication
modulo n. If n is prime, then result will be a field, otherwise it will
be a ring.

.. code:: ipython3

    F3 = alg.generate_algebra_mod_n(3)
    F3.about()


.. parsed-literal::

    
    ** Field **
    Name: F3
    Instance ID: 4969282064
    Description: Autogenerated Field of integers mod 3
    Order: 3
    Identity: '0'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['2', '1']
    Elements:
       Index   Name   Inverse  Order
          0     '0'     '0'       1
          1     '1'     '2'       3
          2     '2'     '1'       3
    Cayley Table (showing indices):
    [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
    Mult. Identity: '1'
    Mult. Commutative? Yes
    Zero Divisors: None
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0], [0, 1, 2], [0, 2, 1]]


Since 3 is a Gaussian prime, the following field of integers modulo 3
will give us an opportunity to test the theorem stated above.

CDAs of F3 (4 versions)
-----------------------

The method ``make_cayley_dickson_algebra`` applies the Cayley-Dickson
(CD) construction to a Ring or Field.

It’s help documentation is shown below.

.. code:: ipython3

    help(F3.make_cayley_dickson_algebra)


.. parsed-literal::

    Help on method make_cayley_dickson_algebra in module finite_algebras:
    
    make_cayley_dickson_algebra(mu=None, version=1) method of finite_algebras.Field instance
        Constructs the Cayley-Dickson algebra using this Ring or Field.
    
        Several different versions of multiplication are supported:
        version=1: (DEFAULT) No mu & no conjugation are used
        version=2: Definition in Schafer, 1966
        version=3: Definition in Schafer, 1954
        version=4: Definition in Baez, 2001.
    
        See the documentation on readthedocs for more information regarding versions.
    
        Versions 2 & 3 require a value for mu. If mu is None (the default), then mu
        will be automatically set to be the additive inverse of the Ring's
        multiplicative identity element (i.e., "-1") if it exists. If it does not
        exist, then an exception will be raised.
    


The following computation creates 4 versions if :math:`\mathscr{C}(F_3)`
and prints out the name stored internally in each CDA.

.. code:: ipython3

    F3cda24 = F3.make_cayley_dickson_algebra(version=1); print(F3cda24.name)
    F3cda66 = F3.make_cayley_dickson_algebra(version=2); print(F3cda66.name)
    F3cda54 = F3.make_cayley_dickson_algebra(version=3); print(F3cda54.name)
    F3cda01 = F3.make_cayley_dickson_algebra(version=4); print(F3cda01.name)


.. parsed-literal::

    F3_CDA_2024
    F3_CDA_1966
    F3_CDA_1954
    F3_CDA_2001


Here’s the [Schafer 1966] version (i.e., version 2). As we’ll see below,
all four versions are the same. Also, note that :math:`\mathscr{C}(F_3)`
**is a field**.

.. code:: ipython3

    F3cda66.about()


.. parsed-literal::

    
    ** Field **
    Name: F3_CDA_1966
    Instance ID: 4970233936
    Description: Cayley-Dickson algebra based on F3, where mu = 2, Schafer 1966 version.
    Order: 9
    Identity: '0:0'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['0:1', '1:2', '0:2', '2:2', '1:1', '2:1']
    Elements:
       Index   Name   Inverse  Order
          0   '0:0'   '0:0'       1
          1   '0:1'   '0:2'       3
          2   '0:2'   '0:1'       3
          3   '1:0'   '2:0'       3
          4   '1:1'   '2:2'       3
          5   '1:2'   '2:1'       3
          6   '2:0'   '1:0'       3
          7   '2:1'   '1:2'       3
          8   '2:2'   '1:1'       3
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5, 6, 7, 8],
     [1, 2, 0, 4, 5, 3, 7, 8, 6],
     [2, 0, 1, 5, 3, 4, 8, 6, 7],
     [3, 4, 5, 6, 7, 8, 0, 1, 2],
     [4, 5, 3, 7, 8, 6, 1, 2, 0],
     [5, 3, 4, 8, 6, 7, 2, 0, 1],
     [6, 7, 8, 0, 1, 2, 3, 4, 5],
     [7, 8, 6, 1, 2, 0, 4, 5, 3],
     [8, 6, 7, 2, 0, 1, 5, 3, 4]]
    Mult. Identity: '1:0'
    Mult. Commutative? Yes
    Zero Divisors: None
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 6, 3, 1, 7, 4, 2, 8, 5],
     [0, 3, 6, 2, 5, 8, 1, 4, 7],
     [0, 1, 2, 3, 4, 5, 6, 7, 8],
     [0, 7, 5, 4, 2, 6, 8, 3, 1],
     [0, 4, 8, 5, 6, 1, 7, 2, 3],
     [0, 2, 1, 6, 8, 7, 3, 5, 4],
     [0, 8, 4, 7, 3, 2, 5, 1, 6],
     [0, 5, 7, 8, 1, 3, 4, 6, 2]]


.. code:: ipython3

    from itertools import combinations
    
    cdas = [F3cda24, F3cda66, F3cda54, F3cda01]
    
    for cda in cdas:
        print(f"{cda.name} is a {cda.__class__.__name__}")
        
    print("")
    
    for pair in list(combinations(cdas, 2)):
        print(f"{pair[0].name} == {pair[1].name} ? {alg.yes_or_no(pair[0] == pair[1])}")


.. parsed-literal::

    F3_CDA_2024 is a Field
    F3_CDA_1966 is a Field
    F3_CDA_1954 is a Field
    F3_CDA_2001 is a Field
    
    F3_CDA_2024 == F3_CDA_1966 ? Yes
    F3_CDA_2024 == F3_CDA_1954 ? Yes
    F3_CDA_2024 == F3_CDA_2001 ? Yes
    F3_CDA_1966 == F3_CDA_1954 ? Yes
    F3_CDA_1966 == F3_CDA_2001 ? Yes
    F3_CDA_1954 == F3_CDA_2001 ? Yes


CDAs of F5 (4 versions)
-----------------------

This section goes through the same calculations as above, except that
:math:`F_5` is used, instead of :math:`F_3`.

This time, all four versions if the CDA, :math:`\mathscr{C}(F_5)`, will
be the same ring.

.. code:: ipython3

    F5 = alg.generate_algebra_mod_n(5)
    F5.about()


.. parsed-literal::

    
    ** Field **
    Name: F5
    Instance ID: 4969990480
    Description: Autogenerated Field of integers mod 5
    Order: 5
    Identity: '0'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['2', '3', '4', '1']
    Elements:
       Index   Name   Inverse  Order
          0     '0'     '0'       1
          1     '1'     '4'       5
          2     '2'     '3'       5
          3     '3'     '2'       5
          4     '4'     '1'       5
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4],
     [1, 2, 3, 4, 0],
     [2, 3, 4, 0, 1],
     [3, 4, 0, 1, 2],
     [4, 0, 1, 2, 3]]
    Mult. Identity: '1'
    Mult. Commutative? Yes
    Zero Divisors: None
    Multiplicative Cayley Table (showing indices):
    [[0, 0, 0, 0, 0],
     [0, 1, 2, 3, 4],
     [0, 2, 4, 1, 3],
     [0, 3, 1, 4, 2],
     [0, 4, 3, 2, 1]]


.. code:: ipython3

    F5cda24 = F5.make_cayley_dickson_algebra(version=1); print(F5cda24.name)
    F5cda66 = F5.make_cayley_dickson_algebra(version=2); print(F5cda66.name)
    F5cda54 = F5.make_cayley_dickson_algebra(version=3); print(F5cda54.name)
    F5cda01 = F5.make_cayley_dickson_algebra(version=4); print(F5cda01.name)


.. parsed-literal::

    F5_CDA_2024
    F5_CDA_1966
    F5_CDA_1954
    F5_CDA_2001


Here’s a representative example, the [Schafer 1966] version:

.. code:: ipython3

    F5cda66.about()


.. parsed-literal::

    
    ** Ring **
    Name: F5_CDA_1966
    Instance ID: 4969316048
    Description: Cayley-Dickson algebra based on F5, where mu = 4, Schafer 1966 version.
    Order: 25
    Identity: '0:0'
    Commutative? Yes
    Cyclic?: Yes
    Generators: ['0:1', '4:4', '3:2', '0:3', '2:3', '1:4', '3:3', '4:1', '1:1', '0:4', '0:2', '2:2']
    Elements:
       Index   Name   Inverse  Order
          0   '0:0'   '0:0'       1
          1   '0:1'   '0:4'       5
          2   '0:2'   '0:3'       5
          3   '0:3'   '0:2'       5
          4   '0:4'   '0:1'       5
          5   '1:0'   '4:0'       5
          6   '1:1'   '4:4'       5
          7   '1:2'   '4:3'       5
          8   '1:3'   '4:2'       5
          9   '1:4'   '4:1'       5
         10   '2:0'   '3:0'       5
         11   '2:1'   '3:4'       5
         12   '2:2'   '3:3'       5
         13   '2:3'   '3:2'       5
         14   '2:4'   '3:1'       5
         15   '3:0'   '2:0'       5
         16   '3:1'   '2:4'       5
         17   '3:2'   '2:3'       5
         18   '3:3'   '2:2'       5
         19   '3:4'   '2:1'       5
         20   '4:0'   '1:0'       5
         21   '4:1'   '1:4'       5
         22   '4:2'   '1:3'       5
         23   '4:3'   '1:2'       5
         24   '4:4'   '1:1'       5
    Ring order is 25 > 12, so no table is printed.
    Mult. Identity: '1:0'
    Mult. Commutative? Yes
    Zero Divisors: ['1:2', '1:3', '2:1', '2:4', '3:1', '3:4', '4:2', '4:3']
    Ring order is 25 > 12, so the mult. table is not printed.


.. code:: ipython3

    cdas = [F5cda24, F5cda66, F5cda54, F5cda01]
    
    for cda in cdas:
        print(f"{cda.name} is a {cda.__class__.__name__}")
        
    print("")
    
    for pair in list(combinations(cdas, 2)):
        print(f"{pair[0].name} == {pair[1].name} ? {alg.yes_or_no(pair[0] == pair[1])}")


.. parsed-literal::

    F5_CDA_2024 is a Ring
    F5_CDA_1966 is a Ring
    F5_CDA_1954 is a Ring
    F5_CDA_2001 is a Ring
    
    F5_CDA_2024 == F5_CDA_1966 ? Yes
    F5_CDA_2024 == F5_CDA_1954 ? Yes
    F5_CDA_2024 == F5_CDA_2001 ? Yes
    F5_CDA_1966 == F5_CDA_1954 ? Yes
    F5_CDA_1966 == F5_CDA_2001 ? Yes
    F5_CDA_1954 == F5_CDA_2001 ? Yes


And, here’s the multiplicative portion of this algebra. It’s a monoid.

.. code:: ipython3

    F5cda66.extract_multiplicative_algebra().about()


.. parsed-literal::

    
    ** Monoid **
    Name: F5_CDA_1966.Mult
    Instance ID: 4970332960
    Description: Multiplicative-only portion of F5_CDA_1966
    Order: 25
    Identity: 1:0
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements: ('0:0', '0:1', '0:2', '0:3', '0:4', '1:0', '1:1', '1:2', '1:3', '1:4', '2:0', '2:1', '2:2', '2:3', '2:4', '3:0', '3:1', '3:2', '3:3', '3:4', '4:0', '4:1', '4:2', '4:3', '4:4')
    Has Inverses? No
    Monoid order is 25 > 12, so the table is not output.


Quads (CDA of a CDA)
--------------------

Four CDAs, each one a :math:`\mathscr{C}^2(F_3)`, are generated below,
each one using a different version of multiplication, per the discussion
above.

.. code:: ipython3

    %%time
    
    F3quad24 = F3cda24.make_cayley_dickson_algebra(version=1)
    F3quad66 = F3cda66.make_cayley_dickson_algebra(version=2)
    F3quad54 = F3cda54.make_cayley_dickson_algebra(version=3)
    F3quad01 = F3cda01.make_cayley_dickson_algebra(version=4)


.. parsed-literal::

    CPU times: user 3.19 s, sys: 12.5 ms, total: 3.2 s
    Wall time: 3.24 s


The computation below shows that the only versions of
:math:`\mathscr{C}^2(F_3)` that are equal to each other are [Schafer
1966] and [Baez 2001].

.. code:: ipython3

    from itertools import combinations
    
    quad_cdas = [F3quad24, F3quad66, F3quad54, F3quad01]
    
    for pair in list(combinations(quad_cdas, 2)):
        print(f"{pair[0].name} == {pair[1].name} ? {alg.yes_or_no(pair[0] == pair[1])}")


.. parsed-literal::

    F3_CDA_2024_CDA_2024 == F3_CDA_1966_CDA_1966 ? No
    F3_CDA_2024_CDA_2024 == F3_CDA_1954_CDA_1954 ? No
    F3_CDA_2024_CDA_2024 == F3_CDA_2001_CDA_2001 ? No
    F3_CDA_1966_CDA_1966 == F3_CDA_1954_CDA_1954 ? No
    F3_CDA_1966_CDA_1966 == F3_CDA_2001_CDA_2001 ? Yes
    F3_CDA_1954_CDA_1954 == F3_CDA_2001_CDA_2001 ? No


.. code:: ipython3

    F3quad66.about(show_conjugates=False)


.. parsed-literal::

    
    ** Ring **
    Name: F3_CDA_1966_CDA_1966
    Instance ID: 4403910640
    Description: Cayley-Dickson algebra based on F3_CDA_1966, where mu = 2:0, Schafer 1966 version.
    Order: 81
    Identity: '0:0:0:0'
    Commutative? Yes
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0 '0:0:0:0' '0:0:0:0'       1
          1 '0:0:0:1' '0:0:0:2'       3
          2 '0:0:0:2' '0:0:0:1'       3
          3 '0:0:1:0' '0:0:2:0'       3
          4 '0:0:1:1' '0:0:2:2'       3
          5 '0:0:1:2' '0:0:2:1'       3
          6 '0:0:2:0' '0:0:1:0'       3
          7 '0:0:2:1' '0:0:1:2'       3
          8 '0:0:2:2' '0:0:1:1'       3
          9 '0:1:0:0' '0:2:0:0'       3
         10 '0:1:0:1' '0:2:0:2'       3
         11 '0:1:0:2' '0:2:0:1'       3
         12 '0:1:1:0' '0:2:2:0'       3
         13 '0:1:1:1' '0:2:2:2'       3
         14 '0:1:1:2' '0:2:2:1'       3
         15 '0:1:2:0' '0:2:1:0'       3
         16 '0:1:2:1' '0:2:1:2'       3
         17 '0:1:2:2' '0:2:1:1'       3
         18 '0:2:0:0' '0:1:0:0'       3
         19 '0:2:0:1' '0:1:0:2'       3
         20 '0:2:0:2' '0:1:0:1'       3
         21 '0:2:1:0' '0:1:2:0'       3
         22 '0:2:1:1' '0:1:2:2'       3
         23 '0:2:1:2' '0:1:2:1'       3
         24 '0:2:2:0' '0:1:1:0'       3
         25 '0:2:2:1' '0:1:1:2'       3
         26 '0:2:2:2' '0:1:1:1'       3
         27 '1:0:0:0' '2:0:0:0'       3
         28 '1:0:0:1' '2:0:0:2'       3
         29 '1:0:0:2' '2:0:0:1'       3
         30 '1:0:1:0' '2:0:2:0'       3
         31 '1:0:1:1' '2:0:2:2'       3
         32 '1:0:1:2' '2:0:2:1'       3
         33 '1:0:2:0' '2:0:1:0'       3
         34 '1:0:2:1' '2:0:1:2'       3
         35 '1:0:2:2' '2:0:1:1'       3
         36 '1:1:0:0' '2:2:0:0'       3
         37 '1:1:0:1' '2:2:0:2'       3
         38 '1:1:0:2' '2:2:0:1'       3
         39 '1:1:1:0' '2:2:2:0'       3
         40 '1:1:1:1' '2:2:2:2'       3
         41 '1:1:1:2' '2:2:2:1'       3
         42 '1:1:2:0' '2:2:1:0'       3
         43 '1:1:2:1' '2:2:1:2'       3
         44 '1:1:2:2' '2:2:1:1'       3
         45 '1:2:0:0' '2:1:0:0'       3
         46 '1:2:0:1' '2:1:0:2'       3
         47 '1:2:0:2' '2:1:0:1'       3
         48 '1:2:1:0' '2:1:2:0'       3
         49 '1:2:1:1' '2:1:2:2'       3
         50 '1:2:1:2' '2:1:2:1'       3
         51 '1:2:2:0' '2:1:1:0'       3
         52 '1:2:2:1' '2:1:1:2'       3
         53 '1:2:2:2' '2:1:1:1'       3
         54 '2:0:0:0' '1:0:0:0'       3
         55 '2:0:0:1' '1:0:0:2'       3
         56 '2:0:0:2' '1:0:0:1'       3
         57 '2:0:1:0' '1:0:2:0'       3
         58 '2:0:1:1' '1:0:2:2'       3
         59 '2:0:1:2' '1:0:2:1'       3
         60 '2:0:2:0' '1:0:1:0'       3
         61 '2:0:2:1' '1:0:1:2'       3
         62 '2:0:2:2' '1:0:1:1'       3
         63 '2:1:0:0' '1:2:0:0'       3
         64 '2:1:0:1' '1:2:0:2'       3
         65 '2:1:0:2' '1:2:0:1'       3
         66 '2:1:1:0' '1:2:2:0'       3
         67 '2:1:1:1' '1:2:2:2'       3
         68 '2:1:1:2' '1:2:2:1'       3
         69 '2:1:2:0' '1:2:1:0'       3
         70 '2:1:2:1' '1:2:1:2'       3
         71 '2:1:2:2' '1:2:1:1'       3
         72 '2:2:0:0' '1:1:0:0'       3
         73 '2:2:0:1' '1:1:0:2'       3
         74 '2:2:0:2' '1:1:0:1'       3
         75 '2:2:1:0' '1:1:2:0'       3
         76 '2:2:1:1' '1:1:2:2'       3
         77 '2:2:1:2' '1:1:2:1'       3
         78 '2:2:2:0' '1:1:1:0'       3
         79 '2:2:2:1' '1:1:1:2'       3
         80 '2:2:2:2' '1:1:1:1'       3
    Ring order is 81 > 12, so no table is printed.
    Mult. Identity: '1:0:0:0'
    Mult. Commutative? No
    Zero Divisors: ['0:1:1:1', '0:1:1:2', '0:1:2:1', '0:1:2:2', '0:2:1:1', '0:2:1:2', '0:2:2:1', '0:2:2:2', '1:0:1:1', '1:0:1:2', '1:0:2:1', '1:0:2:2', '1:1:0:1', '1:1:0:2', '1:1:1:0', '1:1:2:0', '1:2:0:1', '1:2:0:2', '1:2:1:0', '1:2:2:0', '2:0:1:1', '2:0:1:2', '2:0:2:1', '2:0:2:2', '2:1:0:1', '2:1:0:2', '2:1:1:0', '2:1:2:0', '2:2:0:1', '2:2:0:2', '2:2:1:0', '2:2:2:0']
    Ring order is 81 > 12, so the mult. table is not printed.


Zero Divisors
-------------

The next two calculations show that the version of
:math:`\mathscr{C}^2(F_3)` that uses [Reich 2024] has 16 zero divisors,
while the other three versions each have 32 zero divisors.

And, the zero divisors of the [Schafer 1966], [Schafer 1954], and [Baez
2001] versions are all the same, while the zero divisors of the [Reich
2024] version have nothing in common with them.

.. code:: ipython3

    for quad in quad_cdas:
        print(f"{quad.name} has {len(quad.zero_divisors())} zero divisors")


.. parsed-literal::

    F3_CDA_2024_CDA_2024 has 16 zero divisors
    F3_CDA_1966_CDA_1966 has 32 zero divisors
    F3_CDA_1954_CDA_1954 has 32 zero divisors
    F3_CDA_2001_CDA_2001 has 32 zero divisors


.. code:: ipython3

    for pair in list(combinations(quad_cdas, 2)):
        zd0 = set(pair[0].zero_divisors())
        zd1 = set(pair[1].zero_divisors())
        zd_in_common = zd0.intersection(zd1)
        print(f"{pair[0].name} & {pair[1].name} have {len(zd_in_common)} zero divisors in common.")


.. parsed-literal::

    F3_CDA_2024_CDA_2024 & F3_CDA_1966_CDA_1966 have 0 zero divisors in common.
    F3_CDA_2024_CDA_2024 & F3_CDA_1954_CDA_1954 have 0 zero divisors in common.
    F3_CDA_2024_CDA_2024 & F3_CDA_2001_CDA_2001 have 0 zero divisors in common.
    F3_CDA_1966_CDA_1966 & F3_CDA_1954_CDA_1954 have 32 zero divisors in common.
    F3_CDA_1966_CDA_1966 & F3_CDA_2001_CDA_2001 have 32 zero divisors in common.
    F3_CDA_1954_CDA_1954 & F3_CDA_2001_CDA_2001 have 32 zero divisors in common.


.. code:: ipython3

    sorted(F3quad24.zero_divisors())




.. parsed-literal::

    ['0:1:1:0',
     '0:1:2:0',
     '0:2:1:0',
     '0:2:2:0',
     '1:0:0:1',
     '1:0:0:2',
     '1:1:1:2',
     '1:1:2:1',
     '1:2:1:1',
     '1:2:2:2',
     '2:0:0:1',
     '2:0:0:2',
     '2:1:1:1',
     '2:1:2:2',
     '2:2:1:2',
     '2:2:2:1']



.. code:: ipython3

    sorted(F3quad66.zero_divisors())




.. parsed-literal::

    ['0:1:1:1',
     '0:1:1:2',
     '0:1:2:1',
     '0:1:2:2',
     '0:2:1:1',
     '0:2:1:2',
     '0:2:2:1',
     '0:2:2:2',
     '1:0:1:1',
     '1:0:1:2',
     '1:0:2:1',
     '1:0:2:2',
     '1:1:0:1',
     '1:1:0:2',
     '1:1:1:0',
     '1:1:2:0',
     '1:2:0:1',
     '1:2:0:2',
     '1:2:1:0',
     '1:2:2:0',
     '2:0:1:1',
     '2:0:1:2',
     '2:0:2:1',
     '2:0:2:2',
     '2:1:0:1',
     '2:1:0:2',
     '2:1:1:0',
     '2:1:2:0',
     '2:2:0:1',
     '2:2:0:2',
     '2:2:1:0',
     '2:2:2:0']



**Something to Note:** The computation below, shows that all 32 of the
zero divisors of F3_CDA_1966_CDA_1966, F3_CDA_1954_CDA_1954, and
F3_CDA_2001_CDA_2001 have exactly one ‘0’ as a component. Basically, an
element is a zero divisor \*\ **if and only if** it has exactly one ‘0’
component.

There does not seem to be an obvious pattern to the 16 zero divisors of
F3_CDA_2024_CDA_2024.

.. code:: ipython3

    from operator import countOf
    
    algebra = F3quad66
    
    count = 0
    for elem in algebra.elements:
        num = countOf(elem.split(':'), '0')
        if num == 1:
            count += 1
    
    print(count)


.. parsed-literal::

    32


Regarding the Theorem
---------------------

.. code:: ipython3

    %%time
    
    n = 24
    #n = 7
    vers = 2
    
    for i in range(2,n + 1):
        fi = alg.generate_algebra_mod_n(i)
        fi_cda = fi.make_cayley_dickson_algebra(version=vers)
        class_name = fi_cda.__class__.__name__
        if class_name == 'Field':
            print(f"{class_name}: {fi_cda.name} <-- Gaussian prime: {i}")
        else:
            print(f"{class_name}: {fi_cda.name}")
    
    print()


.. parsed-literal::

    Ring: F2_CDA_1966
    Field: F3_CDA_1966 <-- Gaussian prime: 3
    Ring: R4_CDA_1966
    Ring: F5_CDA_1966
    Ring: R6_CDA_1966
    Field: F7_CDA_1966 <-- Gaussian prime: 7
    Ring: R8_CDA_1966
    Ring: R9_CDA_1966
    Ring: R10_CDA_1966
    Field: F11_CDA_1966 <-- Gaussian prime: 11
    Ring: R12_CDA_1966
    Ring: F13_CDA_1966
    Ring: R14_CDA_1966
    Ring: R15_CDA_1966
    Ring: R16_CDA_1966
    Ring: F17_CDA_1966
    Ring: R18_CDA_1966
    Field: F19_CDA_1966 <-- Gaussian prime: 19
    Ring: R20_CDA_1966
    Ring: R21_CDA_1966
    Ring: R22_CDA_1966
    Field: F23_CDA_1966 <-- Gaussian prime: 23
    Ring: R24_CDA_1966
    
    CPU times: user 19min 48s, sys: 2.34 s, total: 19min 50s
    Wall time: 20min 28s


Additional Information
----------------------

-  `Python code for octonion and sedenion
   multiplication <https://www.johndcook.com/blog/2018/07/09/octonioin-multiplication/>`__
   - John D Cook blog

-  `The
   Octonions <https://web.archive.org/web/20180216125124/http://math.ucr.edu:80/home/baez/octonions/>`__
   - The Wayback Machine

-  `Algebra over a
   field <https://en.wikipedia.org/wiki/Algebra_over_a_field>`__ -
   Wikipedia

-  `Cayley-Dickson
   construction <https://en.wikipedia.org/wiki/Cayley%E2%80%93Dickson_construction>`__
   - Wikipedia

-  `Cayley-Dickson
   algebra <https://encyclopediaofmath.org/wiki/Cayley-Dickson_algebra>`__
   - Encyclopedia of Math

-  `What comes after the
   ducentiquinquagintasexions? <https://english.stackexchange.com/questions/234607/what-comes-after-the-ducentiquinquagintasexions>`__
   - StackExchange

-  `“Equivalence in a Class of Division Algebras of Order
   16” <https://core.ac.uk/reader/82141950>`__ by R. D. Schafer

-  `“A Stroll Through the Gaussian
   Primes” <https://maa.org/sites/default/files/pdf/upload_library/22/Chauvenet/Gethner.pdf>`__,
   Gethner, Wagon, and Wick, The American Mathematical Monthly, 1998.

-  `“Equivalence in a Class of Division Algebras of Order
   16” <https://core.ac.uk/reader/82141950>`__ by R. D. Schafer

-  `“Cayley-Dickson Algebras and
   Loops” <https://www.hilarispublisher.com/open-access/cayleydickson-algebras-and-loops-1736-4337-1-101.pdf>`__,
   Culbert, C., Journal of Generalized Lie Theory and Applications Vol.
   1 (2007), No. 1, 1–17

-  `“On Automorphisms and Derivations of Cayley-Dickson
   Algebras” <https://www.sciencedirect.com/science/article/pii/0021869390902219>`__,
   Eakin, P. & Sathaye A., Journal of Algebra 129, 263-278 (1990)
