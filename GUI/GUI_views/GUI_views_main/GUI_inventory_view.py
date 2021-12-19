import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_errorHandling as tk_error_handling
import datetime


class InventoryView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.error_handling = tk_error_handling.ErrorHandling()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.config(bg=self.formatting.colour_code_1)
        self.inventory = ()
        self.inventory_canvas_length = 0
        self.inventory_scrollable_container = tk.Frame(self)
        self.inventory_frame = tk.Frame(self)
        self.inventory_frame.config(bg=self.formatting.colour_code_1)
        self.inventory_navigation_frame = tk.Frame(self)
        self.inventory_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.sort_inventory_view_by = ["INV #",
                                       "Product Name",
                                       "Product Code",
                                       "Product Category",
                                       "Vendor Name",
                                       "Units",
                                       "Received Date",
                                       "Amount Remaining",
                                       "Location",
                                       "Last Updated"]
        self.inventory_sort_value = tk.StringVar(self)
        self.inventory_sort_value.set("INV #")
        self.search_inventory_view_by = ["INV #",
                                         "Product Name",
                                         "Product Code",
                                         "Product Category",
                                         "Vendor Name",
                                         "Location"]
        self.inventory_search_value = tk.StringVar(self)
        self.inventory_search_value.set("INV #")
        self.sort_by_inventory_conversion_dictionary = {"INV #": "i.id",
                                                        "Product Name": "p.name",
                                                        "Product Code": "p.product_code",
                                                        "Product Category": "c.category_name",
                                                        "Vendor Name": "v.vendor_name",
                                                        "Units": "p.unit_of_issue",
                                                        "Received Date": "rc.received_date",
                                                        "Amount Remaining": "i.full_units_remaining",
                                                        "Location": "loc.locations_name",
                                                        "Last Updated": "i.last_updated"
                                                        }
        self.editInventoryFailLabel = tk.Label()
        self.sub_locations_menu = ""
        self.sub_locations_value = ""
        self.search_by_active_term = ""
        self.sort_by = ""
        self.search_by_variable = ""

    def inventory_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.sort_by = sort_by
        self.search_by_active_term = search_by
        self.search_by_variable = search_by_variable
        self.active_user = user
        self.create_inventory_view(sort_by, search_by, search_by_variable)

    def create_inventory_view(self, sort_by=False, search_by=False, search_by_variable=False):
        self.get_active_inventory_from_database(sort_by, search_by, search_by_variable)
        self.make_scrollable_inventory_header_labels()
        self.populate_scrollable_inventory_list()
        self.create_scrollable_inventory_view()
        self.create_inventory_navigation_frame()
        self.inventory_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.inventory_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def get_active_inventory_from_database(self, sort_by=None, search_by=None, search_by_variable=None):
        if sort_by and search_by:
            sort_by_variable = self.sort_by_inventory_conversion_dictionary[sort_by]
            self.inventory_sort_value.set(sort_by)
            search_by_term = self.sort_by_inventory_conversion_dictionary[search_by_variable]
            self.inventory_search_value.set(search_by_variable)
            self.inventory = self.select_db. \
                left_join_multiple_tables("p.name, p.product_code, c.category_name, v.vendor_name, p.unit_of_issue," +
                                          " rc.received_date, i.full_units_remaining, i.partial_units_remaining, " +
                                          " loc.locations_name, subloc.sub_locations_name, i.last_updated, " +
                                          " u.user_name, rc.expiry_date, rc.model, rc.equipment_SN, rc.lot_number, " +
                                          " o.order_date, i.comments, i.id",
                                          [["inventory i", "", "i.received_id"],
                                           ["received rc", "rc.id", "rc.orders_id"],
                                           ["orders o", "o.id", "o.requests_id"],
                                           ["requests r", "r.id", "r.users_id"],
                                           ["users u", "u.id", "r.products_id"],
                                           ["products p", "p.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", "i.location_id"],
                                           ["inventoryLocations loc", "loc.id", "i.sub_location_id"],
                                           ["inventorySubLocations subloc", "subloc.id", ""]],
                                          sort_by_variable,
                                          no_archive="i.archived",
                                          search_by=[search_by_term, '%' + search_by + '%'])
        elif sort_by:
            sort_by_variable = self.sort_by_inventory_conversion_dictionary[sort_by]
            self.inventory_sort_value.set(sort_by)
            self.inventory = self.select_db. \
                left_join_multiple_tables("p.name, p.product_code, c.category_name, v.vendor_name, p.unit_of_issue," +
                                          " rc.received_date, i.full_units_remaining, i.partial_units_remaining, " +
                                          " loc.locations_name, subloc.sub_locations_name, i.last_updated, " +
                                          " u.user_name, rc.expiry_date, rc.model, rc.equipment_SN, rc.lot_number, " +
                                          " o.order_date, i.comments, i.id",
                                          [["inventory i", "", "i.received_id"],
                                           ["received rc", "rc.id", "rc.orders_id"],
                                           ["orders o", "o.id", "o.requests_id"],
                                           ["requests r", "r.id", "r.users_id"],
                                           ["users u", "u.id", "r.products_id"],
                                           ["products p", "p.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", "i.location_id"],
                                           ["inventoryLocations loc", "loc.id", "i.sub_location_id"],
                                           ["inventorySubLocations subloc", "subloc.id", ""]],
                                          sort_by_variable,
                                          no_archive="i.archived")
        elif search_by:
            search_by_term = self.sort_by_inventory_conversion_dictionary[search_by_variable]
            self.inventory_search_value.set(search_by_variable)
            self.inventory = self.select_db. \
                left_join_multiple_tables("p.name, p.product_code, c.category_name, v.vendor_name, p.unit_of_issue," +
                                          " rc.received_date, i.full_units_remaining, i.partial_units_remaining, " +
                                          " loc.locations_name, subloc.sub_locations_name, i.last_updated, " +
                                          " u.user_name, rc.expiry_date, rc.model, rc.equipment_SN, rc.lot_number, " +
                                          " o.order_date, i.comments, i.id",
                                          [["inventory i", "", "i.received_id"],
                                           ["received rc", "rc.id", "rc.orders_id"],
                                           ["orders o", "o.id", "o.requests_id"],
                                           ["requests r", "r.id", "r.users_id"],
                                           ["users u", "u.id", "r.products_id"],
                                           ["products p", "p.id", "p.vendors_id"],
                                           ["vendors v", "v.id", "p.categories_id"],
                                           ["categories c", "c.id", "r.price_id"],
                                           ["priceTracking pt", "pt.id", "i.location_id"],
                                           ["inventoryLocations loc", "loc.id", "i.sub_location_id"],
                                           ["inventorySubLocations subloc", "subloc.id", ""]],
                                          "p.name",
                                          no_archive="i.archived",
                                          search_by=[search_by_term, '%' + search_by + '%'])
        else:
            self.inventory = self.select_db. \
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
                                          no_archive="i.archived")

    def make_scrollable_inventory_header_labels(self):
        tk.Label(self.inventory_frame,
                 text="Product Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="Product ID",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="Category",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="Vendor",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="Unit of Issue",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=5, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="Receive Date",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=6, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="Amount Remaining",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=7, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="Location",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=8, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.inventory_frame,
                 text="last updated",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=9, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_inventory_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.inventory:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            tk.Label(self.inventory_frame,
                     text="INV-" + str(item[18]),
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_purple).grid(
                row=row_counter,
                column=0,
                sticky=tk.W,
                pady=5,
                padx=10)
            if len(item[0]) > 20:
                product_name = item[0][0:20] + "..."
            else:
                product_name = item[0]
            tk.Label(self.inventory_frame,
                     text=product_name,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.inventory_frame,
                     text=item[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.inventory_frame,
                     text=item[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.inventory_frame,
                     text=item[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.inventory_frame,
                     text=item[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=5, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.inventory_frame,
                     text=item[5],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=6, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.inventory_frame,
                     text=str(item[6]) + " F / " + str(item[7]) + " P",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=7, sticky=tk.W, padx=10, pady=5)
            if item[9] == "none":
                sub_location = ""
            else:
                sub_location = " (" + item[9] + ")"
            tk.Label(self.inventory_frame,
                     text=item[8] + sub_location,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=8, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.inventory_frame,
                     text=item[10],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=9, sticky=tk.W, padx=10, pady=5)
            tk.Button(self.inventory_frame,
                      text="Open",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.inventory_product_popup(item)).grid(
                row=row_counter,
                column=10,
                sticky=tk.W,
                padx=10,
                pady=5)
            row_counter += 1
            even_odd += 1
            self.inventory_canvas_length += 50

    def create_inventory_navigation_frame(self):
        inventory_search_entry = tk.Entry(self.inventory_navigation_frame)
        tk.Label(self.inventory_navigation_frame,
                 text="Lab Inventory",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Label(self.inventory_navigation_frame,
                 text="Sort:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.inventory_navigation_frame,
                                          self.inventory_sort_value,
                                          *self.sort_inventory_view_by)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        sort_by_button = tk.Button(self.inventory_navigation_frame,
                                   text="Sort",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_inventory_view(
                                       self.active_user,
                                       sort_by=self.inventory_sort_value.get(),
                                       search_by=self.search_by_active_term,
                                       search_by_variable=self.search_by_variable)).grid(
            row=0, column=3, sticky=tk.W, padx=10, pady=5
        )
        # searching tk widgets
        type_of_search_menu = tk.OptionMenu(self.inventory_navigation_frame,
                                            self.inventory_search_value,
                                            *self.search_inventory_view_by)
        type_of_search_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_search_menu.config(font=self.formatting.medium_step_font)
        tk.Label(self.inventory_navigation_frame,
                 text="Search:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=4, sticky=tk.W, pady=5)
        inventory_search_entry.grid(row=0, column=5, sticky=tk.W, pady=5)
        type_of_search_menu.grid(row=0, column=6, sticky=tk.W, pady=5)
        search_by_button = tk.Button(self.inventory_navigation_frame,
                                     text="Search",
                                     font=self.formatting.medium_step_font,
                                     command=lambda: self.parent.display_inventory_view(
                                         self.active_user,
                                         sort_by=self.sort_by,
                                         search_by=inventory_search_entry.get(),
                                         search_by_variable=self.inventory_search_value.get())).grid(
            row=0, column=7, sticky=tk.W, padx=10, pady=5
        )
        tk.Button(self.inventory_navigation_frame,
                  text="All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_inventory_view(
                      self.active_user)).grid(
            row=0, column=8, sticky=tk.W, padx=10, pady=5
        )

    def create_scrollable_inventory_view(self):
        inventory_canvas = tk.Canvas(self.inventory_scrollable_container,
                                     width=1650,
                                     height=500,
                                     scrollregion=(0, 0, 0, self.inventory_canvas_length),
                                     bd=0,
                                     highlightthickness=0)
        inventory_canvas.config(bg=self.formatting.colour_code_1)
        orders_canvas_scrollbar = tk.Scrollbar(self.inventory_scrollable_container,
                                               orient="vertical",
                                               command=inventory_canvas.yview)
        inventory_canvas.configure(yscrollcommand=orders_canvas_scrollbar.set)
        orders_canvas_scrollbar.pack(side='left',
                                     fill='y')
        inventory_canvas.pack(side="right",
                              fill='y')
        inventory_canvas.create_window((0, 0),
                                       window=self.inventory_frame,
                                       anchor="nw")

    def inventory_product_popup(self, inventory_item):
        receive_product_popup = tk.Toplevel()
        receive_product_popup.config(bg=self.formatting.colour_code_1)
        receive_product_popup.geometry('500x800')
        tk.Label(receive_product_popup,
                 text=inventory_item[0] + " (INV-" + str(inventory_item[18]) + ")",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_purple).grid(row=0, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Product Information",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=1, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Product Code:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=2, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[1],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=2, column=1, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Vendor:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=3, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[3],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=3, column=1, columnspan=3, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Unit of Issue:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=4, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[4],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=4, column=1, columnspan=5, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Lot Number:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[15],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=5, column=1, columnspan=5, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Serial Number:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=6, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[14],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=6, column=1, columnspan=5, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Model:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=7, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[13],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=7, column=1, columnspan=5, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Category:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=8, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[2],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=8, column=1, columnspan=5, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Timeline",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=9, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Order Date:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=10, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[16],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=10, column=1, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Receive Date:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=11, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[5],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=11, column=1, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Expiry Date:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=12, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[12],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=12, column=1, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Inventory Information",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=13, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(receive_product_popup,
                 text="Full Units Remaining:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=14, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[6],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=14, column=1, columnspan=5, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Partial Units Remaining:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=15, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[7],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=15, column=1, columnspan=5, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Location:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=16, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[8],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=16, column=1, sticky=tk.W)
        tk.Label(receive_product_popup,
                 text="Sub-Location:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=17, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[9],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=17, column=1, sticky=tk.W, columnspan=3)
        tk.Label(receive_product_popup,
                 text="Last Updated by:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=18, column=0, sticky=tk.W, padx=10)
        tk.Label(receive_product_popup,
                 text=inventory_item[11] + " on " + inventory_item[10],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=18, column=1, sticky=tk.W, columnspan=5)
        tk.Label(receive_product_popup,
                 text="Inventory Comments",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=19, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        received_notes = tk.Text(receive_product_popup,
                                 height=5,
                                 width=40)
        received_notes.config(bg=self.formatting.colour_code_2)
        received_notes.config(state=tk.NORMAL)
        received_notes.insert(tk.END, inventory_item[17])
        received_notes.config(state=tk.DISABLED, wrap="word")
        received_notes.grid(row=20, column=0, columnspan=6, sticky=tk.W, padx=10)

    def edit_received_product_popup(self, received_order, received_order_popup):
        edit_receive_product_popup = tk.Toplevel()
        edit_receive_product_popup.config(bg=self.formatting.colour_code_1)
        edit_receive_product_popup.geometry('500x700')
        tk.Label(edit_receive_product_popup,
                 text="Edit Receiving Information",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_receive_product_popup,
                 text="Amount Received",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, padx=10)
        amount_received_entry = tk.Entry(edit_receive_product_popup)
        amount_received_entry.grid(row=1, column=1, sticky=tk.W, padx=10)
        amount_received_entry.insert(tk.END, received_order[8])
        tk.Label(edit_receive_product_popup,
                 text="Received Date",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_receive_product_popup,
                 text="Year",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=3, column=0, sticky=tk.W, padx=10)
        year_entry = tk.Entry(edit_receive_product_popup)
        year_entry.grid(row=3, column=1, sticky=tk.W, padx=10)
        year_entry.insert(tk.END, received_order[9].split("-")[0])
        tk.Label(edit_receive_product_popup,
                 text="Month",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=4, column=0, sticky=tk.W, padx=10)
        month_entry = tk.Entry(edit_receive_product_popup)
        month_entry.grid(row=4, column=1, sticky=tk.W, padx=10)
        month_entry.insert(tk.END, received_order[9].split("-")[1])
        tk.Label(edit_receive_product_popup,
                 text="Day",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10)
        day_entry = tk.Entry(edit_receive_product_popup)
        day_entry.grid(row=5, column=1, sticky=tk.W, padx=10)
        day_entry.insert(tk.END, received_order[9].split("-")[2])
        tk.Label(edit_receive_product_popup,
                 text="Receiving Information (Optional)",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_receive_product_popup,
                 text="Lot Number",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=7, column=0, sticky=tk.W, padx=10)
        lot_number_entry = tk.Entry(edit_receive_product_popup)
        lot_number_entry.grid(row=7, column=1, sticky=tk.W, padx=10)
        lot_number_entry.insert(tk.END, received_order[10])
        tk.Label(edit_receive_product_popup,
                 text="Serial Number",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=8, column=0, sticky=tk.W, padx=10)
        serial_entry = tk.Entry(edit_receive_product_popup)
        serial_entry.grid(row=8, column=1, sticky=tk.W, padx=10)
        serial_entry.insert(tk.END, received_order[13])
        tk.Label(edit_receive_product_popup,
                 text="Model",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=9, column=0, sticky=tk.W, padx=10)
        model_entry = tk.Entry(edit_receive_product_popup)
        model_entry.grid(row=9, column=1, sticky=tk.W, padx=10)
        model_entry.insert(tk.END, received_order[12])
        tk.Label(edit_receive_product_popup,
                 text="Product Expiry Date",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=10, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_receive_product_popup,
                 text="Year",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=11, column=0, sticky=tk.W, padx=10)
        expiry_year_entry = tk.Entry(edit_receive_product_popup)
        expiry_year_entry.grid(row=11, column=1, sticky=tk.W, padx=10)
        expiry_year_entry.insert(tk.END, received_order[11].split("-")[0])
        tk.Label(edit_receive_product_popup,
                 text="Month",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=12, column=0, sticky=tk.W, padx=10)
        expiry_month_entry = tk.Entry(edit_receive_product_popup)
        expiry_month_entry.grid(row=12, column=1, sticky=tk.W, padx=10)
        expiry_month_entry.insert(tk.END, received_order[11].split("-")[1])
        tk.Label(edit_receive_product_popup,
                 text="Day",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=13, column=0, sticky=tk.W, padx=10)
        expiry_day_entry = tk.Entry(edit_receive_product_popup)
        expiry_day_entry.grid(row=13, column=1, sticky=tk.W, padx=10)
        expiry_day_entry.insert(tk.END, received_order[11].split("-")[2])
        tk.Label(edit_receive_product_popup,
                 text="Comments",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=14, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        received_notes = tk.Text(edit_receive_product_popup,
                                 height=5,
                                 width=40)
        received_notes.config(bg=self.formatting.colour_code_2)
        received_notes.config(state=tk.NORMAL)
        received_notes.insert(tk.END, received_order[14])
        received_notes.grid(row=15, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_receive_product_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda item=received_order: self.check_edits_and_commit_changes_to_received_product(
                      item[15],
                      year_entry.get(),
                      month_entry.get(),
                      day_entry.get(),
                      expiry_year_entry.get(),
                      expiry_month_entry.get(),
                      expiry_day_entry.get(),
                      amount_received_entry.get(),
                      lot_number_entry.get(),
                      model_entry.get(),
                      serial_entry.get(),
                      received_notes.get("1.0", tk.END),
                      edit_receive_product_popup,
                      received_order_popup)).grid(
            row=16,
            column=0,
            columnspan=3,
            sticky=tk.W,
            padx=10,
            pady=5)

    def check_edits_and_commit_changes_to_received_product(self,
                                                           received_id,
                                                           received_year,
                                                           received_month,
                                                           received_day,
                                                           expiry_year,
                                                           expiry_month,
                                                           expiry_day,
                                                           received_amount,
                                                           lot_number,
                                                           model,
                                                           serial_number,
                                                           comments,
                                                           edit_popup_window,
                                                           received_popup_window):
        int_error_check = self.error_handling.checkIfInt(received_amount)
        date_error_check = self.error_handling.checkYearMonthDayFormat(received_year, received_month, received_day)
        exp_date_error_check = self.error_handling.checkYearMonthDayFormat(expiry_year,
                                                                           expiry_month,
                                                                           expiry_day,
                                                                           expiry=True)
        if int_error_check and date_error_check and exp_date_error_check:
            expiry_date = datetime.date(int(expiry_year), int(expiry_month), int(expiry_day))
            received_date = datetime.date(int(received_year), int(received_month), int(received_day))
            self.edit_db.edit_one_record_one_field_one_table("received",
                                                             "expiry_date",
                                                             expiry_date,
                                                             received_id)
            self.edit_db.edit_one_record_one_field_one_table("received",
                                                             "received_date",
                                                             received_date,
                                                             received_id)
            self.edit_db.edit_one_record_one_field_one_table("received",
                                                             "received_amount",
                                                             received_amount,
                                                             received_id)
            self.edit_db.edit_one_record_one_field_one_table("received",
                                                             "lot_number",
                                                             lot_number,
                                                             received_id)
            self.edit_db.edit_one_record_one_field_one_table("received",
                                                             "model",
                                                             model,
                                                             received_id)
            self.edit_db.edit_one_record_one_field_one_table("received",
                                                             "equipment_SN",
                                                             serial_number,
                                                             received_id)
            self.edit_db.edit_one_record_one_field_one_table("received",
                                                             "comments",
                                                             comments,
                                                             received_id)
            received_popup_window.destroy()
            edit_popup_window.destroy()
            self.parent.display_inventory_view(self.active_user,
                                               sort_by=self.sort_by,
                                               search_by=self.search_by_active_term,
                                               search_by_variable=self.search_by_variable)
        else:
            self.editInventoryFailLabel.destroy()
            self.editInventoryFailLabel = tk.Label(edit_popup_window,
                                                   text="At least one issue with edited information. Try Again.",
                                                   font=self.formatting.medium_step_font,
                                                   bg=self.formatting.colour_code_1,
                                                   fg=self.formatting.colour_code_3).grid(
                row=17,
                column=0,
                columnspan=3,
                sticky=tk.W,
                pady=5,
                padx=10)

    def inventory_received_item_popup(self, item_to_inventory):
        inventory_received_item_popup = tk.Toplevel()
        inventory_received_item_popup.config(bg=self.formatting.colour_code_1)
        inventory_received_item_popup.geometry('600x200')
        locations_dict = {}
        locations_list = []
        sub_locations_dict = {}
        sub_locations_list = []
        locations = self.select_db.select_all_from_table("inventoryLocations")
        for item in locations:
            locations_dict[item[1]] = item[0]
            locations_list.append(item[1])
        sub_locations = self.select_db.select_all_from_table_where_one_field_equals(
            "inventorySubLocations",
            "locations_id",
            locations_dict[locations_list[0]],)
        for item in sub_locations:
            sub_locations_dict[item[2]] = item[0]
            sub_locations_list.append(item[2])
        locations_value = tk.StringVar(inventory_received_item_popup)
        self.sub_locations_value = tk.StringVar(inventory_received_item_popup)
        locations_menu = tk.OptionMenu(inventory_received_item_popup,
                                       locations_value,
                                       *locations_list,)
        locations_menu.config(highlightbackground=self.formatting.colour_code_1)
        locations_menu.config(font=self.formatting.medium_step_font)
        self.sub_locations_menu = tk.OptionMenu(inventory_received_item_popup,
                                                self.sub_locations_value,
                                                *sub_locations_list,)
        self.sub_locations_menu.config(highlightbackground=self.formatting.colour_code_1)
        self.sub_locations_menu.config(font=self.formatting.medium_step_font)
        tk.Label(inventory_received_item_popup,
                 text="Receive " + item_to_inventory[0],
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=1,
                                                        column=0,
                                                        columnspan=3,
                                                        sticky=tk.W,
                                                        padx=10,
                                                        pady=10)
        tk.Label(inventory_received_item_popup,
                 text="Location: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        locations_value.set(locations_list[0])
        locations_menu.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(inventory_received_item_popup,
                  text="Refresh Sub-Locations",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.refresh_sub_locations_on_inventory_window(
                      locations_dict[locations_value.get()],
                      inventory_received_item_popup)).grid(
            row=2, column=2, sticky=tk.W, padx=10, pady=10)
        tk.Label(inventory_received_item_popup,
                 text="Sub-Category",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        self.sub_locations_value.set(sub_locations_list[0])
        self.sub_locations_menu.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(inventory_received_item_popup,
                  text="Add to Inventory",
                  font=self.formatting.medium_step_font,
                  command=lambda item=item_to_inventory: self.add_inventory_item_and_reload_page(
                      item,
                      locations_dict[locations_value.get()],
                      sub_locations_dict[self.sub_locations_value.get()],
                      "",
                      inventory_received_item_popup)).grid(
            row=4,
            column=0,
            columnspan=3,
            sticky=tk.W,
            padx=10,
            pady=5)

    def refresh_sub_locations_on_inventory_window(self,
                                                  new_location,
                                                  inventory_popup):
        self.sub_locations_menu.destroy()
        sub_locations_dict = {}
        sub_locations_list = []
        self.sub_locations_value = tk.StringVar(inventory_popup)
        sub_locations = self.select_db.select_all_from_table_where_one_field_equals(
            "inventorySubLocations",
            "locations_id",
            new_location,)
        for item in sub_locations:
            sub_locations_dict[item[2]] = item[0]
            sub_locations_list.append(item[2])
        self.sub_locations_menu = tk.OptionMenu(inventory_popup,
                                                self.sub_locations_value,
                                                *sub_locations_list,)
        self.sub_locations_menu.config(highlightbackground=self.formatting.colour_code_1)
        self.sub_locations_menu.config(font=self.formatting.medium_step_font)
        self.sub_locations_value.set(sub_locations_list[0])
        self.sub_locations_menu.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)

    def add_inventory_item_and_reload_page(self,
                                           item_to_inventory,
                                           location_id,
                                           sub_location_id,
                                           comments,
                                           inventory_popup_window):
        received_id = item_to_inventory[15]
        full_units_remaining = item_to_inventory[8]
        partial_units_remaining = 0
        last_updated = datetime.date.today()
        updated_user_id = self.active_user[0]
        self.add_delete_db.new_inventory_record((received_id,
                                                 location_id,
                                                 sub_location_id,
                                                 full_units_remaining,
                                                 partial_units_remaining,
                                                 last_updated,
                                                 updated_user_id,
                                                 comments))
        inventory_popup_window.destroy()
        self.edit_db.archive_entry_in_table_by_id("received",
                                                  received_id)
        self.parent.display_inventory_view(self.active_user,
                                           sort_by=self.sort_by,
                                           search_by=self.search_by_active_term,
                                           search_by_variable=self.search_by_variable)
