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

A Semigroup is an associative Magma.

.. autoclass:: finite_algebras.Semigroup
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Monoid
------

A Monoid is a Semigroup with an identity element.

.. autoclass:: finite_algebras.Monoid
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Group
-----

A Group is a Monoid with inverse elements.

.. autoclass:: finite_algebras.Group
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Ring
----

A Ring is an abelian Group with a second binary operation, over which it is a Semigroup, where the second operation distributes over the first operation.

.. autoclass:: finite_algebras.Ring
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Field
-----

A Field is a Ring, where over the second operation it is also an abelian Group.

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

FiniteCompositeAlgebra
----------------------

This is the top-level class for all algebras that are constructed from two sets of elements, scalars and vectors (Modules, VectorSpaces). NOT INTENDED TO BE INSTANTIATED.

.. autoclass:: finite_algebras.FiniteCompositeAlgebra
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

Module
------

A Module is an abelian Group of vectors, V, combined with a Ring of scalars, Re, and a binary operation, R x V -> V.

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

An NDimensionalModule is a Module constructed from a single Ring, where the Group is constructed by computing direct products of the Ring with itself.

.. autoclass:: finite_algebras.NDimensionalModule
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

VectorSpace
-----------

A VectorSpace is an abelian Group of vectors, V, combined with a Field of scalars, S, and a binary operation, S x V -> V.

.. autoclass:: finite_algebras.VectorSpace
    :members:
    :inherited-members:
    :undoc-members:
    :show-inheritance:

NDimensionalVectorSpace
-----------------------

An NDimensionalVectorSpace is a VectorSpace constructed from a single Field, where the Group is constructed by computing direct products of the Field with itself.

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
.. autofunction:: finite_algebras.generate_nxn_matrix_algebra
.. autofunction:: finite_algebras.generate_algebra_from_element_dict

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

Miscellaneous Functions and Utilities
-------------------------------------

The functions here are listed in alphabetical order by module and name

.. autofunction:: cayley_table.about_tables
.. autofunction:: finite_algebras._filter_out_conflicts
.. autofunction:: finite_algebras._no_conflict
.. autofunction:: finite_algebras._no_conflicts
.. autofunction:: finite_algebras.about_isomorphic_partition
.. autofunction:: finite_algebras.about_isomorphic_partitions
.. autofunction:: finite_algebras.about_subalgebras
.. autofunction:: finite_algebras.add_s
.. autofunction:: finite_algebras.are_n
.. autofunction:: finite_algebras.check_associativity
.. autofunction:: finite_algebras.check_dist_of_scalars_over_vec_add
.. autofunction:: finite_algebras.check_dist_of_vec_over_scalar_add
.. autofunction:: finite_algebras.check_module_conditions
.. autofunction:: finite_algebras.check_scaling_by_one
.. autofunction:: finite_algebras.delete_row_col
.. autofunction:: finite_algebras.find_isomorphic_subalgebra
.. autofunction:: finite_algebras.get_duplicates
.. autofunction:: finite_algebras.get_int_forms
.. autofunction:: finite_algebras.get_integer_form
.. autofunction:: finite_algebras.index_table_from_name_table
.. autofunction:: finite_algebras.is_field
.. autofunction:: finite_algebras.is_table_associative
.. autofunction:: finite_algebras.make_cayley_table
.. autofunction:: finite_algebras.make_table_from_xml
.. autofunction:: finite_algebras.module_dot_product
.. autofunction:: finite_algebras.module_sv_mult
.. autofunction:: finite_algebras.np_arr_to_tuple
.. autofunction:: finite_algebras.partition_into_isomorphic_lists
.. autofunction:: finite_algebras.powerset
.. autofunction:: finite_algebras.same_lists_of_lists
.. autofunction:: finite_algebras.symm_diff_of_two_lists_of_lists
.. autofunction:: finite_algebras.tables_to_groups
.. autofunction:: finite_algebras.unpack_components
.. autofunction:: finite_algebras.yes_or_no
.. autofunction:: my_math.divisors
.. autofunction:: my_math.is_relatively_prime
.. autofunction:: my_math.relative_primes
.. autofunction:: my_math.totient
.. autofunction:: my_math.xgcd

