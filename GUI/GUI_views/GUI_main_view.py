import tkinter as tk
import time
from GUI.GUI_views.GUI_views_main import GUI_top_select_view as ts
from GUI.GUI_views.GUI_views_main import GUI_login_view as lv
from GUI.GUI_views.GUI_views_main import GUI_categories_vendors_view as cv
from GUI.GUI_views.GUI_views_main import GUI_product_list_view as pl
from GUI.GUI_views.GUI_views_main import GUI_shopping_cart_view as sc
from GUI.GUI_views.GUI_views_main import GUI_shopping_cart_view_admin as sc_admin
from GUI.GUI_views.GUI_views_main import GUI_orders_view as ord
from GUI.GUI_views.GUI_views_main import GUI_approvals_view as apr
from GUI.GUI_views.GUI_views_main import GUI_archives_view as arc
from GUI.GUI_views.GUI_views_main import GUI_users_view as usr
from GUI.GUI_views.GUI_views_main import GUI_received_view as rcv
from GUI.GUI_views.GUI_views_main import GUI_inventory_view as inv
from GUI.GUI_views.GUI_views_main import GUI_locations_view as loca


class MainWindow(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.login_view = lv.LoginView(self)
        self.top_select_view = ts.TopSelectView(self)
        self.categories_vendors_view = cv.CategoriesVendorsView(self)
        self.product_list_view = pl.ProductListView(self)
        self.shopping_cart_view = sc.ShoppingCartView(self)
        self.shopping_cart_view_admin = sc_admin.ShoppingCartViewAdmin(self)
        self.orders_view = ord.OrdersView(self)
        self.approvals_view = apr.ApprovalsView(self)
        self.archives_view = arc.ArchivesView(self)
        self.users_view = usr.UsersView(self)
        self.received_view = rcv.ReceivedView(self)
        self.inventory_view = inv.InventoryView(self)
        self.locations_view = loca.LocationsView(self)

    def clear_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.login_view = lv.LoginView(self)
        self.top_select_view = ts.TopSelectView(self)
        self.categories_vendors_view = cv.CategoriesVendorsView(self)
        self.product_list_view = pl.ProductListView(self)
        self.shopping_cart_view = sc.ShoppingCartView(self)
        self.shopping_cart_view_admin = sc_admin.ShoppingCartViewAdmin(self)
        self.orders_view = ord.OrdersView(self)
        self.approvals_view = apr.ApprovalsView(self)
        self.archives_view = arc.ArchivesView(self)
        self.users_view = usr.UsersView(self)
        self.received_view = rcv.ReceivedView(self)
        self.inventory_view = inv.InventoryView(self)
        self.locations_view = loca.LocationsView(self)

    def display_login_view(self):
        self.clear_main_window()
        self.login_view.login_view()
        self.login_view.grid()

    def display_top_frame_select_button_view(self, user):
        self.top_select_view.create_top_view_buttons(user)

    def display_users_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.users_view.users_view(user, sort_by=sort_by, search_by=search_by, search_by_variable=search_by_variable)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.users_view.grid(sticky=tk.W, padx=10)

    def display_categories_and_vendors_view(self, user, vendor_search=False, category_search=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.categories_vendors_view.categories_and_vendors_view(user, vendor_search, category_search)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.categories_vendors_view.grid(sticky=tk.W, padx=10)

    def display_products_list_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.product_list_view.products_list_view(user,
                                                  sort_by=sort_by,
                                                  search_by=search_by,
                                                  search_by_variable=search_by_variable)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.product_list_view.grid(sticky=tk.W, padx=10)

    def display_shopping_cart_view(self,
                                   user,
                                   product_sort_by=False,
                                   product_search_by=False,
                                   product_search_by_variable=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.shopping_cart_view.shopping_cart_view(user, product_sort_by, product_search_by, product_search_by_variable)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.shopping_cart_view.grid(sticky=tk.W, padx=10)

    def display_admin_shopping_cart_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.shopping_cart_view_admin.shopping_cart_view_admin(user, sort_by, search_by, search_by_variable)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.shopping_cart_view_admin.grid()

    def display_orders_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.orders_view.orders_view(user, sort_by, search_by, search_by_variable)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.orders_view.grid()

    def display_received_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.received_view.received_view(user, sort_by, search_by, search_by_variable)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.received_view.grid()

    def display_inventory_view(self, user, sort_by=False, search_by=False, search_by_variable=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.inventory_view.inventory_view(user, sort_by, search_by, search_by_variable)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.inventory_view.grid()

    def display_locations_view(self, user, search_by=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.locations_view.locations_view(user, search_by)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.locations_view.grid()

    def display_approvals_view(self, user, sort_by=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.approvals_view.approvals_view(user, sort_by)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.approvals_view.grid()

    def display_archives_view(self, user, sort_by=False):
        self.clear_main_window()
        self.display_top_frame_select_button_view(user)
        self.archives_view.archives_view(user, sort_by)
        self.top_select_view.grid(sticky=tk.W, padx=10)
        self.archives_view.grid()

