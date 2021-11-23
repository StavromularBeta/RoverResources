import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_errorHandling as tk_errorHandling
import datetime


class CategoriesVendorsView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.error_handling = tk_errorHandling.ErrorHandling()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.vendors_list = ""
        self.categories_list = ""
        self.config(bg=self.formatting.colour_code_1)
        self.vendors_list_scrollable_container = tk.Frame(self)
        self.categories_list_scrollable_container = tk.Frame(self)
        self.vendors_navigation_frame = tk.Frame(self)
        self.categories_navigation_frame = tk.Frame(self)
        self.vendors_list_frame = tk.Frame(self)
        self.vendors_list_frame.config(bg=self.formatting.colour_code_1)
        self.categories_list_frame = tk.Frame(self)
        self.categories_list_frame.config(bg=self.formatting.colour_code_1)
        self.vendors_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.categories_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.categories_canvas_length = 0
        self.vendors_canvas_length = 0

    # MAIN METHODS

    def categories_and_vendors_view(self, user, vendor_search=False):
        self.active_user = user
        self.create_vendors_navigation_frame()
        self.create_categories_navigation_frame()
        self.create_vendors_list(vendor_search)
        self.create_categories_list()

    def create_vendors_navigation_frame(self):
        tk.Label(self.vendors_navigation_frame,
                 text="Vendors",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        if self.active_user[1] == 1:
            tk.Button(self.vendors_navigation_frame,
                      text="Add New Vendor",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_vendor_or_category_popup("vendors")).grid(row=0,
                                                                                             column=1,
                                                                                             sticky=tk.W,
                                                                                             padx=10,
                                                                                             pady=5)
        else:
            tk.Button(self.vendors_navigation_frame,
                      text="Request New Vendor",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_vendor_or_category_popup("vendors", True)).grid(row=0,
                                                                                                   column=1,
                                                                                                   sticky=tk.W,
                                                                                                   padx=10,
                                                                                                   pady=5)
        tk.Label(self.vendors_navigation_frame,
                 text="Search: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        vendor_search_entry = tk.Entry(self.vendors_navigation_frame)
        vendor_search_entry.grid(row=0, column=3, sticky=tk.W, pady=5)
        tk.Button(self.vendors_navigation_frame,
                  text="Search",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_categories_and_vendors_view(self.active_user,
                                                                                  vendor_search_entry.get())).grid(
            row=0, column=4, sticky=tk.W, padx=5, pady=5)
        tk.Button(self.vendors_navigation_frame,
                  text="All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_categories_and_vendors_view(self.active_user)).grid(
            row=0, column=5, sticky=tk.W, padx=5, pady=5)
        self.vendors_navigation_frame.grid(row=0, column=0, sticky=tk.W, pady=5)

    def create_categories_navigation_frame(self):
        tk.Label(self.categories_navigation_frame,
                 text="Categories",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        if self.active_user[1] == 1:
            tk.Button(self.categories_navigation_frame,
                      text="Add New Category",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_vendor_or_category_popup("categories")).grid(row=0,
                                                                                                column=1,
                                                                                                sticky=tk.W,
                                                                                                padx=10,
                                                                                                pady=5)
        else:
            tk.Button(self.categories_navigation_frame,
                      text="Request New Category",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_vendor_or_category_popup("categories", True)).grid(
                row=0,
                column=1,
                sticky=tk.W,
                padx=10,
                pady=5)
        self.categories_navigation_frame.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

    def create_vendors_list(self, vendor_search=False):
        self.get_vendors_list_from_database(vendor_search)
        self.populate_scrollable_vendors_list()
        self.create_scrollable_vendors_list()
        self.vendors_list_scrollable_container.grid(row=1, column=0, sticky=tk.W, pady=5)

    def create_categories_list(self):
        self.get_categories_list_from_database()
        self.populate_scrollable_categories_list()
        self.create_scrollable_categories_list()
        self.categories_list_scrollable_container.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

    # PRODUCTS LIST METHODS

    def get_vendors_list_from_database(self, vendor_search=None):
        if vendor_search:
            self.vendors_list = self.select_db.select_all_from_table_where_one_field_like("vendors",
                                                                                          "vendor_name",
                                                                                          '%' + vendor_search + '%',
                                                                                          no_archive=True)
        else:
            self.vendors_list = self.select_db.select_all_from_table("vendors", no_archived=True)

    def create_scrollable_vendors_list(self):
        products_list_canvas = tk.Canvas(self.vendors_list_scrollable_container,
                                         width=600,
                                         height=500,
                                         scrollregion=(0, 0, 0, self.vendors_canvas_length),
                                         bd=0,
                                         highlightthickness=0)
        products_list_canvas.config(bg=self.formatting.colour_code_1)
        products_list_canvas_scrollbar = tk.Scrollbar(self.vendors_list_scrollable_container,
                                                      orient="vertical",
                                                      command=products_list_canvas.yview)
        products_list_canvas.configure(yscrollcommand=products_list_canvas_scrollbar.set)
        products_list_canvas_scrollbar.pack(side='left',
                                            fill='y')
        products_list_canvas.pack(side="right",
                                  fill='y')
        products_list_canvas.create_window((0, 0),
                                           window=self.vendors_list_frame,
                                           anchor="nw")

    def populate_scrollable_vendors_list(self):
        row_counter = 0
        even_odd = 1
        tk.Label(self.vendors_list_frame,
                 text="Vendor Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.vendors_list_frame,
                 text="Approved?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
        row_counter += 1
        for item in self.vendors_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            vendor_name_label = self.formatting.create_shopping_cart_labels(self.vendors_list_frame,
                                                                            item[1],
                                                                            text_color)
            self.formatting.grid_shopping_cart_labels(vendor_name_label, row_counter, 0)
            if item[4] == 1:
                tk.Label(self.vendors_list_frame,
                         text="Yes",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_green).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            else:
                tk.Label(self.vendors_list_frame,
                         text="No",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_red).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            if self.active_user[1] == 1:
                tk.Button(self.vendors_list_frame,
                          text="Open",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.updated_vendor_popup(item)).grid(
                    row=row_counter,
                    column=2,
                    sticky=tk.W,
                    padx=10,
                    pady=5)
                tk.Button(self.vendors_list_frame,
                          text="Archive",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.archive_vendor_popup(item,
                                                                              "vendors")).grid(row=row_counter,
                                                                                               column=3,
                                                                                               sticky=tk.W,
                                                                                               padx=10,
                                                                                               pady=5)
                if item[4] == 0:
                    tk.Button(self.vendors_list_frame,
                              text="Approve",
                              font=self.formatting.medium_step_font,
                              command=lambda item=item: self.approve_vendor_request_and_reload_page(item)).grid(
                        row=row_counter,
                        column=4,
                        sticky=tk.W,
                        padx=10,
                        pady=5)
            else:
                tk.Button(self.vendors_list_frame,
                          text="View Notes",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.updated_vendor_popup(item)).grid(row=row_counter,
                                                                                              column=2,
                                                                                              sticky=tk.W,
                                                                                              padx=10,
                                                                                              pady=5)
            self.vendors_canvas_length += 50
            row_counter += 1
            even_odd += 1

# SHOPPING CART METHODS

    def get_categories_list_from_database(self):
        self.categories_list = self.select_db.select_all_from_table("categories", no_archived=True)

    def populate_scrollable_categories_list(self):
        row_counter = 0
        even_odd = 1
        tk.Label(self.categories_list_frame,
                 text="Category Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.categories_list_frame,
                 text="Approved?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
        row_counter += 1
        for item in self.categories_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            tk.Label(self.categories_list_frame,
                     text=item[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            if item[4] == 1:
                tk.Label(self.categories_list_frame,
                         text="Yes",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_green).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            else:
                tk.Label(self.categories_list_frame,
                         text="No",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_red).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Button(self.categories_list_frame,
                      text="Open",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.vendor_or_category_popup(
                        "categories",
                        item
                        )).grid(row=row_counter,
                                column=2,
                                sticky=tk.W,
                                padx=10,
                                pady=5)
            if self.active_user[1] == 1:
                tk.Button(self.categories_list_frame,
                          text="Archive",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.archive_vendor_popup(item,
                                                                              "categories")).grid(row=row_counter,
                                                                                                  column=3,
                                                                                                  sticky=tk.W,
                                                                                                  padx=10,
                                                                                                  pady=5)
                if item[4] == 0:
                    tk.Button(self.categories_list_frame,
                              text="Approve",
                              font=self.formatting.medium_step_font,
                              command=lambda item=item: self.approve_category_request_and_reload_page(item)).grid(
                        row=row_counter,
                        column=4,
                        sticky=tk.W,
                        padx=10,
                        pady=5)
            self.categories_canvas_length += 50
            row_counter += 1
            even_odd += 1

    def create_scrollable_categories_list(self):
        shopping_cart_canvas = tk.Canvas(self.categories_list_scrollable_container,
                                         width=600,
                                         height=500,
                                         scrollregion=(0, 0, 0, self.categories_canvas_length),
                                         bd=0,
                                         highlightthickness=0)
        shopping_cart_canvas.config(bg=self.formatting.colour_code_1)
        shopping_cart_canvas_scrollbar = tk.Scrollbar(self.categories_list_scrollable_container,
                                                      orient="vertical",
                                                      command=shopping_cart_canvas.yview)
        shopping_cart_canvas.configure(yscrollcommand=shopping_cart_canvas_scrollbar.set)
        shopping_cart_canvas_scrollbar.pack(side='left',
                                            fill='y')
        shopping_cart_canvas.pack(side="right",
                                  fill='y')
        shopping_cart_canvas.create_window((0, 0),
                                           window=self.categories_list_frame,
                                           anchor="nw")

    def updated_vendor_popup(self, vendor):
        vendor_popup = tk.Toplevel()
        vendor_popup.config(bg=self.formatting.colour_code_1)
        vendor_popup.geometry('1400x500')
        vendor_information_frame = tk.Frame(vendor_popup)
        vendor_product_frame = tk.Frame(vendor_popup)
        vendor_order_frame = tk.Frame(vendor_popup)
        vendor_information_frame.config(bg=self.formatting.colour_code_1)
        vendor_product_frame.config(bg=self.formatting.colour_code_3)
        vendor_order_frame.config(bg=self.formatting.colour_code_1)
        # INFORMATION FRAME WIDGETS
        tk.Label(vendor_information_frame,
                 text="Vendor Information",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        tk.Label(vendor_information_frame,
                 text="Name:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(vendor_information_frame,
                 text=vendor[1],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        if self.active_user[1] == 1:
            tk.Button(vendor_information_frame,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_name_popup("vendors", vendor, vendor_popup)
                      ).grid(row=1, column=2, sticky=tk.W, padx=10, pady=5)
        vendor_notes = tk.Text(vendor_information_frame,
                               height=5,
                               width=40)
        vendor_notes.config(bg=self.formatting.colour_code_2)
        vendor_notes.insert(tk.END, vendor[2])
        vendor_notes.config(state=tk.DISABLED, wrap="word")
        vendor_notes.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=10)
        if self.active_user[1] == 1:
            tk.Button(vendor_information_frame,
                      text="Edit Notes",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_notes_popup("vendors",
                                                            vendor,
                                                            vendor_popup)
                      ).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        # VENDOR PRODUCT FRAME WIDGETS
        tk.Label(vendor_product_frame,
                 text="Active Products",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_3,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        product_order_history = self.select_db.left_join_multiple_tables(
            "p.id, p.name, p.product_code, p.unit_of_issue",
            [["products p", "", "p.vendors_id"],
             ["vendors v", "v.id", ""]],
            "p.name",
            search_by=["v.id", '%' + str(vendor[0]) + '%']
            )
        product_order_history_list = [x for x in product_order_history]
        row_counter = 1
        if len(product_order_history_list) == 0:
            tk.Label(vendor_product_frame,
                     text="No Active Products found for this vendor.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_3,
                     fg=self.formatting.colour_code_1).grid(
                row=row_counter,
                column=0,
                columnspan=3,
                sticky=tk.W,
                padx=10,
                pady=5)
            row_counter += 1
        else:
            tk.Label(vendor_product_frame,
                     text=str(len(product_order_history_list)) + " Total Active Products",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_3,
                     fg=self.formatting.colour_code_1).grid(
                row=row_counter,
                column=0,
                columnspan=3,
                sticky=tk.W,
                padx=10,
                pady=5)
            row_counter += 1
            product_textbox = tk.Text(vendor_product_frame,
                                      height=23,
                                      width=60)
            product_textbox.config(state=tk.NORMAL)
            product_textbox.config(bg=self.formatting.colour_code_2)
            product_textbox.insert(tk.END, " Product Name             | Cat #          | Unit of Issue \n")
            product_textbox.insert(tk.END, "-----------------------------------------------------------\n")
            for item in product_order_history_list:
                product_textbox.insert(tk.END, (" " + str(item[1]) + " "*(25-len(str(item[1]))) + "| " +
                                                str(item[2]) + " "*(15-len(str(item[2]))) + "| " +
                                                str(item[3]) +
                                                "\n"))
            product_textbox.config(state=tk.DISABLED, wrap="word")
            product_textbox.grid(row=row_counter, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
            row_counter += 1
        # VENDOR ORDER FRAME WIDGETS
        tk.Label(vendor_order_frame,
                 text="Order History",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        vendor_order_history = self.select_db.left_join_multiple_tables(
            "o.id, o.order_date, o.units_ordered, p.name",
            [["orders o", "", "o.requests_id"],
             ["requests r", "r.id", "r.products_id"],
             ["products p", "p.id", "p.vendors_id"],
             ["vendors v", "v.id", ""]],
            "o.order_date DESC",
            search_by=["v.id", '%' + str(vendor[0]) + '%']
        )
        order_history_list = []
        date_differences = []
        order_amounts = []
        last_order = None
        row_counter = 1
        for item in vendor_order_history:
            order_history_list.append(item)
            if last_order:
                current_order = datetime.date(int(item[1].split("-")[0]),
                                              int(item[1].split("-")[1]),
                                              int(item[1].split("-")[2]))
                difference = last_order - current_order
                last_order = current_order
                date_differences.append(difference)
            else:
                last_order = datetime.date(int(item[1].split("-")[0]),
                                           int(item[1].split("-")[1]),
                                           int(item[1].split("-")[2]))
            order_amounts.append(int(item[2]))
        if len(date_differences) > 0:
            average_timedelta = sum(date_differences, datetime.timedelta(0)) / len(date_differences)
            tk.Label(vendor_order_frame,
                     text="Average time between orders:",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                row=row_counter,
                column=0,
                columnspan=3,
                sticky=tk.W,
                padx=10,
                pady=5)
            row_counter += 1
            tk.Label(vendor_order_frame,
                     text=str(average_timedelta) + " hours.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=row_counter,
                column=0,
                columnspan=3,
                sticky=tk.W,
                padx=10)
            row_counter += 1
        if len(order_amounts) > 0:
            average_order_amount = sum(order_amounts) / len(order_amounts)
            tk.Label(vendor_order_frame,
                     text="Average order amount:",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                row=row_counter,
                column=0,
                columnspan=3,
                sticky=tk.W,
                padx=10,
                pady=5)
            row_counter += 1
            tk.Label(vendor_order_frame,
                     text="{:.1f}".format(float(average_order_amount)) + " units.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=row_counter,
                column=0,
                columnspan=3,
                sticky=tk.W,
                padx=10)
            row_counter += 1
        else:
            tk.Label(vendor_order_frame,
                     text="No Orders Placed for this product.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                row=row_counter,
                column=0,
                columnspan=3,
                sticky=tk.W,
                padx=10,
                pady=5)
            row_counter += 1
        if len(order_amounts) > 0:
            order_history_textbox = tk.Text(vendor_order_frame,
                                            height=18,
                                            width=55)
            order_history_textbox.config(state=tk.NORMAL)
            order_history_textbox.config(bg=self.formatting.colour_code_2)
            order_history_textbox.insert(tk.END, " Product Name             | # Ordered  | Date \n")
            order_history_textbox.insert(tk.END, "-----------------------------------------------------\n")
            for item in order_history_list:
                order_history_textbox.insert(tk.END, (" " + str(item[3]) + " "*(25-len(str(item[3]))) + "| " +
                                                      str(item[2]) + " "*(11-len(str(item[2]))) + "| " +
                                                      str(item[1]) +
                                                      "\n"))
            order_history_textbox.config(state=tk.DISABLED, wrap="word")
            order_history_textbox.grid(row=row_counter, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
            row_counter += 1
        vendor_information_frame.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=10)
        vendor_product_frame.grid(row=0, column=1, sticky=tk.NW, padx=10, pady=10)
        vendor_order_frame.grid(row=0, column=2, sticky=tk.NW, padx=10, pady=10)

    def vendor_or_category_popup(self, table_to_edit, vendor_or_category):
        vendor_or_category_popup = tk.Toplevel()
        vendor_or_category_popup.config(bg=self.formatting.colour_code_1)
        vendor_or_category_popup.geometry('600x250')
        tk.Label(vendor_or_category_popup,
                 text=vendor_or_category[1],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        if self.active_user[1] == 1:
            tk.Button(vendor_or_category_popup,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_name_popup(table_to_edit, vendor_or_category, vendor_or_category_popup)
                      ).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        vendor_or_category_notes = tk.Text(vendor_or_category_popup,
                                           height=5,
                                           width=40)
        vendor_or_category_notes.config(bg=self.formatting.colour_code_2)
        vendor_or_category_notes.insert(tk.END, vendor_or_category[2])
        vendor_or_category_notes.config(state=tk.DISABLED, wrap="word")
        vendor_or_category_notes.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        if self.active_user[1] == 1:
            tk.Button(vendor_or_category_popup,
                      text="Edit Notes",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_notes_popup(table_to_edit,
                                                            vendor_or_category,
                                                            vendor_or_category_popup)
                      ).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
            if table_to_edit == "categories":
                tk.Button(vendor_or_category_popup,
                          text="Edit Sub-Categories",
                          font=self.formatting.medium_step_font,
                          command=lambda: self.edit_sub_categories_popup(vendor_or_category, vendor_or_category_popup)
                          ).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        else:
            if table_to_edit == "categories":
                tk.Button(vendor_or_category_popup,
                          text="View Sub-Categories",
                          font=self.formatting.medium_step_font,
                          command=lambda: self.edit_sub_categories_popup(vendor_or_category, vendor_or_category_popup)
                          ).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

    def edit_notes_popup(self, table_to_edit, vendor_or_category, individual_cat_vend_popup):
        edit_notes_popup = tk.Toplevel()
        edit_notes_popup.config(bg=self.formatting.colour_code_1)
        edit_notes_popup.geometry('500x160')
        product_notes = tk.Text(edit_notes_popup,
                                height=5,
                                width=40)
        product_notes.config(bg=self.formatting.colour_code_2, wrap="word")
        product_notes.config(state=tk.NORMAL)
        product_notes.insert(tk.END, vendor_or_category[2])
        product_notes.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_notes_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(table_to_edit,
                                                                                     product_notes.get("1.0", tk.END),
                                                                                     vendor_or_category,
                                                                                     "comments",
                                                                                     individual_cat_vend_popup,
                                                                                     edit_notes_popup
                                                                                     )).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10)

    def add_new_vendor_or_category_popup(self, table_to_add_to, request=False):
        add_new_popup = tk.Toplevel()
        add_new_popup.config(bg=self.formatting.colour_code_1)
        add_new_popup.geometry('500x350')
        tk.Label(add_new_popup,
                 text="Name: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        vendor_or_category_name = tk.Entry(add_new_popup)
        vendor_or_category_name.config(state=tk.NORMAL)
        vendor_or_category_name.grid(row=0, column=1, sticky=tk.W, pady=10)
        tk.Label(add_new_popup,
                 text="Notes",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        vendor_or_category_notes = tk.Text(add_new_popup,
                                           height=5,
                                           width=40)
        vendor_or_category_notes.config(bg=self.formatting.colour_code_2, wrap="word")
        vendor_or_category_notes.config(state=tk.NORMAL)
        vendor_or_category_notes.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        if table_to_add_to == "vendors":
            add_new_text = "Vendor"
        else:
            add_new_text = "Category"
        if self.active_user[1] == 1:
            tk.Button(add_new_popup,
                      text="Add new " + add_new_text,
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_new_vendor_or_category(table_to_add_to,
                                                                                  vendor_or_category_name.get(),
                                                                                  vendor_or_category_notes.get("1.0",
                                                                                                               tk.END),
                                                                                  add_new_popup)).grid(
                row=3, column=0, sticky=tk.W, padx=10, pady=10)
        else:
            tk.Button(add_new_popup,
                      text="Request new " + add_new_text,
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_new_vendor_or_category(table_to_add_to,
                                                                                  vendor_or_category_name.get(),
                                                                                  vendor_or_category_notes.get("1.0",
                                                                                                               tk.END),
                                                                                  add_new_popup,
                                                                                  request)).grid(
                row=3, column=0, sticky=tk.W, padx=10, pady=10)

    def edit_sub_categories_popup(self,
                                  current_category_record,
                                  vendor_or_category_popup):
        row_counter = 0
        edit_subcategories_popup = tk.Toplevel()
        edit_subcategories_popup.config(bg=self.formatting.colour_code_1)
        edit_subcategories_popup.geometry('600x300')
        category_sub_cats = self.select_db.select_all_from_table_where_one_field_equals("sub_categories",
                                                                                        "categories_id",
                                                                                        current_category_record[0],
                                                                                        no_archive=True,
                                                                                        no_approved=True)
        category_sub_cats_list = []
        category_sub_cats_dict = {}
        for item in category_sub_cats:
            if item[2] == "None":
                pass
            else:
                category_sub_cats_list.append(item[2])
                category_sub_cats_dict[item[2]] = item
        if len(category_sub_cats_list) == 0:
            pass
        else:
            tk.Label(edit_subcategories_popup,
                     text="Existing Subcategories",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                row=row_counter, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)
            row_counter += 1
            sub_category_value = tk.StringVar(edit_subcategories_popup)
            sub_category_value.set(category_sub_cats_list[0])
            sub_category_menu = tk.OptionMenu(edit_subcategories_popup,
                                              sub_category_value,
                                              *category_sub_cats_list,)
            sub_category_menu.config(highlightbackground=self.formatting.colour_code_1)
            sub_category_menu.config(font=self.formatting.medium_step_font)
            sub_category_menu.grid(row=row_counter, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
            if self.active_user[1] == 1:
                tk.Button(edit_subcategories_popup,
                          text="Archive",
                          font=self.formatting.medium_step_font,
                          command=lambda: self.archive_subcategory_and_reload_page(
                              category_sub_cats_dict[sub_category_value.get()][0],
                              edit_subcategories_popup,
                              vendor_or_category_popup)).grid(
                    row=row_counter, column=2, sticky=tk.W, padx=10, pady=10)
                tk.Button(edit_subcategories_popup,
                          text="Edit Name",
                          font=self.formatting.medium_step_font,
                          command=lambda: self.edit_name_popup("sub_categories",
                                                               category_sub_cats_dict[sub_category_value.get()],
                                                               edit_subcategories_popup,
                                                               True)).grid(
                    row=row_counter, column=3, sticky=tk.W, padx=10, pady=10)
            row_counter += 1
        if self.active_user[1] == 1:
            tk.Label(edit_subcategories_popup,
                     text="Add New Subcategory",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                     row=row_counter, column=0, columnspan=3, sticky=tk.W, pady=10, padx=10)
        else:
            tk.Label(edit_subcategories_popup,
                     text="Request New Subcategory",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                     row=row_counter, column=0, columnspan=3, sticky=tk.W, pady=10, padx=10)
        row_counter += 1
        tk.Label(edit_subcategories_popup,
                 text="Name: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=0, sticky=tk.W, pady=10, padx=10)
        subcategory_name = tk.Entry(edit_subcategories_popup)
        subcategory_name.config(state=tk.NORMAL)
        subcategory_name.grid(row=row_counter, column=1, sticky=tk.W, pady=10)
        if self.active_user[1] == 1:
            row_counter += 1
            tk.Button(edit_subcategories_popup,
                      text="Add new Subcategory",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_sub_category(current_category_record[0],
                                                                        subcategory_name.get(),
                                                                        "",
                                                                        edit_subcategories_popup,
                                                                        vendor_or_category_popup,
                                                                        row_counter)).grid(
                row=row_counter-1, column=2, columnspan=2, sticky=tk.W, padx=10, pady=10)
        else:
            row_counter += 1
            tk.Button(edit_subcategories_popup,
                      text="Request new Subcategory",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_sub_category(current_category_record[0],
                                                                        subcategory_name.get(),
                                                                        "",
                                                                        edit_subcategories_popup,
                                                                        vendor_or_category_popup,
                                                                        row_counter,
                                                                        True)).grid(
                row=row_counter-1, column=2, columnspan=2, sticky=tk.W, padx=10, pady=10)

    def edit_name_popup(self, table_to_edit, vendor_or_category, individual_cat_vend_popup, sub_category=False):
        edit_notes_popup = tk.Toplevel()
        edit_notes_popup.config(bg=self.formatting.colour_code_1)
        edit_notes_popup.geometry('500x90')
        edit_name_entry = tk.Entry(edit_notes_popup)
        edit_name_entry.config(state=tk.NORMAL)
        if sub_category:
            edit_name_entry.insert(tk.END, vendor_or_category[2])
        else:
            edit_name_entry.insert(tk.END, vendor_or_category[1])
        edit_name_entry.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_notes_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.check_for_blank_name_edit(table_to_edit,
                                                                 edit_name_entry.get(),
                                                                 vendor_or_category,
                                                                 individual_cat_vend_popup,
                                                                 edit_notes_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)

    def check_for_blank_name_edit(self,
                                  table_to_edit,
                                  name_to_edit,
                                  vendor_or_category,
                                  individual_cat_vendor_popup,
                                  edit_notes_popup):
        check = self.error_handling.checkBlankEntry(name_to_edit)
        if check:
            self.commit_edit_query_close_edit_popup_and_reload(table_to_edit,
                                                               name_to_edit,
                                                               vendor_or_category,
                                                               "name check",
                                                               individual_cat_vendor_popup,
                                                               edit_notes_popup
                                                               )
        else:
            tk.Label(edit_notes_popup,
                     text="Name cannot be blank.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=1, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)

    def archive_subcategory_and_reload_page(self,
                                            subcategory_to_archive,
                                            edit_subcategories_popup,
                                            vendor_or_category_popup):
        self.edit_db.archive_entry_in_table_by_id("sub_categories", subcategory_to_archive)
        edit_subcategories_popup.destroy()
        vendor_or_category_popup.destroy()
        self.parent.display_categories_and_vendors_view(self.active_user)

    def check_for_blank_sub_category(self,
                                     current_category_record_id,
                                     subcategory_name,
                                     subcategory_comments,
                                     edit_subcategories_popup,
                                     vendor_or_category_popup,
                                     row_counter,
                                     request=False):
        check = self.error_handling.checkBlankEntry(subcategory_name)
        if check:
            if request:
                self.add_new_sub_category((current_category_record_id,
                                           subcategory_name,
                                           subcategory_comments,
                                           "0"),
                                          edit_subcategories_popup,
                                          vendor_or_category_popup,
                                          request)
            else:
                self.add_new_sub_category((current_category_record_id,
                                           subcategory_name,
                                           subcategory_comments),
                                          edit_subcategories_popup,
                                          vendor_or_category_popup)
        else:
            tk.Label(edit_subcategories_popup,
                     text="Name cannot be blank.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=row_counter, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)

    def add_new_sub_category(self,
                             values,
                             edit_subcategories_popup,
                             vendor_or_category_popup,
                             request=False):
        if request:
            self.add_delete_db.new_sub_categories_record(values, request)
        else:
            self.add_delete_db.new_sub_categories_record(values)
        edit_subcategories_popup.destroy()
        vendor_or_category_popup.destroy()
        self.parent.display_categories_and_vendors_view(self.active_user)

    def check_for_blank_new_vendor_or_category(self,
                                               table_to_add_to,
                                               vendor_cat_name,
                                               vendor_cat_comments,
                                               add_new_popup,
                                               request=False):
        check = self.error_handling.checkBlankEntry(vendor_cat_name)
        if check:
            if request:
                self.add_new_vendor_or_category(table_to_add_to,
                                                (vendor_cat_name,
                                                 vendor_cat_comments,
                                                 "0"),
                                                add_new_popup,
                                                request)
            else:
                self.add_new_vendor_or_category(table_to_add_to,
                                                (vendor_cat_name,
                                                 vendor_cat_comments),
                                                add_new_popup)
        else:
            tk.Label(add_new_popup,
                     text="Name cannot be blank.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=4, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)

    def add_new_vendor_or_category(self,
                                   table_to_add_to,
                                   values,
                                   add_new_window,
                                   request=False):
        if table_to_add_to == "vendors":
            if request:
                self.add_delete_db.new_vendors_record(values, request)
            else:
                self.add_delete_db.new_vendors_record(values)
        else:
            if request:
                self.add_delete_db.new_categories_record(values, request)
            else:
                self.add_delete_db.new_categories_record(values)
        add_new_window.destroy()
        self.parent.display_categories_and_vendors_view(self.active_user)

    def commit_edit_query_close_edit_popup_and_reload(self,
                                                      table_to_edit,
                                                      new_value_entry,
                                                      vendor_or_category,
                                                      field_to_edit,
                                                      top_level_window,
                                                      category_vendor_window):
        if field_to_edit == "name check":
            if table_to_edit == "categories":
                field_to_edit = "category_name"
            elif table_to_edit == "sub_categories":
                field_to_edit = "sub_category_name"
            else:
                field_to_edit = "vendor_name"
        try:
            new_value_entry = new_value_entry.get()
        except AttributeError:
            pass
        self.edit_db.edit_one_record_one_field_one_table(table_to_edit,
                                                         field_to_edit,
                                                         new_value_entry,
                                                         vendor_or_category[0])
        top_level_window.destroy()
        category_vendor_window.destroy()
        self.parent.display_categories_and_vendors_view(self.active_user)

    def archive_vendor_popup(self, vendor_to_archive, table_to_access):
        are_you_sure_logout_popup = tk.Toplevel()
        are_you_sure_logout_popup.config(bg=self.formatting.colour_code_1)
        are_you_sure_logout_popup.geometry('500x90')
        tk.Label(are_you_sure_logout_popup,
                 text="Are you sure you want to archive?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        yes_i_am = tk.Button(are_you_sure_logout_popup,
                             text="Yes",
                             font=self.formatting.medium_step_font,
                             command=lambda: self.destroy_popup_archive_product_and_reload(
                                 vendor_to_archive,
                                 are_you_sure_logout_popup,
                                 table_to_access)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)
        no_i_aint = tk.Button(are_you_sure_logout_popup,
                              text="No",
                              font=self.formatting.medium_step_font,
                              command=lambda: are_you_sure_logout_popup.destroy()).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    def destroy_popup_archive_product_and_reload(self, vendor_to_archive, top_level_window, table_to_access):
        self.edit_db.archive_entry_in_table_by_id(table_to_access, vendor_to_archive[0])
        self.parent.display_categories_and_vendors_view(self.active_user)
        top_level_window.destroy()

    def approve_vendor_request_and_reload_page(self, record_to_approve):
        self.edit_db.edit_one_record_one_field_one_table("vendors", "approved", "1", record_to_approve[0])
        self.parent.display_categories_and_vendors_view(self.active_user)

    def approve_category_request_and_reload_page(self, record_to_approve):
        self.edit_db.edit_one_record_one_field_one_table("categories", "approved", "1", record_to_approve[0])
        self.parent.display_categories_and_vendors_view(self.active_user)