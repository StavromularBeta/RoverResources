import datetime
from tkinter import font as tk_font
import tkinter as tk


class TkFormattingMethods:

    def __init__(self):
        # self.colour_code_1 = "#5e98b4"
        self.colour_code_1 = "#313ead"
        self.colour_code_2 = "#e3eaee"
        # self.colour_code_3 = "#e6e7bd"
        self.colour_code_3 = "#fbff87"
        # self.colour_code_green = '#186915'
        self.colour_code_green = "#16cb0d"
        # self.colour_code_red = '#9e3315'
        self.colour_code_red = "#ef4715"
        # self.colour_code_purple = '#5c3882'
        self.colour_code_purple = "#e57ff7"
        self.banner_font = tk_font.Font(size=48, weight="bold")
        self.homepage_window_select_button_font = tk_font.Font(size=18, weight="bold")
        self.medium_step_font = tk_font.Font(size=12, weight="bold")

    def create_shopping_cart_labels(self,
                                    frame,
                                    text,
                                    text_colour):
        label_to_return = tk.Label(frame,
                                   text=text,
                                   font=self.medium_step_font,
                                   bg=self.colour_code_1,
                                   fg=text_colour,
                                   wraplength=200,
                                   justify=tk.LEFT)
        return label_to_return

    def create_double_width_shopping_cart_labels(self,
                                                 frame,
                                                 text,
                                                 text_colour):
        label_to_return = tk.Label(frame,
                                   text=text,
                                   font=self.medium_step_font,
                                   bg=self.colour_code_1,
                                   fg=text_colour,
                                   wraplength=400,
                                   justify=tk.LEFT)
        return label_to_return

    def grid_shopping_cart_labels(self,
                                  label,
                                  row,
                                  column):
        label.grid(row=row, column=column, sticky=tk.W, padx=10, pady=5)

    def insert_newlines(self,
                        string,
                        when_to_newline):
        return '\n'.join(string[i:i+when_to_newline] for i in range(0, len(string), when_to_newline))

    def lab_date_format(self,
                        date_to_convert):
        year = date_to_convert.split("-")[0]
        month = date_to_convert.split("-")[1]
        day = date_to_convert.split("-")[2]
        datetime_format = datetime.datetime(int(year),
                                            int(month),
                                            int(day))
        lab_format = datetime_format.strftime("%d%b%y")
        return lab_format
