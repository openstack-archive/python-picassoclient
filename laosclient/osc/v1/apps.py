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

"""Functions v1 App actions implementations"""

import json
import logging

from osc_lib.command import command
from osc_lib import utils


class ListApps(command.Lister):
    """Lists apps"""

    log = logging.getLogger(__name__ + ".ListApps")

    def take_action(self, parsed_args):
        COLUMNS = (
            "name",
            "config",
            "description",
        )
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        result = []
        for item in fc.apps.list()["apps"]:
            result.append(utils.get_dict_properties(item, COLUMNS))

        return COLUMNS, result


class ShowApp(command.ShowOne):
    """Show app info"""

    log = logging.getLogger(__name__ + ".ShowApp")

    def get_parser(self, prog_name):
        parser = super(ShowApp, self).get_parser(prog_name)
        parser.add_argument("name", metavar="<name>",
                            help="Specifies which app to show")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        app_name = parsed_args.name
        app = fc.apps.show(app_name)["app"]
        keys = list(app.keys())
        return keys, utils.get_dict_properties(app, keys)


class CreateApp(command.ShowOne):
    """Creates an app"""

    log = logging.getLogger(__name__ + ".CreateApp")

    def get_parser(self, prog_name):
        parser = super(CreateApp, self).get_parser(prog_name)
        parser.add_argument("name", metavar="<name>",
                            help="App name to create")
        parser.add_argument("--config", metavar="<config>",
                            help="Config for app to create in JSON format")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        app_name = parsed_args.name
        config = parsed_args.config
        if config:
            try:
                config = json.loads(config)
            except Exception as ex:
                self.log.error("Invalid config JSON: Reason: {}".format(str(ex)))
                raise ex

        app = fc.apps.create(app_name, config=config)["app"]
        keys = list(app.keys())
        return keys, utils.get_dict_properties(app, keys)


class DeleteApp(command.Command):
    """Deletes an app"""
    log = logging.getLogger(__name__ + ".DeleteApp")

    def get_parser(self, prog_name):
        parser = super(DeleteApp, self).get_parser(prog_name)
        parser.add_argument("name", metavar="<app-name>",
                            help="App name to delete")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        app_name = parsed_args.name
        fc.apps.delete(app_name)


class UpdateApp(command.ShowOne):
    """Deletes an app"""
    log = logging.getLogger(__name__ + ".UpdateApp")

    def get_parser(self, prog_name):
        parser = super(UpdateApp, self).get_parser(prog_name)
        parser.add_argument("name", metavar="<app-name>",
                            help="App name to delete")
        parser.add_argument("config", metavar="<config>",
                            help="Config for app to create in JSON format")
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        fc = self.app.client_manager.functions
        app_name = parsed_args.name
        fc.apps.update(app_name)
        config = parsed_args.config
        if not config:
            raise Exception("Nothing to update. "
                            "App config was not specified.")
        app = fc.apps.update(app_name, config=json.loads(config))["app"]
        keys = license(app.keys())
        return keys, utils.get_dict_properties(app, keys)
