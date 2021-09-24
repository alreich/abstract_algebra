Groups, Monoids, Semigroups, & Magmas
=====================================

This section provides numerous examples of finite algebra creation and
manipulation, specifically, for algebras with only one set of elements
and one binary operation: Groups, Monoids, Semigroups, and Magmas. See
the previous section, “Definitions”, for definitions of these algebraic
structures.

Internal Representation of Groups, Monoids, Semigroups, & Magmas
----------------------------------------------------------------

Internally, a ``FiniteAlgebra`` can take several different forms. For
algebras that have only one set of elements and one binary operation,
such as Groups, Monoids, Semigroups, and Magmas, the internal
representation is as shown below.

-  **name**: (``str``) A short name for the algebra;
-  **description**: (``str``) Any additional, useful information about
   the algebra;
-  **elements**: (``list`` of ``str``) Names of the algebras’s elements.
-  **table**: (``list`` of ``list`` of ``int``) The algebra’s
   multiplication table, where each list in the list represents a row of
   the table, and each integer represents the position of an element in
   ‘element_names’. For input and ouput, element names (``str``) may be
   used in the table, rather than integers, but integers are still used
   internally.

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

``make_finite_algebra`` uses the input table to determine what type of
algebra it supports and returns the appropriate algebra.

In the following examples, the only algebra constructor used is
``make_finite_algebra``.

Group
~~~~~

We’ll start the examples in the middle of the hierarchy of algebras,
with Groups.

The element names in a finite algebra’s element list are **always**
represented as strings; and, although a Cayley table can be entered (and
displayed) using the same string names, within a Cayley table they are
represented and displayed using a 2-dimensional, square array of
integers that denote the positions of element names in the element list.
To see this, look at the following input table vs. output table.

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



Following Python convention, the representation (``__repr__``) of an
algebra can be used to construct the same algebra, via cut-and-paste.

On the other hand, printing an algebra converts it to a compact string
representation that contains its class name, algebra name, and the
unique ID of the algebra instance:

.. code:: ipython3

    >>> print(z3)


.. parsed-literal::

    <Group:Z3, ID:140728899848400>


The ``about`` method prints information about an algebra. Set
``use_element_names`` to ``True`` to see the Cayley table printed using
element names (``str``) rather than element positions (``int``).

.. code:: ipython3

    >>> z3.about(use_table_names=True)


.. parsed-literal::

    
    ** Group **
    Name: Z3
    Instance ID: 140728899848400
    Description: Cyclic group of order 3
    Order: 3
    Identity: e
    Associative? Yes
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a', 'a^2']
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       a     a^2       3
          2     a^2       a       3
    Cayley Table (showing names):
    [['e', 'a', 'a^2'], ['a', 'a^2', 'e'], ['a^2', 'e', 'a']]


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
element, if it exists. This method is implemented as a property, so no
trailing parentheses (“()”) are required. See the API documentation to
see what other methods are implemented as properties.

If the identity doesn’t exist, then ``None`` is returned.

.. code:: ipython3

    >>> z3.identity




.. parsed-literal::

    'e'



.. code:: ipython3

    >>> z3.inv('a')  # Get an element's inverse, if it exists




.. parsed-literal::

    'a^2'



Internal to algebras, tables are stored as instances of the
``CayleyTable`` class. Under normal usage, there should be no need to
deal with a ``CayleyTable``.

.. code:: ipython3

    >>> z3.table




.. parsed-literal::

    CayleyTable([[0, 1, 2], [1, 2, 0], [2, 0, 1]])



Binary Operation
~~~~~~~~~~~~~~~~

The binary operation, implicitely defined by a Cayley table, is made
explicit by an algebra’s ``op`` method. Obviously, ``op`` should be able
to take two algebraic elements as input, and it does, but it can also
take any number of inputs from none to as many as needed, as shown
below.

For the example Group, Z3, created above, we have that
:math:`a \circ a = a^2` and this is verified below.

.. code:: ipython3

    >>> z3.op('a', 'a')




.. parsed-literal::

    'a^2'



Also, the following holds,
:math:`a \circ a \circ a = a \circ a^2 = a^2 \circ a = e`, as shown
below

.. code:: ipython3

    >>> z3.op('a', 'a', 'a') == z3.op('a', 'a^2') == z3.op('a^2', 'a') == 'e'




