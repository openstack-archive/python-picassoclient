========================
python-picassoclient
========================

OpenStack Functions Client Library

This is a client library for Picasso built on the Picasso API. It
provides a Python API (the ``picassoclient`` module).

The project is hosted on `Launchpad`_, where bugs can be filed. The code is
hosted on `Github`_. Patches must be submitted using `Gerrit`_, *not* Github
pull requests.

.. _Github: https://github.com/iron-io/python-picassoclient
.. _Launchpad: https://github.com/iron-io/python-picassoclient/issues
.. _Gerrit: http://docs.openstack.org/infra/manual/developers.html#development-workflow

python-picassoclient is licensed under the Apache License like the rest of
OpenStack.

.. contents:: Contents:
   :local:

Install the client from PyPI
----------------------------
The :program:`python-picassoclient` package is published on `PyPI`_ and
so can be installed using the pip tool, which will manage installing all
python dependencies::

   $ pip install python-picassoclient

.. note::
   The packages on PyPI may lag behind the git repo in functionality.

.. _PyPI: https://pypi.python.org/pypi/python-picassoclient/

Setup the client from source
----------------------------

* Clone repository for python-picassoclient::

    $ git clone https://github.com/iron-io/python-picassoclient.git
    $ cd python-picassoclient

* Setup a virtualenv

.. note::
   This is an optional step, but will allow picassoclient's dependencies
   to be installed in a contained environment that can be easily deleted
   if you choose to start over or uninstall picassoclient.

::

    $ tox -evenv --notest

Activate the virtual environment whenever you want to work in it.
All further commands in this section should be run with the venv active:

::

    $ source .tox/venv/bin/activate

.. note::
   When ALL steps are complete, deactivate the virtualenv: $ deactivate

* Install picassoclient and its dependencies::

    (venv) $ python setup.py develop

Command-line API
----------------

Set Keystone environment variables to execute CLI commands against Picasso.

* To execute CLI commands::

    $ export OS_USERNAME=<user>
    $ export OS_PASSWORD=<password>
    $ export OS_PROJECT_NAME=<project>
    $ export OS_AUTH_URL=http://localhost:5000/v3

.. note::
   With devstack you just need to $ source openrc <user> <project>. And you can
   work with a local installation by passing --os-token <TOKEN> and --os-url
   http://localhost:9393. You can also set up a `Openstackclient`_ config file
   to work with the CLI.

.. _Openstackclient: http://docs.openstack.org/developer/python-openstackclient/configuration.html#clouds-yaml

::

    $ openstack
    (openstack) fn-apps list
    (openstack) fn-apps create testapp


Python API
----------

To use with keystone as the authentication system::

    >>> from keystoneclient.auth.identity import generic
    >>> from keystoneclient import session
    >>> from picassoclient import client
    >>> auth = generic.Password(auth_url=OS_AUTH_URL, username=OS_USERNAME, password=OS_PASSWORD, tenant_name=OS_TENANT_NAME)
    >>> keystone_session = session.Session(auth=auth)
    >>> picasso = client.Client('v1', session=keystone_session)
    >>> picasso.apps.list()
    [...]


* License: Apache License, Version 2.0
* Documentation: https://github.com/iron-io/python-picassoclient
* Source: https://github.com/iron-io/python-picassoclient
* Bugs: https://github.com/iron-io/python-picassoclient

Testing
-------

There are multiple test targets that can be run to validate the code.

* tox -e pep8 - style guidelines enforcement
* tox -e py34 - traditional unit testing
* tox -e py35 - traditional unit testing
