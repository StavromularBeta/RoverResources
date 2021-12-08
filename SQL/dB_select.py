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

    def select_all_from_table(self,
                              table_name,
                              print_view=False,
                              descending_order=False,
                              no_archived=False,
                              no_approved=False):
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
            if no_archived:
                if no_approved:
                    query = "SELECT * FROM " + table_name +\
                            " WHERE archived = False AND approved = True ORDER BY id DESC"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE archived = False ORDER BY id DESC"
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE approved = True ORDER BY id DESC"
                else:
                    query = "SELECT * FROM " + table_name + " ORDER BY id DESC"
        else:
            if no_archived:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE archived = False AND approved = True ORDER BY id"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE archived = False ORDER BY id"
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE approved = True ORDER BY id"
                else:
                    query = "SELECT * FROM " + table_name + " ORDER BY id"
        return self.print_or_return_query(query, False, print_view)

    def select_all_from_table_where_one_field_like(self,
                                                   table_name,
                                                   field_name,
                                                   condition,
                                                   print_view=False,
                                                   descending_order=False,
                                                   no_archive=False,
                                                   no_approved=False):
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
            if no_archive:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " LIKE (?) AND archived = False AND approved = True ORDER BY id DESC"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " LIKE (?) AND archived = False ORDER BY id DESC"
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " LIKE (?) AND approved = True ORDER BY id DESC"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name + " LIKE (?) ORDER BY id DESC"
        else:
            if no_archive:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " LIKE (?) AND archived = False AND approved = True ORDER BY id"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " LIKE (?) AND archived = False ORDER BY id"
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " LIKE (?) AND approved = True ORDER BY id"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name + " LIKE (?) ORDER BY id"
        return self.print_or_return_query(query, (condition,), print_view)

    def select_all_from_table_where_one_field_equals(self,
                                                     table_name,
                                                     field_name,
                                                     condition,
                                                     print_view=False,
                                                     descending_order=False,
                                                     no_archive=False,
                                                     no_approved=False):
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
            if no_archive:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                        " = (?) AND archived = False AND approved = True ORDER BY id DESC"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                        " = (?) AND archived = False ORDER BY id DESC"
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " = (?) AND approved = True ORDER BY id DESC"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id DESC"
        else:
            if no_archive:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " = (?) AND archived = False AND approved = True ORDER BY id"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " = (?) AND archived = False ORDER BY id"
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " = (?) AND approved = True ORDER BY id"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id"
        return self.print_or_return_query(query, (condition,), print_view)

    def select_all_from_table_where_one_field_equals_order_by(self,
                                                              table_name,
                                                              field_name,
                                                              condition,
                                                              order_by,
                                                              print_view=False,
                                                              descending_order=False,
                                                              no_archive=False,
                                                              no_approved=False):
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
            if no_archive:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                        " = (?) AND archived = False AND approved = True ORDER BY " + order_by + " DESC"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                        " = (?) AND archived = False ORDER BY " + order_by + " DESC"
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " = (?) AND approved = True ORDER BY " + order_by + " DESC"
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " = (?) ORDER BY " + order_by + " DESC"
        else:
            if no_archive:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                        " = (?) AND archived = False AND approved = True ORDER BY " + order_by
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                        " = (?) AND archived = False ORDER BY " + order_by
            else:
                if no_approved:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name +\
                            " = (?) AND approved = True ORDER BY " + order_by
                else:
                    query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY " + order_by
        return self.print_or_return_query(query, (condition,), print_view)

    def select_one_from_table_where_field_equals(self,
                                                 table_name,
                                                 field_name,
                                                 condition,
                                                 print_view=False,
                                                 descending_order=False):
        if descending_order:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id DESC LIMIT 1"
        else:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY id LIMIT 1"
        return self.print_or_return_query(query, (condition,), print_view)

    def select_one_from_table_where_field_equals_order_by(self,
                                                          table_name,
                                                          field_name,
                                                          condition,
                                                          order_by,
                                                          print_view=False,
                                                          descending_order=False):
        if descending_order:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY " + order_by +\
                    " DESC LIMIT 1"
        else:
            query = "SELECT * FROM " + table_name + " WHERE " + field_name + " = (?) ORDER BY " + order_by + " LIMIT 1"
        return self.print_or_return_query(query, (condition,), print_view)

    # LEFT JOINS

    def left_join_multiple_tables(self,
                                  fields_to_select_string,
                                  table_list_of_lists,
                                  order_by_field,
                                  print_view=False,
                                  no_archive=None,
                                  only_archive=None,
                                  no_approved=None,
                                  only_approved=None,
                                  search_by=None):
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

        no_archive : str
            the table reference to the archive field. if true, sets archive for main table to False, hides archived
            records.

        only_archive : str
            the table reference to the archive field. if true, sets archive for main table to True, gets only archived
            records.

        no_approved : str
            needs a better name. the table reference to the approved field. If true, sets approved for main table to
            False, which hides unapproved records.

        only_approved : str
            the table reference to the approved field. If true, sets approved for main table to True, which hides
            approved records.

        search_by : list
            first index is name of the field to search by, second record is string to search for. Does a match by using
            regex percentage tokens at start and end of string, plus use of LIKE term.
        """
        table_index = 0
        query = "SELECT " + fields_to_select_string + " FROM " + table_list_of_lists[0][0]
        for item in table_list_of_lists:
            if table_index == 0:
                table_index += 1
            else:
                query += " LEFT JOIN " + item[0] + " ON " + table_list_of_lists[table_index-1][2] + " = " + item[1]
                table_index += 1
        if no_archive or no_approved or search_by or only_approved or only_archive:
            query += " WHERE "
        # could probably make this much tighter using only elif statements.
        if no_archive:
            query += no_archive + " = False "
            if no_approved:
                query += "AND " + no_approved + " = True "
            elif only_approved:
                query += "AND " + only_approved + " = False "
            if search_by:
                query += " AND " + search_by[0] + " LIKE '" + search_by[1] + "'"
        elif only_archive:
            query += only_archive + " = True "
        else:
            if no_approved:
                query += no_approved + " = True "
                if search_by:
                    query += " AND " + search_by[0] + " LIKE '" + search_by[1] + "'"
            elif only_approved:
                query += only_approved + " = False "
                if search_by:
                    query += " AND " + search_by[0] + " LIKE '" + search_by[1] + "'"
            else:
                if search_by:
                    query += search_by[0] + " LIKE '" + search_by[1] + "'"
        query += " ORDER BY " + order_by_field
        print(query)
        return self.print_or_return_query(query, False, print_view)