.. parsed-literal::

    True



If only one argument is given to the binary operation, then that
argument is simply returned; unless it is not a valid element of the
algebra, in which case an exception is raised.

.. code:: ipython3

    >>> z3.op('a')




.. parsed-literal::

    'a'



With zero arguments, ``op`` returns the identity, if it exists.

.. code:: ipython3

    >>> z3.op()




.. parsed-literal::

    'e'



Note, however, that ``op`` can only be used with elements (``str``) that
are members of an algebra’s element list. So, since ‘a^3’ is not a
string in Z3’s element list, it cannot be used in ``op``.

.. code:: ipython3

    >>> try:
    >>>     z3.op('a^3')
    >>> except Exception as exc:
    >>>     print(exc)


.. parsed-literal::

    a^3 is not a valid element name


**A final word on ``op``**

Since the binary operation here is implemented as a function (i.e., in
prefix notation) rather than an infix operator, the convention for
handling none, one, or more arguments is borrowed from the long-standing
Lisp convention for addition and subtraction.

“Subtraction” in Groups
~~~~~~~~~~~~~~~~~~~~~~~

The method, ``sub``, is a convenience method for computing
“:math:`x - y`”, that is, :math:`x \circ y^{-1}` where
:math:`x, y \in S` and :math:`\langle S, \circ \rangle` is a Group.

.. code:: ipython3

    >>> x = 'a'
    >>> y = 'a^2'
    >>> print(f"For example, \"{x} - {y}\" = {x} * inv({y}) = {x} * {z3.inv(y)} = {z3.op(x, z3.inv(y))}")


.. parsed-literal::

    For example, "a - a^2" = a * inv(a^2) = a * a = a^2


Or, more succinctly using ``sub``:

.. code:: ipython3

    >>> z3.sub(x, y)




.. parsed-literal::

    'a^2'



Magma
~~~~~

A Magma is the most fundamental type of algebra that we can instantiate
with ``make_finite_algebra``.

**Magma** - a set with a binary operation:
:math:`\langle S, \circ \rangle`, where :math:`S` is a finite set and
:math:`\circ: S \times S \to S`

**Example: Rock-Paper-Scissors**

-  paper covers rock
-  rock crushes scissors
-  scissors cuts paper

Expressing this in algebraic form (see
https://en.wikipedia.org/wiki/Commutative_magma), where p *beats* r, and
r *beats* s, and s *beats* p, we have:

-  :math:`\langle S, \circ \rangle`, where :math:`S = \{r,p,s\}`
-  For all :math:`x, y \in S`, if :math:`x` *beats* :math:`y`, then
   :math:`x \circ y = y \circ x = x`
-  Also, for all :math:`x \in S`, :math:`x \circ x = x`

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

    
    ** Magma **
    Name: RPS
    Instance ID: 140727556455504
    Description: Rock, Paper, Scissors Magma
    Order: 3
    Identity: None
    Associative? No
    Commutative? Yes
    Cyclic?: No
    Elements: ['r', 'p', 's']
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 1, 0], [1, 1, 2], [0, 2, 2]]


Paper beats Rock:

.. code:: ipython3

    >>> rps.op('r', 'p')




.. parsed-literal::

    'p'



.. code:: ipython3

    >>> if rps.identity is None:
    >>>     print("RPS does not have an identity element")


.. parsed-literal::

    RPS does not have an identity element


For convenience, the method, ``has_identity``, returns True or False,
depending on whether an algebra has an identity.

.. code:: ipython3

    >>> rps.has_identity()




.. parsed-literal::

    False



The next section demonstrates that a Magma can have an identity element,
as long as the Magma is not associative, otherwise
``make_finite_algebra`` would output a Monoid.

A convention often used with abstract algebras is to denote an identity
element with the letter “e”. That is done in the example below, but the
function, ``make_finite_algebra``, ignores that convention and derives
the identity element, if it exists, from the table properties alone.

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

    
    ** Magma **
    Name: Whatever
    Instance ID: 140727556443984
    Description: Magma with Identity
    Order: 3
    Identity: e
    Associative? No
    Commutative? No
    Cyclic?: Yes
      Generators: ['b']
    Elements: ['e', 'a', 'b']
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 1, 2], [1, 0, 1], [2, 2, 1]]


