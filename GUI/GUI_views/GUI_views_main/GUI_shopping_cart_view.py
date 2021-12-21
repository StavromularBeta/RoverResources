import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from GUI.GUI_formatting import GUI_formatting as tk_formatting
import datetime


class ShoppingCartView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.products_list = ""
        self.shopping_cart = ""
        self.config(bg=self.formatting.colour_code_1)
        self.products_list_scrollable_container = tk.Frame(self)
        self.products_list_scrollable_container.config(bg=self.formatting.colour_code_1, bd=0)
        self.shopping_cart_scrollable_container = tk.Frame(self)
        self.shopping_cart_scrollable_container.config(bg=self.formatting.colour_code_1, bd=0)
        self.products_list_frame = tk.Frame(self)
        self.products_list_frame.config(bg=self.formatting.colour_code_1)
        self.products_list_navigation_frame = tk.Frame(self)
        self.products_list_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.shopping_cart_frame = tk.Frame(self)
        self.shopping_cart_frame.config(bg=self.formatting.colour_code_1)
        self.shopping_cart_navigation_frame = tk.Frame(self)
        self.shopping_cart_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.shopping_cart_canvas_length = 0
        self.shopping_cart_total_cost = 0.0
        self.product_list_canvas_length = 0
        self.product_list_view_by = ["Product Name",
                                     "Product Code",
                                     "Vendor Name",
                                     "Product Category",
                                     "Product Sub-Category",
                                     "Units"]
        self.product_list_sort_value = tk.StringVar(self)
        self.product_list_sort_value.set("Product Name")
        self.product_list_search_by = ["Product Name",
                                       "Product Code",
                                       "Vendor Name",
                                       "Product Category",
                                       "Product Sub-Category",
                                       "Units"]
        self.product_list_search_value = tk.StringVar(self)
        self.product_list_search_value.set("Product Name")
        self.sort_by_shopping_cart_conversion_dictionary = {"Product Code": "p.product_code",
                                                            "Vendor Name": "v.vendor_name",
                                                            "Product Category": "c.category_name",
                                                            "Product Sub-Category": "sc.sub_category_name",
                                                            "Product Name": "p.name",
                                                            "Units": "p.unit_of_issue"}
        self.search_by_active_term = ""

    # MAIN METHODS

    def shopping_cart_view(self,
                           user,
                           product_sort_by=False,
                           product_search_by=False,
                           product_search_by_variable=False):
        self.search_by_active_term = product_search_by
        self.active_user = user
        self.create_products_list(product_sort_by, product_search_by, product_search_by_variable)
        self.create_shopping_cart()

    def create_products_list(self, product_sort_by=False, product_search_by=False, product_search_by_variable=False):
        self.create_products_list_navigation_frame()
        self.get_products_list_from_database(product_sort_by, product_search_by, product_search_by_variable)
        self.make_scrollable_products_list_header_labels()
        self.populate_scrollable_products_list()
        self.create_scrollable_products_list()
        self.products_list_navigation_frame.grid(row=0, column=0, sticky=tk.W, pady=10)
        self.products_list_scrollable_container.grid(row=1, column=0, sticky=tk.W)

    def create_shopping_cart(self):
        self.get_active_user_shopping_cart_from_database()
        self.make_scrollable_shopping_cart_header_labels()
        self.populate_scrollable_shopping_cart()
        self.create_scrollable_shopping_cart()
        self.create_shopping_cart_navigation_frame()
        self.shopping_cart_navigation_frame.grid(row=2, column=0, sticky=tk.W, pady=10)
        self.shopping_cart_scrollable_container.grid(row=3, column=0, sticky=tk.W)

    # PRODUCTS LIST METHODS

    def create_products_list_navigation_frame(self):
        product_search_entry = tk.Entry(self.products_list_navigation_frame)
        if self.search_by_active_term:
            product_search_entry.insert(0, self.search_by_active_term)
        tk.Label(self.products_list_navigation_frame,
                 text="Products List",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.products_list_navigation_frame,
                                          self.product_list_sort_value,
                                          *self.product_list_view_by)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        tk.Label(self.products_list_navigation_frame,
                 text="Sort:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=1, sticky=tk.W, pady=5)
        type_of_sort_menu.grid(row=0, column=2, sticky=tk.W, pady=5)
        sort_by_button = tk.Button(self.products_list_navigation_frame,
                                   text="Sort",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_shopping_cart_view(
                                       self.active_user,
                                       product_sort_by=self.product_list_sort_value.get(),
                                       product_search_by=product_search_entry.get(),
                                       product_search_by_variable=self.product_list_search_value.get())).grid(
            row=0, column=3, sticky=tk.W, padx=10, pady=5
        )
        type_of_search_menu = tk.OptionMenu(self.products_list_navigation_frame,
                                            self.product_list_search_value,
                                            *self.product_list_search_by)
        type_of_search_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_search_menu.config(font=self.formatting.medium_step_font)
        tk.Label(self.products_list_navigation_frame,
                 text="Search:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=4, sticky=tk.W, pady=5)
        product_search_entry.grid(row=0, column=5, sticky=tk.W, pady=5)
        type_of_search_menu.grid(row=0, column=6, sticky=tk.W, pady=5)
        search_by_button = tk.Button(self.products_list_navigation_frame,
                                     text="Search",
                                     font=self.formatting.medium_step_font,
                                     command=lambda: self.parent.display_shopping_cart_view(
                                       self.active_user,
                                       product_search_by=product_search_entry.get(),
                                       product_search_by_variable=self.product_list_search_value.get())).grid(
            row=0, column=7, sticky=tk.W, padx=10, pady=5
        )
        tk.Button(self.products_list_navigation_frame,
                  text="Clear All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_shopping_cart_view(
                      self.active_user)).grid(
            row=0, column=8, sticky=tk.W, padx=10, pady=5
        )

    def get_products_list_from_database(self,
                                        product_sort_by=None,
                                        product_search_by=None,
                                        product_search_by_variable=None):
        if product_sort_by and product_search_by:
            sort_by_variable = self.sort_by_shopping_cart_conversion_dictionary[product_sort_by]
            search_by_field = self.sort_by_shopping_cart_conversion_dictionary[product_search_by_variable]
            self.search_by_active_term = product_search_by
            self.product_list_sort_value.set(product_sort_by)
            self.product_list_search_value.set(product_search_by_variable)
            self.products_list = self.select_db.left_join_multiple_tables(
                "p.name, p.product_code, v.vendor_name, c.category_name, p.id, sc.sub_category_name, p.unit_of_issue",
                [["products p", "", "p.categories_id"],
                 ["categories c", "c.id", "p.vendors_id"],
                 ["vendors v", "v.id", "p.sub_categories_id"],
                 ["sub_categories sc", "sc.id", '']],
                sort_by_variable,
                search_by=[search_by_field, '%' + product_search_by + '%'],
                no_archive="p.archived")
        elif product_sort_by:
            pass
        elif product_search_by:
            self.search_by_active_term = product_search_by
            search_by_field = self.sort_by_shopping_cart_conversion_dictionary[product_search_by_variable]
            self.product_list_search_value.set(product_search_by_variable)
            self.products_list = self.select_db.left_join_multiple_tables(
                "p.name, p.product_code, v.vendor_name, c.category_name, p.id, sc.sub_category_name, p.unit_of_issue",
                [["products p", "", "p.categories_id"],
                 ["categories c", "c.id", "p.vendors_id"],
                 ["vendors v", "v.id", "p.sub_categories_id"],
                 ["sub_categories sc", "sc.id", '']],
                "p.name",
                no_archive="p.archived",
                search_by=[search_by_field, '%' + product_search_by + '%'])
        else:
            pass

    def create_scrollable_products_list(self):
        products_list_canvas = tk.Canvas(self.products_list_scrollable_container,
                                         width=1200,
                                         height=275,
                                         scrollregion=(0, 0, 0, self.product_list_canvas_length),
                                         bd=0,
                                         highlightthickness=0,
                                         confine=True)
        products_list_canvas.config(bg=self.formatting.colour_code_1)
        products_list_canvas_scrollbar = tk.Scrollbar(self.products_list_scrollable_container,
                                                      orient="vertical",
                                                      command=products_list_canvas.yview)
        products_list_canvas.configure(yscrollcommand=products_list_canvas_scrollbar.set)
        products_list_canvas_scrollbar.pack(side='left',
                                            fill='y')
        products_list_canvas.pack(side="right",
                                  fill='y')
        products_list_canvas.create_window((0, 0),
                                           window=self.products_list_frame,
                                           anchor="nw")

    def make_scrollable_products_list_header_labels(self):
        product_name_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                          "Product Name",
                                                                          self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_name_header, 0, 1)
        product_id_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                        "Product ID",
                                                                        self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_id_header, 0, 2)
        product_vendor_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                            "Vendor",
                                                                            self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_vendor_header, 0, 3)
        product_category_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                              "Category",
                                                                              self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_category_header, 0, 4)
        product_category_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                              "Sub Category",
                                                                              self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_category_header, 0, 5)
        product_category_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                              "Units",
                                                                              self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_category_header, 0, 6)

    def populate_scrollable_products_list(self):
        row_counter = 1
        even_odd = 1
        try:
            if len(self.products_list) == 0:
                tk.Label(self.products_list_frame,
                         text="Search for a product to get started.",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_3).grid(
                    row=1, column=1, columnspan=5, sticky=tk.W, pady=5, padx=10)
        except TypeError:
            pass
        for item in self.products_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            if len(item[0]) > 20:
                product_name = item[0][0:20] + "..."
            else:
                product_name = item[0]
            product_name_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                             product_name,
                                                                             text_color)
            self.formatting.grid_shopping_cart_labels(product_name_label, row_counter, 1)
            product_id_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                           item[1],
                                                                           text_color)
            self.formatting.grid_shopping_cart_labels(product_id_label, row_counter, 2)
            product_vendor_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                               item[2],
                                                                               text_color)
            self.formatting.grid_shopping_cart_labels(product_vendor_label, row_counter, 3)
            product_category_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                 item[3],
                                                                                 text_color)
            self.formatting.grid_shopping_cart_labels(product_category_label, row_counter, 4)
            if item[5] == "None":
                product_sub_category_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                         "",
                                                                                         text_color)
            else:
                product_sub_category_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                         item[5],
                                                                                         text_color)
            self.formatting.grid_shopping_cart_labels(product_sub_category_label, row_counter, 5)
            product_units_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                              item[6],
                                                                              text_color)
            self.formatting.grid_shopping_cart_labels(product_units_label, row_counter, 6)
            tk.Button(self.products_list_frame,
                      text="Add to Cart",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.add_product_to_cart(item)).grid(row=row_counter,
                                                                                     column=7,
                                                                                     sticky=tk.W,
                                                                                     padx=10,
                                                                                     pady=5)
            row_counter += 1
            even_odd += 1
            self.product_list_canvas_length += 50

