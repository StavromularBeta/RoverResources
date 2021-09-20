import tkinter as tk
import GUI.GUI_views.GUI_banner_view as Bb
import GUI.GUI_views.GUI_main_view as Mw
import GUI.GUI_formatting.GUI_formatting as tk_formatting


class MainApplication(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.formatting = tk_formatting.TkFormattingMethods()
        parent.config(bg=self.formatting.colour_code_1)
        # Banner Window
        self.BannerBar = Bb.BannerView(self, width=1300)
        self.BannerBar.config(bg=self.formatting.colour_code_1)
        self.BannerBar.pack(side="top", fill="x", expand=True)
        self.BannerBar.pack_propagate(0)
        self.BannerBar.make_banner()
        # Main Window
        self.MainWindow = Mw.MainWindow(self)
        self.MainWindow.pack(side="bottom", fill="both", expand=True)
        self.MainWindow.config(bg=self.formatting.colour_code_1)
        self.MainWindow.pack_propagate(0)
        self.MainWindow.display_login_view()


root = tk.Tk()
root.geometry("1300x800")
MainApplication(root, height=800, width=1300).grid()
root.mainloop()
