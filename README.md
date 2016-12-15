# python-picassoclient

OpenStack Functions Client Library

This is a client library for Picasso built on the Picasso API. It
provides a Python API (the ``picassoclient`` module).

The project is hosted on [Launchpad](https://github.com/iron-io/python-picassoclient/issue),
where bugs can be filed. The code is hosted on [GitHub](https://github.com/iron-io/python-picassoclient).
Patches must be submitted using [Gerrit](http://docs.openstack.org/infra/manual/developers.html#development-workflow),
*not* Github pull requests.

python-picassoclient is licensed under the Apache License, like the rest of OpenStack.

## Install the client from PyPI

The `python-picassoclient` package is published on [PyPI](https://pypi.python.org/pypi/python-picassoclient/)
and can be installed via `pip`.

    $ pip install python-picassoclient

   Note: The packages on PyPI may lag behind the git repo in functionality.

## Setup the client from source

1. Clone the source repo

        $ git clone https://github.com/iron-io/python-picassoclient.git
        $ cd python-picassoclient

2. Setup a Python virtualenv

    Note: This is an optional step, but will allow picassoclient dependencies to be installed in a
    contained environment that can be easily deleted if you choose to start over or uninstall the client.

        $ tox -evenv --notest

    Activate the virtual environment whenever you want to work in it.
    All further commands in this section should be run with the venv active:

        $ source .tox/venv/bin/activate

    When all steps are complete, deactivate the virtualenv by running `deactivate` from your shell.

3. Install picassoclient and its dependencies::

        (venv) $ python setup.py develop

## Picasso CLI

To work with the CLI, set the necessary Keystone environment variables

    $ export OS_USERNAME=<user>
    $ export OS_PASSWORD=<password>
    $ export OS_PROJECT_NAME=<project>
    $ export OS_AUTH_URL=http://localhost:5000/v3


   If working with DevStack, just run `source openrc <user> <project>`. You can then work with a
   local installation by passing `--os-token <TOKEN>` and `--os-url http://localhost:9393`. You can
   also set up a [Openstackclient](http://docs.openstack.org/developer/python-openstackclient/configuration.html#clouds-yaml)
   config file to work with the CLI.

    $ openstack
    (openstack) fn apps list
    (openstack) fn apps create testapp


## Picasso Python API

Refer to the following code to use Keystone as the authentication backend:

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

    tox -e pep8 - style guidelines enforcement
    tox -e py34 - traditional unit testing
    tox -e py35 - traditional unit testing