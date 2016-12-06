#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import functools

from keystoneauth1 import adapter

from laosclient.common import utils


def Client(version, *args, **kwargs):
    module = utils.import_versioned_module(version, 'client')
    client_class = getattr(module, 'Client')
    return client_class(*args, **kwargs)


def construct_http_client(*args, **kwargs):
    kwargs = kwargs.copy()
    if kwargs.get('session') is None:
        raise ValueError("A session instance is required")

    return SessionClient(
        session=kwargs.get('session'),
        auth=kwargs.get('auth'),
        region_name=kwargs.get('region_name'),
        service_type=kwargs.get('service_type', 'functions'),
        service_name=kwargs.get('service_name', 'functions'),
        interface=kwargs.get('endpoint_type', 'public').rstrip('URL'),
        user_agent=kwargs.get('user_agent', 'python-laosclient'),
        endpoint_override=kwargs.get('endpoint_override'),
        timeout=kwargs.get('timeout'),
    )


class SessionClient(adapter.Adapter):
    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.pop('timeout', None)
        super(SessionClient, self).__init__(*args, **kwargs)


def inject_project_id(action):

    @functools.wraps(action)
    def wraps(*args, **kwargs):
        self = args[0]
        project_id = self.client.get_project_id()
        new_args = [self, project_id, ]
        new_args.extend(list(args)[1:])
        return action(*new_args, **kwargs)

    return wraps
