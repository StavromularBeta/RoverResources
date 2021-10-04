from SQL.dB_connector import Connector


class AddDelete(Connector):
    def __init__(self):
        super(AddDelete, self).__init__()
        super(self.__class__, self).__init__()

    # ADDING METHODS

    def new_categories_record(self, values):
        """Inserts new record into categories table. Categories table holds different categories of products the lab
        might purchase.

        Parameters
        ----------

        values : tuple
            (category name, comments)
        """
        query = 'INSERT OR IGNORE INTO categories (category_name, comments) VALUES (?,?)'
        return self.db_connector(query, values)

    def new_sub_categories_record(self, values):
        """Inserts new record into sub categories table. Sub categories table allows further division of categories.
        Mostly used for subdividing standards.

        Parameters
        ----------

        values : tuple
            (categories ID, category name, comments)
        """
        query = 'INSERT OR IGNORE INTO sub_categories (categories_id, sub_category_name, comments) VALUES (?,?,?)'
        return self.db_connector(query, values)

    def new_vendors_record(self, values):
        """Inserts new record into vendors table. Vendors table holds different vendors that might sell products to the
        lab.

        Parameters
        ----------

        values : tuple
            (vendor name, comments)
        """
        query = 'INSERT OR IGNORE INTO vendors (vendor_name, comments) VALUES (?, ?)'
        return self.db_connector(query, values)

    def new_products_record(self, values):
        """Inserts new record into products table. Products table holds approved products that have been ordered
        before. Can only request a product if it exists in the products table. Users with admin credentials can approve
        requests to add new products to this table.

        Parameters
        ----------

        values : tuple
            (category ID, sub category ID, vendors ID, product code, name, comments)
        """
        query = 'INSERT OR IGNORE' \
                ' INTO products' \
                ' (categories_id, sub_categories_id, vendors_id, product_code, name, comments)' \
                ' VALUES (?,?,?,?,?,?)'
        return self.db_connector(query, values)

    def new_credentials_record(self, values):
        """Inserts new record into credentials table. Credentials indicate what a particular user can do in the program.

        Parameters
        ----------

        values : tuple
            (credentials level, comments)
        """
        query = 'INSERT OR IGNORE INTO credentials (credential_level, comments) VALUES (?,?)'
        return self.db_connector(query, values)

    def new_user_record(self, values):
        """Inserts new record into users table. Each user of the program has a name, password, and level of credentials
        that will affect the level of functionality in the program they have access to.

        Parameters
        ----------

        values : tuple
            (credentials ID, user name, user password, comments)
        """
        query = 'INSERT OR IGNORE INTO users (credentials_id, user_name, user_password, comments) VALUES (?,?,?,?)'
        return self.db_connector(query, values)

    def new_requests_record(self, values):
        """Inserts new record into requests table. Requests table hold requests for products made by users. These are
        viewed in the GUI as individual 'shopping carts'.

        Parameters
        ----------

        values : tuple
            (products ID, users ID, request date, unit of issue, dollars per unit, amount, comments)
        """
        query = 'INSERT OR IGNORE' \
                ' INTO requests' \
                ' (products_id, users_id, request_date, unit_of_issue, dollar_per_unit, amount, comments)' \
                ' VALUES (?,?,?,?,?,?,?)'
        return self.db_connector(query, values)

    def new_orders_record(self, values):
        """Inserts new record into orders table. Orders table holds orders made by the lab. Each order has to have an
        associated request, that needs to have been approved by staff with admin credentials.

        Parameters
        ----------

        values : tuple
            (requests ID, order date, units ordered, comments)
        """
        query = 'INSERT OR IGNORE INTO orders (requests_id, order_date, units_ordered, comments) VALUES (?,?,?,?)'
        return self.db_connector(query, values)

    def new_received_record(self, values):
        """Inserts new record into received table. Received records indicate products that have arrived at the lab.
        Due to partial order fulfillment, each order may have multiple received records.

        Parameters
        ----------

        values : tuple
            (orders ID, received date, received amount, lot number,
             expiry date, storage location, model, equipment SIN, comments)
        """
        query = 'INSERT OR IGNORE' \
                ' INTO received' \
                ' (orders_id, received_date, received_amount, lot_number, expiry_date, storage_location, ' \
                'model, equipment_SIN, comments) VALUES (?,?,?,?,?,?,?,?,?)'
        return self.db_connector(query, values)

    def new_active_inventory_record(self, values):
        """Inserts new record into active inventory. Received records become inventory items. Additional information
        may be added to the inventory record upon receiving, such as expiry dates and batch numbers.

        Parameters
        ----------

        values : tuple
            (received ID, lab location, amount)
        """
        query = 'INSERT OR IGNORE INTO active_inventory (received_id, location, amount) VALUES (?,?,?)'
        return self.db_connector(query, values)

    def new_archived_inventory_record(self, values):
        """Inserts new record into archived inventory. When active inventory items are consumed, discontinued, or
        disposed of, they become archived records. Only inventory items currently valid and in use in the lab are
        found in the active inventory table.

        Parameters
        ----------

        values : tuple
            (received ID, archived_date)
        """
        query = 'INSERT OR IGNORE INTO archived_inventory (received_id, archived_date) VALUES (?,?)'
        return self.db_connector(query, values)

    # DELETING METHODS

    def delete_entry_from_table_by_id(self, table_name, record_id):
        """Deletes a record from a table corresponding to a particular primary ID.

        Parameters
        ----------

        table_name : basestring
            the name of the table the record is being deleted from.

        record_id : int
            the ID of the record to be deleted.
        """
        query = 'DELETE FROM ' + table_name + ' WHERE id = ?'
        return self.db_connector(query, (record_id,))

    def delete_entries_from_table_by_field_condition(self, table_name, field_name, field_condition):
        """Deletes record(s) from a table corresponding to a particular condition of a field.

        Parameters
        ----------

        table_name : basestring
            the name of the table the record is being deleted from.

        field_name : basestring
            the ID of the record to be deleted.

        field_condition : object
            the condition to apply to the field. Type will match field type (datetime, float, int, string).
        """
        query = 'DELETE FROM ' + table_name + ' WHERE ' + field_name + " = ?"
        return self.db_connector(query, (field_condition,))
