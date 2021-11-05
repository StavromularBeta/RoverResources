from SQL.dB_connector import Connector


class DataTransfer(Connector):
    """Contains data transfer methods for RoverResourcesDatabases (for updating dB)."""
    def __init__(self):
        super(DataTransfer, self).__init__()
        super(self.__class__, self).__init__()

    def insert_db_one_table_one_into_db_two_table_two(self,
                                                      table_name):
        query = "ATTACH DATABASE " + self.old_database_target + " AS old_db; "
        query += "INSERT INTO " + table_name + " SELECT * FROM old_db." + table_name + "; "
        query += "DETACH old_db;"
        return self.db_connector(query)


data_transfer = DataTransfer()
data_transfer.insert_db_one_table_one_into_db_two_table_two("categories")
data_transfer.insert_db_one_table_one_into_db_two_table_two("sub_categories")
data_transfer.insert_db_one_table_one_into_db_two_table_two("vendors")
data_transfer.insert_db_one_table_one_into_db_two_table_two("products")
data_transfer.insert_db_one_table_one_into_db_two_table_two("priceTracking")
data_transfer.insert_db_one_table_one_into_db_two_table_two("credentials")
data_transfer.insert_db_one_table_one_into_db_two_table_two("users")
data_transfer.insert_db_one_table_one_into_db_two_table_two("requests")
data_transfer.insert_db_one_table_one_into_db_two_table_two("orders")
data_transfer.insert_db_one_table_one_into_db_two_table_two("received")
data_transfer.insert_db_one_table_one_into_db_two_table_two("inventory")

