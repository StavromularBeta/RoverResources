from SQL.dB_connector import Connector


class Select(Connector):
    """Contains selection methods for RoverResourcesDatabase."""
    def __init__(self):
        super(Select, self).__init__()
        super(self.__class__, self).__init__()

    def print_or_return_query(self, query, condition=None, print_view=False):
        """takes a query, optional conditions, and an optional print view bool. Executes on db. Prints if selected.

        Parameters
        ----------

        query : iterable
            SQL query to be executed on database.

        condition : item
            tuple of conditions to apply to query. Either a bool (False) if no condition, or a tuple of conditions.

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.
        """
        if print_view:
            if condition:
                for item in self.db_connector(query, condition):
                    print(item)
            else:
                for item in self.db_connector(query):
                    print(item)
        else:
            if condition:
                return self.db_connector(query, condition)
            else:
                return self.db_connector(query)

    # SINGLE TABLE SELECT METHODS

    def select_all_from_table(self, table_name, print_view=False, descending_order=False):
        """selects all records from a table.

        Parameters
        ----------

        table_name : string
            name of table to select all records from.

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.

        descending_order : bool
            if True, query is returned from db in descending order.
        """
        if descending_order:
            query = "SELECT * FROM " + table_name + " ORDER BY id DESC"
        else:
            query = "SELECT * FROM " + table_name + " ORDER BY id"
        self.print_or_return_query(query, False, print_view)

    def select_all_from_table_where_one_field_like(self,
                                                   table_name,
                                                   field_name,
                                                   condition,
                                                   print_view=False,
                                                   descending_order=False):
        """selects all records from a table, where a particular field matches (using like) a condition. This allows
        for partial matches when combined with regex.

        Parameters
        ----------

        table_name : string
            name of table to select all records from.

        field_name : string
            name of field to apply condition to.

        condition : string
            condition to apply to field (field LIKE condition).

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.

        descending_order : bool
            if True, query is returned from db in descending order.
        """
        if descending_order:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " LIKE (?) ORDER BY id DESC"
        else:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " LIKE (?) ORDER BY id"
        self.print_or_return_query(query, (condition,), print_view)

    def select_all_from_table_where_one_field_equals(self,
                                                     table_name,
                                                     field_name,
                                                     condition,
                                                     print_view=False,
                                                     descending_order=False):
        """selects all records from a table, where a particular field matches (using equals) a condition. Matches must
        be exact.

        Parameters
        ----------

        table_name : string
            name of table to select all records from.

        field_name : string
            name of field to apply condition to.

        condition : string
            condition to apply to field (field = condition).

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.

        descending_order : bool
            if True, query is returned from db in descending order.
        """
        if descending_order:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id DESC"
        else:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id"
        self.print_or_return_query(query, (condition,), print_view)

    # LEFT JOINS

    def left_join_multiple_tables(self,
                                  fields_to_select_string,
                                  table_list_of_lists,
                                  order_by_field,
                                  print_view=False):
        """Left joins any amount of tables.

        Parameters
        ----------

        fields_to_select_string : basestring
            the fields, separated by commas, that you want to display in the join.

        table_list_of_lists : list
            list of lists. Each list has 3 items - a table name, the index to join the table to the left table on, and
            the index to join the table to the right on. The first list is the table we are joining on, and thus has
            no second item (the left table join id). The last list is the last table, and has no third item (the right
            table to join ID).

        order_by_field : basestring
            the field to order the query by

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.
        """
        table_index = 0
        query = "SELECT " + fields_to_select_string + " FROM " + table_list_of_lists[0][0]
        for item in table_list_of_lists:
            if table_index == 0:
                table_index += 1
            else:
                query += " LEFT JOIN " + item[0] + " ON " + table_list_of_lists[table_index-1][2] + " = " + item[1]
                table_index += 1
        query += " ORDER BY " + order_by_field
        self.print_or_return_query(query, False, print_view)
