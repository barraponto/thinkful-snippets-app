import argparse
import logging
import sys

import psycopg2

# Set the log output file and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

# Setup database connection
logging.debug("Connecting to PostgreSQL.")
connection = psycopg2.connect(database="tf-snippets")
logging.debug("Database connection established.")


def put(name, snippet):
    """ Store a snippet with an associated name.

    Returns the name and the snippet.
    """
    logging.info(
        "Storing snippet {!r} {!r}".format(name, snippet[:10] + '...'))
    cursor = connection.cursor()
    command = "insert into snippets values (%s, %s)"
    try:
        cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as error:
        if error.pgcode == '23505':
            connection.rollback()
            logging.debug("Updating existent entry {!r}".format(name))
            command = "update snippets set message=%s where keyword=%s"
            cursor.execute(command, (snippet, name))
        else:
            raise error
    connection.commit()
    logging.debug("Snippet stored succesfully.")
    return name, snippet

def get(name):
    """ Retrieve the snippet with a given name, if any.

    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    cursor = connection.cursor()
    command = "select message from snippets where keyword=%s"
    cursor.execute(command, (name,))
    logging.debug("Snippet retrieved succesfully.")
    row =  cursor.fetchone()
    if not row:
        logging.error('Snippet {!r} not found.'.format(name))
        connection.comit()
        return None
    connection.commit()
    return row[0]


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


    arguments = vars(parser.parse_args(sys.argv[1:]))
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        logging.info("Stored {!r} as {!r}".format(snippet, name[:10] + '...'))
    elif command == "get":
        snippet = get(**arguments)
        if snippet is None:
            logging.info("No snippet retrieved.")
        else:
            logging.info("Retrieved snippet:\n {}".format(snippet))



if __name__ == '__main__':
    main()
