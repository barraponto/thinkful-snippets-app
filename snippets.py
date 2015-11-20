import argparse
import logging
import sys

# Set the log output file and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """ Store a snippet with an associated name.

    Returns the name and the snippet.
    """
    logging.error(
        "FIXME: Unimplemented - put({!r},{!r})".format(name, snippet))

def get(name):
    """ Retrieve the snippet with a given name, if any.

    Returns the snippet.
    """
    logging.error(
        "FIXME: Unimplemented - get({!r})".format(name))

def main():
    """Main function"""

    logging.info("Constructing parser.")
    parser = argparse.ArgumentParser(
        description="Store and retrieve snippets of text.")
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")

    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Store a snippet")
    get_parser.add_argument("name", help="The name of the snippet")


    arguments = parser.parse_known_args(sys.argv[1:])
    print(arguments)

if __name__ == '__main__':
    main()
