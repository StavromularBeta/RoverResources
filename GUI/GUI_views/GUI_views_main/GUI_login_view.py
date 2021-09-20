import tkinter as tk
from SQL import dB_select
import time
from GUI.GUI_formatting import GUI_formatting as tk_formatting


class LoginView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.formatting = tk_formatting.TkFormattingMethods()
        self.select_db = dB_select.Select()
        self.config(bg=self.formatting.colour_code_1)
        self.user_name = tk.Entry()
        self.password = tk.Entry()
        self.user_logging_in = ""
        self.user_success_label = tk.Label(self)

    def login_view(self):
        login_frame = self.generate_login_widgets()
        login_button_frame = self.generate_login_button()
        login_frame.grid(row=0)
        login_button_frame.grid(row=1, sticky=tk.W)

    def generate_login_widgets(self):
        login_frame = tk.Frame(self)
        login_frame.config(bg=self.formatting.colour_code_1)
        tk.Label(login_frame,
                 text="Username: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, padx=10, pady=5)
        self.user_name = tk.Entry(login_frame,
                                  width=25)
        self.user_name.config(bg=self.formatting.colour_code_2,
                              fg=self.formatting.colour_code_1,
                              font=self.formatting.medium_step_font)
        self.user_name.grid(row=0, column=1, sticky='NSEW', padx=10, pady=5)
        tk.Label(login_frame,
                 text="Password: ",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=1, column=0, padx=10, pady=5)
        self.password = tk.Entry(login_frame,
                                 width=25)
        self.password.config(bg=self.formatting.colour_code_2,
                             fg=self.formatting.colour_code_1,
                             font=self.formatting.medium_step_font,
                             show="*")
        self.password.grid(row=1, column=1, sticky='NSEW', padx=10, pady=5)
        return login_frame

    def generate_login_button(self):
        login_button_frame = tk.Frame(self)
        login_button_frame.config(bg=self.formatting.colour_code_1)
        login_button = tk.Button(login_button_frame,
                                 text="Login",
                                 font=self.formatting.medium_step_font,
                                 command=lambda: self.check_if_username_is_match())
        login_button.grid(row=0, column=0, padx=10, pady=5)
        return login_button_frame

    def check_if_username_is_match(self):
        user_name_input = self.user_name.get()
        password_input = self.password.get()
        search_for_user_name = self.select_db.select_all_from_table_where_one_field_equals("users",
                                                                                           "user_name",
                                                                                           user_name_input)
        password_match = False
        for item in search_for_user_name:
            if item[3] == password_input:
                password_match = True
                self.user_logging_in = item
                if item[1] == 1:
                    self.parent.display_admin_shopping_cart_view(self.user_logging_in)
                else:
                    self.parent.display_shopping_cart_view(self.user_logging_in)
        if not password_match:
            self.user_success_label = tk.Label(self,
                                               text="Incorrect Username or Password.",
                                               font=self.formatting.medium_step_font,
                                               bg=self.formatting.colour_code_1,
                                               fg=self.formatting.colour_code_2)
            self.user_success_label.grid(row=2, sticky=tk.W)


