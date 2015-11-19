import logging

# Set the log output file and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """ Store a snippet with an associated name.

    Returns the name and the snippet.
    """
    logging.error(
        "FIXME: Unimplemented - put({!r},{!r})").format(name, snippet)

def get(name):
    """ Retrieve the snippet with a given name, if any.

    Returns the snippet.
    """
    logging.error(
        "FIXME: Unimplemented - get({!r})").format(name)
