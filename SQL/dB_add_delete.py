from SQL.dB_connector import Connector


class AddDelete(Connector):
    def __init__(self):
        super(AddDelete, self).__init__()
        super(self.__class__, self).__init__()

    def new_categories_record(self, value):
        query = 'INSERT OR IGNORE INTO categories (category_name) VALUES (?)'
        return self.db_connector(query, (value,))
