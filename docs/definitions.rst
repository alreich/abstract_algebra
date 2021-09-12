Definitions
===========

The structure and properties of the class hierarchy of the
``finite_algebra`` module are based on the following definitions.

Groups, Rings, Fields, etc.
---------------------------

The following list of algebraic structures is ordered such that each
successive structure builds on the previous one. The class hierarchy of
the ``finite_algebra`` module modeled on this progression.

-  **Magma** – a set with a binary operation:
   :math:`\langle S, \circ \rangle`, where :math:`S` is a set and
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
   Group

Vector Spaces and Modules
-------------------------

In the definitions, below, care is taken to not conflate the
scalar-scalar, vector-vector, and scalar-vector operations.

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

Class Hierarchy
---------------

The definitions, above, are supported by the following class hierarchy,
used in the ``finite_algebras`` module:

.. figure:: attachment:class_hierarchy_sm.jpg
   :alt: class_hierarchy_sm.jpg

   class_hierarchy_sm.jpg
