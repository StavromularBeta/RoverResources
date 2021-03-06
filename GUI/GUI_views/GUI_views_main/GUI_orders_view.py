import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_errorHandling as tk_errorHandling
from GUI.GUI_formatting import GUI_data_export as tk_dataExport
import datetime


class OrdersView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.data_export = tk_dataExport.TkDataExportMethods()
        self.error_handling = tk_errorHandling.ErrorHandling()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.config(bg=self.formatting.colour_code_1)
        self.orders = ()
        self.orders_canvas_length = 0
        self.total_order_cost = 0
        self.orders_scrollable_container = tk.Frame(self)
        self.orders_frame = tk.Frame(self)
        self.orders_frame.config(bg=self.formatting.colour_code_1)
        self.orders_navigation_frame = tk.Frame(self)
        self.orders_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.sort_orders_view_by = ["Product Name",
                                    "Product Code",
                                    "Vendor Name",
                                    "Product Category",
                                    "Order Date",
                                    "Units",
                                    "Cost",
                                    "Staff Member",
                                    "Request Amount",
                                    "Order Amount"]
        self.orders_sort_value = tk.StringVar(self)
        self.orders_sort_value.set("Product Name")
        self.sort_orders_search_by = ["Product Name",
                                      "Product Code",
                                      "Vendor Name",
                                      "Product Category",
                                      "Units",
                                      "Staff Member"]
        self.orders_search_value = tk.StringVar(self)
        self.orders_search_value.set("Product Name")
        self.sort_by_orders_conversion_dictionary = {"Staff Member": "u.user_name",
                                                     "Product Code": "p.product_code",
                                                     "Vendor Name": "v.vendor_name",
                                                     "Product Category": "c.category_name",
                                                     "Order Date": "o.order_date",
                                                     "Product Name": "p.name",
                                                     "Cost": "pt.cost",
                                                     "Units": "p.unit_of_issue",
                                                     "Request Amount": "r.amount",
                                                     "Order Amount": "o.units_ordered"}
        self.search_by_active_term = ""
        self.sort_by = ""
        self.search_by_variable = ""
        self.popup_error_message = tk.Label()
        self.printable_orders_list = []

    def orders_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.sort_by = sort_by
        self.search_by_active_term = search_by
        self.search_by_variable = search_by_variable
        self.active_user = user
        self.create_orders_view(sort_by, search_by, search_by_variable)

    def create_orders_view(self, sort_by=False, search_by=False, search_by_variable=False):
        self.get_active_orders_from_database(sort_by, search_by, search_by_variable)
        self.make_scrollable_orders_header_labels()
        self.populate_scrollable_orders_list()
        self.create_scrollable_orders_view()
        self.create_orders_navigation_frame()
        self.orders_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.orders_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def create_orders_navigation_frame(self):
        orders_search_entry = tk.Entry(self.orders_navigation_frame)
        if self.search_by_active_term:
            orders_search_entry.insert(0, self.search_by_active_term)
        tk.Label(self.orders_navigation_frame,
                 text="All Orders",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Label(self.orders_navigation_frame,
                 text="Total Cost: $ " + "{:.2f}".format(self.total_order_cost),
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=1, sticky=tk.E, padx=10, pady=5)
        tk.Label(self.orders_navigation_frame,
                 text="Sort:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.orders_navigation_frame,
                                          self.orders_sort_value,
                                          *self.sort_orders_view_by)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
        sort_by_button = tk.Button(self.orders_navigation_frame,
                                   text="Sort",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_orders_view(
                                       self.active_user,
                                       sort_by=self.orders_sort_value.get(),
                                       search_by=self.search_by_active_term,
                                       search_by_variable=self.search_by_variable)).grid(
            row=0, column=4, sticky=tk.W, padx=10, pady=5
        )
        tk.Label(self.orders_navigation_frame,
                 text="Search:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=5, sticky=tk.W, pady=5)
        orders_search_entry.grid(row=0, column=6, sticky=tk.W, pady=5)
        # searching tk widgets
        type_of_search_menu = tk.OptionMenu(self.orders_navigation_frame,
                                            self.orders_search_value,
                                            *self.sort_orders_search_by)
        type_of_search_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_search_menu.config(font=self.formatting.medium_step_font)
        type_of_search_menu.grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
        search_by_button = tk.Button(self.orders_navigation_frame,
                                     text="Search",
                                     font=self.formatting.medium_step_font,
                                     command=lambda: self.parent.display_orders_view(
                                       self.active_user,
                                       sort_by=self.sort_by,
                                       search_by=orders_search_entry.get(),
                                       search_by_variable=self.orders_search_value.get())).grid(
            row=0, column=8, sticky=tk.W, padx=10, pady=5
        )
        tk.Button(self.orders_navigation_frame,
                  text="All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_orders_view(
                      self.active_user)).grid(
            row=0, column=9, sticky=tk.W, padx=10, pady=5
        )
        # print view
        tk.Button(self.orders_navigation_frame,
                  text="Print",
                  font=self.formatting.medium_step_font,
                  command=lambda : self.data_export.generate_data_export_popup(
                      self.active_user,
                      self.printable_orders_list,
                      "orders")).grid(
            row=0,
            column=10,
            sticky=tk.W,
            padx=10,
            pady=5)

    def get_active_orders_from_database(self, sort_by=None, search_by=None, search_by_variable=None):
        if sort_by and search_by:
            sort_by_variable = self.sort_by_orders_conversion_dictionary[sort_by]
            self.orders_sort_value.set(sort_by)
            self.search_by_active_term = search_by
            search_by_field = self.sort_by_orders_conversion_dictionary[search_by_variable]
            self.orders = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, p.unit_of_issue," +
                                          " pt.cost, u.user_name, r.amount, o.units_ordered, o.order_date, o.id",
                                          [["orders o", "", "o.requests_id"],
                                           ["requests r", "r.id", "r.users_id"],
                                           ["users u", "u.id", "r.products_id"],
                                           ["products p", "p.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          sort_by_variable,
                                          no_archive="o.archived",
                                          search_by=[search_by_field, '%' + search_by + '%'])
        elif sort_by:
            sort_by_variable = self.sort_by_orders_conversion_dictionary[sort_by]
            self.orders_sort_value.set(sort_by)
            self.orders = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, p.unit_of_issue," +
                                          " pt.cost, u.user_name, r.amount, o.units_ordered, o.order_date, o.id",
                                          [["orders o", "", "o.requests_id"],
                                           ["requests r", "r.id", "r.users_id"],
                                           ["users u", "u.id", "r.products_id"],
                                           ["products p", "p.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          sort_by_variable,
                                          no_archive="o.archived")
        elif search_by:
            self.search_by_active_term = search_by
            search_by_field = self.sort_by_orders_conversion_dictionary[search_by_variable]
            self.orders = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, p.unit_of_issue," +
                                          " pt.cost, u.user_name, r.amount, o.units_ordered, o.order_date, o.id",
                                          [["orders o", "", "o.requests_id"],
                                           ["requests r", "r.id", "r.users_id"],
                                           ["users u", "u.id", "r.products_id"],
                                           ["products p", "p.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          "p.name",
                                          no_archive="o.archived",
                                          search_by=[search_by_field, '%' + search_by + '%'])
        else:
            self.orders = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, p.unit_of_issue," +
                                          " pt.cost, u.user_name, r.amount, o.units_ordered, o.order_date, o.id",
                                          [["orders o", "", "o.requests_id"],
                                           ["requests r", "r.id", "r.users_id"],
                                           ["users u", "u.id", "r.products_id"],
                                           ["products p", "p.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", ""]],
                                          "p.name",
                                          no_archive="o.archived")

    def create_scrollable_orders_view(self):
        orders_canvas = tk.Canvas(self.orders_scrollable_container,
                                  width=1650,
                                  height=500,
                                  scrollregion=(0, 0, 0, self.orders_canvas_length),
                                  bd=0,
                                  highlightthickness=0)
        orders_canvas.config(bg=self.formatting.colour_code_1)
        orders_canvas_scrollbar = tk.Scrollbar(self.orders_scrollable_container,
                                               orient="vertical",
                                               command=orders_canvas.yview)
        orders_canvas.configure(yscrollcommand=orders_canvas_scrollbar.set)
        orders_canvas_scrollbar.pack(side='left',
                                     fill='y')
        orders_canvas.pack(side="right",
                           fill='y')
        orders_canvas.create_window((0, 0),
                                    window=self.orders_frame,
                                    anchor="nw")

    def make_scrollable_orders_header_labels(self):
        tk.Label(self.orders_frame,
                 text="Product Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="Product ID",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="Vendor",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="Category",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="Order Date",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=5, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="Unit of Issue",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="Dollar/Unit",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="Staff",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=8, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="# Requested",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=9, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.orders_frame,
                 text="# Ordered",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=10, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_orders_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.orders:
            print(item)
            self.printable_orders_list.append(item)
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            tk.Label(self.orders_frame,
                     text=item[0],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=200,
                     justify=tk.LEFT).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=item[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=item[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=item[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=item[9],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=5, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=item[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=str(item[5]) + " (" + "{:.2f}".format(float(item[8])*float(item[5])) + ")",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            self.total_order_cost += float(item[8])*float(item[5])
            tk.Label(self.orders_frame,
                     text=item[6],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=8, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=item[7],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=9, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.orders_frame,
                     text=item[8],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=10, sticky=tk.W, padx=10, pady=5)
            if self.active_user[1] in [1, 3]:
                tk.Button(self.orders_frame,
                          text="Receive Order",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.receive_product_popup(item[10])).grid(row=row_counter,
                                                                                               column=11,
                                                                                               sticky=tk.W,
                                                                                               padx=10,
                                                                                               pady=5)
                tk.Button(self.orders_frame,
                          text="Cancel Order",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.cancel_order_popup(item[10])).grid(row=row_counter,
                                                                                            column=12,
                                                                                            sticky=tk.W,
                                                                                            padx=10,
                                                                                            pady=5)
            row_counter += 1
            even_odd += 1
            self.orders_canvas_length += 50

    def cancel_order_popup(self, order_to_cancel):
        cancel_order_popup = tk.Toplevel()
        cancel_order_popup.config(bg=self.formatting.colour_code_1)
        cancel_order_popup.geometry('900x250')
        tk.Label(cancel_order_popup,
                 text="Are you sure you want to cancel this order? it will be removed" +
                 " from the database permanently.\n" +
                 "Alternatively, you can archive this order if you're unsure.",
                 justify=tk.LEFT,
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5, padx=10)
        tk.Button(cancel_order_popup,
                  text="Cancel Order",
                  font=self.formatting.medium_step_font,
                  command=lambda item=order_to_cancel: self.cancel_order_if_not_partially_received_and_reload_page(
                      item,
                      cancel_order_popup)).grid(
            row=1,
            column=0,
            sticky=tk.W,
            padx=10,
            pady=5)
        tk.Button(cancel_order_popup,
                  text="Archive Order",
                  font=self.formatting.medium_step_font,
                  command=lambda item=order_to_cancel: self.archive_order_and_reload_orders_page(
                      item,
                      cancel_order_popup)).grid(
            row=2,
            column=0,
            sticky=tk.W,
            padx=10,
            pady=5)

    def receive_product_popup(self, order_to_receive):
        receive_product_popup = tk.Toplevel()
        receive_product_popup.config(bg=self.formatting.colour_code_1)
        receive_product_popup.geometry('500x700')
        tk.Label(receive_product_popup,
                 text="Receive Order",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Amount Received",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, padx=10)
        amount_received_entry = tk.Entry(receive_product_popup)
        amount_received_entry.grid(row=1, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Date (leave blank if today)",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Year",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=3, column=0, sticky=tk.W, padx=10)
        year_entry = tk.Entry(receive_product_popup)
        year_entry.grid(row=3, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Month",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=4, column=0, sticky=tk.W, padx=10)
        month_entry = tk.Entry(receive_product_popup)
        month_entry.grid(row=4, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Day",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10)
        day_entry = tk.Entry(receive_product_popup)
        day_entry.grid(row=5, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Receiving Information (Optional)",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Lot Number",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=7, column=0, sticky=tk.W, padx=10)
        lot_number_entry = tk.Entry(receive_product_popup)
        lot_number_entry.grid(row=7, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Serial Number",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=8, column=0, sticky=tk.W, padx=10)
        serial_entry = tk.Entry(receive_product_popup)
        serial_entry.grid(row=8, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Model",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=9, column=0, sticky=tk.W, padx=10)
        model_entry = tk.Entry(receive_product_popup)
        model_entry.grid(row=9, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Product Expiry Date",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Year",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=11, column=0, sticky=tk.W, padx=10)
        expiry_year_entry = tk.Entry(receive_product_popup)
        expiry_year_entry.grid(row=11, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Month",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=12, column=0, sticky=tk.W, padx=10)
        expiry_month_entry = tk.Entry(receive_product_popup)
        expiry_month_entry.grid(row=12, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Day",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=13, column=0, sticky=tk.W, padx=10)
        expiry_day_entry = tk.Entry(receive_product_popup)
        expiry_day_entry.grid(row=13, column=1, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text="Comments",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=14, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        received_notes = tk.Text(receive_product_popup,
                                 height=5,
                                 width=40)
        received_notes.config(bg=self.formatting.colour_code_2)
        received_notes.config(state=tk.NORMAL)
        received_notes.grid(row=15, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(receive_product_popup,
                  text="Partially Receive Order",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.receive_order_and_reload_orders_page(order_to_receive,
                                                                            receive_product_popup,
                                                                            (year_entry.get(),
                                                                             month_entry.get(),
                                                                             day_entry.get(),
                                                                             expiry_year_entry.get(),
                                                                             expiry_month_entry.get(),
                                                                             expiry_day_entry.get(),
                                                                             amount_received_entry.get(),
                                                                             lot_number_entry.get(),
                                                                             serial_entry.get(),
                                                                             model_entry.get(),
                                                                             received_notes.get("1.0", tk.END),
                                                                             ),
                                                                            partial=True)).grid(
            row=16,
            column=0,
            sticky=tk.W,
            padx=10,
            pady=5)
        tk.Button(receive_product_popup,
                  text="Receive Order",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.receive_order_and_reload_orders_page(order_to_receive,
                                                                            receive_product_popup,
                                                                            (year_entry.get(),
                                                                             month_entry.get(),
                                                                             day_entry.get(),
                                                                             expiry_year_entry.get(),
                                                                             expiry_month_entry.get(),
                                                                             expiry_day_entry.get(),
                                                                             amount_received_entry.get(),
                                                                             lot_number_entry.get(),
                                                                             serial_entry.get(),
                                                                             model_entry.get(),
                                                                             received_notes.get("1.0", tk.END),
                                                                             ))).grid(
            row=16,
            column=1,
            sticky=tk.W,
            padx=10,
            pady=5)

    def receive_order_and_reload_orders_page(self,
                                             order_to_receive,
                                             receive_product_popup,
                                             values,
                                             partial=None):
        received_date_check = True
        self.popup_error_message = tk.Label()
        if len(values[0]) == 0 and len(values[1]) == 0 and len(values[2]) == 0:
            # blank date = received today
            received_date = datetime.date.today()
        else:
            # date not blank, need to check
            received_date_check = self.error_handling.checkYearMonthDayFormat(values[0], values[1], values[2])
            if received_date_check:
                # receive date check passed
                received_date = datetime.date(int(values[0]), int(values[1]), int(values[2]))
            else:
                # receive date fail label
                self.popup_error_message.destroy()
                self.popup_error_message = tk.Label(receive_product_popup,
                                                    text=
                                                    "Error (blank received amt, invalid received amt, invalid date)",
                                                    font=self.formatting.medium_step_font,
                                                    bg=self.formatting.colour_code_1,
                                                    fg=self.formatting.colour_code_3).grid(
                    row=17, column=0, columnspan=4, sticky=tk.W, pady=5, padx=10)
        expiry_date_check = True
        if len(values[3]) == 0 and len(values[4]) == 0 and len(values[5]) == 0:
            try:
                expiry_date = datetime.date(int(values[0]), int(values[1]), int(values[2]))
            except ValueError:
                expiry_date = datetime.date.today()
        else:
            expiry_date_check = self.error_handling.checkYearMonthDayFormat(values[3],
                                                                            values[4],
                                                                            values[5],
                                                                            expiry=True)
            if expiry_date_check:
                expiry_date = datetime.date(int(values[3]), int(values[4]), int(values[5]))
            else:
                # expiry date fail label.
                self.popup_error_message.destroy()
                self.popup_error_message = tk.Label(receive_product_popup,
                                                    text=
                                                    "Error (blank received amt, invalid received amt, invalid date)",
                                                    font=self.formatting.medium_step_font,
                                                    bg=self.formatting.colour_code_1,
                                                    fg=self.formatting.colour_code_3).grid(
                    row=17, column=0, columnspan=4, sticky=tk.W, pady=5, padx=10)
        invalid_receive_amount_check = True
        invalid_receive_amount_check = self.error_handling.checkBlankEntry(values[6])
        if invalid_receive_amount_check:
            try:
                int(values[6])
            except ValueError:
                invalid_receive_amount_check = False
                self.popup_error_message.destroy()
                self.popup_error_message = tk.Label(receive_product_popup,
                                                    text=
                                                    "Error (blank received amt, invalid received amt, invalid date)",
                                                    font=self.formatting.medium_step_font,
                                                    bg=self.formatting.colour_code_1,
                                                    fg=self.formatting.colour_code_3).grid(
                    row=17, column=0, columnspan=4, sticky=tk.W, pady=5, padx=10)
        else:
            # blank received fail label
            self.popup_error_message.destroy()
            self.popup_error_message = tk.Label(receive_product_popup,
                                                text="Error (blank received amt, invalid received amt, invalid date)",
                                                font=self.formatting.medium_step_font,
                                                bg=self.formatting.colour_code_1,
                                                fg=self.formatting.colour_code_3).grid(
                     row=17, column=0, columnspan=4, sticky=tk.W, pady=5, padx=10)
        if received_date_check and expiry_date_check and invalid_receive_amount_check:
            # new received entry
            self.add_delete_db.new_received_record(
                (order_to_receive,
                 received_date,
                 values[6],
                 values[7],
                 expiry_date,
                 "",
                 values[9],
                 values[8],
                 values[10])
            )
            if not partial:
                # archive order
                self.edit_db.archive_entry_in_table_by_id("orders", order_to_receive)
            receive_product_popup.destroy()
            self.parent.display_orders_view(self.active_user,
                                            sort_by=self.sort_by,
                                            search_by=self.search_by_active_term,
                                            search_by_variable=self.search_by_variable)

    def archive_order_and_reload_orders_page(self,
                                             order_to_receive,
                                             receive_product_popup):
        self.edit_db.archive_entry_in_table_by_id("orders", order_to_receive)
        receive_product_popup.destroy()
        self.parent.display_orders_view(self.active_user,
                                        sort_by=self.sort_by,
                                        search_by=self.search_by_active_term,
                                        search_by_variable=self.search_by_variable)

    def cancel_order_if_not_partially_received_and_reload_page(self,
                                                               order_to_remove,
                                                               cancel_order_popup):
        potential_partial_order_list = self.select_db.select_all_from_table_where_one_field_like("received",
                                                                                                 "orders_id",
                                                                                                 order_to_remove)
        partial_order_list = [item for item in potential_partial_order_list]
        if len(partial_order_list) > 0:
            tk.Label(cancel_order_popup,
                     text="This order has been partially received and therefore can only be archived.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=3, column=0, columnspan=3, sticky=tk.W, pady=5, padx=10)

        else:
            self.add_delete_db.delete_entries_from_table_by_field_condition("orders",
                                                                            "id",
                                                                            order_to_remove)
            cancel_order_popup.destroy()
            self.parent.display_orders_view(self.active_user,
                                            sort_by=self.sort_by,
                                            search_by=self.search_by_active_term,
                                            search_by_variable=self.search_by_variable)

