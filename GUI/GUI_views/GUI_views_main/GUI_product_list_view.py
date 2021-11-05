import tkinter as tk
import datetime
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_errorHandling as tk_errorHandling


class ProductListView(tk.Frame):
    """user interface for the products contained in the RoverResourcesDatabase. Functionality of page dependent on
    user credentials.

    Attributes
    ----------

    parent : tk.Frame
        the parent frame, which in this instance is GUI_main_view.py.

    active_user : tuple
        the active user tuple, in the form (credentials ID, username, password, comments)

    formatting : object
        formatting Tkinter methods from GUI_formatting.py

    select_db : object
        selection SQL methods from dB_select.py

    add_delete_db : object
        adding and deleting SQL methods from dB_add_delete.py

    edit_db : object
        editing SQL methods from dB_edit.py

    products_list : tuple
        the returned products list, the result of a left join of products, categories, vendors, and sub-categories.
        Currently only accessing the priceTracking table when an individual product is opened.

    products_list_navigation_frame : tk.Frame
        the frame that holds the scrollable products list container and canvas.

    products_list_scrollable_container : tk.Frame
        the frame that holds the frame containing the labels that make up the scrollable products list.

    products_list_frame : tk.Frame
        the frame that holds the actual widgets making up the scrollable products list.

    sub_categories_menu : string
        placeholder for the sub categories menu, so it can be refreshed when a category is changed in the new product
        pop-up.

    sub_categories_value : basestring
        placeholder for the sub categories value, so it can be refreshed when a category is changed in the new product
        pop-up.

    """
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ()
        # GUI Formatting
        self.formatting = tk_formatting.TkFormattingMethods()
        self.error_handling = tk_errorHandling.ErrorHandling()
        # SQL methods
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        # Product List View Variables
        self.products_list = ()
        self.config(bg=self.formatting.colour_code_1)
        self.products_list_navigation_frame = tk.Frame(self)
        self.products_list_scrollable_container = tk.Frame(self)
        self.products_list_frame = tk.Frame(self)
        self.products_list_frame.config(bg=self.formatting.colour_code_1)
        self.products_list_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.sub_categories_menu = ""
        self.sub_categories_value = ""
        self.products_list_canvas_length = 0
        self.product_list_view_by = ["Product Name",
                                     "Product Code",
                                     "Vendor Name",
                                     "Product Category",
                                     "Product Sub-Category",
                                     "Approved Status"]
        self.product_list_sort_value = tk.StringVar(self)
        self.product_list_sort_value.set("Product Name")
        self.sort_by_shopping_cart_conversion_dictionary = {"Product Code": "p.product_code",
                                                            "Vendor Name": "v.vendor_name",
                                                            "Product Category": "c.category_name",
                                                            "Product Sub-Category":
                                                                "c.category_name, sc.sub_category_name",
                                                            "Product Name": "p.name",
                                                            "Approved Status": "p.approved"}
        # Error Handling
        self.historicalDateFailLabel = tk.Label()
        self.editDateFailLabel = tk.Label()

    # MAIN METHODS ####################################################################################################

    def products_list_view(self, user, sort_by=False, search_by=False):
        """ Sets the method active user variable to the one that was passed from GUI_main_view.py, then starts the main
        method for the Product List View, create products list.

        Parameters
        ----------

        user : tuple
            tuple in the form (credential ID, user name, user password, comments).
        """
        self.active_user = user
        self.create_products_list(sort_by=sort_by, search_by=search_by)

    def create_products_list(self, sort_by=False, search_by=False):
        """First creates the products list navigation frame, which allows the user to interact with the view. Then gets
        all the products from the database. Makes the headers for the scrollable products list, and then populates it
        with the results from the products list query. Finally generates the canvas and scrollbar containing the info.
        """
        self.create_products_list_navigation_frame()
        self.get_products_list_from_database(sort_by=sort_by, search_by=search_by)
        self.make_scrollable_products_list_header_labels()
        self.populate_scrollable_products_list()
        self.create_scrollable_products_list()
        self.products_list_navigation_frame.grid(sticky=tk.W, pady=10)
        self.products_list_scrollable_container.grid()

    # CREATE PRODUCTS LIST METHODS ####################################################################################

    def create_products_list_navigation_frame(self):
        tk.Label(self.products_list_navigation_frame,
                 text="Products List",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        if self.active_user[1] == 1:
            tk.Button(self.products_list_navigation_frame,
                      text="Add New Product",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.new_product_popup()).grid(row=0,
                                                                     column=1,
                                                                     sticky=tk.W,
                                                                     padx=10,
                                                                     pady=5)
        else:
            tk.Button(self.products_list_navigation_frame,
                      text="Request New Product",
                      font=self.formatting.medium_step_font,
                      command=lambda:self.new_product_popup(request=True)).grid(row=0,
                                                                                column=1,
                                                                                sticky=tk.W,
                                                                                padx=10,
                                                                                pady=5)
        type_of_sort_menu = tk.OptionMenu(self.products_list_navigation_frame,
                                          self.product_list_sort_value,
                                          *self.product_list_view_by)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        tk.Label(self.products_list_navigation_frame,
                 text="Sort:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=2, sticky=tk.W, pady=5)
        type_of_sort_menu.grid(row=0, column=3, sticky=tk.W, pady=5)
        sort_by_button = tk.Button(self.products_list_navigation_frame,
                                   text="Sort",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_products_list_view(
                                       self.active_user,
                                       sort_by=self.product_list_sort_value.get())).grid(
            row=0, column=4, sticky=tk.W, padx=10, pady=5
        )
        tk.Label(self.products_list_navigation_frame,
                 text="Search:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=5, sticky=tk.W, pady=5)
        product_search_entry = tk.Entry(self.products_list_navigation_frame)
        product_search_entry.grid(row=0, column=6, sticky=tk.W, pady=5)
        search_by_button = tk.Button(self.products_list_navigation_frame,
                                     text="Search Name",
                                     font=self.formatting.medium_step_font,
                                     command=lambda: self.parent.display_products_list_view(
                                       self.active_user,
                                       search_by=product_search_entry.get())).grid(
            row=0, column=7, sticky=tk.W, padx=10, pady=5
        )
        tk.Button(self.products_list_navigation_frame,
                  text="All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_products_list_view(
                      self.active_user)).grid(
            row=0, column=8, sticky=tk.W, padx=10, pady=5
        )

    def get_products_list_from_database(self, sort_by=None, search_by=None):
        if sort_by:
            sort_by_variable = self.sort_by_shopping_cart_conversion_dictionary[sort_by]
            self.product_list_sort_value.set(sort_by)
            self.products_list = self.select_db.left_join_multiple_tables(
                "p.id, p.name, p.product_code, v.vendor_name, c.category_name, sc.sub_category_name, p.comments,"
                " p.categories_id, p.sub_categories_id, p.unit_of_issue, p.approved",
                [["products p", "", "p.categories_id"],
                 ["categories c", "c.id", "p.vendors_id"],
                 ["vendors v", "v.id", "p.sub_categories_id"],
                 ["sub_categories sc", "sc.id", '']],
                sort_by_variable,
                no_archive="p.archived")
        elif search_by:
            self.products_list = self.select_db.left_join_multiple_tables(
                "p.id, p.name, p.product_code, v.vendor_name, c.category_name, sc.sub_category_name, p.comments,"
                " p.categories_id, p.sub_categories_id, p.unit_of_issue, p.approved",
                [["products p", "", "p.categories_id"],
                 ["categories c", "c.id", "p.vendors_id"],
                 ["vendors v", "v.id", "p.sub_categories_id"],
                 ["sub_categories sc", "sc.id", '']],
                "p.name",
                no_archive="p.archived",
                search_by=["p.name", '%' + search_by + '%'])
        else:
            self.products_list = self.select_db.left_join_multiple_tables(
                "p.id, p.name, p.product_code, v.vendor_name, c.category_name, sc.sub_category_name, p.comments,"
                " p.categories_id, p.sub_categories_id, p.unit_of_issue, p.approved",
                [["products p", "", "p.categories_id"],
                 ["categories c", "c.id", "p.vendors_id"],
                 ["vendors v", "v.id", "p.sub_categories_id"],
                 ["sub_categories sc", "sc.id", '']],
                "p.name",
                no_archive="p.archived",)

    def create_scrollable_products_list(self):
        products_list_canvas = tk.Canvas(self.products_list_scrollable_container,
                                         width=1200,
                                         height=550,
                                         scrollregion=(0, 0, 0, self.products_list_canvas_length),
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
        product_category_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                              "Sub-Category",
                                                                              self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_category_header, 0, 5)
        product_unit_issue_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                "Units",
                                                                                self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_unit_issue_header, 0, 6)
        product_approved_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                              "Approved?",
                                                                              self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_approved_header, 0, 7)

    def populate_scrollable_products_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.products_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            product_name_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                             item[1],
                                                                             text_color)
            self.formatting.grid_shopping_cart_labels(product_name_label, row_counter, 1)
            product_id_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                           item[2],
                                                                           text_color)
            self.formatting.grid_shopping_cart_labels(product_id_label, row_counter, 2)
            product_vendor_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                               item[3],
                                                                               text_color)
            self.formatting.grid_shopping_cart_labels(product_vendor_label, row_counter, 3)
            product_category_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                 item[4],
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
            product_unit_issue_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                   item[9],
                                                                                   text_color)
            self.formatting.grid_shopping_cart_labels(product_unit_issue_label, row_counter, 6)
            if str(item[10]) == "1":
                product_approved_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                     "Yes",
                                                                                     self.formatting.colour_code_green)
                self.formatting.grid_shopping_cart_labels(product_approved_label, row_counter, 7)
            else:
                product_approved_label = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                                     "No",
                                                                                     self.formatting.colour_code_red)
                self.formatting.grid_shopping_cart_labels(product_approved_label, row_counter, 7)
            if self.active_user[1] == 1:
                tk.Button(self.products_list_frame,
                          text="Open",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.individual_product_popup(item)).grid(row=row_counter,
                                                                                              column=8,
                                                                                              sticky=tk.W,
                                                                                              padx=10,
                                                                                              pady=5)
                tk.Button(self.products_list_frame,
                          text="Archive",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.delete_product_popup(item)).grid(row=row_counter,
                                                                                          column=9,
                                                                                          sticky=tk.W,
                                                                                          padx=10,
                                                                                          pady=5)
                if str(item[10]) == "0":
                    tk.Button(self.products_list_frame,
                              text="Approve",
                              font=self.formatting.medium_step_font,
                              command=lambda item=item: self.approve_product_request_and_reload_page(item)).grid(
                        row=row_counter,
                        column=10,
                        sticky=tk.W,
                        padx=10,
                        pady=5)
            else:
                tk.Button(self.products_list_frame,
                          text="View",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.individual_product_popup(item)).grid(row=row_counter,
                                                                                              column=8,
                                                                                              sticky=tk.W,
                                                                                              padx=10,
                                                                                              pady=5)
            self.products_list_canvas_length += 50
            row_counter += 1
            even_odd += 1

    # POPUPS #########################################################################################################

    # NEW PRODUCT TOP LEVEL POP-UP ###################################################################################

    def new_product_popup(self, request=False):
        new_product_popup = tk.Toplevel()
        new_product_popup.config(bg=self.formatting.colour_code_1)
        new_product_popup.geometry('600x400')
        product_name_entry = tk.Entry(new_product_popup)
        product_catalog_id_entry = tk.Entry(new_product_popup)
        unit_of_issue_entry = tk.Entry(new_product_popup)
        notes_entry = tk.Entry(new_product_popup)
        vendors_dict = {}
        categories_dict = {}
        sub_categories_dict = {}
        vendors_list = []
        categories_list = []
        sub_categories_list = []
        vendors = self.select_db.select_all_from_table("vendors")
        for item in vendors:
            vendors_dict[item[1]] = item[0]
            vendors_list.append(item[1])
        categories = self.select_db.select_all_from_table("categories")
        for item in categories:
            categories_dict[item[1]] = item[0]
            categories_list.append(item[1])
        sub_categories = self.select_db.select_all_from_table_where_one_field_equals(
            "sub_categories",
            "categories_id",
            categories_dict[categories_list[0]],)
        for item in sub_categories:
            sub_categories_dict[item[2]] = item[0]
            sub_categories_list.append(item[2])
        vendors_value = tk.StringVar(new_product_popup)
        categories_value = tk.StringVar(new_product_popup)
        self.sub_categories_value = tk.StringVar(new_product_popup)
        vendors_menu = tk.OptionMenu(new_product_popup,
                                     vendors_value,
                                     *vendors_list,)
        vendors_menu.config(highlightbackground=self.formatting.colour_code_1)
        vendors_menu.config(font=self.formatting.medium_step_font)
        categories_menu = tk.OptionMenu(new_product_popup,
                                        categories_value,
                                        *categories_list,)
        categories_menu.config(highlightbackground=self.formatting.colour_code_1)
        categories_menu.config(font=self.formatting.medium_step_font)
        self.sub_categories_menu = tk.OptionMenu(new_product_popup,
                                                 self.sub_categories_value,
                                                 *sub_categories_list,)
        self.sub_categories_menu.config(highlightbackground=self.formatting.colour_code_1)
        self.sub_categories_menu.config(font=self.formatting.medium_step_font)
        tk.Label(new_product_popup,
                 text="Product Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        product_name_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Label(new_product_popup,
                 text="Catalog No.",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)
        product_catalog_id_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Label(new_product_popup,
                 text="Vendor",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)
        vendors_value.set(vendors_list[0])
        vendors_menu.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Label(new_product_popup,
                 text="Category",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)
        categories_value.set(categories_list[0])
        categories_menu.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(new_product_popup,
                  text="Refresh Sub-Categories",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.refresh_sub_categories_on_new_product_window(
                      categories_dict[categories_value.get()],
                      new_product_popup)).grid(
            row=3, column=2, sticky=tk.W, padx=10, pady=10)
        tk.Label(new_product_popup,
                 text="Sub-Category",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=4, column=0, sticky=tk.W, padx=10, pady=10)
        self.sub_categories_value.set(sub_categories_list[0])
        self.sub_categories_menu.grid(row=4, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Label(new_product_popup,
                 text="Unit of Issue",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        unit_of_issue_entry.grid(row=5, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Label(new_product_popup,
                 text="Notes",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=6, column=0, sticky=tk.W, padx=10, pady=10)
        notes_entry.grid(row=6, column=1, sticky=tk.W, padx=10, pady=10)
        if request:
            tk.Button(new_product_popup,
                      text="Request New Product",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_product_close_popup_and_reload((categories_dict[categories_value.get()],
                                                                                   sub_categories_dict[
                                                                                   self.sub_categories_value.get()],
                                                                                   vendors_dict[vendors_value.get()],
                                                                                   product_catalog_id_entry.get(),
                                                                                   product_name_entry.get(),
                                                                                   unit_of_issue_entry.get(),
                                                                                   notes_entry.get(),
                                                                                   "0"),
                                                                                  new_product_popup,
                                                                                  request=True)).grid(
                row=7, column=0, sticky=tk.W, padx=10, pady=10)
        else:
            tk.Button(new_product_popup,
                      text="Add New Product",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_product_close_popup_and_reload((categories_dict[categories_value.get()],
                                                                                   sub_categories_dict[
                                                                                   self.sub_categories_value.get()],
                                                                                   vendors_dict[vendors_value.get()],
                                                                                   product_catalog_id_entry.get(),
                                                                                   product_name_entry.get(),
                                                                                   unit_of_issue_entry.get(),
                                                                                   notes_entry.get()),
                                                                                  new_product_popup)).grid(
                row=7, column=0, sticky=tk.W, padx=10, pady=10)

    # NEW PRODUCT POPUP METHODS

    def refresh_sub_categories_on_new_product_window(self, current_category, popup):
        self.sub_categories_menu.destroy()
        sub_categories_dict = {}
        sub_categories_list = []
        self.sub_categories_value = tk.StringVar(popup)
        sub_categories = self.select_db.select_all_from_table_where_one_field_equals(
            "sub_categories",
            "categories_id",
            current_category,)
        for item in sub_categories:
            sub_categories_dict[item[2]] = item[0]
            sub_categories_list.append(item[2])
        self.sub_categories_menu = tk.OptionMenu(popup,
                                                 self.sub_categories_value,
                                                 *sub_categories_list,)
        self.sub_categories_menu.config(highlightbackground=self.formatting.colour_code_1)
        self.sub_categories_menu.config(font=self.formatting.medium_step_font)
        self.sub_categories_value.set(sub_categories_list[0])
        self.sub_categories_menu.grid(row=4, column=1, sticky=tk.W, padx=10, pady=10)

    # INDIVIDUAL PRODUCT MAIN POPUP ##################################################################################

    def individual_product_popup(self, product):
        individual_product_popup = tk.Toplevel()
        product_frame = tk.Frame(individual_product_popup)
        pricing_frame = tk.Frame(individual_product_popup)
        individual_product_popup.config(bg=self.formatting.colour_code_1)
        product_frame.config(bg=self.formatting.colour_code_1)
        pricing_frame.config(bg=self.formatting.colour_code_3)
        individual_product_popup.geometry('820x650')
        product_pricing_list = self.select_db.select_all_from_table_where_one_field_equals_order_by(
            "priceTracking",
            "products_id",
            product[0],
            "cost_date",
            descending_order=True,
            no_archive=True,
            no_approved=True
        )
        product_pricing_list = [item for item in product_pricing_list]
        # PRODUCT FRAME WIDGETS
        product_info_label = tk.Label(product_frame,
                                      text="Product Information",
                                      font=self.formatting.homepage_window_select_button_font,
                                      bg=self.formatting.colour_code_1,
                                      fg=self.formatting.colour_code_3)
        self.formatting.grid_shopping_cart_labels(product_info_label, 0, 0)
        product_name = self.formatting.create_shopping_cart_labels(product_frame,
                                                                   product[1],
                                                                   self.formatting.colour_code_3)
        self.formatting.grid_shopping_cart_labels(product_name, 1, 0)
        catalog_id = self.formatting.create_shopping_cart_labels(product_frame,
                                                                 "Catalog: " + product[2],
                                                                 self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(catalog_id, 2, 0)
        vendor_name = self.formatting.create_shopping_cart_labels(product_frame,
                                                                  "Vendor: " + product[3],
                                                                  self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(vendor_name, 3, 0)
        category_name = self.formatting.create_shopping_cart_labels(product_frame,
                                                                    "Category: " + product[4],
                                                                    self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(category_name, 4, 0)
        if product[5] == "None":
            sub_category_name = self.formatting.create_shopping_cart_labels(product_frame,
                                                                            "No Sub Category",
                                                                            self.formatting.colour_code_2)
        else:
            sub_category_name = self.formatting.create_shopping_cart_labels(product_frame,
                                                                            "Sub Category: " + product[5],
                                                                            self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(sub_category_name, 5, 0)
        unit_of_issue = self.formatting.create_shopping_cart_labels(product_frame,
                                                                    "Unit of Issue: " + product[9],
                                                                    self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(unit_of_issue, 6, 0)
        product_notes = tk.Text(product_frame,
                                height=5,
                                width=40)
        product_notes.config(bg=self.formatting.colour_code_2)
        product_notes.config(state=tk.NORMAL)
        product_notes.insert(tk.END, product[6])
        product_notes.config(state=tk.DISABLED, wrap="word")
        product_notes.grid(row=7, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        if self.active_user[1] == 1:
            tk.Button(product_frame,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_product_name_unit_or_catalog_id_popup(product,
                                                                                      "name",
                                                                                      individual_product_popup)).grid(
                row=1, column=1, sticky=tk.W, padx=10, pady=10)
            tk.Button(product_frame,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_product_name_unit_or_catalog_id_popup(product,
                                                                                      "product_code",
                                                                                      individual_product_popup)).grid(
                row=2, column=1, sticky=tk.W, padx=10, pady=10)
            tk.Button(product_frame,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_product_vendor_or_category_popup(product,
                                                                                 "vendors",
                                                                                 individual_product_popup)).grid(
                row=3, column=1, sticky=tk.W, padx=10, pady=10)
            tk.Button(product_frame,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_product_vendor_or_category_popup(product,
                                                                                 "categories",
                                                                                 individual_product_popup)).grid(
                row=4, column=1, sticky=tk.W, padx=10, pady=10)
            tk.Button(product_frame,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_product_sub_category_popup(product,
                                                                           individual_product_popup)).grid(
                row=5, column=1, sticky=tk.W, padx=10, pady=10)
            tk.Button(product_frame,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_product_name_unit_or_catalog_id_popup(product,
                                                                                      "unit_of_issue",
                                                                                      individual_product_popup)).grid(
                row=6, column=1, sticky=tk.W, padx=10, pady=10)
            tk.Button(product_frame,
                      text="Edit Notes",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_notes_popup(product,
                                                            individual_product_popup)).grid(
                row=8, column=0, sticky=tk.W, padx=10, pady=10)
        # PRICING FRAME WIDGETS
        pricing_info_label = tk.Label(pricing_frame,
                                      text="Product Pricing",
                                      font=self.formatting.homepage_window_select_button_font,
                                      bg=self.formatting.colour_code_3,
                                      fg=self.formatting.colour_code_1).grid(
            row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        if self.active_user[1] == 1:
            tk.Button(pricing_frame,
                      text="Add New Price",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_price_popup(product, individual_product_popup)
                      ).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Button(pricing_frame,
                      text="Edit Prices",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_price_popup(product, product_pricing_list, individual_product_popup)
                      ).grid(row=1, column=1, sticky=tk.W, pady=5)
        try:
            tk.Label(pricing_frame,
                     text="Current Price: $" +
                          "{:.2f}".format(product_pricing_list[0][2]) +
                          " (Last Updated " + str(product_pricing_list[0][3]) + ")",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_3,
                     fg=self.formatting.colour_code_1).grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        except IndexError:
            tk.Label(pricing_frame,
                     text="No Price Set Yet.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_3,
                     fg=self.formatting.colour_code_1).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        price_history_textbox = tk.Text(pricing_frame,
                                        height=25,
                                        width=50)
        price_history_textbox.config(state=tk.NORMAL)
        price_history_textbox.insert(tk.END, "Price     | Date \n")
        price_history_textbox.insert(tk.END, "------------------------------\n")
        for item in product_pricing_list[1:]:
            price_history_textbox.insert(tk.END, ("{:.2f}".format(item[2]) + " "*(10-len(str(item[2]))) + "| " +
                                                  str(item[3]) +
                                                  "\n"))
        price_history_textbox.config(state=tk.DISABLED, wrap="word")
        price_history_textbox.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        product_frame.grid(row=0, column=0, sticky=tk.NW, padx=10, pady=10)
        pricing_frame.grid(row=0, column=1, sticky=tk.NW, padx=10, pady=10)

    # INDIVIDUAL PRODUCT SUB-POPUPS

    def edit_price_popup(self, product, product_pricing_list, individual_product_popup):
        product_pricing_list = [item for item in product_pricing_list]
        product_pricing_tk_dict = {}
        product_pricing_tk_list = []
        product_pricing_var = tk.StringVar()
        edit_prices_popup = tk.Toplevel()
        edit_prices_popup.config(bg=self.formatting.colour_code_1)
        edit_prices_popup.geometry('300x300')
        tk.Label(edit_prices_popup,
                 text="Edit Product Pricing",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        if len(product_pricing_list) == 0:
            tk.Label(edit_prices_popup,
                     text="No Prices have been set yet.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        else:
            for item in product_pricing_list:
                product_pricing_tk_dict["{:.2f}".format(float(item[2])) + " (" + str(item[3]) + ")"] = item[0]
                product_pricing_tk_list.append("{:.2f}".format(float(item[2])) + " (" + str(item[3]) + ")")
            product_pricing_var.set(product_pricing_tk_list[0])
            prices_menu = tk.OptionMenu(edit_prices_popup,
                                        product_pricing_var,
                                        *product_pricing_tk_list)
            prices_menu.config(highlightbackground=self.formatting.colour_code_1)
            prices_menu.config(font=self.formatting.medium_step_font)
            prices_menu.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Button(edit_prices_popup,
                      text="Archive Selected Price",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.destroy_popups_archive_price_and_reload(
                          product_pricing_tk_dict[product_pricing_var.get()],
                          edit_prices_popup,
                          individual_product_popup)).grid(
                row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
            tk.Button(edit_prices_popup,
                      text="Edit Selected Price",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_selected_price_popup(
                          product_pricing_tk_dict[product_pricing_var.get()],
                          edit_prices_popup,
                          individual_product_popup)).grid(
                row=3, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    def edit_selected_price_popup(self, price_id, edit_prices_popup, individual_product_popup):
        price_to_edit = self.select_db.select_one_from_table_where_field_equals("priceTracking", "id", price_id)
        edit_selected_price_popup = tk.Toplevel()
        edit_selected_price_popup.config(bg=self.formatting.colour_code_1)
        edit_selected_price_popup.geometry('275x325')
        for item in price_to_edit:
            price_entry = tk.Entry(edit_selected_price_popup)
            price_entry.insert(tk.END, "{:.2f}".format(float(item[2])))
            tk.Label(edit_selected_price_popup,
                     text="Edit Price",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(edit_selected_price_popup,
                     text="Price: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
            price_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(edit_selected_price_popup,
                     text="Edit Date",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)
            year_month_day = item[3].split("-")
            year_entry = tk.Entry(edit_selected_price_popup)
            year_entry.insert(tk.END, year_month_day[0])
            month_entry = tk.Entry(edit_selected_price_popup)
            month_entry.insert(tk.END, year_month_day[1])
            day_entry = tk.Entry(edit_selected_price_popup)
            day_entry.insert(tk.END, year_month_day[2])
            tk.Label(edit_selected_price_popup,
                     text="Year: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
            year_entry.grid(row=3, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(edit_selected_price_popup,
                     text="Month: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
            month_entry.grid(row=4, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(edit_selected_price_popup,
                     text="Day: ",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
            day_entry.grid(row=5, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Button(edit_selected_price_popup,
                      text="Commit Changes",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_valid_date_and_price_then_edit_price(price_id,
                                                                                      price_entry.get(),
                                                                                      year_entry.get(),
                                                                                      month_entry.get(),
                                                                                      day_entry.get(),
                                                                                      individual_product_popup,
                                                                                      edit_prices_popup,
                                                                                      edit_selected_price_popup)).grid(
                row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    def add_new_price_popup(self, product, individual_product_popup):
        add_new_price_popup = tk.Toplevel()
        add_new_price_popup.config(bg=self.formatting.colour_code_1)
        add_new_price_popup.geometry('300x200')
        price_entry = tk.Entry(add_new_price_popup)
        tk.Label(add_new_price_popup,
                 text="New Price: ",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2
                 ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        price_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Button(add_new_price_popup,
                  text="Add New Price",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.add_new_price_query_and_reload_products_page((product[0],
                                                                                     price_entry.get(),
                                                                                     datetime.date.today()),
                                                                                    individual_product_popup,
                                                                                    add_new_price_popup)
                  ).grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10)
        tk.Button(add_new_price_popup,
                  text="Add Historical Price",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.historical_price_popup(product[0],
                                                              price_entry.get(),
                                                              individual_product_popup,
                                                              add_new_price_popup)
                  ).grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    def historical_price_popup(self, product, price, individual_product_popup, add_new_price_popup):
        historical_price_popup = tk.Toplevel()
        historical_price_popup.config(bg=self.formatting.colour_code_1)
        historical_price_popup.geometry('400x200')
        year_entry = tk.Entry(historical_price_popup)
        month_entry = tk.Entry(historical_price_popup)
        day_entry = tk.Entry(historical_price_popup)
        tk.Label(historical_price_popup,
                 text="Year: ",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2
                 ).grid(row=0, column=0, sticky=tk.W, padx=10)
        year_entry.grid(row=0, column=1, sticky=tk.W, padx=10)
        tk.Label(historical_price_popup,
                 text="Month: ",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2
                 ).grid(row=1, column=0, sticky=tk.W, padx=10)
        month_entry.grid(row=1, column=1, sticky=tk.W, padx=10)
        tk.Label(historical_price_popup,
                 text="Day: ",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2
                 ).grid(row=2, column=0, sticky=tk.W, padx=10)
        day_entry.grid(row=2, column=1, sticky=tk.W, padx=10)
        tk.Button(historical_price_popup,
                  text="Add Historical Price",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.check_valid_historical_date_then_add_new_price(
                      product,
                      price,
                      year_entry.get(),
                      month_entry.get(),
                      day_entry.get(),
                      individual_product_popup,
                      add_new_price_popup,
                      historical_price_popup)).grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)

    def edit_notes_popup(self, product, individual_product_popup):
        edit_notes_popup = tk.Toplevel()
        edit_notes_popup.config(bg=self.formatting.colour_code_1)
        edit_notes_popup.geometry('500x160')
        product_notes = tk.Text(edit_notes_popup,
                                height=5,
                                width=40)
        product_notes.config(bg=self.formatting.colour_code_2)
        product_notes.config(state=tk.NORMAL)
        product_notes.insert(tk.END, product[6])
        product_notes.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_notes_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(product_notes.get("1.0", tk.END),
                                                                                     product,
                                                                                     "comments",
                                                                                     edit_notes_popup,
                                                                                     individual_product_popup)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10)

    def edit_product_name_unit_or_catalog_id_popup(self, product_to_edit, field_to_edit, individual_product_popup):
        edit_product_popup = tk.Toplevel()
        edit_product_popup.config(bg=self.formatting.colour_code_1)
        edit_product_popup.geometry('500x90')
        tk.Label(edit_product_popup,
                 text="Change: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        new_value_entry = tk.Entry(edit_product_popup)
        if field_to_edit == "name":
            new_value_entry.insert(tk.END, product_to_edit[1])
        elif field_to_edit == "unit_of_issue":
            new_value_entry.insert(tk.END, product_to_edit[9])
        else:
            new_value_entry.insert(tk.END, product_to_edit[2])
        new_value_entry.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_product_popup,
                  text="Commit Change",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(new_value_entry,
                                                                                     product_to_edit,
                                                                                     field_to_edit,
                                                                                     edit_product_popup,
                                                                                     individual_product_popup)).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    def edit_product_vendor_or_category_popup(self, product_to_edit, field_to_edit, individual_product_popup):
        vendors_or_categories_dict = {}
        vendors_or_categories_list = []
        vendors_or_categories = self.select_db.select_all_from_table(field_to_edit)
        for item in vendors_or_categories:
            vendors_or_categories_dict[item[1]] = item[0]
            vendors_or_categories_list.append(item[1])
        edit_product_popup = tk.Toplevel()
        edit_product_popup.config(bg=self.formatting.colour_code_1)
        edit_product_popup.geometry('500x90')
        vendors_or_categories_value = tk.StringVar(edit_product_popup)
        if field_to_edit == "vendors":
            vendors_or_categories_value.set(product_to_edit[3])
        else:
            vendors_or_categories_value.set(product_to_edit[4])
        vendors_or_categories_menu = tk.OptionMenu(edit_product_popup,
                                                   vendors_or_categories_value,
                                                   *vendors_or_categories_list,)
        vendors_or_categories_menu.config(highlightbackground=self.formatting.colour_code_1)
        vendors_or_categories_menu.config(font=self.formatting.medium_step_font)
        tk.Label(edit_product_popup,
                 text="Change: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        vendors_or_categories_menu.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_product_popup,
                  text="Commit Change",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(
                      vendors_or_categories_dict[vendors_or_categories_value.get()],
                      product_to_edit,
                      field_to_edit+"_id",
                      edit_product_popup,
                      individual_product_popup)).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    def edit_product_sub_category_popup(self, product, top_level_window):
        sub_category_dict = {}
        sub_category_list = []
        product_category_sub_cats = self.select_db.select_all_from_table_where_one_field_equals("sub_categories",
                                                                                                "categories_id",
                                                                                                product[7])
        for item in product_category_sub_cats:
            sub_category_list.append(item[2])
            sub_category_dict[item[2]] = item[0]
        edit_sub_category_popup = tk.Toplevel()
        edit_sub_category_popup.config(bg=self.formatting.colour_code_1)
        edit_sub_category_popup.geometry('500x90')
        sub_category_value = tk.StringVar(edit_sub_category_popup)
        sub_category_value.set(product[5])
        sub_category_menu = tk.OptionMenu(edit_sub_category_popup,
                                          sub_category_value,
                                          *sub_category_list,)
        sub_category_menu.config(highlightbackground=self.formatting.colour_code_1)
        sub_category_menu.config(font=self.formatting.medium_step_font)
        tk.Label(edit_sub_category_popup,
                 text="Change: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        sub_category_menu.grid(row=0, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_sub_category_popup,
                  text="Commit Change",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(
                      sub_category_dict[sub_category_value.get()],
                      product,
                      "sub_categories_id",
                      edit_sub_category_popup,
                      top_level_window)).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    # PRODUCT DELETION MAIN POPUP ####################################################################################

    def delete_product_popup(self, product_to_delete):
        are_you_sure_logout_popup = tk.Toplevel()
        are_you_sure_logout_popup.config(bg=self.formatting.colour_code_1)
        are_you_sure_logout_popup.geometry('500x90')
        tk.Label(are_you_sure_logout_popup,
                 text="Are you sure you want to archive this product?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        yes_i_am = tk.Button(are_you_sure_logout_popup,
                             text="Yes",
                             font=self.formatting.medium_step_font,
                             command=lambda: self.destroy_popup_archive_product_and_reload(
                                 product_to_delete,
                                 are_you_sure_logout_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)
        no_i_aint = tk.Button(are_you_sure_logout_popup,
                              text="No",
                              font=self.formatting.medium_step_font,
                              command=lambda: are_you_sure_logout_popup.destroy()).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    # POPUP CLOSE METHODS ############################################################################################

    def add_new_product_close_popup_and_reload(self,
                                               values,
                                               new_product_window,
                                               request=False):
        if request:
            self.add_delete_db.new_products_record(values, request=True)
        else:
            self.add_delete_db.new_products_record(values)
        self.parent.display_products_list_view(self.active_user)
        new_product_window.destroy()

    def commit_edit_query_close_edit_popup_and_reload(self,
                                                      new_value_entry,
                                                      product_to_edit,
                                                      field_to_edit,
                                                      top_level_window,
                                                      product_window):
        try:
            new_value_entry = new_value_entry.get()
        except AttributeError:
            pass
        self.edit_db.edit_one_product_field(field_to_edit, new_value_entry, product_to_edit[0])
        top_level_window.destroy()
        product_window.destroy()
        self.parent.display_products_list_view(self.active_user)

    def add_new_price_query_and_reload_products_page(self,
                                                     values,
                                                     individual_product_popup,
                                                     new_price_popup,
                                                     historical_price_popup=None):
        check = self.error_handling.checkNewPrice(values[1])
        if check:
            self.add_delete_db.new_price_tracking_record(values)
        individual_product_popup.destroy()
        new_price_popup.destroy()
        if historical_price_popup:
            historical_price_popup.destroy()
        self.parent.display_products_list_view(self.active_user)

    def check_valid_date_and_price_then_edit_price(self,
                                                   price_id,
                                                   price,
                                                   year,
                                                   month,
                                                   day,
                                                   individual_product_popup,
                                                   edit_price_popup,
                                                   edit_price_sub_popup):
        check = self.error_handling.checkYearMonthDayFormat(year, month, day)
        price_check = self.error_handling.checkNewPrice(price)
        if check and price_check:
            self.edit_db.edit_one_record_one_field_one_table("priceTracking",
                                                             "cost",
                                                             price,
                                                             price_id)
            self.edit_db.edit_one_record_one_field_one_table("priceTracking",
                                                             "cost_date",
                                                             datetime.date(int(year), int(month), int(day)),
                                                             price_id)
            individual_product_popup.destroy()
            edit_price_popup.destroy()
            edit_price_sub_popup.destroy()
            self.parent.display_products_list_view(self.active_user)
        else:
            self.editDateFailLabel.destroy()
            self.editDateFailLabel = tk.Label(edit_price_sub_popup,
                                              text="Invalid Date or Price Supplied.",
                                              font=self.formatting.medium_step_font,
                                              bg=self.formatting.colour_code_1,
                                              fg=self.formatting.colour_code_3
                                              ).grid(row=7, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)

    def check_valid_historical_date_then_add_new_price(self,
                                                       product,
                                                       price,
                                                       year,
                                                       month,
                                                       day,
                                                       individual_product_popup,
                                                       add_new_price_popup,
                                                       historical_price_popup):
        check = self.error_handling.checkYearMonthDayFormat(year, month, day)
        price_check = self.error_handling.checkNewPrice(price)
        if check and price_check:
            self.add_new_price_query_and_reload_products_page((product,
                                                               price,
                                                               datetime.date(int(year), int(month), int(day)),
                                                               ),
                                                              individual_product_popup,
                                                              add_new_price_popup,
                                                              historical_price_popup)
        else:
            self.historicalDateFailLabel.destroy()
            self.historicalDateFailLabel = tk.Label(historical_price_popup,
                                                    text="Invalid Date or Price Supplied.",
                                                    font=self.formatting.medium_step_font,
                                                    bg=self.formatting.colour_code_1,
                                                    fg=self.formatting.colour_code_3
                                                    ).grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=10, pady=5)

    def destroy_popup_archive_product_and_reload(self, product_to_archive, top_level_window):
        self.edit_db.archive_entry_in_table_by_id("products", product_to_archive[0])
        self.parent.display_products_list_view(self.active_user)
        top_level_window.destroy()

    def destroy_popups_archive_price_and_reload(self, price_to_archive, price_editing_popup, product_popup):
        self.edit_db.archive_entry_in_table_by_id("priceTracking", price_to_archive)
        price_editing_popup.destroy()
        product_popup.destroy()
        self.parent.display_products_list_view(self.active_user)

    def destroy_popup_and_go_to_products_page(self, top_level_window):
        self.parent.display_products_list_view(self.active_user)
        top_level_window.destroy()

    def approve_product_request_and_reload_page(self, record_to_approve):
        self.edit_db.edit_one_record_one_field_one_table("products", "approved", "1", record_to_approve[0])
        self.parent.display_products_list_view(self.active_user)