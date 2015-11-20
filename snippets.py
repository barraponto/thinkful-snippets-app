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

    insert_command = "insert into snippets values (%s, %s)"
    update_command = "update snippets set message=%s where keyword=%s"

    with connection, connection.cursor() as cursor:
        try:
            cursor.execute(insert_command, (name, snippet))
        except psycopg2.IntegrityError as error:
            if error.pgcode == '23505':
                logging.debug("Updating existent entry {!r}".format(name))
                connection.rollback()
                cursor.execute(update_command, (snippet, name))
            else:
                raise error

    logging.debug("Snippet stored succesfully.")
    return name, snippet

def get(name):
    """ Retrieve the snippet with a given name, if any.

    Returns the snippet.
    """
    logging.info("Retrieving snippet {!r}".format(name))
    command = "select message from snippets where keyword=%s"
    with connection, connection.cursor() as cursor:
        cursor.execute(command, (name,))
        row = cursor.fetchone()

    if not row:
        logging.error('Snippet {!r} not found.'.format(name))
        return None
    else:
        logging.debug("Snippet retrieved succesfully.")
        return row[0]

def catalog():
    """Get the list of existing keywords in database.

    Returns a list of keywords.
    """
    logging.info("Retrieving list of snippet keywords.")
    command = "select keyword from snippets"

    with connection, connection.cursor() as cursor:
        cursor.execute(command)
        keywords = [row[0] for row in cursor.fetchall()]

    return keywords

def search(query):
    """Search for snippets containing query.

    Returns a list of snippets.
    """
    logging.info(
        "Retrieving list of snippets matching query {!r}.".format(query))
    command = "select keyword, message from snippets where message like %s"

    with connection, connection.cursor() as cursor:
        cursor.execute(command, ('%' + query + '%',))
        rows = [row for row in cursor.fetchall()]

    return rows


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

    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Store a snippet")

    # Subparser for the search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Store a snippet")
    search_parser.add_argument("query", help="A query to search for in snippets.")


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
    elif command == "catalog":
        keywords = catalog()
        logging.info(
            "Sucessfully retrieved keywords catalog:\n{}".format(
                '\n'.join(keywords)))
    elif command == "search":
        rows = search(**arguments)
        log_message = "Sucessfully retrieved snippets:\n"
        log_message += '\n'.join(
            '{!r}: {!r}'.format(name, snippet[:10] + '...')
            for name, snippet in rows)
        logging.info(log_message)



if __name__ == '__main__':
    main()
