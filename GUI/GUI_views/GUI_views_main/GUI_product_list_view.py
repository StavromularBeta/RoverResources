import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting


class ProductListView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.products_list = ""
        self.config(bg=self.formatting.colour_code_1)
        self.products_list_navigation_frame = tk.Frame(self)
        self.products_list_scrollable_container = tk.Frame(self)
        self.products_list_frame = tk.Frame(self)
        self.products_list_frame.config(bg=self.formatting.colour_code_1)
        self.products_list_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.sub_categories_menu = ""
        self.sub_categories_value = ""

    # MAIN METHODS

    def products_list_view(self, user):
        self.active_user = user
        self.create_products_list()

    def create_products_list(self):
        self.create_products_list_navigation_frame()
        self.get_products_list_from_database()
        self.make_scrollable_products_list_header_labels()
        self.populate_scrollable_products_list()
        self.create_scrollable_products_list()
        self.products_list_navigation_frame.grid(sticky=tk.W, pady=10)
        self.products_list_scrollable_container.grid()

    # PRODUCTS LIST METHODS

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
                      command=lambda: print("button")).grid(row=0,
                                                            column=1,
                                                            sticky=tk.W,
                                                            padx=10,
                                                            pady=5)

    def get_products_list_from_database(self):
        self.products_list = self.select_db.left_join_multiple_tables(
            "p.id, p.name, p.product_code, v.vendor_name, c.category_name, sc.sub_category_name, p.comments,"
            " p.categories_id, p.sub_categories_id",
            [["products p", "", "p.categories_id"],
             ["categories c", "c.id", "p.vendors_id"],
             ["vendors v", "v.id", "p.sub_categories_id"],
             ["sub_categories sc", "sc.id", '']],
            "p.name")

    def create_scrollable_products_list(self):
        products_list_canvas = tk.Canvas(self.products_list_scrollable_container,
                                         width=1200,
                                         height=550,
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
        product_category_header = self.formatting.create_shopping_cart_labels(self.products_list_frame,
                                                                              "Sub-Category",
                                                                              self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(product_category_header, 0, 5)

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
            if self.active_user[1] == 1:
                tk.Button(self.products_list_frame,
                          text="Open",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.individual_product_popup(item)).grid(row=row_counter,
                                                                                              column=6,
                                                                                              sticky=tk.W,
                                                                                              padx=10,
                                                                                              pady=5)
                tk.Button(self.products_list_frame,
                          text="Delete",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.delete_product_popup(item)).grid(row=row_counter,
                                                                                          column=7,
                                                                                          sticky=tk.W,
                                                                                          padx=10,
                                                                                          pady=5)
            else:
                tk.Button(self.products_list_frame,
                          text="View Notes",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: print("view notes")).grid(row=row_counter,
                                                                              column=6,
                                                                              sticky=tk.W,
                                                                              padx=10,
                                                                              pady=5)
            row_counter += 1
            even_odd += 1

    # POPUPS

    def new_product_popup(self):
        new_product_popup = tk.Toplevel()
        new_product_popup.config(bg=self.formatting.colour_code_1)
        new_product_popup.geometry('600x400')
        product_name_entry = tk.Entry(new_product_popup)
        product_catalog_id_entry = tk.Entry(new_product_popup)
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
                 text="Notes",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=5, column=0, sticky=tk.W, padx=10, pady=10)
        notes_entry.grid(row=5, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(new_product_popup,
                  text="Add New Product",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.add_new_product_close_popup_and_reload((categories_dict[categories_value.get()],
                                                                               sub_categories_dict[
                                                                                   self.sub_categories_value.get()],
                                                                               vendors_dict[vendors_value.get()],
                                                                               product_catalog_id_entry.get(),
                                                                               product_name_entry.get(),
                                                                               notes_entry.get()),
                                                                              new_product_popup)).grid(
            row=6, column=0, sticky=tk.W, padx=10, pady=10)

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

    def individual_product_popup(self, product):
        individual_product_popup = tk.Toplevel()
        individual_product_popup.config(bg=self.formatting.colour_code_1)
        individual_product_popup.geometry('600x500')
        product_info_label = tk.Label(individual_product_popup,
                                      text="Product Information",
                                      font=self.formatting.homepage_window_select_button_font,
                                      bg=self.formatting.colour_code_1,
                                      fg=self.formatting.colour_code_3)
        self.formatting.grid_shopping_cart_labels(product_info_label, 0, 0)
        product_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                   product[1],
                                                                   self.formatting.colour_code_3)
        self.formatting.grid_shopping_cart_labels(product_name, 1, 0)
        catalog_id = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                 "Catalog: " + product[2],
                                                                 self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(catalog_id, 2, 0)
        vendor_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                  "Vendor: " + product[3],
                                                                  self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(vendor_name, 3, 0)
        category_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                    "Category: " + product[4],
                                                                    self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(category_name, 4, 0)
        if product[5] == "None":
            sub_category_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                            "No Sub Category",
                                                                            self.formatting.colour_code_2)
        else:
            sub_category_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                            "Sub Category: " + product[5],
                                                                            self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(sub_category_name, 5, 0)
        product_notes = tk.Text(individual_product_popup,
                                height=5,
                                width=40)
        product_notes.config(bg=self.formatting.colour_code_2)
        product_notes.config(state=tk.NORMAL)
        product_notes.insert(tk.END, product[6])
        product_notes.config(state=tk.DISABLED, wrap="word")
        product_notes.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(individual_product_popup,
                  text="Edit",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.edit_product_name_or_catalog_id_popup(product,
                                                                             "name",
                                                                             individual_product_popup)).grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(individual_product_popup,
                  text="Edit",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.edit_product_name_or_catalog_id_popup(product,
                                                                             "product_code",
                                                                             individual_product_popup)).grid(
            row=2, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(individual_product_popup,
                  text="Edit",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.edit_product_vendor_or_category_popup(product,
                                                                             "vendors",
                                                                             individual_product_popup)).grid(
            row=3, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(individual_product_popup,
                  text="Edit",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.edit_product_vendor_or_category_popup(product,
                                                                             "categories",
                                                                             individual_product_popup)).grid(
            row=4, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(individual_product_popup,
                  text="Edit",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.edit_sub_category_popup(product,
                                                               individual_product_popup)).grid(
            row=5, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(individual_product_popup,
                  text="Edit Notes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.edit_notes_popup(product,
                                                        individual_product_popup)).grid(
            row=7, column=0, sticky=tk.W, padx=10, pady=10)

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

    def edit_product_name_or_catalog_id_popup(self, product_to_edit, field_to_edit, individual_product_popup):
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

    def delete_product_popup(self, product_to_delete):
        are_you_sure_logout_popup = tk.Toplevel()
        are_you_sure_logout_popup.config(bg=self.formatting.colour_code_1)
        are_you_sure_logout_popup.geometry('500x90')
        tk.Label(are_you_sure_logout_popup,
                 text="Are you sure you want to delete this product?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        yes_i_am = tk.Button(are_you_sure_logout_popup,
                             text="Yes",
                             font=self.formatting.medium_step_font,
                             command=lambda: self.destroy_popup_delete_product_and_reload(
                                 are_you_sure_logout_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)
        no_i_aint = tk.Button(are_you_sure_logout_popup,
                              text="No",
                              font=self.formatting.medium_step_font,
                              command=lambda: are_you_sure_logout_popup.destroy()).grid(
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

    def edit_sub_category_popup(self, product, top_level_window):
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
    # POPUP CLOSE METHODS

    def add_new_product_close_popup_and_reload(self,
                                               values,
                                               new_product_window):
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

    def destroy_popup_delete_product_and_reload(self, top_level_window):
        self.parent.display_products_list_view(self.active_user)
        top_level_window.destroy()

    def destroy_popup_and_go_to_products_page(self, top_level_window):
        self.parent.display_products_list_view(self.active_user)
        top_level_window.destroy()
