import os
from setuptools import setup, find_packages

from django_gevent_deploy import __version__, __author__


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-gevent-deploy",
    version=__version__,
    author=__author__,
    author_email="miroslav@miki725.com",
    description=("Django manage.py hook for starting gevent's WSGI server"),
    long_description=read('README.rst') + read('CHANGELOG.rst'),
    license="MIT",
    keywords="django",
    url="https://github.com/miki725/django-gevent-deploy",
    packages=find_packages(),
    install_requires=read('requirements.txt').splitlines(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
