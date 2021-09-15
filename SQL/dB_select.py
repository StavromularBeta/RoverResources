from SQL.dB_connector import Connector


class Select(Connector):
    def __init__(self):
        super(Select, self).__init__()
        super(self.__class__, self).__init__()

    def print_or_return_query(self, query, print_view=False):
        if print_view:
            for item in self.db_connector(query):
                print(item)
        else:
            return self.db_connector(query)

    def select_all_from_table_ascending(self, table_name, print_view=False, descending_order=False):
        if descending_order:
            query = "SELECT * FROM " + table_name + " ORDER BY id DESC"
        else:
            query = "SELECT * FROM " + table_name + " ORDER BY id"
        self.print_or_return_query(query, print_view)

