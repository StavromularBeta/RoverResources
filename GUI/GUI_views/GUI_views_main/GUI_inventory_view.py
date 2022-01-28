import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_errorHandling as tk_error_handling
from GUI.GUI_formatting import GUI_data_export as tk_dataExport
import datetime


class InventoryView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.data_export = tk_dataExport.TkDataExportMethods()
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
        self.sort_inventory_view_by = ["INV # (ASC)",
                                       "INV # (DESC)",
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
        self.inventory_sort_value.set("INV # (DESC)")
        self.search_inventory_view_by = ["INV #",
                                         "Product Name",
                                         "Product Code",
                                         "Product Category",
                                         "Vendor Name",
                                         "Location"]
        self.inventory_search_value = tk.StringVar(self)
        self.inventory_search_value.set("INV #")
        self.sort_by_inventory_conversion_dictionary = {"INV #": "i.id",
                                                        "INV # (ASC)": "i.id ",
                                                        "INV # (DESC)": "i.id DESC",
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
        self.sub_locations_dict = {}
        self.search_by_active_term = ""
        self.sort_by = ""
        self.search_by_variable = ""
        self.printable_inventory_list = []
        self.wizard_inventory_comment = "This Inventory record was created manually.\n\n"

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
                                          "i.id DESC",
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
                                          "i.id DESC",
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
            self.printable_inventory_list.append(item)
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
            product_name = item[0]
            tk.Label(self.inventory_frame,
                     text=product_name,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=200,
                     justify=tk.LEFT).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
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
            if self.active_user[1] == 1:
                tk.Button(self.inventory_frame,
                          text="Archive",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.archive_inventory_popup(item)).grid(row=row_counter,
                                                                                             column=11,
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
        add_new_inventory_button = tk.Button(self.inventory_navigation_frame,
                                             text="Add Existing Inventory",
                                             font=self.formatting.medium_step_font,
                                             command=lambda: self.manual_inventory_addition_wizard_popup(
                                                 product_frame_active=True
                                             )).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=5
        )
        tk.Label(self.inventory_navigation_frame,
                 text="Sort:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.inventory_navigation_frame,
                                          self.inventory_sort_value,
                                          *self.sort_inventory_view_by)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
        sort_by_button = tk.Button(self.inventory_navigation_frame,
                                   text="Sort",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_inventory_view(
                                       self.active_user,
                                       sort_by=self.inventory_sort_value.get(),
                                       search_by=self.search_by_active_term,
                                       search_by_variable=self.search_by_variable)).grid(
            row=0, column=4, sticky=tk.W, padx=10, pady=5
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
                 fg=self.formatting.colour_code_1).grid(row=0, column=5, sticky=tk.W, pady=5)
        inventory_search_entry.grid(row=0, column=6, sticky=tk.W, pady=5)
        type_of_search_menu.grid(row=0, column=7, sticky=tk.W, pady=5)
        search_by_button = tk.Button(self.inventory_navigation_frame,
                                     text="Search",
                                     font=self.formatting.medium_step_font,
                                     command=lambda: self.parent.display_inventory_view(
                                         self.active_user,
                                         sort_by=self.sort_by,
                                         search_by=inventory_search_entry.get(),
                                         search_by_variable=self.inventory_search_value.get())).grid(
            row=0, column=8, sticky=tk.W, padx=10, pady=5
        )
        tk.Button(self.inventory_navigation_frame,
                  text="All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_inventory_view(
                      self.active_user)).grid(
            row=0, column=9, sticky=tk.W, padx=10, pady=5
        )
        # print view
        tk.Button(self.inventory_navigation_frame,
                  text="Print",
                  font=self.formatting.medium_step_font,
                  command=lambda : self.data_export.generate_data_export_popup(
                      self.active_user,
                      self.printable_inventory_list,
                      "inventory")).grid(
            row=0,
            column=10,
            sticky=tk.W,
            padx=10,
            pady=5)

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

    def manual_inventory_addition_wizard_popup(self,
                                               product_search_results=None,
                                               product_frame_active=False,
                                               confirmed_product=None,
                                               request_and_order_frame_active=False,
                                               confirmed_req_and_order_info=None,
                                               receiving_and_inventory_frame_active=False,
                                               confirmed_rec_and_inv_info=None,
                                               confirm_and_location_active=False,
                                               new_main_location=None):
        manual_wizard_popup = tk.Toplevel()
        manual_wizard_popup.config(bg=self.formatting.colour_code_1)
        manual_wizard_popup.geometry('700x900')
        tk.Label(manual_wizard_popup,
                 text="Manual Inventory Addition Wizard",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
        tk.Label(manual_wizard_popup,
                 text="This wizard will guide you through the process of adding an existing inventory item "
                      "to the RoverResources database that wasn't ordered through RoverResources.",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2,
                 wraplength=600,
                 justify=tk.LEFT
                 ).grid(row=1, column=0, sticky=tk.W, padx=10)
        # Product Wizard Code
        if product_frame_active:
            step_1_title_colour = self.formatting.colour_code_purple
        else:
            step_1_title_colour = self.formatting.colour_code_3
        product_wizard_frame = tk.Frame(manual_wizard_popup)
        product_wizard_frame.config(bg=self.formatting.colour_code_1)
        tk.Label(product_wizard_frame,
                 text="Step 1: Find or Add Product",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=step_1_title_colour).grid(row=0, column=0, sticky=tk.W, pady=5, padx=10, columnspan=2)
        if confirmed_product:
            tk.Label(product_wizard_frame,
                     text="Selected Product: " + confirmed_product[0],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=1, column=0, sticky=tk.W, padx=10)
        if product_frame_active:
            tk.Label(product_wizard_frame,
                     text="First search the database to see if the product you are trying to add to inventory "
                          "already exists. If not, the product will have to be added to the database to proceed.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=1, column=0, sticky=tk.W, padx=10, columnspan=2)
            product_search_entry = tk.Entry(product_wizard_frame)
            product_search_entry.config(font=self.formatting.medium_step_font)
            if product_search_results:
                product_search_entry.insert(tk.END, product_search_results[2])
            product_search_entry.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10, columnspan=2)
            tk.Button(product_wizard_frame,
                      text="Search Name",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.search_products_and_reload_wizard(
                          product_search_entry.get(),
                          manual_wizard_popup,
                          name_search=True)).grid(
                row=3, column=0, sticky=tk.W, padx=10, pady=5
            )
            tk.Button(product_wizard_frame,
                      text="Search Product ID",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.search_products_and_reload_wizard(
                          product_search_entry.get(),
                          manual_wizard_popup)).grid(
                row=4, column=0, sticky=tk.W, padx=10, pady=5
            )
            if product_search_results:
                if len(product_search_results[0]) > 0:
                    product_search_results_value = tk.StringVar()
                    product_search_results_menu = tk.OptionMenu(product_wizard_frame,
                                                                product_search_results_value,
                                                                *product_search_results[0],)
                    product_search_results_menu.config(highlightbackground=self.formatting.colour_code_1)
                    product_search_results_menu.config(font=self.formatting.medium_step_font,
                                                       width=45,
                                                       justify=tk.LEFT)
                    product_search_results_value.set(product_search_results[0][0])
                    product_search_results_menu.grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
                    tk.Button(product_wizard_frame,
                              text="Select Product",
                              font=self.formatting.medium_step_font,
                              command=lambda: self.select_existing_product_and_reload_wizard(
                                  (product_search_results_value.get(),
                                   product_search_results[1][product_search_results_value.get()]),
                                  manual_wizard_popup)
                              ).grid(
                        row=6, column=0, sticky=tk.W, padx=10, pady=5)
                else:
                    tk.Label(product_wizard_frame,
                             text="No results found! use button below to add new product.",
                             font=self.formatting.medium_step_font,
                             bg=self.formatting.colour_code_1,
                             fg=self.formatting.colour_code_2,
                             wraplength=600,
                             justify=tk.LEFT
                             ).grid(row=5, column=0, sticky=tk.W, padx=10, columnspan=2)
                    tk.Button(product_wizard_frame,
                              text="Add New Product",
                              font=self.formatting.medium_step_font,
                              command=lambda: print("add new product")).grid(
                        row=6, column=0, sticky=tk.W, padx=10, pady=5)
            else:
                tk.Label(product_wizard_frame,
                         text="Search results will display here.",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_2,
                         wraplength=600,
                         justify=tk.LEFT
                         ).grid(row=5, column=0, sticky=tk.W, padx=10, columnspan=2)
        product_wizard_frame.grid(row=2, column=0, pady=5, sticky=tk.W)
        # Product Request and Order Code
        if request_and_order_frame_active:
            step_2_title_colour = self.formatting.colour_code_purple
        else:
            step_2_title_colour = self.formatting.colour_code_3
        request_and_order_wizard_frame = tk.Frame(manual_wizard_popup)
        request_and_order_wizard_frame.config(bg=self.formatting.colour_code_1)
        tk.Label(request_and_order_wizard_frame,
                 text="Step 2: Add Request and Ordering Info",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=step_2_title_colour).grid(row=0, column=0, sticky=tk.W, pady=5, padx=10, columnspan=6)
        if confirmed_req_and_order_info:
            request_info = confirmed_req_and_order_info[0]
            amount_of_units = request_info[3] + " Units requested,"
            if len(request_info[3]) == 0:
                amount_of_units = "unknown amount requested."
            request_year = request_info[0]
            request_month = request_info[1]
            request_day = request_info[2]
            if len(request_year) == 0 and len(request_month) == 0 and len(request_day) == 0:
                request_date = " Unknown date of request."
            else:
                request_date = " on " + self.formatting.lab_date_format(request_year + "-" + request_month + "-" + request_day)
            tk.Label(request_and_order_wizard_frame,
                     text=amount_of_units + request_date,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=1, column=0, sticky=tk.W, padx=10, columnspan=6)
            order_info = confirmed_req_and_order_info[1]
            amount_of_units = order_info[3] + " Units ordered,"
            if len(order_info[3]) == 0:
                amount_of_units = "unknown amount ordered."
            order_year = order_info[0]
            order_month = order_info[1]
            order_day = order_info[2]
            if len(order_year) == 0 and len(order_month) == 0 and len(order_day) == 0:
                order_date = " Unknown date of order."
            else:
                order_date = " on " + self.formatting.lab_date_format(
                    order_year + "-" + order_month + "-" + order_day)
            tk.Label(request_and_order_wizard_frame,
                     text=amount_of_units + order_date,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=2, column=0, sticky=tk.W, padx=10, columnspan=6)
        if request_and_order_frame_active:
            tk.Label(request_and_order_wizard_frame,
                     text="Enter as much information as you know. If you don't know something, leave"
                          " It blank, and it will be assigned a default value (Default values: request/"
                          "order amount = inventory amount in step 3, request/order date = today's date)",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=1, column=0, sticky=tk.W, padx=10, columnspan=6)
            tk.Label(request_and_order_wizard_frame,
                     text="Request Date",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10, columnspan=2)
            request_date_entry_year = tk.Entry(request_and_order_wizard_frame)
            request_date_entry_year.config(width=4, font=self.formatting.medium_step_font)
            tk.Label(request_and_order_wizard_frame,
                     text="YYYY",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=3, column=0, sticky=tk.W, padx=10)
            request_date_entry_year.grid(row=3, column=1, sticky=tk.W)
            request_date_entry_month = tk.Entry(request_and_order_wizard_frame)
            request_date_entry_month.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(request_and_order_wizard_frame,
                     text="MM",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=600,
                     justify=tk.LEFT
                     ).grid(row=4, column=0, sticky=tk.W, padx=10)
            request_date_entry_month.grid(row=4, column=1, sticky=tk.W)
            request_date_entry_day = tk.Entry(request_and_order_wizard_frame)
            request_date_entry_day.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(request_and_order_wizard_frame,
                     text="DD",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=5, column=0, sticky=tk.W, padx=10)
            request_date_entry_day.grid(row=5, column=1, sticky=tk.W)
            tk.Label(request_and_order_wizard_frame,
                     text="Request Amount:",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
            request_amount_entry = tk.Entry(request_and_order_wizard_frame)
            request_amount_entry.config(width=4, font=self.formatting.medium_step_font)
            request_amount_entry.grid(row=6, column=1, pady=10, sticky=tk.W)
            tk.Label(request_and_order_wizard_frame,
                     text="Order Date",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=2, column=2, sticky=tk.W, padx=10, pady=10, columnspan=2)
            order_date_entry_year = tk.Entry(request_and_order_wizard_frame)
            order_date_entry_year.config(width=4, font=self.formatting.medium_step_font)
            tk.Label(request_and_order_wizard_frame,
                     text="YYYY",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=3, column=2, sticky=tk.W, padx=10)
            order_date_entry_year.grid(row=3, column=3, sticky=tk.W)
            order_date_entry_month = tk.Entry(request_and_order_wizard_frame)
            order_date_entry_month.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(request_and_order_wizard_frame,
                     text="MM",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=4, column=2, sticky=tk.W, padx=10)
            order_date_entry_month.grid(row=4, column=3, sticky=tk.W)
            order_date_entry_day = tk.Entry(request_and_order_wizard_frame)
            order_date_entry_day.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(request_and_order_wizard_frame,
                     text="DD",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=5, column=2, sticky=tk.W, padx=10)
            order_date_entry_day.grid(row=5, column=3, sticky=tk.W)
            tk.Label(request_and_order_wizard_frame,
                     text="Order Amount:",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=6, column=2, sticky=tk.W, padx=10, pady=10)
            order_amount_entry = tk.Entry(request_and_order_wizard_frame)
            order_amount_entry.config(width=4, font=self.formatting.medium_step_font)
            order_amount_entry.grid(row=6, column=3, pady=10, sticky=tk.W)
            tk.Button(request_and_order_wizard_frame,
                      text="Submit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.step_two_to_step_three_in_wizard(confirmed_product,
                                                                            manual_wizard_popup,
                                                                            (request_date_entry_year.get(),
                                                                             request_date_entry_month.get(),
                                                                             request_date_entry_day.get(),
                                                                             request_amount_entry.get()),
                                                                            (order_date_entry_year.get(),
                                                                             order_date_entry_month.get(),
                                                                             order_date_entry_day.get(),
                                                                             order_amount_entry.get()),
                                                                            request_and_order_wizard_frame)
                      ).grid(
                row=7, column=0, sticky=tk.W, padx=10, pady=5)
        request_and_order_wizard_frame.grid(row=3, column=0, pady=5, sticky=tk.W)
        # Product Receiving and Inventory Code
        if receiving_and_inventory_frame_active:
            step_3_title_colour = self.formatting.colour_code_purple
        else:
            step_3_title_colour = self.formatting.colour_code_3
        receiving_and_inventory_wizard_frame = tk.Frame(manual_wizard_popup)
        receiving_and_inventory_wizard_frame.config(bg=self.formatting.colour_code_1)
        tk.Label(receiving_and_inventory_wizard_frame,
                 text="Step 3: Add Receiving and Inventory Info",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=step_3_title_colour).grid(row=0, column=0, sticky=tk.W, pady=5, padx=10, columnspan=6)
        if confirmed_rec_and_inv_info:
            receiving_info = confirmed_rec_and_inv_info[0]
            lot_number = "lot No: " + receiving_info[0] + ","
            if len(receiving_info[0]) == 0:
                lot_number = "No lot number,"
            model = " Model: " + receiving_info[1] + ","
            if len(receiving_info[1]) == 0:
                model = " No Model,"
            serial_number = " Serial No: " + receiving_info[2] + ","
            if len(receiving_info[2]) == 0:
                serial_number = " No Serial #,"
            expiry_year = receiving_info[3]
            expiry_month = receiving_info[4]
            expiry_day = receiving_info[5]
            if len(expiry_year) == 0 and len(expiry_month) == 0 and len(expiry_day) == 0:
                expiry_date = " No Expiry."
            else:
                expiry_date = " Expires on: " +\
                              self.formatting.lab_date_format(expiry_year + "-" + expiry_month + "-" + expiry_day)
            recv_year = receiving_info[6]
            recv_month = receiving_info[7]
            recv_day = receiving_info[8]
            if len(recv_year) == 0 and len(recv_month) == 0 and len(recv_day) == 0:
                recv_date = " No Receive date."
            else:
                recv_date = " Received on: " +\
                              self.formatting.lab_date_format(recv_year + "-" + recv_month + "-" + recv_day)
            received_units = receiving_info[9]
            if len(received_units) == 0:
                received_units = " Unknown Amount Received."
            receiving_label = lot_number + model + serial_number + expiry_date + received_units + recv_date
            inventory_info = confirmed_rec_and_inv_info[1]
            full_units_remaining = inventory_info[0]
            partial_units_remaining = inventory_info[1]
            if len(full_units_remaining) == 0:
                full_units_remaining = "0"
            if len(partial_units_remaining) == 0:
                partial_units_remaining = "0"
            inventory_label = "Full Units: " + full_units_remaining +\
                              ". Partial Units: " + partial_units_remaining + "."
            tk.Label(receiving_and_inventory_wizard_frame,
                     text=receiving_label,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2,
                     wraplength=600,
                     justify=tk.LEFT).grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text=inventory_label,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=2, column=0, sticky=tk.W, pady=5, padx=10)
        if receiving_and_inventory_frame_active:
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Receiving Information",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=2, column=0, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Lot Number: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=3, column=0, sticky=tk.W, pady=5, padx=10)
            lot_number_entry = tk.Entry(receiving_and_inventory_wizard_frame)
            lot_number_entry.config(font=self.formatting.medium_step_font)
            lot_number_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Model: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=4, column=0, sticky=tk.W, pady=5, padx=10)
            model_number_entry = tk.Entry(receiving_and_inventory_wizard_frame)
            model_number_entry.config(font=self.formatting.medium_step_font)
            model_number_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Serial Number: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=5, column=0, sticky=tk.W, pady=5, padx=10)
            serial_number_entry = tk.Entry(receiving_and_inventory_wizard_frame)
            serial_number_entry.config(font=self.formatting.medium_step_font)
            serial_number_entry.grid(row=5, column=1, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Received Units: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=6, column=0, sticky=tk.W, pady=5, padx=10)
            received_units_entry = tk.Entry(receiving_and_inventory_wizard_frame)
            received_units_entry.config(font=self.formatting.medium_step_font)
            received_units_entry.grid(row=6, column=1, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Inventory Information",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=7, column=0, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Full Units: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=8, column=0, sticky=tk.W, pady=5, padx=10)
            full_units_entry = tk.Entry(receiving_and_inventory_wizard_frame)
            full_units_entry.config(font=self.formatting.medium_step_font)
            full_units_entry.grid(row=8, column=1, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Opened Units: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(row=9, column=0, sticky=tk.W, pady=5, padx=10)
            partial_units_entry = tk.Entry(receiving_and_inventory_wizard_frame)
            partial_units_entry.config(font=self.formatting.medium_step_font)
            partial_units_entry.grid(row=9, column=1, sticky=tk.W, pady=5, padx=10)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Expiry Date",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=3, column=2, sticky=tk.W, padx=10, pady=10, columnspan=2)
            expiry_date_entry_year = tk.Entry(receiving_and_inventory_wizard_frame)
            expiry_date_entry_year.config(width=4, font=self.formatting.medium_step_font)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="YYYY",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=4, column=2, sticky=tk.W, padx=10)
            expiry_date_entry_year.grid(row=4, column=3, sticky=tk.W)
            expiry_date_entry_month = tk.Entry(receiving_and_inventory_wizard_frame)
            expiry_date_entry_month.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="MM",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=5, column=2, sticky=tk.W, padx=10)
            expiry_date_entry_month.grid(row=5, column=3, sticky=tk.W)
            expiry_date_entry_day = tk.Entry(receiving_and_inventory_wizard_frame)
            expiry_date_entry_day.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="DD",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=6, column=2, sticky=tk.W, padx=10)
            expiry_date_entry_day.grid(row=6, column=3, sticky=tk.W)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="Received Date",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=3, column=4, sticky=tk.W, padx=10, pady=10, columnspan=2)
            receive_date_entry_year = tk.Entry(receiving_and_inventory_wizard_frame)
            receive_date_entry_year.config(width=4, font=self.formatting.medium_step_font)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="YYYY",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=4, column=4, sticky=tk.W, padx=10)
            receive_date_entry_year.grid(row=4, column=5, sticky=tk.W)
            receive_date_entry_month = tk.Entry(receiving_and_inventory_wizard_frame)
            receive_date_entry_month.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="MM",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=5, column=4, sticky=tk.W, padx=10)
            receive_date_entry_month.grid(row=5, column=5, sticky=tk.W)
            receive_date_entry_day = tk.Entry(receiving_and_inventory_wizard_frame)
            receive_date_entry_day.config(width=2, font=self.formatting.medium_step_font)
            tk.Label(receiving_and_inventory_wizard_frame,
                     text="DD",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=6, column=4, sticky=tk.W, padx=10)
            receive_date_entry_day.grid(row=6, column=5, sticky=tk.W)
            tk.Button(receiving_and_inventory_wizard_frame,
                      text="Submit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.step_three_to_confirmation_popup_wizard(confirmed_product,
                                                                                   confirmed_req_and_order_info,
                                                                                   (lot_number_entry.get(),
                                                                                    model_number_entry.get(),
                                                                                    serial_number_entry.get(),
                                                                                    expiry_date_entry_year.get(),
                                                                                    expiry_date_entry_month.get(),
                                                                                    expiry_date_entry_day.get(),
                                                                                    receive_date_entry_year.get(),
                                                                                    receive_date_entry_month.get(),
                                                                                    receive_date_entry_day.get(),
                                                                                    received_units_entry.get()),
                                                                                   (full_units_entry.get(),
                                                                                    partial_units_entry.get()),
                                                                                   manual_wizard_popup,
                                                                                   receiving_and_inventory_wizard_frame)
                      ).grid(
                row=10, column=0, sticky=tk.W, padx=10, pady=5)
        receiving_and_inventory_wizard_frame.grid(row=4, column=0, pady=5, sticky=tk.W)
        # Confirmation and Location Code
        if confirm_and_location_active:
            confirm_title_colour = self.formatting.colour_code_purple
        else:
            confirm_title_colour = self.formatting.colour_code_3
        confirm_and_location_inventory_wizard_frame = tk.Frame(manual_wizard_popup)
        confirm_and_location_inventory_wizard_frame.config(bg=self.formatting.colour_code_1)
        tk.Label(confirm_and_location_inventory_wizard_frame,
                 text="Confirm Info and Assign Location",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=confirm_title_colour).grid(row=0, column=0, sticky=tk.W, pady=5, padx=10, columnspan=6)
        if confirm_and_location_active:
            tk.Label(confirm_and_location_inventory_wizard_frame,
                     text="Review the above information provided in Step 1, 2, and 3. If everything"
                          " is correct, select a location and press the confirm button. Use the refresh"
                          " sub-locations button to change sub-locations when selecting a location.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2,
                     wraplength=450,
                     justify=tk.LEFT
                     ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10, columnspan=6)
            # locations and sub-locations
            locations_dict = {}
            locations_list = []
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
                self.sub_locations_dict[item[2]] = item[0]
                sub_locations_list.append(item[2])
            locations_value = tk.StringVar(confirm_and_location_inventory_wizard_frame)
            self.sub_locations_value = tk.StringVar(confirm_and_location_inventory_wizard_frame)
            locations_menu = tk.OptionMenu(confirm_and_location_inventory_wizard_frame,
                                           locations_value,
                                           *locations_list,)
            locations_menu.config(highlightbackground=self.formatting.colour_code_1)
            locations_menu.config(font=self.formatting.medium_step_font)
            self.sub_locations_menu = tk.OptionMenu(confirm_and_location_inventory_wizard_frame,
                                                    self.sub_locations_value,
                                                    *sub_locations_list,)
            self.sub_locations_menu.config(highlightbackground=self.formatting.colour_code_1)
            self.sub_locations_menu.config(font=self.formatting.medium_step_font)
            tk.Button(confirm_and_location_inventory_wizard_frame,
                      text="Refresh Sub-Locations",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.refresh_sub_locations_on_inventory_window(
                          locations_dict[locations_value.get()],
                          confirm_and_location_inventory_wizard_frame,
                          wizard=True)).grid(
                row=3, column=1, sticky=tk.W, padx=10, pady=5)
            locations_value.set(locations_list[0])
            locations_menu.grid(row=2, column=0, sticky=tk.W, padx=10, columnspan=6)
            self.sub_locations_value.set(sub_locations_list[0])
            self.sub_locations_menu.grid(row=3, column=0, sticky=tk.W, padx=10, columnspan=6)
            tk.Button(confirm_and_location_inventory_wizard_frame,
                      text="Confirm All & Add Inventory Item",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.post_confirmation_record_assembler_for_wizard(
                          confirmed_product,
                          confirmed_req_and_order_info,
                          confirmed_rec_and_inv_info,
                          (locations_dict[locations_value.get()],
                           self.sub_locations_dict[self.sub_locations_value.get()]),
                          manual_wizard_popup
                      )).grid(
                row=4, column=0, sticky=tk.W, padx=10, pady=20)
        confirm_and_location_inventory_wizard_frame.grid(row=5, column=0, pady=5, sticky=tk.W)

    def post_confirmation_record_assembler_for_wizard(self,
                                                      confirmed_product,
                                                      confirmed_req_and_order_info,
                                                      confirmed_rec_and_inv_info,
                                                      location_information,
                                                      original_wizard_popup):
        price_id = self.post_confirmation_get_price_id(confirmed_product[1])
        request_date = self.post_confirmation_assemble_date_return_now_as_default(
            confirmed_req_and_order_info[0][0],
            confirmed_req_and_order_info[0][1],
            confirmed_req_and_order_info[0][2],)
        request_amount = self.post_confirmation_check_request_amount(
            confirmed_req_and_order_info[0][3],
            confirmed_rec_and_inv_info[1][0],
            confirmed_rec_and_inv_info[1][1])
        request_record = (confirmed_product[1],
                          self.active_user[0],
                          price_id,
                          request_date,
                          request_amount,
                          "Request made using inventory wizard.",
                          1,
                          1)
        self.post_confirmation_submit_record(request_record=request_record)
        latest_request_record = self.post_confirmation_get_latest_request_id(request_record=True)
        request_id = ""
        for item in latest_request_record:
            request_id = item[0]
        order_date = self.post_confirmation_assemble_date_return_now_as_default(
            confirmed_req_and_order_info[1][0],
            confirmed_req_and_order_info[1][1],
            confirmed_req_and_order_info[1][2],
            order_date=True)
        order_amount = self.post_confirmation_check_request_amount(
            confirmed_req_and_order_info[1][3],
            confirmed_rec_and_inv_info[1][0],
            confirmed_rec_and_inv_info[1][1],
            order_amount=True)
        order_record = (request_id, order_date, order_amount, "This order record made by wizard.", 1, 1)
        self.post_confirmation_submit_record(order_record=order_record)
        latest_order_record = self.post_confirmation_get_latest_request_id(order_record=True)
        order_id = ""
        for item in latest_order_record:
            order_id = item[0]
        received_date = self.post_confirmation_assemble_date_return_now_as_default(confirmed_rec_and_inv_info[0][6],
                                                                                   confirmed_rec_and_inv_info[0][7],
                                                                                   confirmed_rec_and_inv_info[0][8],
                                                                                   receive_date=True)
        expiry_date = self.post_confirmation_assemble_date_return_now_as_default(confirmed_rec_and_inv_info[0][3],
                                                                                 confirmed_rec_and_inv_info[0][4],
                                                                                 confirmed_rec_and_inv_info[0][5],
                                                                                 expiry_date=True)
        received_amount = self.post_confirmation_check_request_amount(confirmed_rec_and_inv_info[0][9],
                                                                      confirmed_rec_and_inv_info[1][0],
                                                                      confirmed_rec_and_inv_info[1][1],
                                                                      received_amount=True)
        received_record = (order_id,
                           received_date,
                           received_amount,
                           confirmed_rec_and_inv_info[0][0],
                           expiry_date,
                           "",
                           confirmed_rec_and_inv_info[0][1],
                           confirmed_rec_and_inv_info[0][2],
                           "Received record made using inventory wizard.",
                           1,
                           1)
        self.post_confirmation_submit_record(received_record=received_record)
        latest_received_record = self.post_confirmation_get_latest_request_id(received_record=True)
        received_id = ""
        for item in latest_received_record:
            received_id = item[0]
        location_id = location_information[0]
        sub_location_id = location_information[1]
        if len(confirmed_rec_and_inv_info[1][0]) == 0:
            full_units_remaining = "0"
        else:
            full_units_remaining = confirmed_rec_and_inv_info[1][0]
        if len(confirmed_rec_and_inv_info[1][1]) == 0:
            partial_units_remaining = "0"
        else:
            partial_units_remaining = confirmed_rec_and_inv_info[1][1]
        inventory_record = (received_id,
                            location_id,
                            sub_location_id,
                            full_units_remaining,
                            partial_units_remaining,
                            datetime.date.today(),
                            self.active_user[0],
                            self.wizard_inventory_comment)
        self.post_confirmation_submit_record(inventory_record=inventory_record)
        original_wizard_popup.destroy()
        self.parent.display_inventory_view(
            self.active_user,
            sort_by=self.sort_by,
            search_by=self.search_by_active_term,
            search_by_variable=self.search_by_variable)

    def post_confirmation_submit_record(self,
                                        request_record=None,
                                        order_record=None,
                                        received_record=None,
                                        inventory_record=None):
        if request_record:
            self.add_delete_db.new_requests_record(request_record, wizard=True)
        if order_record:
            self.add_delete_db.new_orders_record(order_record, wizard=True)
        if received_record:
            self.add_delete_db.new_received_record(received_record, wizard=True)
        if inventory_record:
            self.add_delete_db.new_inventory_record(inventory_record)

    def post_confirmation_get_latest_request_id(self,
                                                request_record=None,
                                                order_record=None,
                                                received_record=None):
        if request_record:
            latest_id = self.select_db.select_one_from_table_order_by("requests",
                                                                      "id",
                                                                      descending_order=True)
            return latest_id
        if order_record:
            latest_id = self.select_db.select_one_from_table_order_by("orders",
                                                                      "id",
                                                                      descending_order=True)
            return latest_id
        if received_record:
            latest_id = self.select_db.select_one_from_table_order_by("received",
                                                                      "id",
                                                                      descending_order=True)
            return latest_id

    def post_confirmation_get_price_id(self,
                                       product_id):
        current_product_price =\
            self.select_db.select_one_from_table_where_field_equals_order_by("priceTracking",
                                                                             "products_id",
                                                                             product_id,
                                                                             "cost_date",
                                                                             descending_order=True)
        current_product_price_id = [item for item in current_product_price][0][0]
        return current_product_price_id

    def post_confirmation_assemble_date_return_now_as_default(self,
                                                              string_year,
                                                              string_month,
                                                              string_day,
                                                              order_date=False,
                                                              receive_date=False,
                                                              expiry_date=False):
        if len(string_year) == 0 and len(string_month) == 0 and len(string_day) == 0:
            if order_date:
                self.wizard_inventory_comment += "order date not provided, set to day record made.\n"
            elif receive_date:
                self.wizard_inventory_comment += "received date not provided, set to day record made.\n"
            elif expiry_date:
                self.wizard_inventory_comment += "expiry date not provided, set to day record made.\n"
            else:
                self.wizard_inventory_comment += "request date not provided, set to day record made.\n"
            return datetime.date.today()
        else:
            return datetime.date(int(string_year), int(string_month), int(string_day))

    def post_confirmation_check_request_amount(self,
                                               request_amount,
                                               full_units_remaining,
                                               partial_units_remaining,
                                               order_amount=False,
                                               received_amount=False):
        if len(request_amount) == 0:
            if order_amount:
                self.wizard_inventory_comment += \
                    "order amount not provided, set to sum of full and partial inv. units at time record made.\n"
            elif received_amount:
                self.wizard_inventory_comment += \
                    "received amount not provided, set to sum of full and partial inv. units at time record made.\n"
            else:
                self.wizard_inventory_comment += \
                    "request amount not provided, set to sum of full and partial inv. units at time record made.\n"
            if len(full_units_remaining) == 0:
                full_units_remaining = "0"
            if len(partial_units_remaining) == 0:
                partial_units_remaining = "0"
            return str(int(full_units_remaining)+int(partial_units_remaining))
        else:
            return request_amount

    def step_three_to_confirmation_popup_wizard(self,
                                                confirmed_product,
                                                confirmed_req_and_order_info,
                                                receiving_information,
                                                inventory_information,
                                                original_wizard_popup,
                                                receiving_and_inventory_frame):
        receive_amount_check = True
        if len(receiving_information[9]) > 0:
            receive_amount_check = self.error_handling.checkIfInt(receiving_information[9])
        receive_date_check = True
        if len(receiving_information[6]) > 0 or len(receiving_information[7]) > 0 or len(receiving_information[8]) > 0:
            receive_date_check = self.error_handling.checkYearMonthDayFormat(receiving_information[6],
                                                                             receiving_information[7],
                                                                             receiving_information[8])
        expiry_date_check = True
        if len(receiving_information[3]) > 0 or len(receiving_information[4]) > 0 or len(receiving_information[5]) > 0:
            expiry_date_check = self.error_handling.checkYearMonthDayFormat(receiving_information[3],
                                                                            receiving_information[4],
                                                                            receiving_information[5])
        inventory_values_check = True
        if len(inventory_information[0]) == 0 and len(inventory_information[1]) == 0:
            inventory_values_check = False
        full_units_check = True
        partial_units_check = True
        if len(inventory_information[0]) > 0:
            full_units_check = self.error_handling.checkIfInt(inventory_information[0])
        if len(inventory_information[1]) > 0:
            partial_units_check = self.error_handling.checkIfInt(inventory_information[1])
        if (receive_amount_check and receive_date_check and expiry_date_check and
           inventory_values_check and full_units_check and partial_units_check):
            self.manual_inventory_addition_wizard_popup(confirmed_product=confirmed_product,
                                                        confirmed_req_and_order_info=confirmed_req_and_order_info,
                                                        confirmed_rec_and_inv_info=(receiving_information,
                                                                                    inventory_information),
                                                        confirm_and_location_active=True)
            original_wizard_popup.destroy()
        else:
            tk.Label(receiving_and_inventory_frame,
                     font=self.formatting.medium_step_font,
                     text="Error with input information. Fix to proceed. At least 1 partial or full unit is required"
                          " for an inventory item, due to the way default values are assigned.",
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3,
                     wraplength=600).grid(
                row=11, column=0, sticky=tk.W, padx=10, pady=5, columnspan=5)

    def step_two_to_step_three_in_wizard(self,
                                         existing_product,
                                         original_wizard_popup,
                                         request_information,
                                         ordering_information,
                                         request_and_order_frame):
        request_date_check = True
        if len(request_information[0]) > 0 or len(request_information[1]) > 0 or len(request_information[2]) > 0:
            request_date_check = self.error_handling.checkYearMonthDayFormat(request_information[0],
                                                                             request_information[1],
                                                                             request_information[2])
        request_amount_check = True
        if len(request_information[3]) > 0:
            request_amount_check = self.error_handling.checkIfInt(request_information[3])
        order_date_check = True
        if len(ordering_information[0]) > 0 or len(ordering_information[1]) > 0 or len(ordering_information[2]) > 0:
            order_date_check = self.error_handling.checkYearMonthDayFormat(ordering_information[0],
                                                                           ordering_information[1],
                                                                           ordering_information[2])
        order_amount_check = True
        if len(ordering_information[3]) > 0:
            order_amount_check = self.error_handling.checkIfInt(ordering_information[3])
        if request_date_check and request_amount_check and order_date_check and order_amount_check:
            self.manual_inventory_addition_wizard_popup(confirmed_product=existing_product,
                                                        confirmed_req_and_order_info=(request_information,
                                                                                      ordering_information),
                                                        receiving_and_inventory_frame_active=True)
            original_wizard_popup.destroy()
        else:
            tk.Label(request_and_order_frame,
                     font=self.formatting.medium_step_font,
                     text="Error with input information. Fix to proceed.",
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=8, column=0, sticky=tk.W, padx=10, pady=5, columnspan=5)

    def select_existing_product_and_reload_wizard(self,
                                                  existing_product,
                                                  original_wizard_window):
        self.manual_inventory_addition_wizard_popup(confirmed_product=existing_product,
                                                    request_and_order_frame_active=True)
        original_wizard_window.destroy()

    def search_products_and_reload_wizard(self,
                                          value,
                                          original_wizard_window,
                                          name_search=False):
        product_search_list = []
        product_search_dict = {}
        if name_search:
            product_search_query_return = self.select_db.left_join_multiple_tables(
                "p.id, p.name, p.product_code, v.vendor_name, p.unit_of_issue",
                [["products p", "", "p.categories_id"],
                 ["categories c", "c.id", "p.vendors_id"],
                 ["vendors v", "v.id", "p.sub_categories_id"],
                 ["sub_categories sc", "sc.id", '']],
                "p.name",
                search_by=["p.name", '%' + value + '%'])
        else:
            product_search_query_return = self.select_db.left_join_multiple_tables(
                "p.id, p.name, p.product_code, v.vendor_name, p.unit_of_issue",
                [["products p", "", "p.categories_id"],
                 ["categories c", "c.id", "p.vendors_id"],
                 ["vendors v", "v.id", "p.sub_categories_id"],
                 ["sub_categories sc", "sc.id", '']],
                "p.name",
                search_by=["p.product_code", '%' + value + '%'])
        for item in product_search_query_return:
            product_search_token = "(" + item[2] + ") " + item[1] + "\n Vendor: " + item[3] + " (" + item[4] + ")"
            product_search_dict[product_search_token] = item[0]
            product_search_list.append(product_search_token)
        self.manual_inventory_addition_wizard_popup(
            product_search_results=(
                product_search_list,
                product_search_dict,
                value),
            product_frame_active=True)
        original_wizard_window.destroy()

    def inventory_product_popup(self, inventory_item):
        inventory_product_popup = tk.Toplevel()
        inventory_product_popup.config(bg=self.formatting.colour_code_1)
        inventory_product_popup.geometry('600x850')
        tk.Label(inventory_product_popup,
                 text=inventory_item[0] + " (INV-" + str(inventory_item[18]) + ")",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 wraplength=400,
                 justify=tk.LEFT,
                 fg=self.formatting.colour_code_purple).grid(row=0, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(inventory_product_popup,
                 text="Product Information",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=1, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(inventory_product_popup,
                 text="Product Code:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=2, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[1],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=2, column=1, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Vendor:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=3, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[3],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=3, column=1, columnspan=3, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Unit of Issue:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=4, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[4],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=4, column=1, columnspan=5, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Lot Number:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[15],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=5, column=1, columnspan=5, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Serial Number:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=6, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[14],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=6, column=1, columnspan=5, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Model:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=7, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[13],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=7, column=1, columnspan=5, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Category:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=8, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[2],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=8, column=1, columnspan=5, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Timeline",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=9, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(inventory_product_popup,
                 text="Order Date:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=10, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[16],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=10, column=1, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Receive Date:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=11, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[5],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=11, column=1, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Expiry Date:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=12, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[12],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=12, column=1, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Inventory Information",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=13, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        tk.Label(inventory_product_popup,
                 text="Full Units Remaining:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=14, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[6],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=14, column=1, columnspan=5, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Partial Units Remaining:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=15, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[7],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=15, column=1, columnspan=5, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Location:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=16, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[8],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=16, column=1, sticky=tk.W)
        tk.Label(inventory_product_popup,
                 text="Sub-Location:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=17, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[9],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=17, column=1, sticky=tk.W, columnspan=3)
        tk.Label(inventory_product_popup,
                 text="Last Updated by:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=18, column=0, sticky=tk.W, padx=10)
        tk.Label(inventory_product_popup,
                 text=inventory_item[11] + " on " + inventory_item[10],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=18, column=1, sticky=tk.W, columnspan=5)
        tk.Label(inventory_product_popup,
                 text="Inventory Comments",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=19, column=0, columnspan=6, sticky=tk.W, pady=5, padx=10)
        received_notes = tk.Text(inventory_product_popup,
                                 height=8,
                                 width=60)
        received_notes.config(bg=self.formatting.colour_code_2)
        received_notes.config(state=tk.NORMAL)
        received_notes.insert(tk.END, inventory_item[17])
        received_notes.config(state=tk.DISABLED, wrap="word")
        received_notes.grid(row=20, column=0, columnspan=6, sticky=tk.W, padx=10)
        tk.Button(inventory_product_popup,
                  text="Edit Inventory Information",
                  font=self.formatting.medium_step_font,
                  command=lambda item=inventory_item: self.edit_inventoried_product_popup(
                      item,
                      inventory_product_popup
                  )).grid(
            row=21,
            column=0,
            columnspan=3,
            sticky=tk.W,
            padx=10,
            pady=5)

    def edit_inventoried_product_popup(self, inventory_item, inventory_item_popup):
        # Popup Info
        edit_inventory_product_popup = tk.Toplevel()
        edit_inventory_product_popup.config(bg=self.formatting.colour_code_1)
        edit_inventory_product_popup.geometry('500x700')
        # locations and sub-locations
        locations_dict = {}
        locations_list = []
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
            self.sub_locations_dict[item[2]] = item[0]
            sub_locations_list.append(item[2])
        locations_value = tk.StringVar(edit_inventory_product_popup)
        self.sub_locations_value = tk.StringVar(edit_inventory_product_popup)
        locations_menu = tk.OptionMenu(edit_inventory_product_popup,
                                       locations_value,
                                       *locations_list,)
        locations_menu.config(highlightbackground=self.formatting.colour_code_1)
        locations_menu.config(font=self.formatting.medium_step_font)
        self.sub_locations_menu = tk.OptionMenu(edit_inventory_product_popup,
                                                self.sub_locations_value,
                                                *sub_locations_list,)
        self.sub_locations_menu.config(highlightbackground=self.formatting.colour_code_1)
        self.sub_locations_menu.config(font=self.formatting.medium_step_font)
        # Amount Remaining Information
        tk.Label(edit_inventory_product_popup,
                 text="Editing Inventory",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_inventory_product_popup,
                 text="INV-" + str(inventory_item[18]),
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_purple).grid(
            row=0, column=1, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_inventory_product_popup,
                 text="Edit Amounts Information",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_inventory_product_popup,
                 text="Full Units Remaining",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=2, column=0, sticky=tk.W, padx=10)
        full_units_remaining_entry = tk.Entry(edit_inventory_product_popup)
        full_units_remaining_entry.grid(row=2, column=1, sticky=tk.W, padx=10)
        full_units_remaining_entry.insert(tk.END, inventory_item[6])
        tk.Label(edit_inventory_product_popup,
                 text="Partial Units Remaining",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=10)
        partial_units_remaining_entry = tk.Entry(edit_inventory_product_popup)
        partial_units_remaining_entry.grid(row=3, column=1, sticky=tk.W, padx=10)
        partial_units_remaining_entry.insert(tk.END, inventory_item[7])
        tk.Label(edit_inventory_product_popup,
                 text="Edit Location Information",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        tk.Label(edit_inventory_product_popup,
                 text="Main Location:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10)
        locations_value.set(locations_list[0])
        locations_menu.grid(row=5, column=1, sticky=tk.W, padx=10)
        tk.Label(edit_inventory_product_popup,
                 text="Sub Location:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=6, column=0, sticky=tk.W, padx=10)
        self.sub_locations_value.set(sub_locations_list[0])
        self.sub_locations_menu.grid(row=6, column=1, sticky=tk.W, padx=10)
        tk.Button(edit_inventory_product_popup,
                  text="Refresh Sub-Locations",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.refresh_sub_locations_on_inventory_window(
                      locations_dict[locations_value.get()],
                      edit_inventory_product_popup)).grid(
            row=7, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(edit_inventory_product_popup,
                 text="Inventory Comments",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=5, padx=10)
        inventory_notes = tk.Text(edit_inventory_product_popup,
                                  height=5,
                                  width=40)
        inventory_notes.config(bg=self.formatting.colour_code_2)
        inventory_notes.config(state=tk.NORMAL)
        inventory_notes.insert(tk.END, inventory_item[17])
        inventory_notes.grid(row=9, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_inventory_product_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda item=inventory_item: self.check_edits_and_commit_changes_to_inventory_product(
                      item[18],
                      full_units_remaining_entry.get(),
                      partial_units_remaining_entry.get(),
                      locations_dict[locations_value.get()],
                      self.sub_locations_dict[self.sub_locations_value.get()],
                      inventory_notes.get("1.0", tk.END),
                      edit_inventory_product_popup,
                      inventory_item_popup
                  )).grid(
            row=10,
            column=0,
            columnspan=3,
            sticky=tk.W,
            padx=10,
            pady=5)

    def check_edits_and_commit_changes_to_inventory_product(self,
                                                            inventory_id,
                                                            full_units_remaining,
                                                            partial_units_remaining,
                                                            location_id,
                                                            sub_location_id,
                                                            comments,
                                                            edit_popup_window,
                                                            inventory_popup_window):
        full_units_int_check = self.error_handling.checkIfInt(full_units_remaining)
        partial_units_int_check = self.error_handling.checkIfInt(partial_units_remaining)
        if full_units_int_check and partial_units_int_check:
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "full_units_remaining",
                                                             full_units_remaining,
                                                             inventory_id)
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "partial_units_remaining",
                                                             partial_units_remaining,
                                                             inventory_id)
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "location_id",
                                                             location_id,
                                                             inventory_id)
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "sub_location_id",
                                                             sub_location_id,
                                                             inventory_id)
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "comments",
                                                             comments,
                                                             inventory_id)
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "sub_location_id",
                                                             sub_location_id,
                                                             inventory_id)
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "updated_user_id",
                                                             self.active_user[0],
                                                             inventory_id)
            self.edit_db.edit_one_record_one_field_one_table("inventory",
                                                             "last_updated",
                                                             datetime.date.today(),
                                                             inventory_id)
            inventory_popup_window.destroy()
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
                row=11,
                column=0,
                columnspan=3,
                sticky=tk.W,
                pady=5,
                padx=10)

    def archive_inventory_popup(self, product_to_delete):
        are_you_sure_logout_popup = tk.Toplevel()
        are_you_sure_logout_popup.config(bg=self.formatting.colour_code_1)
        are_you_sure_logout_popup.geometry('600x90')
        tk.Label(are_you_sure_logout_popup,
                 text="Are you sure you want to archive this inventory item?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        yes_i_am = tk.Button(are_you_sure_logout_popup,
                             text="Yes",
                             font=self.formatting.medium_step_font,
                             command=lambda: self.destroy_popup_archive_inventory_and_reload(
                                 product_to_delete,
                                 are_you_sure_logout_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)
        no_i_aint = tk.Button(are_you_sure_logout_popup,
                              text="No",
                              font=self.formatting.medium_step_font,
                              command=lambda: are_you_sure_logout_popup.destroy()).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    def destroy_popup_archive_inventory_and_reload(self, product_to_archive, top_level_window):
        self.edit_db.archive_entry_in_table_by_id("inventory", product_to_archive[18])
        self.parent.display_inventory_view(self.active_user,
                                           sort_by=self.sort_by,
                                           search_by=self.search_by_active_term,
                                           search_by_variable=self.search_by_variable)
        top_level_window.destroy()

    def refresh_sub_locations_on_inventory_window(self,
                                                  new_location,
                                                  inventory_popup,
                                                  wizard=False):
        self.sub_locations_menu.destroy()
        sub_locations_list = []
        self.sub_locations_value = tk.StringVar(inventory_popup)
        sub_locations = self.select_db.select_all_from_table_where_one_field_equals(
            "inventorySubLocations",
            "locations_id",
            new_location,)
        for item in sub_locations:
            self.sub_locations_dict[item[2]] = item[0]
            sub_locations_list.append(item[2])
        self.sub_locations_menu = tk.OptionMenu(inventory_popup,
                                                self.sub_locations_value,
                                                *sub_locations_list,)
        self.sub_locations_menu.config(highlightbackground=self.formatting.colour_code_1)
        self.sub_locations_menu.config(font=self.formatting.medium_step_font)
        self.sub_locations_value.set(sub_locations_list[0])
        if wizard:
            self.sub_locations_menu.grid(row=3, column=0, sticky=tk.W, padx=10)
        else:
            self.sub_locations_menu.grid(row=6, column=1, sticky=tk.W, padx=10)

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
