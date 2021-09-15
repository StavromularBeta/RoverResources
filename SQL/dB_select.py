from SQL.dB_connector import Connector


class Select(Connector):
    def __init__(self):
        super(Select, self).__init__()
        super(self.__class__, self).__init__()

    def print_or_return_query(self, query, condition=None, print_view=False):
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
        if descending_order:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id DESC"
        else:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id"
        self.print_or_return_query(query, (condition,), print_view)

    def left_join_table_one_table_two(self,
                                      table_one_name_and_field,
                                      table_two_name_and_field,
                                      table_one_join_id,
                                      table_two_join_id,
                                      order_by_field,
                                      print_view=False):
        query = "SELECT " + table_one_name_and_field + ", " + table_two_name_and_field + " FROM " +\
                table_one_name_and_field.split(".")[0] + " LEFT JOIN " + table_two_name_and_field.split(".")[0] +\
                " ON " + table_one_join_id + " = " + table_two_join_id + " ORDER BY " + order_by_field
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
        query = "SELECT " + fields_to_select_string + " FROM " +\
                leftmost_table +\
                " LEFT JOIN " + middle_table +\
                " ON " + leftmost_id + " = " + middle_id_with_left +\
                " LEFT JOIN " + rightmost_table +\
                " ON " + middle_id_with_right + " = " + right_id +\
                " ORDER BY " + order_by_field
        self.print_or_return_query(query, False, print_view)
