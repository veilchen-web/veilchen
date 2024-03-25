.. image:: http://bottlepy.org/docs/dev/_static/logo_nav.png
  :target: http://bottlepy.org/
  :alt: Bottle Logo
  :align: right

.. image:: https://github.com/bottlepy/bottle/workflows/Tests/badge.svg
    :target: https://github.com/bottlepy/bottle/workflows/Tests
    :alt: Tests Status

.. image:: https://img.shields.io/pypi/v/bottle.svg
    :target: https://pypi.python.org/pypi/bottle/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/l/bottle.svg
    :target: https://pypi.python.org/pypi/bottle/
    :alt: License

.. _jinja2: http://jinja.pocoo.org/
.. _bjoern: https://github.com/jonashaag/bjoern
.. _WSGI: https://wsgi.readthedocs.io/
.. _Python: http://python.org/

=====================================================
Veilchen: A minimal and friendly Python Web Framework
=====================================================

Veilchen is a fast, simple and lightweight WSGI_ micro web-framework for Python_.
It is distributed as a single file module and has no dependencies other than the
`Python Standard Library <http://docs.python.org/library/>`_.
It is a friendly fork of the `Bottle <http://bottlepy.org>`_ project.


* **Routing:** Requests to function-call mapping with support for clean and  dynamic URLs.
* **Templates:** Fast and pythonic `*built-in template engine* <http://bottlepy.org/docs/dev/tutorial.html#tutorial-templates>`_ and support for mako_, jinja2_ and cheetah_ templates.
* **Utilities:** Convenient access to form data, file uploads, cookies, headers and other HTTP-related metadata.
* **Server:** Built-in HTTP development server and support for paste_, fapws3_, bjoern_, `Google App Engine <https://cloud.google.com/appengine/>`_, cherrypy_ or any other WSGI_ capable HTTP server.

Homepage and documentation: https://github.com/veilchen-web/veilchen


Example: "Hello World" in a Veilchen
------------------------------------

.. code-block:: python

  from veilchen import route, run, template

  @route('/hello/<name>')
  def index(name):
      return template('<b>Hello {{name}}</b>!', name=name)

  run(host='localhost', port=8080)

Run this script or paste it into a Python console, then point your browser to `<http://localhost:8080/hello/world>`_. That's it.


Download and Install
--------------------

.. __: https://raw.githubusercontent.com/veilchen-web/veilchen/master/veilchen.py

Install the latest stable release with ``pip install veilchen`` or download `veilchen.py`__ (unstable)
into your project directory.
There are no hard dependencies other than the Python standard library. Veilchen runs with Python version **3.7+**.


License
-------

.. __: https://raw.githubusercontent.com/veilchen-web/veilchen/master/LICENSE

Code and documentation are available according to the MIT License (see LICENSE__).

The Veilchen logo however is *NOT* covered by that license.
It is allowed to use the logo as a link to the Veilchen homepage or in direct context with the unmodified library.
In all other cases, please ask first.
