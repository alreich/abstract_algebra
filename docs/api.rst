.. _api:

API Reference
=============

The Recommended Algebra Constructor
-----------------------------------

The function, make_finite_algebra, is the recommended way to create any finite algebra. It analyzes the input and returns the appropriate finite algebra: Group, Ring, Field, VectorSpace, Module, Monoid, Semigroup, or Magma.

.. autofunction:: finite_algebras.make_finite_algebra

FiniteOperator
--------------

The FiniteOperator is a callable class that implements the binary operators used by the various algebras supported here. This class is automatically created whenever an algebra is created. It is based on the algebra's Cayley table.

.. autoclass:: finite_algebras.FiniteOperator
    :members:
    :undoc-members:

FiniteAlgebra
-------------

This is the top-level class for all algebras that have a single set of elements (Magma, Quasigroup, Loop, Semigroup, Monoid, Group, Ring, Field). It is an abstract base class (ABC) and is NOT INTENDED TO BE INSTANTIATED.

.. autoclass:: finite_algebras.FiniteAlgebra
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Magma
-----

A Magma is a set of elements with a closed, binary operation.

.. autoclass:: finite_algebras.Magma
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Quasigroup
----------

A Quasigroup is a Magma that has the cancellation property.

.. autoclass:: finite_algebras.Quasigroup
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Loop
----

A Loop is a Quasigroup with an identity element.

.. autoclass:: finite_algebras.Loop
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Semigroup
---------

.. autoclass:: finite_algebras.Semigroup
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Monoid
------

.. autoclass:: finite_algebras.Monoid
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Group
-----

.. autoclass:: finite_algebras.Group
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Ring
----

.. autoclass:: finite_algebras.Ring
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Field
-----

.. autoclass:: finite_algebras.Field
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Support for Infix Notation
--------------------------

The Element class, together with the context manager class, InfixNotation, provide a way to use infix operators (+, -, *, /, **) on an algebra's "elements".

.. autoclass:: finite_algebras.Element
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: finite_algebras.InfixNotation
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

MultipleElementSetAlgebra
-------------------------

This is the top-level class for all algebras that are constructed from two sets of elements, scalars and vectors (Modules, VectorSpaces). NOT INTENDED TO BE INSTANTIATED.

.. autoclass:: finite_algebras.MultipleElementSetAlgebra
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Module
------

.. autofunction:: finite_algebras.module_sv_mult
.. autofunction:: finite_algebras.module_dot_product

.. autoclass:: finite_algebras.Module
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:
.. autofunction:: finite_algebras.check_module_conditions

NDimensionalModule
------------------

.. autoclass:: finite_algebras.NDimensionalModule
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

VectorSpace
-----------

.. autoclass:: finite_algebras.VectorSpace
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

NDimensionalVectorSpace
-----------------------

.. autoclass:: finite_algebras.NDimensionalVectorSpace
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Algebra Generators
------------------

.. autofunction:: finite_algebras.generate_cyclic_group
.. autofunction:: finite_algebras.generate_symmetric_group
.. autofunction:: finite_algebras.generate_powerset_group
.. autofunction:: finite_algebras.generate_relative_primes_group
.. autofunction:: finite_algebras.generate_commutative_monoid
.. autofunction:: finite_algebras.generate_powerset_ring
.. autofunction:: finite_algebras.generate_algebra_mod_n

Cayley Table
------------

.. autoclass:: cayley_table.CayleyTable
    :members:
    :undoc-members:

Permutations
------------

.. autoclass:: permutations.Perm
    :members:
    :undoc-members:

Abstract Matrix
---------------

.. autoclass:: abstract_matrix.AbstractMatrix
    :members:
    :undoc-members:



Examples
--------

.. autoclass:: finite_algebras.Examples
    :members:
    :undoc-members:

Misc Utilities
--------------

.. autofunction:: finite_algebras.relative_primes
.. autofunction:: finite_algebras.divisors
.. autofunction:: finite_algebras.delete_row_col
.. autofunction:: finite_algebras.make_cayley_table
.. autofunction:: finite_algebras.index_table_from_name_table
.. autofunction:: finite_algebras.generate_all_group_tables
.. autofunction:: finite_algebras.get_duplicates
.. autofunction:: finite_algebras.get_int_forms
.. autofunction:: finite_algebras.get_integer_form
.. autofunction:: finite_algebras.is_table_associative
.. autofunction:: finite_algebras.make_table_from_xml
.. autofunction:: finite_algebras.partition_into_isomorphic_lists
.. autofunction:: finite_algebras.powerset
.. autofunction:: finite_algebras.tables_to_groups
.. autofunction:: finite_algebras.yes_or_no
