import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_data_export as tk_dataExport
import datetime


class ShoppingCartViewAdmin(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.data_export = tk_dataExport.TkDataExportMethods()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.products_list = ""
        self.shopping_cart = ""
        self.total_cost = 0.0
        self.config(bg=self.formatting.colour_code_1)
        self.products_list_scrollable_container = tk.Frame(self)
        self.shopping_cart_scrollable_container = tk.Frame(self)
        self.products_list_frame = tk.Frame(self)
        self.products_list_frame.config(bg=self.formatting.colour_code_1)
        self.shopping_cart_frame = tk.Frame(self)
        self.shopping_cart_frame.config(bg=self.formatting.colour_code_1)
        self.shopping_cart_navigation_frame = tk.Frame(self)
        self.shopping_cart_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.sort_shopping_cart_view_by = ["Product Name",
                                           "Product Code",
                                           "Vendor Name",
                                           "Product Category",
                                           "Request Date",
                                           "Units",
                                           "Cost",
                                           "Amount Requested",
                                           "Staff Member"]
        self.shopping_cart_sort_value = tk.StringVar(self)
        self.shopping_cart_sort_value.set("Product Name")
        self.sort_shopping_cart_search_by = ["Product Name",
                                             "Product Code",
                                             "Vendor Name",
                                             "Product Category",
                                             "Staff Member"]
        self.shopping_cart_search_value = tk.StringVar(self)
        self.shopping_cart_search_value.set("Product Name")
        self.sort_by_shopping_cart_conversion_dictionary = {"Staff Member": "u.user_name",
                                                            "Product Code": "p.product_code",
                                                            "Vendor Name": "v.vendor_name",
                                                            "Product Category": "c.category_name",
                                                            "Request Date": "r.request_date",
                                                            "Product Name": "p.name",
                                                            "Units": "p.unit_of_issue",
                                                            "Cost": "pt.cost",
                                                            "Amount Requested": "r.amount"}
        self.admin_shopping_cart_canvas_length = 0
        self.search_by_active_term = ""
        self.sort_by = ""
        self.search_by_variable = ""
        self.printable_shopping_cart = []

    # MAIN METHOD

    def shopping_cart_view_admin(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.search_by_active_term = search_by
        self.sort_by = sort_by
        self.search_by_variable = search_by_variable
        self.active_user = user
        self.create_shopping_cart(sort_by, search_by, search_by_variable)

    # SHOPPING CART METHODS

    def create_shopping_cart(self, sort_by=False, search_by=False, search_by_variable=False):
        self.get_active_user_shopping_cart_from_database(sort_by, search_by, search_by_variable)
        self.make_scrollable_shopping_cart_header_labels()
        self.populate_scrollable_shopping_cart()
        self.create_scrollable_shopping_cart()
        self.create_shopping_cart_navigation_frame()
        self.shopping_cart_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.shopping_cart_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def create_shopping_cart_navigation_frame(self):
        product_search_entry = tk.Entry(self.shopping_cart_navigation_frame)
        # if there is an active search term, inserts it into entry box.
        if self.search_by_active_term:
            product_search_entry.insert(0, self.search_by_active_term)
        tk.Label(self.shopping_cart_navigation_frame,
                 text="All Shopping Carts",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Label(self.shopping_cart_navigation_frame,
                 text="Total Cost: $ " + "{:.2f}".format(self.total_cost),
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=1, sticky=tk.E, padx=10, pady=5)
        tk.Label(self.shopping_cart_navigation_frame,
                 text="Sort: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=2, sticky=tk.W, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.shopping_cart_navigation_frame,
                                          self.shopping_cart_sort_value,
                                          *self.sort_shopping_cart_view_by)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(row=0, column=3, sticky=tk.W, pady=5)
        sort_by_button = tk.Button(self.shopping_cart_navigation_frame,
                                   text="Sort",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_admin_shopping_cart_view(
                                       self.active_user,
                                       sort_by=self.shopping_cart_sort_value.get(),
                                       search_by=self.search_by_active_term,
                                       search_by_variable=self.search_by_variable)).grid(
            row=0, column=4, sticky=tk.W, padx=10, pady=5
        )
        # searching tk widgets
        type_of_search_menu = tk.OptionMenu(self.shopping_cart_navigation_frame,
                                            self.shopping_cart_search_value,
                                            *self.sort_shopping_cart_search_by)
        type_of_search_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_search_menu.config(font=self.formatting.medium_step_font)
        tk.Label(self.shopping_cart_navigation_frame,
                 text="Search:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=5, sticky=tk.W, pady=5)
        product_search_entry.grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
        type_of_search_menu.grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
        search_by_button = tk.Button(self.shopping_cart_navigation_frame,
                                     text="Search",
                                     font=self.formatting.medium_step_font,
                                     command=lambda: self.parent.display_admin_shopping_cart_view(
                                       self.active_user,
                                       sort_by=self.sort_by,
                                       search_by=product_search_entry.get(),
                                       search_by_variable=self.shopping_cart_search_value.get())).grid(
            row=0, column=8, sticky=tk.W, pady=5
        )
        tk.Button(self.shopping_cart_navigation_frame,
                  text="All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_admin_shopping_cart_view(
                      self.active_user)).grid(
            row=0, column=9, sticky=tk.W, padx=10, pady=5
        )
        # print view
        tk.Button(self.shopping_cart_navigation_frame,
                  text="Print",
                  font=self.formatting.medium_step_font,
                  command=lambda : self.data_export.generate_data_export_popup(
                      self.active_user,
                      self.printable_shopping_cart,
                      "requests")).grid(
            row=0,
            column=10,
            sticky=tk.W,
            padx=10,
            pady=5)

    def get_active_user_shopping_cart_from_database(self, sort_by=None, search_by=None, search_by_variable=None):
        if sort_by and search_by:
            sort_by_variable = self.sort_by_shopping_cart_conversion_dictionary[sort_by]
            self.shopping_cart_sort_value.set(sort_by)
            search_by_field = self.sort_by_shopping_cart_conversion_dictionary[search_by_variable]
            self.shopping_cart_search_value.set(search_by_variable)
            self.shopping_cart = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date," +
                                          " r.amount, u.user_name, p.unit_of_issue, pt.cost, r.id",
                                          [["requests r", "", "r.products_id"],
                                           ["products p", "p.id", "r.users_id"],
                                           ["users u", "u.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          sort_by_variable,
                                          no_archive="r.archived",
                                          search_by=[search_by_field, '%' + search_by + '%'],)
        elif sort_by:
            sort_by_variable = self.sort_by_shopping_cart_conversion_dictionary[sort_by]
            self.shopping_cart_sort_value.set(sort_by)
            self.shopping_cart = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date," +
                                          " r.amount, u.user_name, p.unit_of_issue, pt.cost, r.id",
                                          [["requests r", "", "r.products_id"],
                                           ["products p", "p.id", "r.users_id"],
                                           ["users u", "u.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          sort_by_variable,
                                          no_archive="r.archived")
        elif search_by:
            search_by_field = self.sort_by_shopping_cart_conversion_dictionary[search_by_variable]
            self.shopping_cart_search_value.set(search_by_variable)
            self.shopping_cart = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date," +
                                          " r.amount, u.user_name, p.unit_of_issue, pt.cost, r.id",
                                          [["requests r", "", "r.products_id"],
                                           ["products p", "p.id", "r.users_id"],
                                           ["users u", "u.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          "p.name",
                                          no_archive="r.archived",
                                          search_by=[search_by_field, '%' + search_by + '%'],)
        else:
            self.shopping_cart = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date," +
                                          " r.amount, u.user_name, p.unit_of_issue, pt.cost, r.id",
                                          [["requests r", "", "r.products_id"],
                                           ["products p", "p.id", "r.users_id"],
                                           ["users u", "u.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          "u.user_name",
                                          no_archive="r.archived")

    def make_scrollable_shopping_cart_header_labels(self):
        tk.Label(self.shopping_cart_frame,
                 text="Product Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Product ID",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Vendor",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Category",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Request Date",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=5, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Unit of Issue",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Dollar/Unit",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Amount Requested",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=8, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Staff Member",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=9, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_shopping_cart(self):
        row_counter = 1
        even_odd = 1
        for item in self.shopping_cart:
            self.printable_shopping_cart.append(item)
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            product_name = item[0]
            tk.Label(self.shopping_cart_frame,
                     text=product_name,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=200,
                     justify=tk.LEFT).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=5, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[7],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[8],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=str(item[5]) + " (" + "{:.2f}".format(float(item[8])*float(item[5])) + ")",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=8, sticky=tk.W, padx=10, pady=5)
            self.total_cost += float(item[8])*float(item[5])
            tk.Label(self.shopping_cart_frame,
                     text=item[6],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=9, sticky=tk.W, padx=10, pady=5)
            if self.active_user[1] == 1:
                tk.Button(self.shopping_cart_frame,
                          text="Remove Request",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.remove_product_from_cart(item[9])).grid(row=row_counter,
                                                                                                 column=10,
                                                                                                 sticky=tk.W,
                                                                                                 padx=10,
                                                                                                 pady=5)
                tk.Button(self.shopping_cart_frame,
                          text="Order",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.order_product_popup(item[9], item[0])).grid(row=row_counter,
                                                                                                     column=11,
                                                                                                     sticky=tk.W,
                                                                                                     padx=10,
                                                                                                     pady=5)
            row_counter += 1
            even_odd += 1
            self.admin_shopping_cart_canvas_length += 50

    def create_scrollable_shopping_cart(self):
        shopping_cart_canvas = tk.Canvas(self.shopping_cart_scrollable_container,
                                         width=1650,
                                         height=500,
                                         scrollregion=(0, 0, 0, self.admin_shopping_cart_canvas_length),
                                         bd=0,
                                         highlightthickness=0)
        shopping_cart_canvas.config(bg=self.formatting.colour_code_1)
        shopping_cart_canvas_scrollbar = tk.Scrollbar(self.shopping_cart_scrollable_container,
                                                      orient="vertical",
                                                      command=shopping_cart_canvas.yview)
        shopping_cart_canvas.configure(yscrollcommand=shopping_cart_canvas_scrollbar.set)
        shopping_cart_canvas_scrollbar.pack(side='left',
                                            fill='y')
        shopping_cart_canvas.pack(side="right",
                                  fill='y')
        shopping_cart_canvas.create_window((0, 0),
                                           window=self.shopping_cart_frame,
                                           anchor="nw")

    def remove_product_from_cart(self, request_to_remove):
        self.add_delete_db.delete_entries_from_table_by_field_condition("requests",
                                                                        "id",
                                                                        request_to_remove)
        self.parent.display_admin_shopping_cart_view(self.active_user,
                                                     sort_by=self.sort_by,
                                                     search_by=self.search_by_active_term,
                                                     search_by_variable=self.search_by_variable)

    def order_product_popup(self, request_to_order, product_to_order):
        order_product_popup = tk.Toplevel()
        order_product_popup.config(bg=self.formatting.colour_code_1)
        order_product_popup.geometry('550x450')
        units_ordered_entry = tk.Entry(order_product_popup)
        most_recent_order_check = self.select_db.left_join_multiple_tables(
            "o.id, p.name, o.units_ordered, o.order_date",
            [["orders o", "", "o.requests_id"],
             ["requests r", "r.id", "r.products_id"],
             ["products p", "p.id", ""]],
            "o.order_date DESC LIMIT 1",
            search_by=["p.name", '%' + product_to_order + '%'],
            no_archive="o.archived"
        )
        most_recent_order_check = [item for item in most_recent_order_check]
        tk.Label(order_product_popup,
                 text="Units Ordered: ",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2
                 ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        units_ordered_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(order_product_popup,
                 text="Comments",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2
                 ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        order_comments_textbox = tk.Text(order_product_popup,
                                         height=10,
                                         width=45)
        order_comments_textbox.config(state=tk.NORMAL, wrap="word")
        order_comments_textbox.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        tk.Button(order_product_popup,
                  text="Order Product",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.order_request_and_reload_admin_shopping_cart(request_to_order,
                                                                                    datetime.date.today(),
                                                                                    units_ordered_entry.get(),
                                                                                    order_comments_textbox.get("1.0",
                                                                                                               tk.END),
                                                                                    order_product_popup,
                                                                                    product_to_order)).grid(
            row=3, column=0, sticky=tk.W, padx=10, pady=5
        )
        if len(most_recent_order_check) > 0:
            tk.Label(order_product_popup,
                     text="Last ordered: " + str(most_recent_order_check[0][2]) + " Units on " +
                     str(most_recent_order_check[0][3]) + ".",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=4, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        else:
            tk.Label(order_product_popup,
                     text="No record of product being ordered previously.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=4, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)

    def order_request_and_reload_admin_shopping_cart(self,
                                                     requests_id,
                                                     order_date,
                                                     units_ordered,
                                                     comments,
                                                     order_popup,
                                                     product_to_order,
                                                     confirmed=False):
        active_orders_check = self.select_db.left_join_multiple_tables(
            "o.id, p.name, o.units_ordered",
            [["orders o", "", "o.requests_id"],
             ["requests r", "r.id", "r.products_id"],
             ["products p", "p.id", ""]],
            "p.name",
            search_by=["p.name", '%' + product_to_order + '%'],
            no_archive="o.archived"
        )
        active_ordered_units = 0
        for item in active_orders_check:
            active_ordered_units += int(item[2])
        if active_ordered_units > 0 and not confirmed:
            tk.Label(order_popup,
                     text="There are " + str(active_ordered_units) +
                          " unit(s) of this product currently ordered. Continue?",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=5, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
            tk.Button(order_popup,
                      text="Confirm Order",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.order_request_and_reload_admin_shopping_cart(requests_id,
                                                                                        order_date,
                                                                                        units_ordered,
                                                                                        comments,
                                                                                        order_popup,
                                                                                        product_to_order,
                                                                                        confirmed=True)).grid(
                row=6, column=0, sticky=tk.W, padx=10, pady=5)
        else:
            self.add_delete_db.new_orders_record((requests_id,
                                                 order_date,
                                                 units_ordered,
                                                 comments))
            self.edit_db.archive_entry_in_table_by_id("requests",
                                                      requests_id)
            order_popup.destroy()
            self.parent.display_admin_shopping_cart_view(self.active_user,
                                                         sort_by=self.sort_by,
                                                         search_by=self.search_by_active_term,
                                                         search_by_variable=self.search_by_variable)
