import datetime
import tkinter as tk
import os.path
import errno
from GUI.GUI_formatting import GUI_formatting as tk_formatting


class TkDataExportMethods:

    def __init__(self):
        # gets current working directory
        cwd = os.getcwd()
        # splits current working directory
        cwd = cwd.split("\\")
        # removes any sub-directories after the main RoverResources directory if they exist
        cwd = cwd[0:cwd.index("RoverResources")+1]
        # concatenates list back into string
        cwd = "\\".join(cwd)
        # adds desired sub-directories
        target = cwd + r'\EXPORTS\ '
        # adds name of database to end of target
        self.file_name = target[:-1]
        self.table_to_export = ""
        self.active_user = ""
        self.view_to_print = ""
        self.formatting = tk_formatting.TkFormattingMethods()
        self.text_file_header_labels = {"products": ["Product Name",
                                                     "Product ID",
                                                     "Vendor Name",
                                                     "Category Name",
                                                     "Sub-Category",
                                                     "Unit of Issue"],
                                        "requests": ["Product Name",
                                                     "Product Code",
                                                     "Vendor Name",
                                                     "Category Name",
                                                     "Request Date",
                                                     "Unit of Issue",
                                                     "Cost Per Unit",
                                                     "Amount Requested",
                                                     "Staff Member"],
                                        "orders": ["Product Name",
                                                   "Product Code",
                                                   "Vendor Name",
                                                   "Category",
                                                   "Order Date",
                                                   "Unit of Issue",
                                                   "Cost",
                                                   "Staff Member",
                                                   "Amount Requested",
                                                   "Amount Ordered"],
                                        "inventory": ["INV Number",
                                                      "Product Name",
                                                      "Product ID",
                                                      "Category",
                                                      "Vendor",
                                                      "Unit of Issue",
                                                      "Receive Date",
                                                      "Full Units Remaining",
                                                      "Partial Units Remaining",
                                                      "Location",
                                                      "Sub-Location",
                                                      "Last Updated"]}

    def generate_data_export_popup(self,
                                   active_user,
                                   table_to_export,
                                   view_to_print):
        self.active_user = active_user
        self.table_to_export = table_to_export
        self.view_to_print = view_to_print
        self.file_name += str(datetime.date.today()) + "_" + self.view_to_print + ".csv"
        # Popup
        generate_data_export_popup = tk.Toplevel()
        generate_data_export_popup.config(bg=self.formatting.colour_code_1)
        generate_data_export_popup.geometry('500x90')
        self.write_to_file()

    def write_to_file(self):
        with self.safe_open_w(self.file_name) as f:
            for item in self.text_file_header_labels[self.view_to_print]:
                f.write(item + ",")
            f.write("\n")
            if self.view_to_print == "products":
                for item in self.table_to_export:
                    f.write(item[1].replace(",", "-") + "," + item[2] + "," + item[3] + "," + item[4] + "," + item[5] + "," + item[9] + ",\n")
            elif self.view_to_print == "requests":
                for item in self.table_to_export:
                    f.write(item[0].replace(",", "-") + "," + item[1] + "," + item[2] + "," + item[3] + "," + item[4] + "," + str(item[7]) + "," + str(item[8]) + "," + str(item[5]) + "," + item[6] + ",\n")
            elif self.view_to_print == "orders":
                for item in self.table_to_export:
                    f.write(item[0].replace(",", "-") + "," + item[1] + "," + item[2] + "," + item[3] + "," + item[9] + "," + str(item[4]) + "," + str(item[5]) + "," + item[6] + "," + str(item[7]) + "," + str(item[8]) + ",\n")
            elif self.view_to_print == "inventory":
                for item in self.table_to_export:
                    f.write(str(item[18]) +
                            "," + item[0].replace(",", "-") +
                            "," + item[1] +
                            "," + item[2] +
                            "," + item[3] +
                            "," + str(item[4]) +
                            "," + str(item[5]) +
                            "," + str(item[6]) +
                            "," + str(item[7]) +
                            "," + item[8] +
                            "," + item[9] +
                            "," + item[10] + ",\n")

    def mkdir_p(self, path):
        """tries to make the directory."""
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def safe_open_w(self, path):
        """ Open "path" for writing, creating any parent directories as needed. """
        self.mkdir_p(os.path.dirname(path))
        return open(path, 'w', encoding="utf-8")