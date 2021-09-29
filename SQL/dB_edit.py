from SQL.dB_connector import Connector


class EditDb(Connector):
    def __init__(self):
        super(EditDb, self).__init__()
        super(self.__class__, self).__init__()

    def edit_one_product_field(self, field, update, product_id):
        query = "UPDATE products SET " + field + " = '" + str(update) + "' WHERE id = " + str(product_id)
        return self.db_connector(query)


