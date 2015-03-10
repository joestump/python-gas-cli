import json
import pprint
from optparse import make_option
from oauth2client import client, tools
from oauth2client.tools import run_flow
from oauth2client.file import Storage
from gas.base import BaseCommand, CommandError


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--auth-host-name', default='localhost',
                    dest='auth_host_name',
                    help='Hostname when running a local web server.'),
        make_option('--noauth_local_webserver', action='store_true',
                    dest='noauth_local_webserver',
                    default=False, help='Do not run a local web server.'),
        make_option('--auth_host_port', default=[8080, 8090], type=int,
                    dest='auth_host_port',
                    nargs='*', help='Port web server should listen on.'),
        make_option('--logging_level', default='ERROR',
                    dest='logging_level',
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                    help='Set the logging level of detail.'),
    )

    SCOPES = [
        'https://www.googleapis.com/auth/drive.scripts',
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
    ]

    def handle(self, args, opts):
        flow = client.flow_from_clientsecrets(opts.client_secrets_file,
            ' '.join(self.SCOPES))

        store = self.get_store(opts)
        credentials = store.get()
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, store, opts)
        else:
            pprint.pprint(json.loads(credentials.to_json()))
