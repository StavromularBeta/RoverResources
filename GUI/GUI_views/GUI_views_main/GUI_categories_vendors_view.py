import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
import datetime


class CategoriesVendorsView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
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

    def categories_and_vendors_view(self, user):
        self.active_user = user
        self.create_vendors_navigation_frame()
        self.create_categories_navigation_frame()
        self.create_vendors_list()
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
                      command=lambda: print("request new vendor")).grid(row=0,
                                                                        column=1,
                                                                        sticky=tk.W,
                                                                        padx=10,
                                                                        pady=5)
        self.vendors_navigation_frame.grid(row=0, column=0, sticky=tk.W, pady=5)

    def create_categories_navigation_frame(self):
        tk.Label(self.categories_navigation_frame,
                 text="Products List",
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
                      command=lambda: print("button")).grid(row=0,
                                                            column=1,
                                                            sticky=tk.W,
                                                            padx=10,
                                                            pady=5)
        self.categories_navigation_frame.grid(row=0, column=1, sticky=tk.W, pady=5)

    def create_vendors_list(self):
        self.get_vendors_list_from_database()
        self.populate_scrollable_vendors_list()
        self.create_scrollable_vendors_list()
        self.vendors_list_scrollable_container.grid(row=1, column=0, sticky=tk.W, pady=5)

    def create_categories_list(self):
        self.get_categories_list_from_database()
        self.populate_scrollable_categories_list()
        self.create_scrollable_categories_list()
        self.categories_list_scrollable_container.grid(row=1, column=1, sticky=tk.W, pady=5)

    # PRODUCTS LIST METHODS

    def get_vendors_list_from_database(self):
        self.vendors_list = self.select_db.select_all_from_table("vendors")

    def create_scrollable_vendors_list(self):
        products_list_canvas = tk.Canvas(self.vendors_list_scrollable_container,
                                         width=500,
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
        for item in self.vendors_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            vendor_name_label = self.formatting.create_shopping_cart_labels(self.vendors_list_frame,
                                                                            item[1],
                                                                            text_color)
            self.formatting.grid_shopping_cart_labels(vendor_name_label, row_counter, 1)
            if self.active_user[1] == 1:
                tk.Button(self.vendors_list_frame,
                          text="Open",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.vendor_or_category_popup(
                            "vendors",
                            item
                          )).grid(row=row_counter,
                                  column=2,
                                  sticky=tk.W,
                                  padx=10,
                                  pady=5)
            else:
                tk.Button(self.vendors_list_frame,
                          text="View Notes",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.vendor_or_category_popup("vendors",
                                                                                 item)).grid(row=row_counter,
                                                                                             column=2,
                                                                                             sticky=tk.W,
                                                                                             padx=10,
                                                                                             pady=5)
            self.vendors_canvas_length += 50
            row_counter += 1
            even_odd += 1

# SHOPPING CART METHODS

    def get_categories_list_from_database(self):
        self.categories_list = self.select_db.select_all_from_table("categories")

    def populate_scrollable_categories_list(self):
        row_counter = 0
        even_odd = 1
        for item in self.categories_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            tk.Label(self.categories_list_frame,
                     text=item[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            if self.active_user[1] == 1:
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
            else:
                tk.Button(self.categories_list_frame,
                          text="View Notes",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item:self.vendor_or_category_popup("categories",
                                                                                 item)).grid(row=row_counter,
                                                                                             column=2,
                                                                                             sticky=tk.W,
                                                                                             padx=10,
                                                                                             pady=5)
            self.categories_canvas_length += 50
            row_counter += 1
            even_odd += 1

    def create_scrollable_categories_list(self):
        shopping_cart_canvas = tk.Canvas(self.categories_list_scrollable_container,
                                         width=500,
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

    def edit_name_popup(self, table_to_edit, vendor_or_category, individual_cat_vend_popup):
        edit_notes_popup = tk.Toplevel()
        edit_notes_popup.config(bg=self.formatting.colour_code_1)
        edit_notes_popup.geometry('500x90')
        product_notes = tk.Entry(edit_notes_popup)
        product_notes.config(state=tk.NORMAL)
        product_notes.insert(tk.END, vendor_or_category[1])
        product_notes.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_notes_popup,
                  text="Commit Changess",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(table_to_edit,
                                                                                     product_notes.get(),
                                                                                     vendor_or_category,
                                                                                     "name check",
                                                                                     individual_cat_vend_popup,
                                                                                     edit_notes_popup
                                                                                     )).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)

    def add_new_vendor_or_category_popup(self, table_to_add_to):
        add_new_popup = tk.Toplevel()
        add_new_popup.config(bg=self.formatting.colour_code_1)
        add_new_popup.geometry('500x250')
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
        tk.Button(add_new_popup,
                  text="Add new " + add_new_text,
                  font=self.formatting.medium_step_font,
                  command=lambda: self.add_new_vendor_or_category(table_to_add_to,
                                                                  (vendor_or_category_name.get(),
                                                                   vendor_or_category_notes.get("1.0", tk.END)),
                                                                  add_new_popup)).grid(
            row=3, column=0, sticky=tk.W, padx=10, pady=10)

    def edit_sub_categories_popup(self,
                                  current_category_record,
                                  vendor_or_category_popup):
        row_counter = 0
        edit_subcategories_popup = tk.Toplevel()
        edit_subcategories_popup.config(bg=self.formatting.colour_code_1)
        edit_subcategories_popup.geometry('600x150')
        category_sub_cats = self.select_db.select_all_from_table_where_one_field_equals("sub_categories",
                                                                                        "categories_id",
                                                                                        current_category_record[0])
        category_sub_cats_list = []
        category_sub_cats_dict = {}
        for item in category_sub_cats:
            if item[2] == "None":
                pass
            else:
                category_sub_cats_list.append(item[2])
                category_sub_cats_dict[item[2]] = item[0]
        if len(category_sub_cats_list) == 0:
            pass
        else:
            sub_category_value = tk.StringVar(edit_subcategories_popup)
            sub_category_value.set(category_sub_cats_list[0])
            sub_category_menu = tk.OptionMenu(edit_subcategories_popup,
                                              sub_category_value,
                                              *category_sub_cats_list,)
            sub_category_menu.config(highlightbackground=self.formatting.colour_code_1)
            sub_category_menu.config(font=self.formatting.medium_step_font)
            sub_category_menu.grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=10)
            if self.active_user[1] == 1:
                tk.Button(edit_subcategories_popup,
                          text="Delete Selected",
                          font=self.formatting.medium_step_font,
                          command=lambda: print("delete subcategory")).grid(
                    row=row_counter, column=1, sticky=tk.W, padx=10, pady=10)
                tk.Button(edit_subcategories_popup,
                          text="Edit Selected",
                          font=self.formatting.medium_step_font,
                          command=lambda: print("edit subcategory")).grid(
                    row=row_counter, column=2, sticky=tk.W, padx=10, pady=10)
            row_counter += 1
        tk.Label(edit_subcategories_popup,
                 text="Name: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=0, sticky=tk.W, pady=10, padx=10)
        vendor_or_category_name = tk.Entry(edit_subcategories_popup)
        vendor_or_category_name.config(state=tk.NORMAL)
        vendor_or_category_name.grid(row=row_counter, column=1, sticky=tk.W, pady=10)
        if self.active_user[1] == 1:
            tk.Button(edit_subcategories_popup,
                      text="Add new Subcategory",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_sub_category((current_category_record[0],
                                                                vendor_or_category_name.get(),
                                                                ""),
                                                                edit_subcategories_popup,
                                                                vendor_or_category_popup)).grid(
                row=row_counter, column=2, sticky=tk.W, padx=10, pady=10)

    def add_new_sub_category(self,
                             values,
                             edit_subcategories_popup,
                             vendor_or_category_popup):
        self.add_delete_db.new_sub_categories_record(values)
        edit_subcategories_popup.destroy()
        vendor_or_category_popup.destroy()
        self.parent.display_categories_and_vendors_view(self.active_user)

    def add_new_vendor_or_category(self,
                                   table_to_add_to,
                                   values,
                                   add_new_window):
        if table_to_add_to == "vendors":
            self.add_delete_db.new_vendors_record(values)
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
