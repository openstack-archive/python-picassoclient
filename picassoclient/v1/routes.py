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


class Routes(object):

    routes_path = "/v1/{project_id}/apps/{app}/routes"
    route_path = "/v1/{project_id}/apps/{app}/routes{route_path}"
    private_execution = "/v1/r/{project_id}/{app}{route_path}"
    public_execution = "/r/{app}{route_path}"

    def __init__(self, session_client):
        self.client = session_client

    @client.inject_project_id
    def create(self, project_id, app_name,
               execution_type, route_path, image,
               is_public=False, memory=None,
               timeout=None, max_concurrency=None,
               config=None):
        """
        Creates app route

        :param app_name: App name
        :type app_name: str
        :param execution_type: App route execution type (async, sync)
        :type execution_type: str
        :param route_path: App route path
        :type route_path: str
        :param image: Docker image reference
        :type image: str
        :param is_public: Whether app route is public or private
        :type is_public: bool
        :param memory: App route RAM to allocate
        :type memory: int
        :param timeout: App route execution time frame
        :type timeout: int
        :param max_concurrency: Number of app route max concurrent
            requests before container dies
        :type max_concurrency: int
        :param config: App route config
        :type config: dict
        :return: App route
        :rtype: dict
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
        Lists project-scoped app routes

        :param app_name: App route
        :type app_name: str
        :return: list of routes
        :rtype: list of dict
        """
        response = self.client.get(self.routes_path.format(
            project_id=project_id, app=app_name))
        return response.json()

    @client.inject_project_id
    def show(self, project_id, app_name, route_path):
        """
        Retrieves app route information

        :param app_name: App name
        :type app_name: str
        :param route_path: App route path
        :type route_path: str
        :return: App route
        :rtype: dict
        """
        response = self.client.get(self.route_path.format(
            project_id=project_id, app=app_name,
            route_path=route_path))
        return response.json()

    @client.inject_project_id
    def update(self, project_id, app_name,
               route_path, **data):
        """
        Updates route with provided data

        :param app_name: App name
        :type app_name: str
        :param route_path: App route to update
        :type route_path: str
        :param data:
        :type data: dict
        :return: App route
        :rtype: dict
        """
        response = self.client.put(self.route_path.format(
            project_id=project_id, app=app_name,
            route_path=route_path), json=data)
        return response.json()

    @client.inject_project_id
    def delete(self, project_id, app_name, route_path):
        """
        Deletes app

        :param app_name: App name
        :type app_name: str
        :param route_path: App route path
        :return: None
        :rtype: None
        """
        response = self.client.delete(
            self.route_path.format(
                project_id=project_id, app=app_name,
                route_path=route_path))
        return response.json()

    @client.inject_project_id
    def execute(self, project_id, app_name, route_path,
                supply_auth_properties=False, **data):
        """
        Runs execution against public/private routes

        :param app_name: App name
        :type app_name: str
        :param route_path: App route path
        :type route_path: str
        :param supply_auth_properties: Whether to include auth properties
            like OS_AUTH_URL and OS_TOKEN into execution parameters data
        :type supply_auth_properties: bool
        :param data: execution data
        :type data: dict
        :return: execution result, depends on the type of execution
        :rtype: dict
        """
        route = self.show(app_name, route_path)
        is_public = route["route"].get("is_public")
        url = (self.public_execution.format(
            app=app_name, route_path=route_path) if is_public else
               self.private_execution.format(
                   project_id=project_id, app=app_name,
                   route_path=route_path))
        if supply_auth_properties:
            data.update(OS_AUTH_URL=self.client.session.auth.auth_url,
                        OS_TOKEN=self.client.get_token(),
                        OS_PROJECT_ID=project_id)
        response = self.client.post(url, json=data)
        return response.json()
