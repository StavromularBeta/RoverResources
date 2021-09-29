import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from GUI.GUI_formatting import GUI_formatting as tk_formatting
import datetime


class ShoppingCartViewAdmin(tk.Frame):

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
        self.sort_shopping_cart_view_by = ["Staff Member",
                                           "Product Code",
                                           "Vendor Name",
                                           "Product Category",
                                           "Request Date",
                                           "Product Name"]
        self.shopping_cart_sort_value = tk.StringVar(self)
        self.shopping_cart_sort_value.set("Staff Member")
        self.sort_by_shopping_cart_conversion_dictionary = {"Staff Member": "u.user_name",
                                                            "Product Code": "p.product_code",
                                                            "Vendor Name": "v.vendor_name",
                                                            "Product Category": "c.category_name",
                                                            "Request Date": "r.request_date",
                                                            "Product Name": "p.name"}

    # MAIN METHOD

    def shopping_cart_view_admin(self, user, sort_by=False):
        self.active_user = user
        self.create_shopping_cart(sort_by)

    # SHOPPING CART METHODS

    def create_shopping_cart(self, sort_by=False):
        tk.Label(self,
                 text="All Shopping Carts (Admin: " + self.active_user[2] + ")",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(sticky=tk.W, padx=10, pady=5)
        type_of_sort_menu = tk.OptionMenu(self,
                                          self.shopping_cart_sort_value,
                                          *self.sort_shopping_cart_view_by)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_1)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(sticky=tk.W, padx=10, pady=5)
        sort_by_button = tk.Button(self,
                                   text="Sort Data",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_admin_shopping_cart_view(
                                       self.active_user,
                                       self.shopping_cart_sort_value.get())).grid(
            sticky=tk.W, padx=10, pady=5
        )
        self.get_active_user_shopping_cart_from_database(sort_by)
        self.make_scrollable_shopping_cart_header_labels()
        self.populate_scrollable_shopping_cart()
        self.create_scrollable_shopping_cart()
        self.shopping_cart_scrollable_container.grid(padx=10, pady=5)

    def get_active_user_shopping_cart_from_database(self, sort_by=None):
        if sort_by:
            sort_by_variable = self.sort_by_shopping_cart_conversion_dictionary[sort_by]
            self.shopping_cart_sort_value.set(sort_by)
            self.shopping_cart = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date," +
                                          " r.amount, u.user_name",
                                          [["requests r", "", "r.products_id"],
                                           ["products p", "p.id", "r.users_id"],
                                           ["users u", "u.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", ""]],
                                          sort_by_variable)
        else:
            self.shopping_cart = self.select_db.\
                left_join_multiple_tables("p.name, p.product_code, v.vendor_name, c.category_name, r.request_date," +
                                          " r.amount, u.user_name",
                                          [["requests r", "", "r.products_id"],
                                           ["products p", "p.id", "r.users_id"],
                                           ["users u", "u.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", ""]],
                                          "u.user_name")

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
                 text="Amount Requested",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.shopping_cart_frame,
                 text="Staff Member",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)

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
                     text=item[5],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.shopping_cart_frame,
                     text=item[6],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            row_counter += 1
            even_odd += 1

    def create_scrollable_shopping_cart(self):
        shopping_cart_canvas = tk.Canvas(self.shopping_cart_scrollable_container,
                                         width=1200,
                                         height=500,
                                         scrollregion=(0, 0, 0, 1500),
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
