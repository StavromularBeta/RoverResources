from SQL.dB_connector import Connector


class DataTransfer(Connector):
    """Contains data transfer methods for RoverResourcesDatabases (for updating dB)."""
    def __init__(self):
        super(DataTransfer, self).__init__()
        super(self.__class__, self).__init__()

    def insert_db_one_table_one_into_db_two_table_two(self,
                                                      database_2_name,
                                                      table_name):
        query = "ATTACH DATABASE " + database_2_name + " AS old_db; "
        query += "INSERT INTO " + table_name + " SELECT * FROM old_db." + table_name + "; "
        query += "DETACH old_db;"
        print(query)


data_transfer = DataTransfer()
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "categories")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "sub_categories")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "vendors")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "products")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "priceTracking")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "credentials")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "users")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "requests")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "orders")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "received")
data_transfer.insert_db_one_table_one_into_db_two_table_two("RoverResourcesDatabase2", "inventory")

