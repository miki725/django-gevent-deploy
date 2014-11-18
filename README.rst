Gevent Deploy
=============

.. image:: https://badge.fury.io/py/django-gevent-deploy.png
    :target: http://badge.fury.io/py/django-gevent-deploy

This library adds a simple hook into Django's ``manage.py`` to be able to start gevent's WSGI
server to serve the Django project.

Install
-------

Install the library into your Python installation via ``pip``::

    pip install django-gevent-deploy

Then add the library into ``INSTALLED_APPS`` within Django's project ``settings.py``::

    INSTALLED_APPS = (
        ...
        'django_gevent_deploy',
    )

Configuration
-------------

You may add two settings to your ``settings.py``:

``GEVENT_ADDR_PORT``
~~~~~~~~~~~~~~~~~~~~

Specifies what address and what port should be used for the gevent's WSGI server.
Must be a **string** and of the ``[[addr:]port]`` format::

    '8000'            # default
    'localhost:8000'
    '127.0.0.1:8000'

``GEVENT_POOL_SIZE``
~~~~~~~~~~~~~~~~~~~~

Specifies the number of greenlets gevent can spawn for the server. Can be ``None``
or an integer value::

    None              # default
    1
    100

Usage
-----

To start the gevent's WSGI server, simply call ``rungevent`` in ``manage.py``. The command
accepts optional argumets which are the same as described in `Configuration`_ section.
If the arguments are not provided, then the configuration from the ``settings.py`` is used,
or default if ``settings.py`` is not configured::

    $ python manage.py rungevent [[addr]:port] [pool_size]

Credits
-------

* Miroslav Shubernetskiy
* Alex Rothberg

License
-------

This library is packaged with MIT license::

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



.. image:: https://d2weczhvl823v0.cloudfront.net/miki725/django-gevent-deploy/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

