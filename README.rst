.. image:: https://rawcdn.githack.com/CollageLabs/candyshop/bd7fd97adee104d1e906130ec695f61368586d31/docs/_static/banner.svg

..

    An assistant to determine if all your dependencies are declared properly in your odoo module.

.. image:: https://img.shields.io/github/release/CollageLabs/candyshop.svg
   :target: https://github.com/CollageLabs/candyshop/releases
   :alt: Github Releases

.. image:: https://img.shields.io/github/issues/CollageLabs/candyshop
   :target: https://github.com/CollageLabs/candyshop/issues?q=is%3Aopen
   :alt: Github Issues

.. image:: https://github.com/CollageLabs/candyshop/workflows/Push/badge.svg
   :target: https://github.com/CollageLabs/candyshop/actions?query=workflow%3APush
   :alt: Push

.. image:: https://codeclimate.com/github/CollageLabs/candyshop/badges/gpa.svg
   :target: https://codeclimate.com/github/CollageLabs/candyshop
   :alt: Code Climate

.. image:: https://snyk.io/test/github/CollageLabs/candyshop/badge.svg
   :target: https://snyk.io/test/github/CollageLabs/candyshop
   :alt: Snyk

.. image:: https://cla-assistant.io/readme/badge/CollageLabs/candyshop
   :target: https://cla-assistant.io/CollageLabs/candyshop
   :alt: Contributor License Agreement

.. image:: https://img.shields.io/pypi/v/candyshop.svg
   :target: https://pypi.python.org/pypi/candyshop
   :alt: PyPI Package

.. image:: https://readthedocs.org/projects/candyshop/badge/?version=latest
   :target: https://readthedocs.org/projects/candyshop/?badge=latest
   :alt: Read The Docs

.. image:: https://img.shields.io/badge/chat-discord-ff69b4.svg
   :target: https://discord.gg/GMm3R76RQ2
   :alt: Discord Channel

|
|

.. _full documentation: https://candyshop.readthedocs.org

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

.. _PyPI: https://pypi.python.org/pypi/candyshop

The ``candyshop`` program is written in python and hosted on PyPI_. Therefore, you can use
pip to install the stable version::

    $ pip install --upgrade candyshop

If you want to install the development version (not recomended), you can install
directlty from GitHub like this::

    $ pip install --upgrade https://github.com/CollageLabs/candyshop/archive/master.tar.gz

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

.. _Gitter Chat: https://gitter.im/CollageLabs/candyshop
.. _StackOverflow: http://stackoverflow.com/questions/ask

If you have any doubts or problems, suscribe to our `Gitter Chat`_ and ask for help. You can also
ask your question on StackOverflow_ (tag it ``pypicontents``) or drop me an email at luis@collagelabs.org.

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

.. _COPYING.rst: COPYING.rst
.. _AUTHORS.rst: AUTHORS.rst
.. _GPL-3 License: LICENSE.rst

Copyright 2016-2017, Candyshop Developers (read AUTHORS.rst_ for a full list of copyright holders).

Released under a `GPL-3 License`_ (read COPYING.rst_ for license details).

Made with :heart: and :hamburger:
=================================

.. image:: https://rawcdn.githack.com/CollageLabs/candyshop/4fc50d0f22c7c221275586b193b9e0b3170a0340/docs/_static/promo-open-source.svg

.. _CollageLabsTwitter: https://twitter.com/CollageLabs
.. _CollageLabsGitHub: https://github.com/CollageLabs
.. _collagelabs.org: http://collagelabs.org

|

    Web collagelabs.org_ · GitHub `@CollageLabs`__ · Twitter `@CollageLabs`__

__ CollageLabsGitHub_
__ CollageLabsTwitter_

|
|