Semigroup
~~~~~~~~~

**Semigroup** – an associative Magma: for any
:math:`a,b,c \in S \Rightarrow a \circ (b \circ c) = (a \circ b) \circ c`

**Example:**

Reference: `Groupoids and Smarandache
Groupoids <https://arxiv.org/ftp/math/papers/0304/0304490.pdf>`__ by W.
B. Vasantha Kandasamy

.. code:: ipython3

    >>> sg = make_finite_algebra(
        'Example 1.4.1',
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

    
    ** Semigroup **
    Name: Example 1.4.1
    Instance ID: 140727289003728
    Description: See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    Order: 6
    Identity: None
    Associative? Yes
    Commutative? No
    Cyclic?: No
    Elements: ['a', 'b', 'c', 'd', 'e', 'f']
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



This Semigroup is regular and every element is a weak inverse of every
other element.

.. code:: ipython3

    >>> sg.is_regular()




.. parsed-literal::

    True



.. code:: ipython3

    >>> sg.weak_inverses()




.. parsed-literal::

    {'a': ['a', 'c', 'e'],
     'b': ['b', 'd', 'f'],
     'c': ['a', 'c', 'e'],
     'd': ['b', 'd', 'f'],
     'e': ['a', 'c', 'e'],
     'f': ['b', 'd', 'f']}



Monoid
~~~~~~

**Monoid** – a Semigroup with identity element: :math:`\exists e \in S`,
such that, for all :math:`a \in S, a \circ e = e \circ a = a`

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

    
    ** Monoid **
    Name: M4
    Instance ID: 140727556504912
    Description: Example of a commutative monoid
    Order: 4
    Identity: b
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements: ['a', 'b', 'c', 'd']
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

The path to the JSON file is constructed by using Python’s
*os.path.join* to join strings together. So, the quantity, ``v4_json``,
below, is a string. And then we’ve used Jupyter Notebook’s ability to
“reach out” into the external environment (via “!”) and printout the
file using the UNIX command, ``cat``.

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


And, here’s the **algebra** that is loaded from the JSON file:

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

The examples, below, show a Magma and a Group being converted into
dictionaries.

.. code:: ipython3

    >>> rps.to_dict()




.. parsed-literal::

    {'name': 'RPS',
     'description': 'Rock, Paper, Scissors Magma',
     'elements': ['r', 'p', 's'],
     'table': [[0, 1, 0], [1, 1, 2], [0, 2, 2]]}



Note that the only difference between the JSON and Python dictionary
representations of an algebra is the type of quotes used aroung strings.
JSON requires that double quotes be used, while Python uses single
quotes by default.

In the second example, below, the **type** of algebra (e.g., Magma) can
be included in the dictionary for readability, however, the *type* field
is ignored when ``make_finite_algebra`` reads a dictionary or JSON file.
Again, the type of algebra and its properties are always derived from
its Cayley table.

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



Instantiate Algebra from Python Dictionary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For these examples, we’ll use the Python dictionaries, created above, as
inputs to ``make_finite_algebra``.

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



Convert Algebra to JSON String
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note that the conversion example here outputs a single Python string
(i.e., enclosed by single quotes), within which, all the strings are
enclosed by double quotes, as required by JSON.

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
``make_finite_algebra``, as shown below, using the JSON string
constructed above:

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

There are several functions for autogenerating finite algebras of any
desired size:

**Groups**

-  ``generate_cyclic_group(n)``: :math:`Z_n`, where
   :math:`a \circ b \equiv a+b` mod :math:`n`, where
   :math:`a,b \in \{0,1,...,n-1\}`; order is :math:`n`
-  ``generate_symmetric_group(n)``: :math:`S_n`, where :math:`\circ` is
   composition of permutations of :math:`(0, 1, ..., n-1)`; order is
   :math:`n!`
-  ``generate_powerset_group(n)``:
   :math:`A \circ B \equiv A \bigtriangleup B`, where
   :math:`A,B \in P(\{0, 1, ..., n-1\})`; order is :math:`2^n`

**Monoid**

-  ``generate_commutative_monoid(n)``: :math:`a \circ b \equiv ab` mod
   :math:`n`, where :math:`a,b \in \{0,1,...,n-1\}`; order is :math:`n`

Autogenerated Cyclic Group
~~~~~~~~~~~~~~~~~~~~~~~~~~

A cyclic group of any desired order can be generated. A very small one
is created, below, because it will be used later to demonstrate Direct
Products and Isomorphisms.

.. code:: ipython3

    >>> from finite_algebras import generate_cyclic_group
    
    >>> z2 = generate_cyclic_group(2)
    
    >>> z2.about()


.. parsed-literal::

    
    ** Group **
    Name: Z2
    Instance ID: 140727825364048
    Description: Autogenerated cyclic Group of order 2
    Order: 2
    Identity: e
    Associative? Yes
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a']
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

    
    ** Group **
    Name: S3
    Instance ID: 140727825363920
    Description: Autogenerated symmetric Group on 3 elements
    Order: 6
    Identity: (1, 2, 3)
    Associative? Yes
    Commutative? No
    Cyclic?: No
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

    
    ** Group **
    Name: PS3
    Instance ID: 140727825366608
    Description: Autogenerated Group on the powerset of 3 elements, with symmetric difference operator
    Order: 8
    Identity: {}
    Associative? Yes
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

    
    ** Monoid **
    Name: M7
    Instance ID: 140727825353872
    Description: Autogenerated commutative Monoid of order 7
    Order: 7
    Identity: a1
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements: ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6']
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

    
    ** Group **
    Name: Z2_x_Z2_x_Z2
    Instance ID: 140727289000848
    Description: Direct product of Z2_x_Z2 & Z2
    Order: 8
    Identity: e:e:e
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
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

    
    ** Monoid **
    Name: M3_x_M3
    Instance ID: 140727825351184
    Description: Direct product of M3 & M3
    Order: 9
    Identity: a1:a1
    Associative? Yes
    Commutative? Yes
    Cyclic?: No
    Elements: ['a0:a0', 'a0:a1', 'a0:a2', 'a1:a0', 'a1:a1', 'a1:a2', 'a2:a0', 'a2:a1', 'a2:a2']
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

If two algebras are isomorphic, then the mapping between their elements
is returned as a Python dictionary.

Here is a well-known example, using two small groups created above, v4
and the direct product of z2 with itself, z2 \* z2:

Group Isomorphism
~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> z2_sqr = z2 * z2
    
    >>> v4.isomorphic(z2_sqr)




.. parsed-literal::

    {'e': 'e:e', 'h': 'e:a', 'v': 'a:e', 'r': 'a:a'}



If two algebras are not isomorphic, then ``False`` is returned.

.. code:: ipython3

    >>> z4 = generate_cyclic_group(4)
    
    >>> z4.isomorphic(z2_sqr)




.. parsed-literal::

    False



Magma Isomorphism
~~~~~~~~~~~~~~~~~

In this example, we’ll use a made-up Magma, similar to Rock, Paper,
Scissors.

**Water, Fire, Stick:**

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

An algebra can contain subalgebras (e.g., a Group can have subgroups).
In fact, sometimes the subalgebra may not even be of the same type as
the parent algebra. For, example, we’ll see below that a Semigroup can
contain a Group as a subalgebra.

The method, ``proper_subalgebras``, extracts all possible proper
subalgebras that exist within an algebra, regardless of whether they are
isomorphic to each other or not, or even of the same algebraic class as
the parent algebra.

A subalgebra is constructed from a subset of elements that are closed
under the algebra’s binary operation.

Example: Proper Subgroups
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    >>> z8 = generate_cyclic_group(8)
    >>> z8.about()


.. parsed-literal::

    
    ** Group **
    Name: Z8
    Instance ID: 140727556576656
    Description: Autogenerated cyclic Group of order 8
    Order: 8
    Identity: e
    Associative? Yes
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a', 'a^3', 'a^5', 'a^7']
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1       a     a^7       8
          2     a^2     a^6       4
          3     a^3     a^5       8
          4     a^4     a^4       2
          5     a^5     a^3       8
          6     a^6     a^2       4
          7     a^7       a       8
    Cayley Table (showing indices):
    [[0, 1, 2, 3, 4, 5, 6, 7],
     [1, 2, 3, 4, 5, 6, 7, 0],
     [2, 3, 4, 5, 6, 7, 0, 1],
     [3, 4, 5, 6, 7, 0, 1, 2],
     [4, 5, 6, 7, 0, 1, 2, 3],
     [5, 6, 7, 0, 1, 2, 3, 4],
     [6, 7, 0, 1, 2, 3, 4, 5],
     [7, 0, 1, 2, 3, 4, 5, 6]]


.. code:: ipython3

    >>> z8_proper_subs = z8.proper_subalgebras()
    
    >>> for sub in z8_proper_subs:
    >>>     sub.about()


.. parsed-literal::

    
    ** Group **
    Name: Z8_subalgebra_0
    Instance ID: 140727825438672
    Description: Subalgebra of: Autogenerated cyclic Group of order 8
    Order: 4
    Identity: e
    Associative? Yes
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a^2', 'a^6']
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1     a^2     a^6       4
          2     a^4     a^4       2
          3     a^6     a^2       4
    Cayley Table (showing indices):
    [[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]]
    
    ** Group **
    Name: Z8_subalgebra_1
    Instance ID: 140727825439760
    Description: Subalgebra of: Autogenerated cyclic Group of order 8
    Order: 2
    Identity: e
    Associative? Yes
    Commutative? Yes
    Cyclic?: Yes
      Generators: ['a^4']
    Elements:
       Index   Name   Inverse  Order
          0       e       e       1
          1     a^4     a^4       2
    Cayley Table (showing indices):
    [[0, 1], [1, 0]]


Normal Subgroups
~~~~~~~~~~~~~~~~

Both of the subgroups of Z8, derived above, are **normal**:

.. code:: ipython3

    >>> [z8.is_normal(g) for g in z8_proper_subs]




.. parsed-literal::

    [True, True]



Proper Subalgebras up to Isomorphism
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The function, ``partition_into_isomorphic_lists``, partitions a list of
algebras (subgroups in this case) into a list of lists, where each
sublist contains subalgebras that are all isomophic to each other.

The function, ``about_isomorphic_partitions``, prints out a summary of
information about the partitions output by
``partition_into_isomorphic_list``.

.. code:: ipython3

    from finite_algebras import partition_into_isomorphic_lists, about_isomorphic_partitions

The example, below, uses the autogenerated powerset group, **ps3**, that
was created earlier.

.. code:: ipython3

    >>> ps3_proper_subs = ps3.proper_subalgebras()
    
    >>> partitions = partition_into_isomorphic_lists(ps3_proper_subs)
    
    >>> about_isomorphic_partitions(ps3, partitions)


.. parsed-literal::

    
    Subalgebras of <Group:PS3, ID:140727825366608>
      There are 2 unique proper subalgebras, up to isomorphism, out of 14 total subalgebras.
      as shown by the partitions below:
    
    7 Isomorphic Commutative Normal Groups of order 4 with identity '{}':
          Group: PS3_subalgebra_0: ['{}', '{1}', '{2}', '{1, 2}']
          Group: PS3_subalgebra_4: ['{}', '{1}', '{0, 2}', '{0, 1, 2}']
          Group: PS3_subalgebra_6: ['{}', '{0}', '{2}', '{0, 2}']
          Group: PS3_subalgebra_7: ['{}', '{0, 1}', '{0, 2}', '{1, 2}']
          Group: PS3_subalgebra_8: ['{}', '{0}', '{1}', '{0, 1}']
          Group: PS3_subalgebra_10: ['{}', '{2}', '{0, 1}', '{0, 1, 2}']
          Group: PS3_subalgebra_11: ['{}', '{0}', '{1, 2}', '{0, 1, 2}']
    
    7 Isomorphic Commutative Normal Groups of order 2 with identity '{}':
          Group: PS3_subalgebra_1: ['{}', '{1, 2}']
          Group: PS3_subalgebra_2: ['{}', '{0, 1, 2}']
          Group: PS3_subalgebra_3: ['{}', '{2}']
          Group: PS3_subalgebra_5: ['{}', '{0, 1}']
          Group: PS3_subalgebra_9: ['{}', '{0, 2}']
          Group: PS3_subalgebra_12: ['{}', '{1}']
          Group: PS3_subalgebra_13: ['{}', '{0}']
    


Subalgebras of Semigroups, Etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recall the Semigroup example from above:

.. code:: ipython3

    >>> sg.about()


.. parsed-literal::

    
    ** Semigroup **
    Name: Example 1.4.1
    Instance ID: 140727289003728
    Description: See: Groupoids and Smarandache Groupoids by W. B. Vasantha Kandasamy
    Order: 6
    Identity: None
    Associative? Yes
    Commutative? No
    Cyclic?: No
    Elements: ['a', 'b', 'c', 'd', 'e', 'f']
    Has Inverses? No
    Cayley Table (showing indices):
    [[0, 3, 0, 3, 0, 3],
     [1, 4, 1, 4, 1, 4],
     [2, 5, 2, 5, 2, 5],
     [3, 0, 3, 0, 3, 0],
     [4, 1, 4, 1, 4, 1],
     [5, 2, 5, 2, 5, 2]]


As we will see, below, the Semigroup, sg, contains 4 unique subalgebras,
up to isomorphism:

-  3 Semigroups and
-  1 Group

However, instead of running the three commands:

-  sg_proper_subs = sg.proper_subalgebras()
-  partitions = partition_into_isomorphic_lists(sg_proper_subs)
-  about_isomorphic_partitions(sg, partitions)

as we did above, we’ll use a single function, ``about_subalgebras``,
that wraps up those three commands into one, for convenience. It also
returns the partitions, but we’ll ignore the returned value in this
example:

.. code:: ipython3

    >>> from finite_algebras import about_subalgebras

.. code:: ipython3

    >>> _ = about_subalgebras(sg)


.. parsed-literal::

    
    Subalgebras of <Semigroup:Example 1.4.1, ID:140727289003728>
      There are 4 unique proper subalgebras, up to isomorphism, out of 10 total subalgebras.
      as shown by the partitions below:
    
    3 Isomorphic Semigroups of order 4:
          Semigroup: Example 1.4.1_subalgebra_0: ['a', 'b', 'd', 'e']
          Semigroup: Example 1.4.1_subalgebra_1: ['b', 'c', 'e', 'f']
          Semigroup: Example 1.4.1_subalgebra_6: ['a', 'c', 'd', 'f']
    
    3 Isomorphic Commutative Groups of order 2:
          Group: Example 1.4.1_subalgebra_2: ['a', 'd'] with identity 'a'
          Group: Example 1.4.1_subalgebra_3: ['c', 'f'] with identity 'c'
          Group: Example 1.4.1_subalgebra_9: ['b', 'e'] with identity 'e'
    
    3 Isomorphic Semigroups of order 2:
          Semigroup: Example 1.4.1_subalgebra_4: ['c', 'e']
          Semigroup: Example 1.4.1_subalgebra_5: ['a', 'c']
          Semigroup: Example 1.4.1_subalgebra_8: ['a', 'e']
    
    1 Semigroup of order 3:
          Semigroup: Example 1.4.1_subalgebra_7: ['a', 'c', 'e']
    


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
      15 example algebras are available.
      Use "Examples[INDEX]" to retrieve a specific example,
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


**Example**:

.. code:: ipython3

    >>> alg = ex[3]  # i.e., the 4th algebra in the list, above.
    >>> alg.about(use_table_names=True)


.. parsed-literal::

    
    ** Group **
    Name: Pinter29
    Instance ID: 140727825370000
    Description: Non-abelian group, p.29, 'A Book of Abstract Algebra' by Charles C. Pinter
    Order: 6
    Identity: I
    Associative? Yes
    Commutative? No
    Cyclic?: No
    Elements:
       Index   Name   Inverse  Order
          0       I       I       1
          1       A       A       2
          2       B       D       3
          3       C       C       2
          4       D       B       3
          5       K       K       2
    Cayley Table (showing names):
    [['I', 'A', 'B', 'C', 'D', 'K'],
     ['A', 'I', 'C', 'B', 'K', 'D'],
     ['B', 'K', 'D', 'A', 'I', 'C'],
     ['C', 'D', 'K', 'I', 'A', 'B'],
     ['D', 'C', 'I', 'K', 'B', 'A'],
     ['K', 'B', 'A', 'D', 'C', 'I']]


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
-  `SACK <https://github.com/johnkerl/sack>`__ A simple abstract-algebra
   calculator. Includes some elementary group routines.
