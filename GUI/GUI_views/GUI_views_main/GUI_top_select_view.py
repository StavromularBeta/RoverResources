import tkinter as tk
from GUI.GUI_formatting import GUI_formatting as tk_formatting


class TopSelectView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.parent = parent
        self.formatting = tk_formatting.TkFormattingMethods()
        self.config(bg=self.formatting.colour_code_3)
        self.active_user = ""

    def create_top_view_buttons(self, user):
        column_count = 0
        self.active_user = user
        tk.Label(self,
                 text="Navigation",
                 font=self.formatting.homepage_window_select_button_font,
                 bg=self.formatting.colour_code_3,
                 fg=self.formatting.colour_code_1).grid(row=0,
                                                        column=column_count,
                                                        sticky=tk.W,
                                                        pady=5)
        column_count += 1
        log_out_button = tk.Button(self,
                                   text="Log Out",
                                   font=self.formatting.medium_step_font,
                                   command=lambda: self.are_you_sure_logout_popup())
        log_out_button.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
        column_count += 1
        if self.active_user[1] == 1:
            users_button = tk.Button(self,
                                     text="Users",
                                     font=self.formatting.medium_step_font,
                                     command=lambda: self.parent.display_users_view(self.active_user))
            users_button.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
        column_count += 1
        display_products_list = tk.Button(self,
                                          text="Categories & Vendors",
                                          font=self.formatting.medium_step_font,
                                          command=lambda:
                                          self.parent.display_categories_and_vendors_view(self.active_user))
        display_products_list.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
        column_count += 1
        display_products_list = tk.Button(self,
                                          text="Products List",
                                          font=self.formatting.medium_step_font,
                                          command=lambda: self.parent.display_products_list_view(self.active_user))
        display_products_list.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
        column_count += 1
        display_personal_cart = tk.Button(self,
                                          text="Personal Shopping Cart",
                                          font=self.formatting.medium_step_font,
                                          command=lambda: self.parent.display_shopping_cart_view(self.active_user))
        display_personal_cart.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
        column_count += 1
        if self.active_user[1] == 1:
            display_all_carts = tk.Button(self,
                                          text="All Shopping Carts",
                                          font=self.formatting.medium_step_font,
                                          command=lambda: self.parent.display_admin_shopping_cart_view(
                                              self.active_user))
            display_all_carts.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
            column_count += 1
        orders_view = tk.Button(self,
                                text="Orders",
                                font=self.formatting.medium_step_font,
                                command=lambda: self.parent.display_orders_view(
                                    self.active_user))
        orders_view.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
        column_count += 1
        received_view = tk.Button(self,
                                  text="Receiving",
                                  font=self.formatting.medium_step_font,
                                  command=lambda: self.parent.display_received_view(
                                      self.active_user))
        received_view.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
        column_count += 1
        if self.active_user[1] == 1:
            display_all_carts = tk.Button(self,
                                          text="Approvals",
                                          font=self.formatting.medium_step_font,
                                          command=lambda: self.parent.display_approvals_view(
                                              self.active_user
                                          ))
            display_all_carts.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
            column_count += 1
            display_all_carts = tk.Button(self,
                                          text="Archives",
                                          font=self.formatting.medium_step_font,
                                          command=lambda: self.parent.display_archives_view(
                                              self.active_user
                                          ))
            display_all_carts.grid(row=0, column=column_count, sticky=tk.W, padx=10, pady=5)
            column_count += 1

    def are_you_sure_logout_popup(self):
        are_you_sure_logout_popup = tk.Toplevel()
        are_you_sure_logout_popup.config(bg=self.formatting.colour_code_1)
        are_you_sure_logout_popup.geometry('400x90')
        tk.Label(are_you_sure_logout_popup,
                 text="Are you sure you want to log out?",
                 font=self.formatting.medium_step_font,
                 bg=self.formatting.colour_code_1,
                 fg=self.formatting.colour_code_2).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        yes_i_am = tk.Button(are_you_sure_logout_popup,
                             text="Yes",
                             font=self.formatting.medium_step_font,
                             command=lambda: self.destroy_popup_and_go_to_login(are_you_sure_logout_popup)).grid(
            row=0, column=1, sticky=tk.W, padx=10, pady=10)
        no_i_aint = tk.Button(are_you_sure_logout_popup,
                              text="No",
                              font=self.formatting.medium_step_font,
                              command=lambda: are_you_sure_logout_popup.destroy()).grid(
            row=0, column=2, sticky=tk.W, padx=10, pady=10)

    def destroy_popup_and_go_to_login(self, top_level_window):
        self.parent.display_login_view()
        top_level_window.destroy()
