import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
import datetime


class OrdersView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
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
        self.sort_orders_view_by = ["Staff Member",
                                    "Product Code",
                                    "Vendor Name",
                                    "Product Category",
                                    "Order Date",
                                    "Product Name",
                                    "Cost per Unit"]
        self.orders_sort_value = tk.StringVar(self)
        self.orders_sort_value.set("Staff Member")
        self.sort_by_orders_conversion_dictionary = {"Staff Member": "u.user_name",
                                                     "Product Code": "p.product_code",
                                                     "Vendor Name": "v.vendor_name",
                                                     "Product Category": "c.category_name",
                                                     "Order Date": "o.order_date",
                                                     "Product Name": "p.name",
                                                     "Cost per Unit": "pt.cost"}

    def orders_view(self, user, sort_by=False):
        self.active_user = user
        self.create_orders_view(sort_by)

    def create_orders_view(self, sort_by=False):
        self.get_active_orders_from_database(sort_by)
        self.make_scrollable_orders_header_labels()
        self.populate_scrollable_orders_list()
        self.create_scrollable_orders_view()
        self.create_orders_navigation_frame()
        self.orders_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.orders_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def create_orders_navigation_frame(self):
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
                 text="Sort Orders",
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
                                   text="Sort Orders",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_orders_view(
                                       self.active_user,
                                       self.orders_sort_value.get())).grid(
            row=0, column=4, sticky=tk.W, padx=10, pady=5
        )

    def get_active_orders_from_database(self, sort_by=None):
        if sort_by:
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
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            tk.Label(self.orders_frame,
                     text=item[0],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
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
            if self.active_user[1] == 1:
                tk.Button(self.orders_frame,
                          text="Receive Product",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.receive_product_popup(item[10])).grid(row=row_counter,
                                                                                           column=11,
                                                                                           sticky=tk.W,
                                                                                           padx=10,
                                                                                           pady=5)
            row_counter += 1
            even_odd += 1
            self.orders_canvas_length += 50

    def receive_product_popup(self, order_to_receive):
        receive_product_popup = tk.Toplevel()
        receive_product_popup.config(bg=self.formatting.colour_code_1)
        receive_product_popup.geometry('500x90')
        tk.Label(receive_product_popup,
                 text="At this stage of development, received orders will be archived.",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Button(receive_product_popup,
                  text="Receive Order",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.archive_order_and_reload_orders_page(order_to_receive,
                                                                            receive_product_popup)).grid(row=1,
                                                                                                         column=0,
                                                                                                         sticky=tk.W,
                                                                                                         padx=10,
                                                                                                         pady=5)

    def archive_order_and_reload_orders_page(self,
                                             order_to_receive,
                                             receive_product_popup):
        self.edit_db.archive_entry_in_table_by_id("orders", order_to_receive)
        receive_product_popup.destroy()
        self.parent.display_orders_view(self.active_user)


