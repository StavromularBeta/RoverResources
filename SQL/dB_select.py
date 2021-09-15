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

    def left_join_two_tables(self,
                             fields_to_select_string,
                             left_table,
                             left_id,
                             right_table,
                             right_id,
                             order_by_field,
                             print_view=True):
        """Left joins two tables.

        Parameters
        ----------

        fields_to_select_string : basestring
            the fields, separated by commas, that you want to display in the join.

        left_table : basestring
            the leftmost table of the join.

        left_id : basestring
            the left table id used to combine the two tables.

        right_table : basestring
            the rightmost table of the join.

        right_id : basestring
            the right table id used to combine the two tables.

        order_by_field : basestring
            the field to order the query by

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.
        """
        query = "SELECT " + fields_to_select_string + " FROM " +\
            left_table +\
            " LEFT JOIN " + right_table +\
            " ON " + left_id + " = " + right_id +\
            " ORDER BY " + order_by_field
        self.print_or_return_query(query, False, print_view)

    def left_join_three_tables(self,
                               fields_to_select_string,
                               leftmost_table,
                               leftmost_id,
                               middle_table,
                               middle_id_with_left,
                               middle_id_with_right,
                               rightmost_table,
                               right_id,
                               order_by_field,
                               print_view=True):
        """Left joins three tables.

        Parameters
        ----------

        fields_to_select_string : basestring
            the fields, separated by commas, that you want to display in the join.

        leftmost_table : basestring
            the leftmost table of the join.

        leftmost_id : basestring
            the left table id used to combine the leftmost table to the middle table.

        middle_table : basestring
            the middle table of the join.

        middle_id_with_left : basestring
            the middle table id used to combine the middle table to the leftmost table.

        middle_id_with_right : basestring
            the middle table id used to combine the middle table to the rightmost table.

        rightmost_table : basestring
            the rightmost table of the join.

        right_id : basestring
            the right table id used to combine the right table to the middle table.

        order_by_field : basestring
            the field to order the query by

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.
        """
        query = "SELECT " + fields_to_select_string + " FROM " +\
                leftmost_table +\
                " LEFT JOIN " + middle_table +\
                " ON " + leftmost_id + " = " + middle_id_with_left +\
                " LEFT JOIN " + rightmost_table +\
                " ON " + middle_id_with_right + " = " + right_id +\
                " ORDER BY " + order_by_field
        self.print_or_return_query(query, False, print_view)

    def left_join_four_tables(self,
                              fields_to_select_string,
                              leftmost_table,
                              leftmost_id,
                              middle_table_1,
                              middle_id_with_left_1,
                              middle_id_with_right_1,
                              middle_table_2,
                              middle_id_with_left_2,
                              middle_id_with_right_2,
                              rightmost_table,
                              right_id,
                              order_by_field,
                              print_view=True):
        """Left joins three tables.

        Parameters
        ----------

        fields_to_select_string : basestring
            the fields, separated by commas, that you want to display in the join.

        leftmost_table : basestring
            the leftmost table of the join.

        leftmost_id : basestring
            the left table id used to combine the leftmost table to the middle table.

        middle_table_1 : basestring
            the second table of the join.

        middle_id_with_left_1 : basestring
            the second table id used to combine the second table to the leftmost table.

        middle_id_with_right_1 : basestring
            the second table id used to combine the second table to the third table.

        middle_table_2 : basestring
            the third table of the join.

        middle_id_with_left_2 : basestring
            the third table id used to combine the third table to the second table.

        middle_id_with_right_2 : basestring
            the third table id used to combine the third table to the rightmost table.

        rightmost_table : basestring
            the rightmost table of the join.

        right_id : basestring
            the right table id used to combine the rightmost table to the third table.

        order_by_field : basestring
            the field to order the query by

        print_view : bool
            True if you want to print query result to console. If selected, method returns nothing. Otherwise,
            returns query.
        """
        query = "SELECT " + fields_to_select_string + " FROM " +\
                leftmost_table +\
                " LEFT JOIN " + middle_table_1 +\
                " ON " + leftmost_id + " = " + middle_id_with_left_1 +\
                " LEFT JOIN " + middle_table_2 +\
                " ON " + middle_id_with_right_1 + " = " + middle_id_with_left_2 +\
                " LEFT JOIN " + rightmost_table +\
                " ON " + middle_id_with_right_2 + " = " + right_id +\
                " ORDER BY " + order_by_field
        self.print_or_return_query(query, False, print_view)
