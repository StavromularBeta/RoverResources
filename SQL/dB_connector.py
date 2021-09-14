import sqlite3
import os


class Connector(object):
    """Handles connections to the database (RoverResourcesDatabase.db).

    Attributes
    ----------
    database_target : str
        target of RoverResourcesDatabase. File path is relative, so should be the same regardless of computer.

    Methods
    -------

    * `db_connector()` -
        takes a query with optional arguments. Opens db connection. Executes query on database. Closes db connection.
        Returns results of query.

    """
    def __init__(self):
        # gets current working directory
        cwd = os.getcwd()
        # splits current working directory
        cwd = cwd.split("\\")
        # removes any sub-directories after the main RoverResources directory if they exist
        cwd = cwd[0:cwd.index("RoverResources")+1]
        # concatenates list back into string
        cwd = "\\".join(cwd)
        # adds desired sub-directories
        target = cwd + r'\SQL\Database\ '
        # adds name of database to end of target
        self.database_target = target[:-1] + "RoverResourcesDatabase.db"

    def db_connector(self, query, arguments=None):
        """takes a query with optional arguments. Opens db connection. Executes query on database. Closes db connection.
        Returns results of query.

        Parameters
        ----------

        query : str
            a SQLite query.

        arguments : tuple
            a tuple of arguments. Will be inserted into query in order using question mark notation. Optional.
        """
        # opens connection
        db_connection = sqlite3.connect(self.database_target)
        # creates cursor (this is what we pass queries to)
        cursor = db_connection.cursor()
        if arguments:
            # arguments have to be in the form of a tuple.
            cursor.execute(query, arguments)
        else:
            cursor.execute(query)
        db_connection.commit()
        returned_query = cursor
        return returned_query

