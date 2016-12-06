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

import json

from laosclient import client


class Routes(object):

    routes_path = "/v1/{project_id}/apps/{app}/routes"
    route_path = "/v1/{project_id}/apps/{app}/routes{route_path}"
    private_execution = "/v1/r/{app}{route_path}"
    public_execution = "/r/{app}{route_path}"

    def __init__(self, session_client: client.SessionClient):
        self.client = session_client

    @client.inject_project_id
    def create(self, project_id, app_name, execution_type,
               route_path, image, is_public=False, memory=None,
               timeout=None, max_concurrency=None, config=None):
        """
        Creates an app route

        :param app_name:
        :param execution_type:
        :param route_path:
        :param image:
        :param is_public:
        :param memory:
        :param timeout:
        :param max_concurrency:
        :param config:
        :return:
        """
        body = {
            "route": {
                "type": execution_type,
                "path": route_path,
                "image": image,
                "memory": memory if memory else 128,
                "timeout": timeout if timeout else 30,
                "max_concurrency": (max_concurrency
                                    if max_concurrency else 1),
                "is_public": str(is_public if
                                 is_public is not None else False).lower(),
                "config": config if config else {},
            }
        }
        response = self.client.post(self.routes_path.format(
            project_id=project_id, app=app_name), json=body)
        return response.json()

    @client.inject_project_id
    def list(self, project_id, app_name):
        """

        :param app_name:
        :return:
        """
        response = self.client.get(self.routes_path.format(
            project_id=project_id, app=app_name))
        return response.json()

    @client.inject_project_id
    def show(self, project_id, app_name, route_path):
        """

        :param app_name:
        :param route_path:
        :return:
        """
        response = self.client.get(self.route_path.format(
            project_id=project_id, app=app_name,
            route_path=route_path))
        return response.json()

    @client.inject_project_id
    def update(self, project_id, app_name, route_path, **data):
        """

        :param app_name:
        :param route_path:
        :param data:
        :return:
        """
        response = self.client.put(self.route_path.format(
            project_id=project_id, app=app_name,
            route_path=route_path), json=data)
        return response.json()

    @client.inject_project_id
    def delete(self, project_id, app_name, route_path):
        """

        :param app_name:
        :param route_path:
        :return:
        """
        response = self.client.delete(
            self.route_path.format(
                project_id=project_id, app=app_name,
                route_path=route_path))
        return response.json()

    @client.inject_project_id
    def execute(self, project_id, app_name, route_path, **data):
        """

        :param app_name:
        :param route_path:
        :param data:
        :return:
        """
        route = self.show(app_name, route_path)
        is_public = json.loads(route.get("is_public"))
        url = (self.public_execution.format(
            app=app_name, route_path=route_path) if is_public else
               self.private_execution.format(
                   project_id=project_id, app=app_name,
                   route_path=route_path))
        response = self.client.post(url, json=data)
        return response.json()
