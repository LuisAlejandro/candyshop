=========
Use cases
=========

Here you can consult practical uses for some of the Odoo Candyshop functions.
For a more detailed review on what you can do with it, we recommend you to read
the :doc:`api` documentation.

The ``Module`` class
====================

The ``Module`` class is an abstraction of an Odoo Module. You can perform
several operations to access the module information::

    >>> from candyshop.bundle import Module

    >>> # Create a Module instance
    >>> module = Module('path/to/module')

    >>> # Query for data
    >>> print(module.path)
    >>> print(module.manifest)

    >>> # Query information in manifest file
    >>> print(module.properties.name)
    >>> print(module.properties.version)
    >>> print(module.properties.depends)


The ``Bundle`` class
====================

The ``Bundle`` class is an abstraction of a *Group* of modules, often referred
to as *Addons*. Here you can see

The ``OdooEnvironment`` class
=============================

#. Create an Odoo Environment, add bundles and make reports.
   ::

        from candyshop.environment import OdooEnvironment

        # Create an Environment
        env = OdooEnvironment()

        # Insert bundles
        env.insert_bundles(['./path-to-bundle', '../addons', '../etc'])

        # If any bundle has an oca_dependencies.txt file,
        # clone its dependencies
        env.satisfy_oca_dependencies()

        # Make a report about record ids that reference modules
        # which are not present in the environment
        env.get_notmet_record_ids_report()

        # Make a report about dependencies that are not present in
        # the environment
        env.get_notmet_dependencies_report()
