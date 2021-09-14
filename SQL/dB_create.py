from SQL.dB_connector import Connector
from SQL.dB_view import DbViews
import datetime


class CreateTb(Connector):
    def __init__(self):
        super(CreateTb, self).__init__()
        super(self.__class__, self).__init__()
        self.table_dictionary = {
                                "categories": """ CREATE TABLE IF NOT EXISTS categories (
                                                       id integer PRIMARY KEY,
                                                       category_name text) """,

                                "vendors": """ CREATE TABLE IF NOT EXISTS vendors (
                                                   id integer PRIMARY KEY,
                                                   vendor_name text) """,

                                "products": """ CREATE TABLE IF NOT EXISTS products (
                                                    id integer PRIMARY KEY,
                                                    categories_id int,
                                                    vendors_id int,
                                                    product_code text,
                                                    name text) """,

                                "credentials": """ CREATE TABLE IF NOT EXISTS credentials (
                                                       id integer PRIMARY KEY,
                                                       credential_level text) """,

                                "users": """ CREATE TABLE IF NOT EXISTS users (
                                                 id integer PRIMARY KEY,
                                                 credentials_id int,
                                                 user_name text,
                                                 user_password text) """,

                                "requests": """ CREATE TABLE IF NOT EXISTS requests (
                                                    id integer PRIMARY KEY,
                                                    products_id int,
                                                    users_id int,
                                                    request_date date,
                                                    amount int) """,

                                "orders": """ CREATE TABLE IF NOT EXISTS orders (
                                                  id integer PRIMARY KEY,
                                                  requests_id int,
                                                  order_date date) """,

                                "received": """ CREATE TABLE IF NOT EXISTS received (
                                                    id integer PRIMARY KEY,
                                                    orders_id int,
                                                    received_date date,
                                                    received_amount int) """,

                                "active_inventory": """ CREATE TABLE IF NOT EXISTS active_inventory (
                                                            id integer PRIMARY KEY,
                                                            received_id,
                                                            location text,
                                                            amount float) """,

                                "archived_inventory": """ CREATE TABLE IF NOT EXISTS archived_inventory (
                                                              id integer PRIMARY KEY,
                                                              received_id,
                                                              archived_date) """
                                 }
        self.db_views = DbViews()

    def db_table_creator(self, view_tables=False):
        for key, value in self.table_dictionary.items():
            self.db_connector(value)
        if view_tables:
            print("true")
            self.db_views.view_database_architecture()


db = CreateTb()
db.db_table_creator(True)
