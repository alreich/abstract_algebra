.. _api:

API Reference
=============

Magma
-----

.. autoclass:: finite_algebras.Magma
    :members:
    :special-members:
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
    :special-members: __contains__, __eq__, __getitem__, __len__, __mul__
    :undoc-members:
    :private-members:

Group Generators
----------------

.. autofunction:: finite_algebras.generate_cyclic_group
.. autofunction:: finite_algebras.generate_symmetric_group
.. autofunction:: finite_algebras.generate_powerset_group

Utilities
---------
.. autofunction:: finite_algebras.index_table_from_name_table
.. autofunction:: finite_algebras.generate_all_group_tables
.. autofunction:: finite_algebras.tables_to_groups

Cayley Table
------------

.. autoclass:: cayley_table.CayleyTable
    :members:
    :special-members: __eq__, __repr__, __str__, __getitem__
    :undoc-members:
    :private-members:

.. autofunction:: cayley_table.get_duplicates
.. autofunction:: cayley_table.check_inputs

Permutations
------------

.. autoclass:: permutations.Perm
    :members:
    :special-members: __eq__, __len__, __hash__, __mul__, __repr__
    :undoc-members:
    :private-members:

Ring
----

.. autoclass:: finite_algebras.Ring
    :members:
    :special-members:
    :undoc-members:
    :private-members:

.. autofunction:: finite_algebras.powerset_mult_table
.. autofunction:: finite_algebras.generate_powerset_ring

Field
-----

.. TBD
