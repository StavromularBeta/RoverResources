from SQL.dB_connector import Connector


def print_master_table_query(master_table_query):
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
    print("RoverResourcesDatabase - Table Architecture\n")
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    for item in master_table_query:
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n")
        print("Table Name: " + item[1] + "\n\n")
        print(item[4] + "\n\n")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


class DbViews(Connector):
    def __init__(self):
        super(DbViews, self).__init__()
        super(self.__class__, self).__init__()

    def view_database_architecture(self):
        print_master_table_query(self.master_table_query())

    def master_table_query(self):
        query = " SELECT * FROM sqlite_master "
        return self.db_connector(query)

