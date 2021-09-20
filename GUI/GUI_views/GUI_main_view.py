import tkinter as tk
import time
from GUI.GUI_views.GUI_views_main import GUI_login_view as lv
from GUI.GUI_views.GUI_views_main import GUI_shopping_cart_view as sc


class MainWindow(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.login_view = lv.LoginView(self)
        self.shopping_cart_view = sc.ShoppingCartView(self)

    def clear_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.login_view = lv.LoginView(self)
        self.shopping_cart_view = sc.ShoppingCartView(self)

    def display_login_view(self):
        self.clear_main_window()
        self.login_view.login_view()
        self.login_view.grid()

    def display_shopping_cart_view(self, user):
        self.clear_main_window()
        self.shopping_cart_view.shopping_cart_view(user)
        self.shopping_cart_view.grid()

