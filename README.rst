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

.. _USAGE.rst: USAGE.rst

See USAGE.rst_ for details.

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

Made with 💖 and 🍔
====================

.. image:: https://raw.githubusercontent.com/LuisAlejandro/candyshop/develop/docs/_static/author-banner.svg

.. _LuisAlejandroTwitter: https://twitter.com/LuisAlejandro
.. _LuisAlejandroGitHub: https://github.com/LuisAlejandro
.. _luisalejandro.org: https://luisalejandro.org

|

    Web luisalejandro.org_ · GitHub `@LuisAlejandro`__ · Twitter `@LuisAlejandro`__

__ LuisAlejandroGitHub_
__ LuisAlejandroTwitter_
