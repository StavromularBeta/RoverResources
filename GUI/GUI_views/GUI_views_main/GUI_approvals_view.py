import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
import datetime


class ApprovalsView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.config(bg=self.formatting.colour_code_1)
        self.approvals = ()
        self.approvals_canvas_length = 0
        self.approvals_scrollable_container = tk.Frame(self)
        self.approvals_frame = tk.Frame(self)
        self.approvals_frame.config(bg=self.formatting.colour_code_1)
        self.approvals_navigation_frame = tk.Frame(self)
        self.approvals_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.current_table = ""
        self.approvals_table_select = ["Categories",
                                       "Sub-Categories",
                                       "Vendors",
                                       "Products"]
        self.approvals_sort_value = tk.StringVar(self)
        self.approvals_sort_value.set("Categories")
        self.approvals_table_select_conversion_dictionary = {"Categories": "categories",
                                                             "Sub-Categories": "sub_categories",
                                                             "Vendors": "vendors",
                                                             "Products": "products"}

    def approvals_view(self, user, sort_by=False):
        self.active_user = user
        self.create_approvals_view(sort_by)

    def create_approvals_view(self, sort_by=False):
        self.get_approvals_from_table(sort_by)
        self.create_approvals_navigation_frame()
        self.make_scrollable_approvals_header_labels()
        self.populate_scrollable_approvals_list()
        self.create_scrollable_approvals_view()
        self.approvals_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.approvals_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def create_approvals_navigation_frame(self):
        tk.Label(self.approvals_navigation_frame,
                 text="Select Un-Approved Records",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        type_of_sort_menu = tk.OptionMenu(self.approvals_navigation_frame,
                                          self.approvals_sort_value,
                                          *self.approvals_table_select)
        type_of_sort_menu.config(highlightbackground=self.formatting.colour_code_2)
        type_of_sort_menu.config(font=self.formatting.medium_step_font)
        type_of_sort_menu.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        sort_by_button = tk.Button(self.approvals_navigation_frame,
                                   text="Select",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.parent.display_approvals_view(
                                       self.active_user,
                                       self.approvals_sort_value.get())).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=5
        )

    def get_approvals_from_table(self, sort_by=None):
        if sort_by:
            sort_by_variable = self.approvals_table_select_conversion_dictionary[sort_by]
            print(sort_by_variable)
            self.current_table = sort_by_variable
            self.approvals_sort_value.set(sort_by)
            if self.current_table == "sub_categories":
                self.approvals = self.select_db.left_join_multiple_tables(
                    "sc.id, c.category_name, sc.sub_category_name",
                    [["sub_categories sc", "", "sc.categories_id"],
                     ["categories c", "c.id", ""]],
                    "sc.sub_category_name",
                    only_approved="sc.approved"
                )
            elif self.current_table == "products":
                self.approvals = self.select_db.left_join_multiple_tables(
                    "p.id, p.name, p.product_code, v.vendor_name, c.category_name, sc.sub_category_name, p.comments,"
                    " p.categories_id, p.sub_categories_id, p.unit_of_issue, p.approved",
                    [["products p", "", "p.categories_id"],
                     ["categories c", "c.id", "p.vendors_id"],
                     ["vendors v", "v.id", "p.sub_categories_id"],
                     ["sub_categories sc", "sc.id", '']],
                    "p.name",
                    only_approved="p.approved")
            elif self.current_table == "priceTracking":
                self.approvals = self.select_db.left_join_multiple_tables(
                    "pt.id, p.name, pt.cost, pt.cost_date",
                    [["priceTracking pt", "", "pt.products_id"],
                     ["products p", "p.id", ""]],
                    "p.name",
                    only_approved="p.approved")
            else:
                self.approvals = self.select_db.\
                    select_all_from_table_where_one_field_equals(sort_by_variable, "approved", "0")
        else:
            self.current_table = "categories"
            self.approvals = self.select_db.\
                select_all_from_table_where_one_field_equals(self.current_table, "approved", "0")

    def create_scrollable_approvals_view(self):
        orders_canvas = tk.Canvas(self.approvals_scrollable_container,
                                  width=1650,
                                  height=500,
                                  scrollregion=(0, 0, 0, self.approvals_canvas_length),
                                  bd=0,
                                  highlightthickness=0)
        orders_canvas.config(bg=self.formatting.colour_code_1)
        orders_canvas_scrollbar = tk.Scrollbar(self.approvals_scrollable_container,
                                               orient="vertical",
                                               command=orders_canvas.yview)
        orders_canvas.configure(yscrollcommand=orders_canvas_scrollbar.set)
        orders_canvas_scrollbar.pack(side='left',
                                     fill='y')
        orders_canvas.pack(side="right",
                           fill='y')
        orders_canvas.create_window((0, 0),
                                    window=self.approvals_frame,
                                    anchor="nw")

    def make_scrollable_approvals_header_labels(self):
        if self.current_table == "categories":
            tk.Label(self.approvals_frame,
                     text="Category Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "sub_categories":
            tk.Label(self.approvals_frame,
                     text="Category Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.approvals_frame,
                     text="Sub-Category Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "vendors":
            tk.Label(self.approvals_frame,
                     text="Vendor Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "products":
            tk.Label(self.approvals_frame,
                     text="Product Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.approvals_frame,
                     text="Catalog Number",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.approvals_frame,
                     text="Vendor",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.approvals_frame,
                     text="Category",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=3, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.approvals_frame,
                     text="Sub-Category",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=4, sticky=tk.W, padx=10, pady=5)
        elif self.current_table == "priceTracking":
            tk.Label(self.approvals_frame,
                     text="Product Name",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.approvals_frame,
                     text="Price ($)",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.approvals_frame,
                     text="Date of Price",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        else:
            tk.Label(self.approvals_frame,
                     text="Requested " + self.approvals_sort_value.get() +
                          " Pending Approval (Integer fields hidden for readability)",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_approvals_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.approvals:
            print(item)
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            approve_column_location_from_row_create =\
                self.populate_scrollable_list_by_table(row_counter, text_color, item)
            tk.Button(self.approvals_frame,
                      text="Approve",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.approve_request_and_reload_approvals(item)).grid(
                row=row_counter,
                column=approve_column_location_from_row_create,
                sticky=tk.W,
                padx=10,
                pady=5)
            self.approvals_canvas_length += 50
            row_counter += 1
            even_odd += 1

    def populate_scrollable_list_by_table(self, row_counter, text_color, record):
        approve_button_column = 0
        if self.current_table in ["categories", "vendors"]:
            tk.Label(self.approvals_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "sub_categories":
            tk.Label(self.approvals_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.approvals_frame,
                     text=record[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "products":
            tk.Label(self.approvals_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.approvals_frame,
                     text=record[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.approvals_frame,
                     text=record[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.approvals_frame,
                     text=record[4],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=3, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            if record[5] == "None":
                tk.Label(self.approvals_frame,
                         text="",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=text_color,
                         wraplength=0).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            else:
                tk.Label(self.approvals_frame,
                         text=record[5],
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=text_color,
                         wraplength=0).grid(row=row_counter, column=4, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        elif self.current_table == "priceTracking":
            tk.Label(self.approvals_frame,
                     text=record[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.approvals_frame,
                     text="{:.2f}".format(float(record[2])),
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
            tk.Label(self.approvals_frame,
                     text=record[3],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
        else:
            tk.Label(self.approvals_frame,
                     text=record,
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color,
                     wraplength=0).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            approve_button_column += 1
        return approve_button_column

    def approve_request_and_reload_approvals(self, record_to_approve):
        self.edit_db.edit_one_record_one_field_one_table(self.current_table, "approved", "1", record_to_approve[0])
        self.parent.display_approvals_view(self.active_user)
