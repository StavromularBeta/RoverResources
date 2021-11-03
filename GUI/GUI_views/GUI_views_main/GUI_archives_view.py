import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
import datetime


class ArchivesView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.config(bg=self.formatting.colour_code_1)
        self.archives = ()
        self.archives_canvas_length = 0
        self.archives_scrollable_container = tk.Frame(self)
        self.archives_frame = tk.Frame(self)
        self.archives_frame.config(bg=self.formatting.colour_code_1)
        self.archives_navigation_frame = tk.Frame(self)
        self.archives_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.current_table = ""
        self.archives_table_select = ["Categories",
                                      "Sub-Categories",
                                      "Vendors",
                                      "Products",
                                      "Prices",
                                      "Credentials",
                                      "Users",
                                      "Requests",
                                      "Orders",
                                      "Received",
                                      "Inventory"]
        self.archives_sort_value = tk.StringVar(self)
        self.archives_sort_value.set("Categories")
        self.archives_table_select_conversion_dictionary = {"Categories": "categories",
                                                            "Sub-Categories": "sub_categories",
                                                            "Vendors": "vendors",
                                                            "Products": "products",
                                                            "Prices": "priceTracking",
                                                            "Credentials": "credentials",
                                                            "Users": "users",
                                                            "Requests": "requests",
                                                            "Orders": "orders",
                                                            "Received": "received",
                                                            "Inventory": "inventory"}

    def archives_view(self, user, sort_by=False):
        self.active_user = user
        self.create_archives_view(sort_by)

    def create_archives_view(self, sort_by=False):
        self.get_archives_from_table(sort_by)
        self.create_approvals_navigation_frame()
        self.make_scrollable_archives_header_labels()
        self.populate_scrollable_archives_list()
        self.create_scrollable_approvals_view()
        self.archives_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.archives_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def create_approvals_navigation_frame(self):
        tk.Label(self.archives_navigation_frame,
                 text="Select Table",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.archives_navigation_frame,
                                          self.archives_sort_value,
                                          *self.archives_table_select)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        sort_by_button = tk.Button(self.archives_navigation_frame,
                                   text="Select",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_archives_view(
                                       self.active_user,
                                       self.archives_sort_value.get())).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=5
        )

    def get_archives_from_table(self, sort_by=None):
        if sort_by:
            sort_by_variable = self.archives_table_select_conversion_dictionary[sort_by]
            self.current_table = sort_by_variable
            self.archives_sort_value.set(sort_by)
            self.archives = self.select_db.\
                select_all_from_table_where_one_field_equals(sort_by_variable, "archived", "1")
        else:
            self.current_table = "categories"
            self.archives = self.select_db.\
                select_all_from_table_where_one_field_equals(self.current_table, "archived", "1")

    def create_scrollable_approvals_view(self):
        orders_canvas = tk.Canvas(self.archives_scrollable_container,
                                  width=1650,
                                  height=500,
                                  scrollregion=(0, 0, 0, self.archives_canvas_length),
                                  bd=0,
                                  highlightthickness=0)
        orders_canvas.config(bg=self.formatting.colour_code_1)
        orders_canvas_scrollbar = tk.Scrollbar(self.archives_scrollable_container,
                                               orient="vertical",
                                               command=orders_canvas.yview)
        orders_canvas.configure(yscrollcommand=orders_canvas_scrollbar.set)
        orders_canvas_scrollbar.pack(side='left',
                                     fill='y')
        orders_canvas.pack(side="right",
                           fill='y')
        orders_canvas.create_window((0, 0),
                                    window=self.archives_frame,
                                    anchor="nw")

    def make_scrollable_archives_header_labels(self):
        tk.Label(self.archives_frame,
                 text="Archived " + self.archives_sort_value.get() + " Records (Integer fields hidden for readability)",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_archives_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.archives:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            non_integer_fields = []
            for subitem in item:
                try:
                    int(subitem)
                except ValueError:
                    non_integer_fields.append(subitem)
            tk.Label(self.archives_frame,
                     text=non_integer_fields,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Button(self.archives_frame,
                      text="Restore",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.restore_record_and_reload_archives(item)).grid(row=row_counter,
                                                                                          column=1,
                                                                                          sticky=tk.W,
                                                                                          padx=10,
                                                                                          pady=5)
            self.archives_canvas_length += 50
            row_counter += 1
            even_odd += 1

    def restore_record_and_reload_archives(self, record_to_restore):
        self.edit_db.edit_one_record_one_field_one_table(self.current_table, "archived", "0", record_to_restore[0])
        self.parent.display_archives_view(self.active_user)
