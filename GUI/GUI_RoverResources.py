import tkinter as tk
import GUI.GUI_views.GUI_banner_view as Bb
import GUI.GUI_views.GUI_main_view as Mw
import GUI.GUI_formatting.GUI_formatting as tk_formatting


class MainApplication(tk.Frame):

    def __init__(self, parent, window_width, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)
        self.formatting = tk_formatting.TkFormattingMethods()
        parent.config(bg=self.formatting.colour_code_1)
        # Banner Window
        self.BannerBar = Bb.BannerView(self, width=window_width)
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
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
root.geometry(str(root.winfo_screenwidth()-25)+"x"+str(root.winfo_screenheight()-150).
              format(positionRight, positionDown))
MainApplication(root, root.winfo_screenwidth(), height=windowHeight, width=windowWidth).grid()
root.mainloop()
