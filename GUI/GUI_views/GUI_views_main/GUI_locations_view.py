import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_errorHandling as tk_error_handling
import datetime


class LocationsView(tk.Frame):

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
        self.locations = ()
        self.locations_canvas_length = 0
        self.locations_scrollable_container = tk.Frame(self)
        self.locations_frame = tk.Frame(self)
        self.locations_frame.config(bg=self.formatting.colour_code_1)
        self.locations_navigation_frame = tk.Frame(self)
        self.locations_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.search_by_active_term = ""

    def locations_view(self, user, search_by=False):
        self.search_by_active_term = search_by
        self.active_user = user
        self.create_locations_view(search_by)

    def create_locations_view(self, search_by=None):
        self.get_locations_list_from_database(search_by)
        self.populate_scrollable_locations_list()
        self.create_scrollable_inventory_view()
        self.create_locations_navigation_frame()
        self.locations_navigation_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.locations_scrollable_container.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)

    def get_locations_list_from_database(self, search_by=None):
        if search_by:
            self.locations = self.select_db.select_all_from_table_where_one_field_like(
                "inventoryLocations",
                "locations_name",
                '%' + search_by + '%',
                no_archive=True)
        else:
            self.locations = self.select_db.select_all_from_table("inventoryLocations", no_archived=True)

    def populate_scrollable_locations_list(self):
        row_counter = 0
        even_odd = 1
        tk.Label(self.locations_frame,
                 text="Category Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.locations_frame,
                 text="Approved?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
        row_counter += 1
        for item in self.locations:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            tk.Label(self.locations_frame,
                     text=item[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            if item[4] == 1:
                tk.Label(self.locations_frame,
                         text="Yes",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_green).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            else:
                tk.Label(self.locations_frame,
                         text="No",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_red).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Button(self.locations_frame,
                      text="Open",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.locations_popup(item)).grid(
                row=row_counter, column=2, sticky=tk.W, padx=10, pady=5)
            if self.active_user[1] == 1:
                tk.Button(self.locations_frame,
                          text="Archive",
                          font=self.formatting.medium_step_font,
                          command=lambda item=item: self.archive_location_popup(item)).grid(row=row_counter,
                                                                                            column=3,
                                                                                            sticky=tk.W,
                                                                                            padx=10,
                                                                                            pady=5)
                if item[4] == 0:
                    tk.Button(self.locations_frame,
                              text="Approve",
                              font=self.formatting.medium_step_font,
                              command=lambda item=item: print("approve")).grid(
                        row=row_counter,
                        column=4,
                        sticky=tk.W,
                        padx=10,
                        pady=5)
            self.locations_canvas_length += 50
            row_counter += 1
            even_odd += 1

    def create_scrollable_inventory_view(self):
        inventory_canvas = tk.Canvas(self.locations_scrollable_container,
                                     width=1650,
                                     height=500,
                                     scrollregion=(0, 0, 0, self.locations_canvas_length),
                                     bd=0,
                                     highlightthickness=0)
        inventory_canvas.config(bg=self.formatting.colour_code_1)
        orders_canvas_scrollbar = tk.Scrollbar(self.locations_scrollable_container,
                                               orient="vertical",
                                               command=inventory_canvas.yview)
        inventory_canvas.configure(yscrollcommand=orders_canvas_scrollbar.set)
        orders_canvas_scrollbar.pack(side='left',
                                     fill='y')
        inventory_canvas.pack(side="right",
                              fill='y')
        inventory_canvas.create_window((0, 0),
                                       window=self.locations_frame,
                                       anchor="nw")

    def create_locations_navigation_frame(self):
        locations_search_entry = tk.Entry(self.locations_navigation_frame)
        # if there is an active search term, inserts it into entry box.
        if self.search_by_active_term:
            locations_search_entry.insert(0, self.search_by_active_term)
        tk.Label(self.locations_navigation_frame,
                 text="Locations",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        if self.active_user[1] == 1:
            tk.Button(self.locations_navigation_frame,
                      text="Add New Location",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_location_popup()).grid(row=0,
                                                                          column=1,
                                                                          sticky=tk.W,
                                                                          padx=10,
                                                                          pady=5)
        else:
            tk.Button(self.locations_navigation_frame,
                      text="Request New Location",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.add_new_location_popup(request=True)).grid(
                row=0,
                column=1,
                sticky=tk.W,
                padx=10,
                pady=5)
        tk.Label(self.locations_navigation_frame,
                 text="Search: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        locations_search_entry.grid(row=0, column=3, sticky=tk.W, pady=5)
        tk.Button(self.locations_navigation_frame,
                  text="Search",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_locations_view(
                      self.active_user,
                      search_by=locations_search_entry.get())).grid(
            row=0, column=4, sticky=tk.W, padx=5, pady=5)
        tk.Button(self.locations_navigation_frame,
                  text="All",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.parent.display_locations_view(
                      self.active_user,
                      search_by=locations_search_entry.get())).grid(
            row=0, column=5, sticky=tk.W, padx=5, pady=5)

    def add_new_location_popup(self, request=False):
        add_new_location_popup = tk.Toplevel()
        add_new_location_popup.config(bg=self.formatting.colour_code_1)
        add_new_location_popup.geometry('500x350')
        tk.Label(add_new_location_popup,
                 text="Name: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, pady=10, padx=10)
        location_name = tk.Entry(add_new_location_popup)
        location_name.config(state=tk.NORMAL)
        location_name.grid(row=0, column=1, sticky=tk.W, pady=10)
        tk.Label(add_new_location_popup,
                 text="Notes",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, sticky=tk.W, pady=10, padx=10)
        location_notes = tk.Text(add_new_location_popup,
                                 height=5,
                                 width=40)
        location_notes.config(bg=self.formatting.colour_code_2, wrap="word")
        location_notes.config(state=tk.NORMAL)
        location_notes.grid(row=2, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        if self.active_user[1] == 1:
            tk.Button(add_new_location_popup,
                      text="Add new Location",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_new_location("inventoryLocations",
                                                                        location_name.get(),
                                                                        location_notes.get("1.0", tk.END),
                                                                        add_new_location_popup)).grid(
                row=3, column=0, sticky=tk.W, padx=10, pady=10)
        else:
            tk.Button(add_new_location_popup,
                      text="Add new Location",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_new_location("inventoryLocations",
                                                                        location_name.get(),
                                                                        location_notes.get("1.0", tk.END),
                                                                        add_new_location_popup,
                                                                        request)).grid(
                row=3, column=0, sticky=tk.W, padx=10, pady=10)

    def locations_popup(self, location):
        locations_popup = tk.Toplevel()
        locations_popup.config(bg=self.formatting.colour_code_1)
        locations_popup.geometry('600x250')
        tk.Label(locations_popup,
                 text=location[1],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        if self.active_user[1] == 1:
            tk.Button(locations_popup,
                      text="Edit",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_name_popup("inventoryLocations",
                                                           location,
                                                           locations_popup)
                      ).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        vendor_or_category_notes = tk.Text(locations_popup,
                                           height=5,
                                           width=40)
        vendor_or_category_notes.config(bg=self.formatting.colour_code_2)
        vendor_or_category_notes.insert(tk.END, location[2])
        vendor_or_category_notes.config(state=tk.DISABLED, wrap="word")
        vendor_or_category_notes.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        if self.active_user[1] == 1:
            tk.Button(locations_popup,
                      text="Edit Notes",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_notes_popup("inventoryLocations", location, locations_popup)
                      ).grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Button(locations_popup,
                      text="Edit Sub-Locations",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_sub_locations_popup(location, locations_popup)).grid(
                row=3, column=0, sticky=tk.W, padx=10, pady=5)
        else:
            tk.Button(locations_popup,
                      text="View Sub-Locations",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.edit_sub_locations_popup(location, locations_popup)).grid(
                row=3, column=0, sticky=tk.W, padx=10, pady=5)

    def edit_name_popup(self, table_to_edit, location, individual_location_popup, sub_location=False):
        edit_name_popup = tk.Toplevel()
        edit_name_popup.config(bg=self.formatting.colour_code_1)
        edit_name_popup.geometry('500x90')
        edit_name_entry = tk.Entry(edit_name_popup)
        edit_name_entry.config(state=tk.NORMAL)
        if sub_location:
            edit_name_entry.insert(tk.END, location[2])
        else:
            edit_name_entry.insert(tk.END, location[1])
        edit_name_entry.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_name_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.check_for_blank_name_edit(table_to_edit,
                                                                 edit_name_entry.get(),
                                                                 location,
                                                                 individual_location_popup,
                                                                 edit_name_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)

    def edit_notes_popup(self, table_to_edit, location, individual_location_popup):
        edit_notes_popup = tk.Toplevel()
        edit_notes_popup.config(bg=self.formatting.colour_code_1)
        edit_notes_popup.geometry('500x160')
        locations_notes = tk.Text(edit_notes_popup,
                                  height=5,
                                  width=40)
        locations_notes.config(bg=self.formatting.colour_code_2, wrap="word")
        locations_notes.config(state=tk.NORMAL)
        locations_notes.insert(tk.END, location[2])
        locations_notes.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_notes_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(table_to_edit,
                                                                                     locations_notes.get("1.0", tk.END),
                                                                                     location,
                                                                                     "comments",
                                                                                     individual_location_popup,
                                                                                     edit_notes_popup
                                                                                     )).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10)

    def edit_sub_locations_popup(self,
                                 current_location_record,
                                 locations_popup):
        row_counter = 0
        edit_sublocations_popup = tk.Toplevel()
        edit_sublocations_popup.config(bg=self.formatting.colour_code_1)
        edit_sublocations_popup.geometry('600x300')
        location_sub_locs = self.select_db.select_all_from_table_where_one_field_equals("inventorySubLocations",
                                                                                        "locations_id",
                                                                                        current_location_record[0],
                                                                                        no_archive=True,
                                                                                        no_approved=True)
        location_sub_locs_list = []
        locations_sub_locs_dict = {}
        for item in location_sub_locs:
            if item[2] == "None":
                pass
            else:
                location_sub_locs_list.append(item[2])
                locations_sub_locs_dict[item[2]] = item
        if len(location_sub_locs_list) == 0:
            pass
        else:
            tk.Label(edit_sublocations_popup,
                     text="Existing Sub-locations",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                row=row_counter, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)
            row_counter += 1
            sub_locations_value = tk.StringVar(edit_sublocations_popup)
            sub_locations_value.set(location_sub_locs_list[0])
            sub_locations_menu = tk.OptionMenu(edit_sublocations_popup,
                                               sub_locations_value,
                                               *location_sub_locs_list,)
            sub_locations_menu.config(highlightbackground=self.formatting.colour_code_1)
            sub_locations_menu.config(font=self.formatting.medium_step_font)
            sub_locations_menu.grid(row=row_counter, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
            if self.active_user[1] == 1:
                tk.Button(edit_sublocations_popup,
                          text="Archive",
                          font=self.formatting.medium_step_font,
                          command=lambda: self.archive_sublocation_and_reload_page(
                              locations_sub_locs_dict[sub_locations_value.get()][0],
                              edit_sublocations_popup,
                              locations_popup)).grid(
                    row=row_counter, column=2, sticky=tk.W, padx=10, pady=10)
                tk.Button(edit_sublocations_popup,
                          text="Edit Name",
                          font=self.formatting.medium_step_font,
                          command=lambda: self.edit_name_popup("inventorySubLocations",
                                                               locations_sub_locs_dict[sub_locations_value.get()],
                                                               edit_sublocations_popup,
                                                               True)).grid(
                    row=row_counter, column=3, sticky=tk.W, padx=10, pady=10)
            row_counter += 1
        if self.active_user[1] == 1:
            tk.Label(edit_sublocations_popup,
                     text="Add New Sub-location",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                     row=row_counter, column=0, columnspan=3, sticky=tk.W, pady=10, padx=10)
        else:
            tk.Label(edit_sublocations_popup,
                     text="Request New Sub-location",
                     font=self.formatting.homepage_window_select_button_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_2).grid(
                     row=row_counter, column=0, columnspan=3, sticky=tk.W, pady=10, padx=10)
        row_counter += 1
        tk.Label(edit_sublocations_popup,
                 text="Name: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=row_counter, column=0, sticky=tk.W, pady=10, padx=10)
        sub_location_name = tk.Entry(edit_sublocations_popup)
        sub_location_name.config(state=tk.NORMAL)
        sub_location_name.grid(row=row_counter, column=1, sticky=tk.W, pady=10)
        if self.active_user[1] == 1:
            row_counter += 1
            tk.Button(edit_sublocations_popup,
                      text="Add new Sub-location",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_sub_location(current_location_record[0],
                                                                        sub_location_name.get(),
                                                                        "",
                                                                        edit_sublocations_popup,
                                                                        locations_popup,
                                                                        row_counter)).grid(
                row=row_counter-1, column=2, columnspan=2, sticky=tk.W, padx=10, pady=10)
        else:
            row_counter += 1
            tk.Button(edit_sublocations_popup,
                      text="Request new Sub-location",
                      font=self.formatting.medium_step_font,
                      command=lambda: self.check_for_blank_sub_location(current_location_record[0],
                                                                        sub_location_name.get(),
                                                                        "",
                                                                        edit_sublocations_popup,
                                                                        locations_popup,
                                                                        row_counter)).grid(
                row=row_counter-1, column=2, columnspan=2, sticky=tk.W, padx=10, pady=10)

    def archive_sublocation_and_reload_page(self,
                                            subcategory_to_archive,
                                            edit_subcategories_popup,
                                            vendor_or_category_popup):
        self.edit_db.archive_entry_in_table_by_id("inventorySubLocations", subcategory_to_archive)
        edit_subcategories_popup.destroy()
        vendor_or_category_popup.destroy()
        self.parent.display_locations_view(
            self.active_user,
            search_by=self.search_by_active_term)

    def archive_location_popup(self, location_to_archive):
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
                                 location_to_archive,
                                 are_you_sure_logout_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)
        no_i_aint = tk.Button(are_you_sure_logout_popup,
                              text="No",
                              font=self.formatting.medium_step_font,
                              command=lambda: are_you_sure_logout_popup.destroy()).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    def destroy_popup_archive_product_and_reload(self, location_to_archive, top_level_window):
        self.edit_db.archive_entry_in_table_by_id("inventoryLocations", location_to_archive[0])
        self.parent.display_locations_view(
            self.active_user,
            search_by=self.search_by_active_term)
        top_level_window.destroy()

    def check_for_blank_sub_location(self,
                                     current_location_id,
                                     sub_location_name,
                                     sub_location_comments,
                                     edit_sublocations_popup,
                                     locations_popup,
                                     row_counter,
                                     request=False):
        check = self.error_handling.checkBlankEntry(sub_location_name)
        if check:
            if request:
                self.add_new_sub_location((current_location_id,
                                           sub_location_name,
                                           sub_location_comments),
                                          edit_sublocations_popup,
                                          locations_popup,
                                          request)
            else:
                self.add_new_sub_location((current_location_id,
                                           sub_location_name,
                                           sub_location_comments),
                                          edit_sublocations_popup,
                                          locations_popup)
        else:
            tk.Label(edit_sublocations_popup,
                     text="Name cannot be blank.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=row_counter, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)

    def add_new_sub_location(self,
                             values,
                             edit_sublocations_popup,
                             locations_popup,
                             request=False):
        if request:
            self.add_delete_db.new_sub_inventory_location_record(values)
        else:
            self.add_delete_db.new_sub_inventory_location_record(values)
        edit_sublocations_popup.destroy()
        locations_popup.destroy()
        self.parent.display_locations_view(
            self.active_user,
            search_by=self.search_by_active_term)

    def check_for_blank_name_edit(self,
                                  table_to_edit,
                                  name_to_edit,
                                  location,
                                  individual_cat_vendor_popup,
                                  edit_notes_popup):
        check = self.error_handling.checkBlankEntry(name_to_edit)
        if check:
            self.commit_edit_query_close_edit_popup_and_reload(table_to_edit,
                                                               name_to_edit,
                                                               location,
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

    def check_for_blank_new_location(self,
                                     table_to_add_to,
                                     location_name,
                                     location_comments,
                                     add_new_popup,
                                     request=False):
        check = self.error_handling.checkBlankEntry(location_name)
        if check:
            if request:
                self.add_new_location((location_name,
                                       location_comments,
                                       "0"),
                                      add_new_popup,
                                      request)
            else:
                self.add_new_location((location_name,
                                       location_comments),
                                      add_new_popup)
        else:
            tk.Label(add_new_popup,
                     text="Name cannot be blank.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=4, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)

    def add_new_location(self,
                         values,
                         add_new_window,
                         request=False):
        if request:
            self.add_delete_db.new_inventory_location_record(values)
        else:
            self.add_delete_db.new_inventory_location_record(values)
        add_new_window.destroy()
        self.parent.display_locations_view(
            self.active_user,
            search_by=self.search_by_active_term)

    def commit_edit_query_close_edit_popup_and_reload(self,
                                                      table_to_edit,
                                                      new_value_entry,
                                                      location,
                                                      field_to_edit,
                                                      top_level_window,
                                                      category_vendor_window):
        if field_to_edit == "name check":
            if table_to_edit == "inventoryLocations":
                field_to_edit = "locations_name"
            elif table_to_edit == "inventorySubLocations":
                field_to_edit = "sub_locations_name"
        try:
            new_value_entry = new_value_entry.get()
        except AttributeError:
            pass
        self.edit_db.edit_one_record_one_field_one_table(table_to_edit,
                                                         field_to_edit,
                                                         new_value_entry,
                                                         location[0])
        top_level_window.destroy()
        category_vendor_window.destroy()
        self.parent.display_locations_view(
            self.active_user,
            search_by=self.search_by_active_term)
