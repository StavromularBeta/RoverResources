import tkinter as tk
from SQL import dB_select
from SQL import dB_add_delete
from SQL import dB_edit
from GUI.GUI_formatting import GUI_formatting as tk_formatting
from GUI.GUI_formatting import GUI_errorHandling as tk_errorHandling


class UsersView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.active_user = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.error_handling = tk_errorHandling.ErrorHandling()
        self.select_db = dB_select.Select()
        self.add_delete_db = dB_add_delete.AddDelete()
        self.edit_db = dB_edit.EditDb()
        self.config(bg=self.formatting.colour_code_1)
        self.users_list_navigation_frame = tk.Frame(self)
        self.users_list_navigation_frame.config(bg=self.formatting.colour_code_2)
        self.users_list_scrollable_container = tk.Frame(self)
        self.users_list_frame = tk.Frame(self)
        self.users_list_frame.config(bg=self.formatting.colour_code_1)
        self.users_list_canvas_length = 0
        self.users_list = ()

    def users_view(self, user):
        self.active_user = user
        self.create_users_list()

    def create_users_list(self):
        self.create_users_list_navigation_frame()
        self.get_users_list_from_database()
        self.make_scrollable_users_list_header_labels()
        self.populate_scrollable_users_list()
        self.create_scrollable_users_list()
        self.users_list_navigation_frame.grid(sticky=tk.W, pady=10)
        self.users_list_scrollable_container.grid()

    def create_users_list_navigation_frame(self):
        tk.Label(self.users_list_navigation_frame,
                 text="Users List",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_2,
                 fg=self.formatting.colour_code_1).grid(row=0, column=0, sticky=tk.W, pady=5)
        tk.Button(self.users_list_navigation_frame,
                  text="Add New User",
                  font=self.formatting.medium_step_font,
                  command= lambda: self.new_user_popup()).grid(row=0,
                                                               column=1,
                                                               sticky=tk.W,
                                                               padx=10,
                                                               pady=5)

    def get_users_list_from_database(self):
        self.users_list = self.select_db.left_join_multiple_tables(
            "u.id, u.user_name, cr.credential_level, u.user_password, u.comments",
            [["users u", "", "u.credentials_id"],
             ["credentials cr", "cr.id", ""]],
            "u.user_name",
            no_archive="u.archived"
            )

    def make_scrollable_users_list_header_labels(self):
        tk.Label(self.users_list_frame,
                 text="User Name",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(self.users_list_frame,
                 text="Credential Level",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)

    def populate_scrollable_users_list(self):
        row_counter = 1
        even_odd = 1
        for item in self.users_list:
            if even_odd % 2 == 0:
                text_color = self.formatting.colour_code_2
            else:
                text_color = self.formatting.colour_code_3
            tk.Label(self.users_list_frame,
                     text=item[1],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=0, sticky=tk.W, padx=10, pady=5)
            tk.Label(self.users_list_frame,
                     text=item[2],
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=text_color).grid(row=row_counter, column=1, sticky=tk.W, padx=10, pady=5)
            tk.Button(self.users_list_frame,
                      text="Open",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.open_user_popup(item)).grid(row=row_counter,
                                                                                 column=2,
                                                                                 sticky=tk.W,
                                                                                 padx=10,
                                                                                 pady=5)
            tk.Button(self.users_list_frame,
                      text="Archive",
                      font=self.formatting.medium_step_font,
                      command=lambda item=item: self.archive_user_and_reload(item)).grid(row=row_counter,
                                                                                         column=3,
                                                                                         sticky=tk.W,
                                                                                         padx=10,
                                                                                         pady=5)
            self.users_list_canvas_length += 50
            row_counter += 1
            even_odd += 1

    def create_scrollable_users_list(self):
        products_list_canvas = tk.Canvas(self.users_list_scrollable_container,
                                         width=1200,
                                         height=550,
                                         scrollregion=(0, 0, 0, self.users_list_canvas_length),
                                         bd=0,
                                         highlightthickness=0)
        products_list_canvas.config(bg=self.formatting.colour_code_1)
        products_list_canvas_scrollbar = tk.Scrollbar(self.users_list_scrollable_container,
                                                      orient="vertical",
                                                      command=products_list_canvas.yview)
        products_list_canvas.configure(yscrollcommand=products_list_canvas_scrollbar.set)
        products_list_canvas_scrollbar.pack(side='left',
                                            fill='y')
        products_list_canvas.pack(side="right",
                                  fill='y')
        products_list_canvas.create_window((0, 0),
                                           window=self.users_list_frame,
                                           anchor="nw")

    def open_user_popup(self, user):
        open_user_popup = tk.Toplevel()
        open_user_popup.config(bg=self.formatting.colour_code_1)
        open_user_popup.geometry('600x400')
        tk.Label(open_user_popup,
                 text="Individual User Page",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=0, column=0, columnspan=4, sticky=tk.W, padx=10, pady=5)
        tk.Label(open_user_popup,
                 text="Name:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(open_user_popup,
                 text=user[1],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Button(open_user_popup,
                  text="Edit",
                  font=self.formatting.medium_step_font,
                  command=lambda user=user: self.edit_name_popup(user, open_user_popup)).grid(
            row=1,
            column=2,
            sticky=tk.W,
            padx=10,
            pady=5)
        tk.Label(open_user_popup,
                 text="Credential Level:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(open_user_popup,
                 text=user[2],
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_3).grid(
            row=2, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Button(open_user_popup,
                  text="Change",
                  font=self.formatting.medium_step_font,
                  command=lambda user=user: self.change_credential_level_popup(user,
                                                                               open_user_popup)).grid(
            row=2,
            column=2,
            sticky=tk.W,
            padx=10,
            pady=5)
        user_notes = tk.Text(open_user_popup,
                             height=5,
                             width=40)
        user_notes.config(bg=self.formatting.colour_code_2)
        user_notes.insert(tk.END, user[4])
        user_notes.config(state=tk.DISABLED, wrap="word")
        user_notes.grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        tk.Button(open_user_popup,
                  text="Edit Notes",
                  font=self.formatting.medium_step_font,
                  command=lambda user=user: self.edit_notes_popup(user, open_user_popup)).grid(
            row=4,
            column=0,
            sticky=tk.W,
            padx=10,
            pady=5)
        tk.Button(open_user_popup,
                  text="Reset Password",
                  font=self.formatting.medium_step_font,
                  command=lambda user=user: self.reset_password_popup(user, open_user_popup)).grid(
            row=4,
            column=1,
            sticky=tk.W,
            padx=10,
            pady=5)

    def new_user_popup(self):
        credentials = self.select_db.select_all_from_table("credentials")
        credentials_var = tk.StringVar()
        credentials_list = [item for item in credentials]
        credentials_tk_dict = {}
        credentials_tk_list = []
        for item in credentials_list:
            credentials_tk_list.append(item[1])
            credentials_tk_dict[item[1]] = item[0]
        credentials_var.set(credentials_tk_list[0])
        new_user_popup = tk.Toplevel()
        new_user_popup.config(bg=self.formatting.colour_code_1)
        new_user_popup.geometry('600x450')
        tk.Label(new_user_popup,
                 text="New User Page",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Label(new_user_popup,
                 text="Name:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=5)
        user_name_entry = tk.Entry(new_user_popup)
        user_name_entry.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(new_user_popup,
                 text="Credential Level:",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=5)
        credentials_menu = tk.OptionMenu(new_user_popup,
                                         credentials_var,
                                         *credentials_tk_list)
        credentials_menu.config(highlightbackground=self.formatting.colour_code_1)
        credentials_menu.config(font=self.formatting.medium_step_font)
        credentials_menu.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(new_user_popup,
                 text="Notes",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=3, column=0, sticky=tk.W, padx=10, pady=5)
        user_notes = tk.Text(new_user_popup,
                             height=5,
                             width=40)
        user_notes.config(bg=self.formatting.colour_code_2)
        user_notes.config(state=tk.NORMAL, wrap="word")
        user_notes.grid(row=4, column=0, columnspan=4, sticky=tk.W, padx=10, pady=10)
        tk.Label(new_user_popup,
                 text="Password: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=5, column=0, sticky=tk.W, padx=10, pady=5)
        password_entry = tk.Entry(new_user_popup)
        password_entry.config(show="*")
        password_entry.grid(row=5, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Label(new_user_popup,
                 text="Confirm Password: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(
            row=6, column=0, sticky=tk.W, padx=10, pady=5)
        password_confirm_entry = tk.Entry(new_user_popup)
        password_confirm_entry.config(show="*")
        password_confirm_entry.grid(row=6, column=1, sticky=tk.W, padx=10, pady=5)
        tk.Button(new_user_popup,
                  text="Add New User",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.check_user_name_and_matching_passwords_and_add_new_user(
                      user_name_entry.get(),
                      credentials_tk_dict[credentials_var.get()],
                      user_notes.get("1.0", tk.END),
                      password_entry.get(),
                      password_confirm_entry.get(),
                      new_user_popup
                  )).grid(row=7, column=0, sticky=tk.W, padx=10, pady=5)

    def reset_password_popup(self, user, individual_user_popup):
        are_you_sure_logout_popup = tk.Toplevel()
        are_you_sure_logout_popup.config(bg=self.formatting.colour_code_1)
        are_you_sure_logout_popup.geometry('500x90')
        tk.Label(are_you_sure_logout_popup,
                 text="Password will be reset to '1234'. Continue?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Button(are_you_sure_logout_popup,
                  text="Yes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(
                      "1234",
                      user,
                      "user_password",
                      individual_user_popup,
                      are_you_sure_logout_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)

    def edit_notes_popup(self, user, individual_user_popup):
        edit_notes_popup = tk.Toplevel()
        edit_notes_popup.config(bg=self.formatting.colour_code_1)
        edit_notes_popup.geometry('500x160')
        user_notes = tk.Text(edit_notes_popup,
                             height=5,
                             width=40)
        user_notes.config(bg=self.formatting.colour_code_2)
        user_notes.config(state=tk.NORMAL)
        user_notes.insert(tk.END, user[4])
        user_notes.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_notes_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(user_notes.get("1.0", tk.END),
                                                                                     user,
                                                                                     "comments",
                                                                                     individual_user_popup,
                                                                                     edit_notes_popup)).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10)

    def edit_name_popup(self, user, individual_user_popup):
        edit_name_popup = tk.Toplevel()
        edit_name_popup.config(bg=self.formatting.colour_code_1)
        edit_name_popup.geometry('500x90')
        edit_name_entry = tk.Entry(edit_name_popup)
        edit_name_entry.config(state=tk.NORMAL)
        edit_name_entry.insert(tk.END, user[1])
        edit_name_entry.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        tk.Button(edit_name_popup,
                  text="Commit Changes",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.check_for_blank_name_edit(edit_name_entry.get(),
                                                                 user,
                                                                 individual_user_popup,
                                                                 edit_name_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)

    def change_credential_level_popup(self, user, individual_user_popup):
        credentials = self.select_db.select_all_from_table("credentials")
        change_credentials_popup = tk.Toplevel()
        change_credentials_popup.config(bg=self.formatting.colour_code_1)
        change_credentials_popup.geometry('500x90')
        credentials_var = tk.StringVar()
        credentials_list = [item for item in credentials]
        credentials_tk_dict = {}
        credentials_tk_list = []
        for item in credentials_list:
            credentials_tk_list.append(item[1])
            credentials_tk_dict[item[1]] = item[0]
        credentials_var.set(credentials_tk_list[0])
        credentials_menu = tk.OptionMenu(change_credentials_popup,
                                         credentials_var,
                                         *credentials_tk_list)
        tk.Label(change_credentials_popup,
                 text="Edit Credentials",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        credentials_menu.config(highlightbackground=self.formatting.colour_code_1)
        credentials_menu.config(font=self.formatting.medium_step_font)
        credentials_menu.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        tk.Button(change_credentials_popup,
                  text="Set Credential Level",
                  font=self.formatting.medium_step_font,
                  command=lambda: self.commit_edit_query_close_edit_popup_and_reload(
                      credentials_tk_dict[credentials_var.get()],
                      user,
                      "credentials_id",
                      individual_user_popup,
                      change_credentials_popup
                  )).grid(
                row=1, column=1, columnspan=2, sticky=tk.W, padx=10, pady=5)

    def check_user_name_and_matching_passwords_and_add_new_user(self,
                                                                user_name,
                                                                credential_level,
                                                                comments,
                                                                password_entry,
                                                                password_check_entry,
                                                                new_user_popup):
        password_check = False
        if password_entry == password_check_entry:
            password_check = True
        if password_check:
            blank_check = self.error_handling.checkBlankEntry(user_name)
            if blank_check:
                # can add new user
                self.add_delete_db.new_user_record((credential_level,
                                                    user_name,
                                                    password_entry,
                                                    comments))
                new_user_popup.destroy()
                self.parent.display_users_view(self.active_user)
            else:
                # passwords match but name is blank
                tk.Label(new_user_popup,
                         text="Name cannot be blank, can't add new user.",
                         font=self.formatting.medium_step_font,
                         bg=self.formatting.colour_code_1,
                         fg=self.formatting.colour_code_3).grid(
                    row=8, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)
        else:
            # passwords don't match
            tk.Label(new_user_popup,
                     text="Passwords don't match, can't add new user.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                    row=8, column=0, columnspan=3, sticky=tk.W, padx=10, pady=5)

    def check_for_blank_name_edit(self,
                                  name_to_edit,
                                  user,
                                  top_level_window,
                                  edit_name_window):
        check = self.error_handling.checkBlankEntry(name_to_edit)
        if check:
            self.commit_edit_query_close_edit_popup_and_reload(name_to_edit,
                                                               user,
                                                               "user_name",
                                                               top_level_window,
                                                               edit_name_window
                                                               )
        else:
            tk.Label(edit_name_window,
                     text="Name cannot be blank.",
                     font=self.formatting.medium_step_font,
                     bg=self.formatting.colour_code_1,
                     fg=self.formatting.colour_code_3).grid(
                row=1, column=0, columnspan=2, sticky=tk.W, pady=10, padx=10)

    def archive_user_and_reload(self, user_to_archive):
        self.edit_db.archive_entry_in_table_by_id("users", user_to_archive[0])
        self.parent.display_users_view(self.active_user)

    def commit_edit_query_close_edit_popup_and_reload(self,
                                                      new_value_entry,
                                                      user_to_edit,
                                                      field_to_edit,
                                                      top_level_window,
                                                      edit_notes_window):
        try:
            new_value_entry = new_value_entry.get()
        except AttributeError:
            pass
        self.edit_db.edit_one_record_one_field_one_table("users", field_to_edit, new_value_entry, user_to_edit[0])
        top_level_window.destroy()
        edit_notes_window.destroy()
        self.parent.display_users_view(self.active_user)
