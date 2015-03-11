from .base import get_command, run_command
import sys

def main():
    command = get_command(sys.argv[1])
    run_command(command)

if __name__ == "__main__":
    main()
