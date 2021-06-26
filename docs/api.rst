.. _api:

API Reference
=============

Group
-----

.. autoclass:: algebras.Group
    :members:
    :special-members: __contains__, __eq__, __getitem__, __len__, __mul__
    :undoc-members:
    :private-members:

Group Generators
----------------

.. autofunction:: algebras.generate_cyclic_group
.. autofunction:: algebras.generate_symmetric_group
.. autofunction:: algebras.generate_powerset_group
.. autofunction:: algebras.powerset
.. autofunction:: algebras.powerset_mult_table

Utilities
---------
.. autofunction:: algebras.index_table_from_name_table
.. autofunction:: algebras.powerset
.. autofunction:: algebras.generate_all_group_tables
.. autofunction:: algebras.tables_to_groups
.. autofunction:: algebras.get_duplicates

Permutation
-----------

.. autoclass:: algebras.Perm
    :members:
    :special-members: __eq__, __len__, __hash__, __mul__, __repr__
    :undoc-members:
    :private-members:

Ring
----

.. autoclass:: algebras.Ring
    :members:
    :special-members:
    :undoc-members:
    :private-members:


Field
-----

.. TBD
