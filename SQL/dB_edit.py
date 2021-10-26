from SQL.dB_connector import Connector


class EditDb(Connector):
    def __init__(self):
        super(EditDb, self).__init__()
        super(self.__class__, self).__init__()

    def edit_one_product_field(self, field, update, product_id):
        query = "UPDATE products SET " + field + " = '" + str(update) + "' WHERE id = " + str(product_id)
        return self.db_connector(query)

    def edit_one_record_one_field_one_table(self, table, field, update, product_id):
        query = "UPDATE " + table + " SET " + field + " = '" + str(update) + "' WHERE id = " + str(product_id)
        return self.db_connector(query)

    def archive_entry_in_table_by_id(self, table, record_id):
        query = "UPDATE " + table + " SET archived = True WHERE id = " + str(record_id)
        return self.db_connector(query)
