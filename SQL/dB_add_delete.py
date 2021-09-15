from SQL.dB_connector import Connector


class AddDelete(Connector):
    def __init__(self):
        super(AddDelete, self).__init__()
        super(self.__class__, self).__init__()

    def new_categories_record(self, value):
        query = 'INSERT OR IGNORE INTO categories (category_name) VALUES (?)'
        return self.db_connector(query, (value,))

    def new_vendors_record(self, value):
        query = 'INSERT OR IGNORE INTO vendors (vendor_name) VALUES (?)'
        return self.db_connector(query, (value,))

    def new_products_record(self, values):
        query = 'INSERT OR IGNORE INTO products (categories_id, vendors_id, product_code, name) VALUES (?,?,?,?)'
        return self.db_connector(query, values)
