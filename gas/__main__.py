from .base import get_command, run_command
import sys


if __name__ == "__main__":
    command = get_command(sys.argv[1])
    run_command(command)