# SHOPPING CART METHODS

    def create_shopping_cart_navigation_frame(self):
        tk.Label(self.shopping_cart_navigation_frame,
                 text=self.active_user[2] + "'s Shopping Cart",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Label(self.shopping_cart_navigation_frame,
                 text="Total Cost: $" + "{:.2f}".format(self.shopping_cart_total_cost),
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)

    def get_active_user_shopping_cart_from_database(self):
        self.shopping_cart = self.select_db.\
            left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date,+"
                                      " r.amount, u.user_name, r.id, p.unit_of_issue, pt.cost",
                                      [["requests r", "", "r.products_id"],
                                       ["products p", "p.id", "r.users_id"],
                                       ["users u", "u.id", "p.vendors_id"],
                                       ["vendors v", "v.id", "p.categories_id"],
                                       ["categories c", "c.id", "r.price_id"],
                                       ["priceTracking pt", "pt.id", ""]],
                                      "u.user_name",
                                      no_archive="r.archived")
        active_user_shopping_cart = []
        for item in self.shopping_cart:
            if item[6] == self.active_user[2]:
                active_user_shopping_cart.append(item)
        self.shopping_cart = active_user_shopping_cart

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
                 text="Unit Of Issue",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Dollar/Unit",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Amount Req.",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=8, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_shopping_cart(self):
        row_counter = 1
        even_odd = 1
        for item in self.shopping_cart:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            if len(item[0]) > 20:
                product_name = item[0][0:20] + "..."
            else:
                product_name = item[0]
            tk.Label(self.shopping_cart_frame,
                     text=product_name,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
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
                     text=item[8],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[9],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=str(item[5]) + " (" + "{:.2f}".format(float(item[9])*float(item[5])) + ")",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=8, sticky=tk.W, padx=10, pady=5)
            tk.Button(self.shopping_cart_frame,
                      text="Remove Request",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.remove_product_from_cart(item[7])).grid(row=row_counter,
                                                                                             column=9,
                                                                                             sticky=tk.W,
                                                                                             padx=10,
                                                                                             pady=5)
            row_counter += 1
            even_odd += 1
            self.shopping_cart_total_cost += float(item[9])*float(item[5])
            self.shopping_cart_canvas_length += 50

    def create_scrollable_shopping_cart(self):
        shopping_cart_canvas = tk.Canvas(self.shopping_cart_scrollable_container,
                                         width=1450,
                                         height=275,
                                         scrollregion=(0, 0, 0, self.shopping_cart_canvas_length),
                                         bd=1,
                                         highlightthickness=0,
                                         confine=True)
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

    # SHARED METHODS

    def add_product_to_cart(self, product_to_add):
        add_product_amount_popup = tk.Toplevel()
        add_product_amount_popup.config(bg=self.formatting.colour_code_1)
        add_product_amount_popup.geometry('500x200')
        tk.Label(add_product_amount_popup,
                 text="Amount to Request: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        amount_of_product = tk.Entry(add_product_amount_popup)
        amount_of_product.config(bg=self.formatting.colour_code_2,
                                 fg=self.formatting.colour_code_1,
                                 font=self.formatting.medium_step_font)
        amount_of_product.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(add_product_amount_popup,
                  text="Add Request",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.add_product_to_cart_query(product_to_add,
                                                                 amount_of_product.get(),
                                                                 add_product_amount_popup)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=5
        )

    def add_product_to_cart_query(self, product_to_add, amount_of_product, top_level):
        current_product_price = self.select_db.select_one_from_table_where_field_equals_order_by("priceTracking",
                                                                                                 "products_id",
                                                                                                 product_to_add[4],
                                                                                                 "cost_date",
                                                                                                 descending_order=True)
        try:
            current_product_price = [item for item in current_product_price][0][0]
            active_request_for_product_check = self.select_db.select_all_from_table_where_one_field_equals(
                "requests",
                "products_id",
                product_to_add[4],
                no_archive=True
            )
            total_active_requested_units = 0
            for item in active_request_for_product_check:
                total_active_requested_units += float(item[5])
            if total_active_requested_units > 0:
                tk.Label(top_level,
                         text=str(total_active_requested_units) +
                         " Units of this product are currently requested. Continue?",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_3).grid(
                    row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
                tk.Button(top_level,
                          text="Confirm Request",
                          font=self.formatting.medium_step_font,
                          command=lambda: self.confirmed_request_entry((product_to_add[4],
                                                                        self.active_user[0],
                                                                        current_product_price,
                                                                        datetime.date.today(),
                                                                        amount_of_product,
                                                                        ""),
                                                                       top_level)).grid(
                    row=3, column=0, sticky=tk.W, padx=10, pady=5)
            else:
                self.add_delete_db.new_requests_record((product_to_add[4],
                                                        self.active_user[0],
                                                        current_product_price,
                                                        datetime.date.today(),
                                                        amount_of_product,
                                                        ""))
                self.parent.display_shopping_cart_view(self.active_user)
                top_level.destroy()
        except IndexError:
            tk.Label(top_level,
                     text="No price set yet for product. See Admin.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5
            )

    def confirmed_request_entry(self, values, top_level_window):
        self.add_delete_db.new_requests_record(values)
        top_level_window.destroy()
        self.parent.display_shopping_cart_view(self.active_user)

    def remove_product_from_cart(self, request_to_remove):
        self.add_delete_db.delete_entries_from_table_by_field_condition("requests",
                                                                        "id",
                                                                        request_to_remove)
        self.parent.display_shopping_cart_view(self.active_user)
