import os
import sys
import importlib
import httplib2
from optparse import OptionParser, make_option
from oauth2client.file import Storage


class CommandError(Exception):
    pass


def get_command(command_name):
    command = importlib.import_module("gas.%s" % command_name)
    return command.Command()


def run_command(command):
    parser = OptionParser(option_list=command.option_list)    
    (opts, args) = parser.parse_args()
    try:
        command.handle(args, opts)
    except CommandError, e:
        print "ERROR: %s" % str(e)       


class BaseCommand(object):
    option_list = (
        make_option("-s", "--client-secrets", action="store",
            dest="client_secrets_file"),
        make_option("-c", "--credentials", action="store",
            dest="credentials_file"),
    )

    def get_credentials(self, opts):
        if not os.path.isfile(opts.credentials_file):
            raise CommandError("Credentials file %s not found." % \
                opts.credentials_file)

        store = Storage(opts.credentials_file)
        credentials = store.get()

        if credentials is None or credentials.invalid:
            raise CommandError("Credentials are missing or invalid. Please "
                "refresh them with `gas authorize`.") 

        return credentials 

    def get_client(self, opts):
        self.get_credentials(opts).authorize(httplib2.Http()) 
