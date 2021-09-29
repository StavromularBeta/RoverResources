import tkinter as tk
import time
from GUI.GUI_views.GUI_views_main import GUI_top_select_view as ts
from GUI.GUI_views.GUI_views_main import GUI_login_view as lv
from GUI.GUI_views.GUI_views_main import GUI_product_list_view as pl
from GUI.GUI_views.GUI_views_main import GUI_shopping_cart_view as sc
from GUI.GUI_views.GUI_views_main import GUI_shopping_cart_view_admin as sc_admin


class MainWindow(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.login_view = lv.LoginView(self)
        self.top_select_view = ts.TopSelectView(self)
        self.product_list_view = pl.ProductListView(self)
        self.shopping_cart_view = sc.ShoppingCartView(self)
        self.shopping_cart_view_admin = sc_admin.ShoppingCartViewAdmin(self)

    def clear_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.login_view = lv.LoginView(self)
        self.top_select_view = ts.TopSelectView(self)
        self.product_list_view = pl.ProductListView(self)
        self.shopping_cart_view = sc.ShoppingCartView(self)
        self.shopping_cart_view_admin = sc_admin.ShoppingCartViewAdmin(self)

    def display_login_view(self):
        self.clear_main_window()
        self.login_view.login_view()
        self.login_view.grid()

    def display_top_frame_select_button_view(self, user):
        self.top_select_view.create_top_view_buttons(user)

    def display_products_list_view(self, user):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.product_list_view.products_list_view(user)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.product_list_view.grid(sticky=tk.W, padx=10)

    def display_shopping_cart_view(self, user):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.shopping_cart_view.shopping_cart_view(user)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.shopping_cart_view.grid()

    def display_admin_shopping_cart_view(self, user, sort_by=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.shopping_cart_view_admin.shopping_cart_view_admin(user, sort_by)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.shopping_cart_view_admin.grid()

