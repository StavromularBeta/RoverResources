import tkinter as tk
from GUI.GUI_views.GUI_views_main import LoginView as lv


class MainWindow(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.login_view = lv.LoginView(self)

    def clear_main_window(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.login_view = lv.LoginView(self)

    def display_login_view(self):
        self.clear_main_window()
        self.login_view.login_view()
        self.login_view.grid()
