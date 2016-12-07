#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Functions v1 App routes actions implementations"""

import json
import logging

from osc_lib.command import command
from osc_lib import utils


class ListAppRoutes(command.Lister):
    """Lists app routes"""
    log = logging.getLogger(__name__ + ".ListAppRoutes")

    def get_parser(self, prog_name):
        parser = super(ListAppRoutes, self).get_parser(prog_name)
        parser.add_argument("app", metavar="<app-name>",
                            help="Specifies which app to show")
        return parser

    def take_action(self, parsed_args):
        COLUMNS = (
            "type",
            "path",
            "image",
            "memory",
            "timeout",
            "max_concurrency",
            "is_public",
            "config",
        )
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        app = parsed_args.app
        result = []
        for item in fc.routes.list(app)["routes"]:
            result.append(utils.get_dict_properties(item, COLUMNS))

        return COLUMNS, result


class ShowAppRoute(command.ShowOne):
    """Shows specific route info"""
    log = logging.getLogger(__name__ + ".GetAppRoute")

    def get_parser(self, prog_name):
        parser = super(ShowAppRoute, self).get_parser(prog_name)
        parser.add_argument("app", metavar="<app-name>",
                            help="Specifies at which app to search for route")
        parser.add_argument("route", metavar="<route-path>",
                            help="Specifies which app to show")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        app, route_path = parsed_args.app, parsed_args.route
        route = fc.routes.show(app, route_path)["route"]
        keys = list(route.keys())
        return keys, utils.get_dict_properties(route, keys)


class CreateAppRoute(command.ShowOne):
    """Creates a new app route"""
    log = logging.getLogger(__name__ + ".CreateAppRoute")

    def get_parser(self, prog_name):
        parser = super(CreateAppRoute, self).get_parser(prog_name)
        parser.add_argument("app", metavar="<app-name>",
                            help="Specifies which app to show")
        parser.add_argument("route", metavar="<route-path>",
                            help="App route name to create")
        parser.add_argument("type", metavar="<execution-type>",
                            help="App route type to create",
                            choices=["async", "sync"])
        parser.add_argument("image", metavar="<docker-image>",
                            help="Docker image to run")
        parser.add_argument("--is-public",
                            help="Public/Private route to create",
                            action="store_true", default=False)
        parser.add_argument("--memory", metavar="<memory>",
                            help="App route memory to allocate, in Mbs",
                            type=int)
        parser.add_argument("--timeout", metavar="<timeout>",
                            help="For how log to run the function",
                            type=int)
        parser.add_argument("--max-concurrency", metavar="<max_concurrency>",
                            help="Cold/Hot container to use.", type=int)
        parser.add_argument("--config", metavar="<config>",
                            help="App route config", type=json.loads)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        # required
        app, route, r_type, image = (parsed_args.app, parsed_args.route,
                                     parsed_args.type, parsed_args.image)
        # optional
        is_public, memory, timeout, max_c, config = (
            parsed_args.is_public, parsed_args.memory,
            parsed_args.timeout, parsed_args.max_concurrency,
            parsed_args.config
        )

        new_route = fc.routes.create(app, r_type, route, image,
                                     is_public=is_public, memory=memory,
                                     timeout=timeout, max_concurrency=max_c,
                                     config=config)["route"]
        keys = list(new_route.keys())
        return keys, utils.get_dict_properties(new_route, keys)


class DeleteAppRoute(command.Command):
    """Deletes specific app route"""
    log = logging.getLogger(__name__ + ".DeleteAppRoute")

    def get_parser(self, prog_name):
        parser = super(DeleteAppRoute, self).get_parser(prog_name)
        parser.add_argument("app", metavar="<app-name>",
                            help="Specifies which app to show")
        parser.add_argument("route", metavar="<route-path>",
                            help="App route to look for")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        app, route = parsed_args.app, parsed_args.route
        fc.routes.delete(app, route)


class UpdateAppRoute(command.ShowOne):
    """Updates specific app route"""
    log = logging.getLogger(__name__ + ".UpdateAppRoute")

    def get_parser(self, prog_name):
        parser = super(UpdateAppRoute, self).get_parser(prog_name)
        parser.add_argument("app", metavar="<app-name>",
                            help="Specifies which app to show")
        parser.add_argument("route", metavar="<route-path>",
                            help="App route to look for")
        parser.add_argument("--image", metavar="<docker-image>",
                            help="New Docker image")
        parser.add_argument("--memory", metavar="<memory>",
                            help="App route memory to allocate, in Mbs",
                            type=int)
        parser.add_argument("--timeout", metavar="<timeout>",
                            help="For how log to run the function",
                            type=int)
        parser.add_argument("--max-concurrency",
                            metavar="<max-concurrency>",
                            type=int,
                            help="Cold/Hot container to use.")
        parser.add_argument("--type", metavar="<execution-type>",
                            help="App route type to updae",
                            choices=["async", "sync"])
        parser.add_argument("--config", metavar="<config>",
                            help="App route config", type=json.loads)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        # required
        app, route = parsed_args.app, parsed_args.route
        # optional
        image, memory, max_c, timeout, config = (
            parsed_args.image, parsed_args.memory,
            parsed_args.max_concurrency, parsed_args.timeout,
            parsed_args.config)

        data = {}
        if image:
            data.update(image=image)
        if memory:
            data.update(memory=memory)
        if max_c:
            data.update(max_concurrency=max_c)
        if timeout:
            data.update(timeout=timeout)
        if config:
            data.update(config=config)

        updated_route = fc.routes.update(app, route, **data)["route"]
        keys = list(updated_route.keys())
        return keys, utils.get_dict_properties(updated_route, keys)


class ExecuteAppRoute(command.ShowOne):
    """Runs execution against specific app route"""
    log = logging.getLogger(__name__ + ".ExecuteAppRoute")

    def get_parser(self, prog_name):
        parser = super(ExecuteAppRoute, self).get_parser(prog_name)
        parser.add_argument("app", metavar="<app-name>",
                            help="Specifies which app to show")
        parser.add_argument("route", metavar="<route-path>",
                            help="App route to look for")
        parser.add_argument("--supply-auth-properties", action='store_true',
                            help=("Whether to include auth properties "
                                  "like OS_AUTH_URL and OS_TOKEN into "
                                  "execution parameters data"))
        parser.add_argument("--data", metavar="<data>",
                            help="Execution data", type=json.loads)
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        # required
        app, route, data = parsed_args.app, parsed_args.route, parsed_args.data
        # optional
        supply_auth_properties = parsed_args.supply_auth_properties
        if data:
            data = json.loads(data)
        else:
            data = {}
        result = fc.routes.execute(
            app, route,
            supply_auth_properties=supply_auth_properties, **data)
        clmns = list(result.keys())
        return clmns, utils.get_dict_properties(result, clmns)
