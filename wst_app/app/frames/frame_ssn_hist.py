
import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image
import pyperclip
import os
import sys
from .components import session_comp

##
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logics


class SessionHistoryFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app  # Reference to MainApp

        dirname = os.path.join(os.path.dirname(__file__), "..", "images")
        self.bin_img = ctk.CTkImage(Image.open(os.path.join(dirname, "bin-icon2.png")))
        self.copy_img = ctk.CTkImage(Image.open(os.path.join(dirname, "copy-icon2.png")))
        self.refresh_img = ctk.CTkImage(Image.open(os.path.join(dirname, "refresh-icon2.png")))
        self.create_widgets()


    def create_widgets(self):

        # Amazon Section
        azon_lbl = ctk.CTkLabel(self, text="Amazon", font=("Georgia bold", 16), text_color="white")
        azon_lbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Refresh Session-Keys
        azon_refresh_btn = ctk.CTkButton(self, text="", width=10, image=self.refresh_img,
            fg_color="gray10", hover_color="gray15",
            command=lambda: self.update_ssn_info("Azon")
        )
        azon_refresh_btn.grid(row=0, column=1, padx=10, pady=5, sticky="e")

        # Session Keys Frame
        self.azon_ssn_frame = session_comp.SessionFrame(
            self,
            [],
            "Azon",
            height=200  # Adjust frame size as needed
        )
        self.azon_ssn_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")


        # Flipkart Section
        fkart_lbl = ctk.CTkLabel(self, text="Flipkart", font=("Georgia bold", 16), text_color="white")
        fkart_lbl.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Refresh Session-Keys
        fkart_refresh_btn = ctk.CTkButton(self, text="", width=10, image=self.refresh_img,
            fg_color="gray10", hover_color="gray15",
            command=lambda: self.update_ssn_info("Fkart")
        )
        fkart_refresh_btn.grid(row=2, column=1, padx=10, pady=5, sticky="e")

        # Session Keys Frame
        self.fkart_ssn_frame = session_comp.SessionFrame(
            self,
            [],
            "Fkart",
            # width=400, height=400  # Adjust frame size as needed
        )
        self.fkart_ssn_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")


        # root.grid_rowconfigure(0, weight=1)
        # root.grid_rowconfigure(1, weight=1)
        # root.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure(2, weight=1)


    def update_ssn_info(self, tag):
        cacheDir = os.path.join("Server", "Cache", tag)
        dirname = os.path.join(os.path.dirname(__file__), "..", "..", cacheDir)
        file_names = self.get_filenames_without_extension(dirname)
        if tag == "Azon" :
            self.azon_ssn_frame.addComponents(file_names)
        elif tag == "Fkart" :
            self.fkart_ssn_frame.addComponents(file_names)


    def get_filenames_without_extension(self, directory):
        try:
            # Step 1: Check if the directory exists
            if not os.path.isdir(directory):
                raise ValueError(f"Invalid Directory:\n{directory}")            
            # Step 2: Get the list of files in the directory
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            # Step 3: Sort the filenames in decreasing order
            files_sorted = sorted(files, reverse=True)
            # Step 4: Remove the file extensions and return the names
            filenames_without_extension = [os.path.splitext(f)[0] for f in files_sorted]
            return filenames_without_extension

        except ValueError as e:
            errHead = e.__class__.__name__
            errBody = str(ve)
            logics.log_error("ssn-hist-err.log", "frame-ssn-hist.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)

        except PermissionError as e:
            errHead = e.__class__.__name__
            errBody = f"You Don't have Permission Access:\n{directory}"
            logics.log_error("ssn-hist-err.log", "frame-ssn-hist.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)

        except FileNotFoundError as e:
            errHead = e.__class__.__name__
            errBody = f"Directory does not exist:\n{directory}"
            logics.log_error("ssn-hist-err.log", "frame-ssn-hist.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)

        except Exception as e:
            errHead = e.__class__.__name__
            errBody = str(e)
            logics.log_error("ssn-hist-err.log", "frame-ssn-hist.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)


    # # Example usage:
    # directory_path = "/path/to/your/directory"
    # result = get_filenames_without_extension(directory_path)
    # print(result)



if __name__ == "__main__" :
    root = ctk.CTk()
    SessionHistoryFrame(root, None)

    # root.grid_rowconfigure(0, weight=1)
    # root.grid_rowconfigure(1, weight=1)
    # root.grid_columnconfigure(0, weight=1)

    root.mainloop()
