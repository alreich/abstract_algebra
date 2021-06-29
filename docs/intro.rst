Introduction to Abstract Algebra
================================

Groups
------

A group, :math:`G = \langle S, \otimes \rangle`, consists of a set,
:math:`S`, and a binary operation, :math:`\otimes: S \times S \to S`
such that:

1. :math:`\otimes` assigns a unique value, :math:`a \otimes b \in S`,
   for every :math:`(a,b) \in S \times S`.
2. :math:`\otimes` is associative. That is, for any
   :math:`a,b,c \in S \Rightarrow a \otimes (b \otimes c) = (a \otimes b) \otimes c`.
3. There is an identity element :math:`e \in S`, such that, for all
   :math:`a \in S, a \otimes e = e \otimes a = a`. Sometimes, :math:`e`
   is referred to as the natural element of the group.
4. Every element :math:`a \in S` has an inverse element,
   :math:`a^{-1} \in S`, such that,
   :math:`a \otimes a^{-1} = a^{-1} \otimes a = e`.

The symbol, :math:`\otimes`, is used here to emphasize that it is not
the same as numeric addition, :math:`+`, or multiplication,
:math:`\times`. It can be more abstract…and sometimes not; it depends on
which group is being discussed. For this reason, other symbols might be
used to describe a group’s binary operation, often :math:`+`,
:math:`\times`, and :math:`\cdot`. Very often, no symbol at all is used,
e.g., :math:`ab` instead of :math:`a \otimes b`. That will be the case
here

Also, since groups are associative, there is no ambiquity in writing
products like, :math:`abc`, without paretheses.

Motivation for Group Definition
-------------------------------

A motivation for the specific group axioms, above, is provided by
considering the assumptions required to solve the simplest equation.

Let :math:`ax = b`, where :math:`a,b,x` are elements of a group,
:math:`G`,

.. raw:: html

   <p>

and solve for :math:`x`:

.. raw:: html

   </p>

-  from assumption #1, all of the operations here will be well-defined

-  

   .. raw:: html

      <p>

   from assumption #4, :math:`a` has inverse
   :math:`a^{-1} \Rightarrow a^{-1}(ax) = a^{-1}b`

   .. raw:: html

      </p>

-  

   .. raw:: html

      <p>

   from assumption #2, G is associatve
   :math:`\Rightarrow (a^{-1}a)x = a^{-1}b`

   .. raw:: html

      </p>

-  

   .. raw:: html

      <p>

   from assumption #4, :math:`a^{-1}a=e \Rightarrow ex = a^{-1}b`

   .. raw:: html

      </p>

-  

   .. raw:: html

      <p>

   from assumption #3, :math:`ex = x \Rightarrow x = a^{-1}b`

   .. raw:: html

      </p>

The assumptions are exactly those that make up the group definition.

Note that cummutability is not necessary.

Groups and Geometric Symmetry
-----------------------------

TBD

Abelian Groups
--------------

An abelian group is a group where the binary operation is commutative.

That is, for all :math:`a,b \in S \Rightarrow ab = ba`.

Abelian groups are also referred to as commutative groups.

Finite Groups
-------------

A finite group is a group, :math:`G = \langle S, \cdot \rangle`, where
the number of elements is finite.

So, for example, :math:`S = \{e, a_1, a_2, a_3, ... , a_{n-1}\}`. In
this case, we say that the order of :math:`G` is :math:`n`.

For infinite groups, the operator, :math:`\otimes`, is usually defined
according to a rule or function. This can also be done for finite
groups, however, in the finite case, it also possible to define the
operator via a multiplication table, where each row and each column
represents one of the finite number of elements.

For example, if :math:`S = \{E, H, V, R\}`, where :math:`E` is the
identity element, then a possible multiplication table would be as shown
below (i.e., the Klein-4 Group):

= = = = =
. E H V R
= = = = =
E E H V R
H H E R V
V R R E H
R E V H E
= = = = =

Subgroups
---------

Given a group, :math:`G = \langle S, \otimes \rangle`, suppose that
:math:`T \subseteq S`, such that :math:`H = \langle T, \otimes \rangle`
forms a group itself, then :math:`H` is said to be a subgroup of
:math:`G`, usually denoted by :math:`H \le G`.

There are two trivial subgroups of :math:`G`: the group consisting of
just the identity element, :math:`\langle \{e\}, \otimes \rangle`, and
entire group, :math:`G`, itself. All other subgroups are proper
subgroups.

A subgroup, :math:`H`, is a normal subgroup of a group G, if, for all
elements :math:`g \in G` and for all
:math:`h \in H \Rightarrow ghg^{-1} \in H`.

Isomorphisms
------------

TBD

References
----------

TBD
