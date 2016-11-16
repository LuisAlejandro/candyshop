.. image:: https://cdn.rawgit.com/LuisAlejandro/odoo-candyshop/master/docs/_static/banner.svg

-----

.. image:: https://img.shields.io/pypi/v/odoo-candyshop.svg
           :target: https://pypi.python.org/pypi/odoo-candyshop

.. image:: https://readthedocs.org/projects/odoo-candyshop/badge/?version=latest
           :target: https://readthedocs.org/projects/odoo-candyshop/?badge=latest

.. image:: https://img.shields.io/travis/LuisAlejandro/odoo-candyshop.svg
           :target: https://travis-ci.org/LuisAlejandro/odoo-candyshop

.. image:: https://coveralls.io/repos/github/LuisAlejandro/odoo-candyshop/badge.svg?branch=master
           :target: https://coveralls.io/github/LuisAlejandro/odoo-candyshop?branch=master

.. image:: https://www.quantifiedcode.com/api/v1/project/9963672ff8484d7ea498b91b2f44e555/badge.svg
           :target: https://www.quantifiedcode.com/app/project/9963672ff8484d7ea498b91b2f44e555

Odoo Candyshop is a helper to determine if all your dependencies are declared
properly. A Candyshop is a place where you can pick sweets and candies from
a list of wonderful options ... but choose wisely.

* Free software: AGPL-3
* Documentation: https://odoo-candyshop.readthedocs.org.

Features
--------

* Access an Odoo Module as an object abstraction.
* Get all module references from all xml files of a module.
* Generate and clone the dependency tree of a group of modules (bundle).
* Generate a virtual enviroment where you can add group of modules.
* Determine which Odoo Modules declare a dependency to another module that is not
  present in the environment.
* Determine which XML files make reference to an Odoo Module that is not present
  in the environment.
