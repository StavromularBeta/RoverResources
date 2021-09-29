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
        self.products_list_scrollable_container = tk.Frame(self)
        self.products_list_frame = tk.Frame(self)
        self.products_list_frame.config(bg=self.formatting.colour_code_1)

    # MAIN METHODS

    def products_list_view(self, user):
        self.active_user = user
        self.create_products_list()

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
        self.products_list_scrollable_container.grid()

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
            if self.active_user[1] == 1:
                tk.Button(self.products_list_frame,
                          text="Open",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.individual_product_popup(item)).grid(row=row_counter,
                                                                                              column=5,
                                                                                              sticky=tk.W,
                                                                                              padx=10,
                                                                                              pady=5)
                tk.Button(self.products_list_frame,
                          text="Delete",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.delete_product_popup(item)).grid(row=row_counter,
                                                                                          column=6,
                                                                                          sticky=tk.W,
                                                                                          padx=10,
                                                                                          pady=5)
            row_counter += 1
            even_odd += 1

    def individual_product_popup(self, product):
        individual_product_popup = tk.Toplevel()
        individual_product_popup.config(bg=self.formatting.colour_code_1)
        individual_product_popup.geometry('600x300')
        product_info_label = tk.Label(individual_product_popup,
                                      text="Product Information",
                                      font=self.formatting.homepage_window_select_button_font,
                                      bg=self.formatting.colour_code_1,
                                      fg=self.formatting.colour_code_3)
        self.formatting.grid_shopping_cart_labels(product_info_label, 0, 0)
        product_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                   product[0],
                                                                   self.formatting.colour_code_3)
        self.formatting.grid_shopping_cart_labels(product_name, 1, 0)
        catalog_id = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                 "Catalog: " + product[1],
                                                                 self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(catalog_id, 2, 0)
        vendor_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                  "Vendor: " + product[2],
                                                                  self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(vendor_name, 3, 0)
        category_name = self.formatting.create_shopping_cart_labels(individual_product_popup,
                                                                    "Category: " + product[3],
                                                                    self.formatting.colour_code_2)
        self.formatting.grid_shopping_cart_labels(category_name, 4, 0)
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
                  command=lambda: self.destroy_popup_and_go_to_products_page(individual_product_popup)).grid(
            row=3, column=1, sticky=tk.W, padx=10, pady=10)
        tk.Button(individual_product_popup,
                  text="Edit",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.destroy_popup_and_go_to_products_page(individual_product_popup)).grid(
            row=4, column=1, sticky=tk.W, padx=10, pady=10)

    def destroy_popup_and_go_to_products_page(self, top_level_window):
        self.parent.display_products_list_view(self.active_user)
        top_level_window.destroy()

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

    def commit_edit_query_close_edit_popup_and_reload(self,
                                                      new_value_entry,
                                                      product_to_edit,
                                                      field_to_edit,
                                                      top_level_window,
                                                      product_window):
        new_value_entry = new_value_entry.get()
        self.edit_db.edit_one_product_field(field_to_edit, new_value_entry, product_to_edit[4])
        top_level_window.destroy()
        product_window.destroy()
        self.parent.display_products_list_view(self.active_user)

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

    def destroy_popup_delete_product_and_reload(self, top_level_window):
        self.parent.display_products_list_view(self.active_user)
        top_level_window.destroy()
