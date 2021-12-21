import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
import datetime


class ArchivesView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.config(bg=self.formatting.colour_code_1)
        self.archives = ()
        self.archives_canvas_length = 0
        self.archives_scrollable_container = tk.Frame(self)
        self.archives_frame = tk.Frame(self)
        self.archives_frame.config(bg=self.formatting.colour_code_1)
        self.archives_navigation_frame = tk.Frame(self)
        self.archives_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.current_table = ""
        self.archives_table_select = ["Categories",
                                      "Sub-Categories",
                                      "Vendors",
                                      "Products",
                                      "Prices",
                                      "Users",
                                      "Orders",
                                      "Receiving",
                                      "Inventory"]
        self.archives_sort_value = tk.StringVar(self)
        self.archives_sort_value.set("Categories")
        self.archives_table_select_conversion_dictionary = {"Categories": "categories",
                                                            "Sub-Categories": "sub_categories",
                                                            "Vendors": "vendors",
                                                            "Products": "products",
                                                            "Prices": "priceTracking",
                                                            "Users": "users",
                                                            "Orders": "orders",
                                                            "Receiving": "received",
                                                            "Inventory": "inventory"}

    def archives_view(self, user, sort_by=False):
        self.active_user = user
        self.create_archives_view(sort_by)

    def create_archives_view(self, sort_by=False):
        self.get_archives_from_table(sort_by)
        self.create_approvals_navigation_frame()
        self.make_scrollable_archives_header_labels()
        self.populate_scrollable_archives_list()
        self.create_scrollable_approvals_view()
        self.archives_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.archives_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def create_approvals_navigation_frame(self):
        tk.Label(self.archives_navigation_frame,
                 text="Select Archived Records",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.archives_navigation_frame,
                                          self.archives_sort_value,
                                          *self.archives_table_select)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        sort_by_button = tk.Button(self.archives_navigation_frame,
                                   text="Select",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_archives_view(
                                       self.active_user,
                                       self.archives_sort_value.get())).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=5
        )

    def get_archives_from_table(self, sort_by=None):
        if sort_by:
            sort_by_variable = self.archives_table_select_conversion_dictionary[sort_by]
            print(sort_by_variable)
            self.current_table = sort_by_variable
            self.archives_sort_value.set(sort_by)
            if self.current_table == "sub_categories":
                self.archives = self.select_db.left_join_multiple_tables(
                    "sc.id, c.category_name, sc.sub_category_name",
                    [["sub_categories sc", "", "sc.categories_id"],
                     ["categories c", "c.id", ""]],
                    "sc.sub_category_name",
                    only_archive="sc.archived"
                )
            elif self.current_table == "products":
                self.archives = self.select_db.left_join_multiple_tables(
                    "p.id, p.name, p.product_code, v.vendor_name, c.category_name, sc.sub_category_name, p.comments,"
                    " p.categories_id, p.sub_categories_id, p.unit_of_issue, p.approved",
                    [["products p", "", "p.categories_id"],
                     ["categories c", "c.id", "p.vendors_id"],
                     ["vendors v", "v.id", "p.sub_categories_id"],
                     ["sub_categories sc", "sc.id", '']],
                    "p.name",
                    only_archive="p.archived")
            elif self.current_table == "priceTracking":
                self.archives = self.select_db.left_join_multiple_tables(
                    "pt.id, p.name, pt.cost, pt.cost_date",
                    [["priceTracking pt", "", "pt.products_id"],
                     ["products p", "p.id", ""]],
                    "p.name",
                    only_archive="pt.archived")
            elif self.current_table == "orders":
                self.archives = self.select_db.\
                    left_join_multiple_tables("o.id, p.name, p.product_code, v.vendor_name, c.category_name," +
                                              "p.unit_of_issue, pt.cost, u.user_name, r.amount, o.units_ordered, " +
                                              "o.order_date",
                                              [["orders o", "", "o.requests_id"],
                                               ["requests r", "r.id", "r.users_id"],
                                               ["users u", "u.id", "r.products_id"],
                                               ["products p", "p.id", "p.vendors_id"],
                                               ["vendors v", "v.id", "p.categories_id"],
                                               ["categories c", "c.id", "r.price_id"],
                                               ["priceTracking pt", "pt.id", ""]],
                                              "o.order_date",
                                              only_archive="o.archived")
            elif self.current_table == "users":
                self.archives = self.select_db.left_join_multiple_tables(
                    "u.id, u.user_name, cr.credential_level",
                    [["users u", "", "u.credentials_id"],
                     ["credentials cr", "cr.id", ""]],
                    "u.user_name",
                    only_archive="u.archived")
            elif self.current_table == "received":
                self.archives = self.select_db. \
                    left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, p.unit_of_issue," +
                                              " pt.cost, u.user_name, o.units_ordered, rc.received_amount," +
                                              " rc.received_date, rc.lot_number, rc.expiry_date, rc.model," +
                                              " rc.equipment_SN, rc.comments, rc.id",
                                              [["received rc", "", "rc.orders_id"],
                                               ["orders o", "o.id", "o.requests_id"],
                                               ["requests r", "r.id", "r.users_id"],
                                               ["users u", "u.id", "r.products_id"],
                                               ["products p", "p.id", "p.vendors_id"],
                                               ["vendors v", "v.id", "p.categories_id"],
                                               ["categories c", "c.id", "r.price_id"],
                                               ["priceTracking pt", "pt.id", ""]],
                                              "p.name",
                                              only_archive="rc.archived")

            elif self.current_table == "inventory":
                self.archives = self.select_db. \
                    left_join_multiple_tables("p.name, p.product_code, c.category_name, v.vendor_name, p.unit_of_issue," +
                                              " rc.received_date, i.full_units_remaining, i.partial_units_remaining, " +
                                              " loc.locations_name, subloc.sub_locations_name, i.last_updated, " +
                                              " u.user_name, rc.expiry_date, rc.model, rc.equipment_SN, rc.lot_number, " +
                                              " o.order_date, i.comments, i.id",
                                              [["inventory i", "", "i.received_id"],
                                               ["received rc", "rc.id", "rc.orders_id"],
                                               ["orders o", "o.id", "o.requests_id"],
                                               ["requests r", "r.id", "i.updated_user_id"],
                                               ["users u", "u.id", "r.products_id"],
                                               ["products p", "p.id", "p.vendors_id"],
                                               ["vendors v", "v.id", "p.categories_id"],
                                               ["categories c", "c.id", "r.price_id"],
                                               ["priceTracking pt", "pt.id", "i.location_id"],
                                               ["inventoryLocations loc", "loc.id", "i.sub_location_id"],
                                               ["inventorySubLocations subloc", "subloc.id", ""]],
                                              "p.name",
                                              only_archive="i.archived")
            else:
                self.archives = self.select_db.\
                    select_all_from_table_where_one_field_equals(sort_by_variable, "archived", "1")
        else:
            self.current_table = "categories"
            self.archives = self.select_db.\
                select_all_from_table_where_one_field_equals(self.current_table, "archived", "1")

    def create_scrollable_approvals_view(self):
        orders_canvas = tk.Canvas(self.archives_scrollable_container,
                                  width=1650,
                                  height=500,
                                  scrollregion=(0, 0, 0, self.archives_canvas_length),
                                  bd=0,
                                  highlightthickness=0)
        orders_canvas.config(bg=self.formatting.colour_code_1)
        orders_canvas_scrollbar = tk.Scrollbar(self.archives_scrollable_container,
                                               orient="vertical",
                                               command=orders_canvas.yview)
        orders_canvas.configure(yscrollcommand=orders_canvas_scrollbar.set)
        orders_canvas_scrollbar.pack(side='left',
                                     fill='y')
        orders_canvas.pack(side="right",
                           fill='y')
        orders_canvas.create_window((0, 0),
                                    window=self.archives_frame,
                                    anchor="nw")

    def make_scrollable_archives_header_labels(self):
        if self.current_table == "categories":
            tk.Label(self.archives_frame,
                     text="Category Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "sub_categories":
            tk.Label(self.archives_frame,
                     text="Category Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Sub-Category Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "vendors":
            tk.Label(self.archives_frame,
                     text="Vendor Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "products":
            tk.Label(self.archives_frame,
                     text="Product Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Catalog Number",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Vendor",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Category",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Sub-Category",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "priceTracking":
            tk.Label(self.archives_frame,
                     text="Product Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Price ($)",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Date of Price",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "orders":
            tk.Label(self.archives_frame,
                     text="Product Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Catalog Number",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Vendor",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Category",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Unit of Issue",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Cost per Unit",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=5, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Requested By",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="# Req.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="# Ord.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=8, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Order Date",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=9, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "users":
            tk.Label(self.archives_frame,
                     text="User Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Credentials",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "received":
            tk.Label(self.archives_frame,
                     text="Product Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Product ID",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Vendor",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Category",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Received Date",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Unit of Issue",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=5, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Dollar/Unit",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Staff",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="# Ordered",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=8, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="# Received",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=9, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "inventory":
            tk.Label(self.archives_frame,
                     text="Product Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Product ID",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Category",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Vendor",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Unit of Issue",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=5, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Receive Date",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Amount Remaining",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Location",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=8, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.archives_frame,
                     text="Last Updated",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=9, sticky=tk.W, padx=10, pady=5)
        else:
            tk.Label(self.archives_frame,
                     text="Archived " + self.archives_sort_value.get() +
                          " (Integer fields hidden for readability)",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_archives_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.archives:
            print(item)
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            approve_column_location_from_row_create =\
                self.populate_scrollable_list_by_table(row_counter, text_color, item)
            tk.Button(self.archives_frame,
                      text="Restore",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.restore_record_and_reload_archives(item)).grid(
                row=row_counter,
                column=approve_column_location_from_row_create,
                sticky=tk.W,
                padx=10,
                pady=5)
            self.archives_canvas_length += 50
            row_counter += 1
            even_odd += 1

    def populate_scrollable_list_by_table(self, row_counter, text_color, record):
        approve_button_column = 0
        if self.current_table in ["categories", "vendors"]:
            tk.Label(self.archives_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table in ["sub_categories", "users"]:
            tk.Label(self.archives_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "products":
            tk.Label(self.archives_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            if record[5] == "None":
                tk.Label(self.archives_frame,
                         text="",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=text_color,
                         wraplength=0).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            else:
                tk.Label(self.archives_frame,
                         text=record[5],
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=text_color,
                         wraplength=0).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "priceTracking":
            tk.Label(self.archives_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text="{:.2f}".format(float(record[2])),
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "orders":
            tk.Label(self.archives_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[5],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text="{:.2f}".format(float(record[6])),
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=5, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[7],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[8],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[9],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=8, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[10],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=9, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "received":
            tk.Label(self.archives_frame,
                     text=record[0],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[9],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=5, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[5],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[6],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[7],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=8, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[8],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=9, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "inventory":
            tk.Label(self.archives_frame,
                     text="INV-" + str(record[18]),
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_purple).grid(
                row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[0],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=5, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[5],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=str(record[6]) + " F / " + str(record[7]) + " P",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[8],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=8, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.archives_frame,
                     text=record[10],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=9, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        else:
            tk.Label(self.archives_frame,
                     text=record,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        return approve_button_column

    def restore_record_and_reload_archives(self, record_to_restore):
        if self.current_table == "inventory":
            self.edit_db.edit_one_record_one_field_one_table(self.current_table, "archived", "0", record_to_restore[18])
        else:
            self.edit_db.edit_one_record_one_field_one_table(self.current_table, "archived", "0", record_to_restore[0])
        self.parent.display_archives_view(self.active_user)
