import tkinter as tk
import GUI.GUI_formatting.Formatting as tk_formatting


class BannerView(tk.Frame):

    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.formatting = tk_formatting.TkFormattingMethods()

    def make_banner(self):
        main_banner = tk.Label(self,
                               text="RoverResources",
                               font=self.formatting.banner_font,
                               bg=self.formatting.colour_code_1,
                               fg=self.formatting.colour_code_2)
        main_banner.grid(sticky=tk.W, padx=10)
