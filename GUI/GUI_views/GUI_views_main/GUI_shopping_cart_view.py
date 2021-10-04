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
        self.shopping_cart_scrollable_container = tk.Frame(self)
        self.products_list_frame = tk.Frame(self)
        self.products_list_frame.config(bg=self.formatting.colour_code_1)
        self.shopping_cart_frame = tk.Frame(self)
        self.shopping_cart_frame.config(bg=self.formatting.colour_code_1)

    # MAIN METHODS

    def shopping_cart_view(self, user):
        self.active_user = user
        self.create_products_list()
        self.create_shopping_cart()

    def create_products_list(self):
        tk.Label(self,
                 text="Products List",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, sticky=tk.W, padx=10, pady=5)
        self.get_products_list_from_database()
        self.make_scrollable_products_list_header_labels()
        self.populate_scrollable_products_list()
        self.create_scrollable_products_list()
        self.products_list_scrollable_container.grid(sticky=tk.W, padx=10, pady=5)

    def create_shopping_cart(self):
        tk.Label(self,
                 text="Shopping Cart for " + self.active_user[2],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(sticky=tk.W, padx=10, pady=5)
        self.get_active_user_shopping_cart_from_database()
        self.make_scrollable_shopping_cart_header_labels()
        self.populate_scrollable_shopping_cart()
        self.create_scrollable_shopping_cart()
        self.shopping_cart_scrollable_container.grid(sticky=tk.W, padx=10, pady=5)

    # PRODUCTS LIST METHODS

    def get_products_list_from_database(self):
        self.products_list = self.select_db.left_join_multiple_tables(
            "p.name, p.product_code, v.vendor_name, c.category_name, p.id ",
            [["products p", "", "p.categories_id"],
             ["categories c", "c.id", "p.vendors_id"],
             ["vendors v", "v.id", ""]],
            "p.name")

    def create_scrollable_products_list(self):
        products_list_canvas = tk.Canvas(self.products_list_scrollable_container,
                                         width=1200,
                                         height=275,
                                         scrollregion=(0, 0, 0, 1000),
                                         bd=0,
                                         highlightthickness=0)
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

    def populate_scrollable_products_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.products_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            product_name_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                             item[0],
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
            tk.Button(self.products_list_frame,
                      text="Add to Cart",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.add_product_to_cart(item)).grid(row=row_counter,
                                                                                     column=5,
                                                                                     sticky=tk.W,
                                                                                     padx=10,
                                                                                     pady=5)
            row_counter += 1
            even_odd += 1

# SHOPPING CART METHODS

    def get_active_user_shopping_cart_from_database(self):
        self.shopping_cart = self.select_db.\
            left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date,+"
                                      " r.amount, u.user_name, r.id, r.unit_of_issue, r.dollar_per_unit",
                                      [["requests r", "", "r.products_id"],
                                       ["products p", "p.id", "r.users_id"],
                                       ["users u", "u.id", "p.vendors_id"],
                                       ["vendors v", "v.id", "p.categories_id"],
                                       ["categories c", "c.id", ""]],
                                      "u.user_name")
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
            tk.Label(self.shopping_cart_frame,
                     text=item[0],
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
                     text=str(item[5]) + " (" + str(float(item[9])*float(item[5])) + ")",
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

    def create_scrollable_shopping_cart(self):
        shopping_cart_canvas = tk.Canvas(self.shopping_cart_scrollable_container,
                                         width=1450,
                                         height=275,
                                         scrollregion=(0, 0, 0, 1000),
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

    # SHARED METHODS

    def add_product_to_cart(self, product_to_add):
        add_product_amount_popup = tk.Toplevel()
        add_product_amount_popup.config(bg=self.formatting.colour_code_1)
        add_product_amount_popup.geometry('400x250')
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
        tk.Label(add_product_amount_popup,
                 text="Unit of Issue: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        unit_of_issue = tk.Entry(add_product_amount_popup)
        unit_of_issue.config(bg=self.formatting.colour_code_2,
                             fg=self.formatting.colour_code_1,
                             font=self.formatting.medium_step_font)
        unit_of_issue.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Label(add_product_amount_popup,
                 text="Cost per Unit: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        cost_per_unit = tk.Entry(add_product_amount_popup)
        cost_per_unit.config(bg=self.formatting.colour_code_2,
                             fg=self.formatting.colour_code_1,
                             font=self.formatting.medium_step_font)
        cost_per_unit.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(add_product_amount_popup,
                  text="Add Request",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.add_product_to_cart_query(product_to_add,
                                                                 amount_of_product.get(),
                                                                 unit_of_issue.get(),
                                                                 cost_per_unit.get(),
                                                                 add_product_amount_popup)).grid(
            row=3, column=0, sticky=tk.W, padx=10, pady=5
        )

    def add_product_to_cart_query(self, product_to_add, amount_of_product, unit_of_issue, cost_per_unit, top_level):
        self.add_delete_db.new_requests_record((product_to_add[4],
                                                self.active_user[0],
                                                datetime.date.today(),
                                                unit_of_issue,
                                                cost_per_unit,
                                                amount_of_product,
                                                ""))
        self.parent.display_shopping_cart_view(self.active_user)
        top_level.destroy()

    def remove_product_from_cart(self, request_to_remove):
        self.add_delete_db.delete_entries_from_table_by_field_condition("requests",
                                                                        "id",
                                                                        request_to_remove)
        self.parent.display_shopping_cart_view(self.active_user)