.. _api:

API Reference
=============

Primary Algebra Constructors
----------------------------

.. autofunction:: finite_algebras.make_finite_algebra
.. autofunction:: modules_and_vector_spaces.make_module

Operator
--------

.. autoclass:: finite_algebras.FiniteOperator
    :members:
    :special-members: __call__
    :undoc-members:
    :private-members:

FiniteAlgebra
-------------

.. autoclass:: finite_algebras.FiniteAlgebra
    :members:
    :undoc-members:
    :private-members:

Magma
-----

.. autoclass:: finite_algebras.Magma
    :members:
    :special-members: __contains__, __eq__, __getitem__, __len__, __mul__
    :undoc-members:
    :private-members:

Semigroup
---------

.. autoclass:: finite_algebras.Semigroup
    :members:
    :special-members:
    :undoc-members:
    :private-members:

Monoid
------

.. autoclass:: finite_algebras.Monoid
    :members:
    :special-members:
    :undoc-members:
    :private-members:

Group
-----

.. autoclass:: finite_algebras.Group
    :members:
    :special-members:
    :undoc-members:
    :private-members:

Ring
----

.. autoclass:: finite_algebras.Ring
    :members:
    :special-members:
    :undoc-members:
    :private-members:

Field
-----

.. autoclass:: finite_algebras.Field
    :members:
    :special-members:
    :undoc-members:
    :private-members:

Module
------

.. autofunction:: modules_and_vector_spaces.make_dp_sv_op
.. autoclass:: modules_and_vector_spaces.Module
    :members:
    :special-members:
    :undoc-members:
    :private-members:
.. autofunction:: modules_and_vector_spaces.check_module_conditions

VectorSpace
-----------

.. autoclass:: modules_and_vector_spaces.VectorSpace
    :members:
    :special-members:
    :undoc-members:
    :private-members:

Algebra Generators
------------------

.. autofunction:: finite_algebras.generate_cyclic_group
.. autofunction:: finite_algebras.generate_symmetric_group
.. autofunction:: finite_algebras.generate_powerset_group
.. autofunction:: finite_algebras.generate_commutative_monoid
.. autofunction:: finite_algebras.generate_powerset_ring
.. autofunction:: finite_algebras.generate_algebra_mod_n
.. autofunction:: modules_and_vector_spaces.generate_n_dim_module

Cayley Table
------------

.. autoclass:: cayley_table.CayleyTable
    :members:
    :special-members: __eq__, __repr__, __str__, __getitem__
    :undoc-members:
    :private-members:

Permutations
------------

.. autoclass:: permutations.Perm
    :members:
    :special-members: __eq__, __len__, __hash__, __mul__, __repr__
    :undoc-members:
    :private-members:

Examples
--------

.. autoclass:: finite_algebras.Examples
    :members:
    :special-members: __init__
    :undoc-members:
    :private-members:

Misc Utilities
--------------

.. autofunction:: finite_algebras.generate_all_group_tables
.. autofunction:: finite_algebras.get_duplicates
.. autofunction:: finite_algebras.get_int_forms
.. autofunction:: finite_algebras.get_integer_form
.. autofunction:: finite_algebras.index_table_from_name_table
.. autofunction:: finite_algebras.is_table_associative
.. autofunction:: finite_algebras.make_table_from_xml
.. autofunction:: finite_algebras.partition_into_isomorphic_lists
.. autofunction:: finite_algebras.powerset
.. autofunction:: finite_algebras.tables_to_groups
.. autofunction:: finite_algebras.yes_or_no
