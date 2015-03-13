from .base import get_command, run_command
import sys


COMMANDS = {
    'authorize': 'Initiate an OAuth2 flow to create valid access tokens.',
    'deploy': 'Push code from a local build folder to a GAS file.'
}


def error():
    print "ERROR: You must supply a valid command.\n"
    for command_name, command_desc in COMMANDS.iteritems():
        print "  %s\t%s" % (command_name, command_desc)
    sys.exit(1)


def main():
    try:
        command_name = sys.argv[1]
    except IndexError:
        error()

    if command_name not in COMMANDS.keys():
        error()

    command = get_command(sys.argv[1])
    run_command(command)

if __name__ == "__main__":
    main()
