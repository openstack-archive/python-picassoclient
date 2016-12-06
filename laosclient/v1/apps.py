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

from laosclient import client


class Apps(object):

    apps_route = "/v1/{project_id}/apps"
    app_route = "/v1/{project_id}/apps/{app}"

    def __init__(self, session_client: client.SessionClient):
        self.client = session_client

    @client.inject_project_id
    def list(self, project_id):
        """

        :param project_id:
        :return:
        """
        response = self.client.get(
            self.apps_route.format(project_id=project_id))
        return response.json()

    @client.inject_project_id
    def show(self, project_id, app_name):
        """

        :param project_id:
        :param app_name:
        :return:
        """
        response = self.client.get(
            self.app_route.format(project_id=project_id,
                                  app=app_name))
        return response.json()

    @client.inject_project_id
    def create(self, project_id, app_name, config=None):
        """

        :param project_id:
        :param app_name:
        :param config:
        :return:
        """
        data = {
            "app": {
                "name": app_name,
                "config": config if config else {}
            }
        }
        response = self.client.post(
            self.apps_route.format(project_id=project_id),
            json=data)
        return response.json()

    @client.inject_project_id
    def update(self, project_id, app_name, **data):
        """

        :param project_id:
        :param app_name:
        :param data:
        :return:
        """
        response = self.client.put(
            self.app_route.format(project_id=project_id,
                                  app=app_name), json=data)
        return response.json()

    @client.inject_project_id
    def delete(self, project_id, app_name):
        """

        :param project_id:
        :param app_name:
        :return:
        """
        response = self.client.delete(
            self.app_route.format(project_id=project_id,
                                  app=app_name))
        return response.json()
