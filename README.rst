.. image:: https://raw.githubusercontent.com/LuisAlejandro/candyshop/develop/docs/_static/banner.svg

..

    An assistant to determine if all your dependencies are declared properly in your odoo module.

.. image:: https://img.shields.io/pypi/v/candyshop.svg
   :target: https://pypi.org/project/candyshop
   :alt: PyPI Package

.. image:: https://img.shields.io/github/release/LuisAlejandro/candyshop.svg
   :target: https://github.com/LuisAlejandro/candyshop/releases
   :alt: Github Releases

.. image:: https://img.shields.io/github/issues/LuisAlejandro/candyshop
   :target: https://github.com/LuisAlejandro/candyshop/issues?q=is%3Aopen
   :alt: Github Issues

.. image:: https://github.com/LuisAlejandro/candyshop/workflows/Push/badge.svg
   :target: https://github.com/LuisAlejandro/candyshop/actions?query=workflow%3APush
   :alt: Push

.. image:: https://coveralls.io/repos/github/LuisAlejandro/candyshop/badge.svg?branch=develop
   :target: https://coveralls.io/github/LuisAlejandro/candyshop?branch=develop
   :alt: Coverage

.. image:: https://cla-assistant.io/readme/badge/LuisAlejandro/candyshop
   :target: https://cla-assistant.io/LuisAlejandro/candyshop
   :alt: Contributor License Agreement

.. image:: https://readthedocs.org/projects/candyshop/badge/?version=latest
   :target: https://readthedocs.org/projects/candyshop/?badge=latest
   :alt: Read The Docs

.. image:: https://img.shields.io/discord/809504357359157288.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2
   :target: https://discord.gg/pVteBmNWZu
   :alt: Discord Channel

|
|

.. _full documentation: https://candyshop.readthedocs.org

Current version: 0.2.1

Candyshop is a helper to determine if all your dependencies are declared
properly. A Candyshop is a place where you can pick sweets and candies from
a list of wonderful options, but choose wisely.

For more information, please read the `full documentation`_.

Features
========

* Access an Odoo Module as an object abstraction.
* Get all module references from all xml files of a module.
* Generate and clone the dependency tree of a group of modules (bundle).
* Generate a virtual enviroment where you can add group of modules.
* Determine which Odoo Modules declare a dependency to another module that is not
  present in the environment.
* Determine which XML files make reference to an Odoo Module that is not present
  in the environment.

Getting started
===============

Installation
------------

.. _PyPI: https://pypi.org/project/candyshop

The ``candyshop`` program is written in python and hosted on PyPI_. Therefore, you can use
pip to install the stable version::

    $ pip install --upgrade candyshop

If you want to install the development version (not recomended), you can install
directlty from GitHub like this::

    $ pip install --upgrade https://github.com/LuisAlejandro/candyshop/archive/master.tar.gz

Usage
-----

Here you can consult practical uses for some of the Candyshop functions.
For a more detailed review on what you can do with it, we recommend you to read
the `api` documentation.

The ``Module`` class
~~~~~~~~~~~~~~~~~~~~

The ``Module`` class is an abstraction of an Odoo Module. You can perform
several operations to access the module information::

    from candyshop.bundle import Module

    # Create a Module instance
    module = Module('path/to/module')

    # Query for data
    print(module.path)
    print(module.manifest)

    # Query information in manifest file
    print(module.properties.name)
    print(module.properties.version)
    print(module.properties.depends)

The ``Bundle`` class
~~~~~~~~~~~~~~~~~~~~

The ``Bundle`` class is an abstraction of a *Group* of modules, often referred
to as *Addons*. Here you can see how to interact with a bundle::

    from candyshop.bundle import Bundle

    # Create a Bundle instance
    bundle = Bundle('path/to/bundle')

    # Query for data
    print(bundle.name)
    print(bundle.path)
    print(bundle.modules)
    print(bundle.oca_dependencies)

The ``Environment`` class
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``Environment`` class is an abstraction of a virtual Odoo Environment.
Think of it as an imaginary container inside of which you can add ``Bundles``
and ask for specific information about them. For example::

    from candyshop.environment import Environment

    # Create an Environment
    env = Environment()

    # Insert bundles
    # If any bundle has an oca_dependencies.txt file,
    # clone its dependencies and insert them as bundles
    env.addbundles(['./path-to-bundle', '../addons', '../etc'])

    # Make a report about dependencies that are not present in
    # the environment
    env.get_notmet_dependencies_report()

    # Make a report about record ids that reference modules
    # which are not present in the environment
    env.get_notmet_record_ids_report()

Getting help
============

.. _Discord server: https://discord.gg/pVteBmNWZu
.. _StackOverflow: http://stackoverflow.com/questions/ask

If you have any doubts or problems, suscribe to our `Discord server`_ and ask for help. You can also
ask your question on StackOverflow_ (tag it ``candyshop``) or drop me an email at luis@collagelabs.org.

Contributing
============

.. _CONTRIBUTING.rst: CONTRIBUTING.rst

See CONTRIBUTING.rst_ for details.


Release history
===============

.. _HISTORY.rst: HISTORY.rst

See HISTORY.rst_ for details.

License
=======

.. _AUTHORS.rst: AUTHORS.rst
.. _GPL-3 License: LICENSE

Copyright 2016-2022, Candyshop Developers (read AUTHORS.rst_ for a full list of copyright holders).

Released under a `GPL-3 License`_.

Made with :heart: and :hamburger:
=================================

.. image:: https://github.com/LuisAlejandro/candyshop/blob/develop/docs/_static/author-banner.svg

.. _LuisAlejandroTwitter: https://twitter.com/LuisAlejandro
.. _LuisAlejandroGitHub: https://github.com/LuisAlejandro
.. _luisalejandro.org: https://luisalejandro.org

|

    Web luisalejandro.org_ · GitHub `@LuisAlejandro`__ · Twitter `@LuisAlejandro`__

__ LuisAlejandroGitHub_
__ LuisAlejandroTwitter_
