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

from picassoclient import client
from picassoclient.v1 import apps
from picassoclient.v1 import routes


class Client(object):
    def __init__(self, *args, **kwargs):
        """
        Client for the Functions v1 API.

        :param session: a keystoneauth session object
        :type session: keystoneauth1.session.Session
        :param str service_type: The default service_type for URL discovery
        :param str interface: The default interface for URL discovery
                              (Default: public)
        :param str region_name: The default region_name for URL discovery
        :param str endpoint_override: Always use this endpoint URL for requests
                                      for this picassoclient
        :param auth: An auth plugin to use instead of the session one
        :type auth: keystoneauth1.plugin.BaseAuthPlugin
        :param str user_agent: The User-Agent string to set
                               (Default is python-picassoclient)
        """
        self.http_client = client.construct_http_client(*args, **kwargs)
        self.apps = apps.Apps(self.http_client)
        self.routes = routes.Routes(self.http_client)
