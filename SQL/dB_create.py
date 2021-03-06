from SQL.dB_connector import Connector
from SQL.dB_view import DbViews


class CreateTb(Connector):
    """ Creates the tables that make up RoverResourcesDatabase.

    Attributes
    ----------
    table_dictionary : dict
        key = table name, value = table create query.

    db_views : object
        db_views class, which contains the methods to query and print the table architecture.

    Methods
    -------

    * `db_table_creator(view_methods=False)` -
        creates database tables. Option to view tables after creation.
    """
    def __init__(self):
        super(CreateTb, self).__init__()
        super(self.__class__, self).__init__()
        self.table_dictionary = {
                                "categories": """ CREATE TABLE IF NOT EXISTS categories (
                                                       id integer PRIMARY KEY,
                                                       category_name text,
                                                       comments text,
                                                       archived bool DEFAULT False,
                                                       approved bool DEFAULT True) """,

                                "sub_categories": """ CREATE TABLE IF NOT EXISTS sub_categories (
                                                       id integer PRIMARY KEY,
                                                       categories_id int,
                                                       sub_category_name text,
                                                       comments text,
                                                       archived bool DEFAULT False,
                                                       approved bool DEFAULT True) """,

                                "vendors": """ CREATE TABLE IF NOT EXISTS vendors (
                                                   id integer PRIMARY KEY,
                                                   vendor_name text,
                                                   comments text,
                                                   archived bool DEFAULT False,
                                                   approved bool DEFAULT True) """,

                                "products": """ CREATE TABLE IF NOT EXISTS products (
                                                    id integer PRIMARY KEY,
                                                    categories_id int,
                                                    sub_categories_id int,
                                                    vendors_id int,
                                                    product_code text,
                                                    name text,
                                                    unit_of_issue text,
                                                    comments text,
                                                    archived bool DEFAULT False,
                                                    approved bool DEFAULT True) """,

                                "priceTracking": """ CREATE TABLE IF NOT EXISTS priceTracking (
                                                         id integer PRIMARY KEY,
                                                         products_id int,
                                                         cost decimal,
                                                         cost_date datetime,
                                                         archived bool DEFAULT False,
                                                         approved bool DEFAULT True) """,

                                "credentials": """ CREATE TABLE IF NOT EXISTS credentials (
                                                       id integer PRIMARY KEY,
                                                       credential_level text,
                                                       comments text,
                                                       archived bool DEFAULT False,
                                                       approved bool DEFAULT True) """,

                                "users": """ CREATE TABLE IF NOT EXISTS users (
                                                 id integer PRIMARY KEY,
                                                 credentials_id int,
                                                 user_name text,
                                                 user_password text,
                                                 comments text,
                                                 archived bool DEFAULT False,
                                                 approved bool DEFAULT True) """,

                                "requests": """ CREATE TABLE IF NOT EXISTS requests (
                                                    id integer PRIMARY KEY,
                                                    products_id int,
                                                    users_id int,
                                                    price_id int,
                                                    request_date date,
                                                    amount int,
                                                    comments text,
                                                    archived bool DEFAULT False,
                                                    approved bool DEFAULT True) """,

                                "orders": """ CREATE TABLE IF NOT EXISTS orders (
                                                  id integer PRIMARY KEY,
                                                  requests_id int,
                                                  order_date date,
                                                  units_ordered int,
                                                  comments text,
                                                  archived bool DEFAULT False,
                                                  approved bool DEFAULT True) """,

                                "received": """ CREATE TABLE IF NOT EXISTS received (
                                                    id integer PRIMARY KEY,
                                                    orders_id int,
                                                    received_date date,
                                                    received_amount int,
                                                    lot_number text,
                                                    expiry_date datetime,
                                                    storage_location text,
                                                    model text,
                                                    equipment_SN text,
                                                    comments text,
                                                    archived bool DEFAULT False,
                                                    approved bool DEFAULT True) """,

                                "inventory": """ CREATE TABLE IF NOT EXISTS inventory (
                                                            id integer PRIMARY KEY,
                                                            received_id int,
                                                            location_id int,
                                                            sub_location_id int,
                                                            full_units_remaining int,
                                                            partial_units_remaining int,
                                                            last_updated datetime,
                                                            updated_user_id int,
                                                            comments text,
                                                            archived bool DEFAULT False,
                                                            approved bool DEFAULT True) """,

                                "inventoryLocations": """ CREATE TABLE IF NOT EXISTS inventoryLocations (
                                                              id integer PRIMARY KEY,
                                                              locations_name text,
                                                              comments text,
                                                              archived bool DEFAULT False,
                                                              approved bool DEFAULT True) """,

                                "inventorySubLocations": """ CREATE TABLE IF NOT EXISTS inventorySubLocations (
                                                                id integer PRIMARY KEY,
                                                                locations_id int,
                                                                sub_locations_name text,
                                                                comments text,
                                                                archived bool DEFAULT False,
                                                                approved bool DEFAULT True) """,
                                 }
        self.db_views = DbViews()

    def db_table_creator(self, view_tables=False):
        """Iterates through the table dictionary and creates each table. if view_tables is True, will print
         the database architecture to the terminal.

         Parameters
         ----------

         view_tables : bool
            optional. if true, will print tables to console.
        """
        for key, value in self.table_dictionary.items():
            self.db_connector(value)

        if view_tables:
            self.db_views.view_database_architecture()

    def db_table_add_approved_column(self):
        """Iterates through the table dictionary and adds a field called approved, which is a bool, and is default
        true. This field allows products to be requested, as well as added directly by an admin. """
        for key, value in self.table_dictionary.items():
            query = "ALTER TABLE " + key + " ADD COLUMN approved bool DEFAULT True"
            self.db_connector(query)

    def db_table_add_default_column(self, table_name, column_name, column_type, default_value):
        """Iterates through the table dictionary and adds a field called approved, which is a bool, and is default
        true. This field allows products to be requested, as well as added directly by an admin. """
        query = "ALTER TABLE " + table_name + " ADD COLUMN " + column_name + " " + column_type + " DEFAULT " +\
            default_value
        self.db_connector(query)

    def db_drop_table(self, table_name):
        """Iterates through the table dictionary and adds a field called approved, which is a bool, and is default
        true. This field allows products to be requested, as well as added directly by an admin. """
        query = "DROP TABLE " + table_name
        self.db_connector(query)


# set up to create tables if run, and print tables to console.
db = CreateTb()
# db.db_table_creator(True)
# db.db_table_add_default_column("products", "card_comments", "text", "''")
