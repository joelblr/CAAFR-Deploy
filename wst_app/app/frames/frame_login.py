
import customtkinter as ctk
import tkinter.messagebox as messagebox
from PIL import Image
import pyperclip
import threading
import os
import logics


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app  # Reference to MainApp

        dirname = os.path.join(os.path.dirname(__file__), "..", 'Images')
        self.hide_img = ctk.CTkImage(Image.open(os.path.join(dirname, "hide-icon2.png")))
        self.show_img = ctk.CTkImage(Image.open(os.path.join(dirname, "show-icon2.png")))
        self.copy_img = ctk.CTkImage(Image.open(os.path.join(dirname, "copy-icon2.png")))
        self.create_widgets()


    def create_widgets(self):

        # Amazon Section
        azon_lbl = ctk.CTkLabel(self, text="Amazon", font=("Georgia bold", 16), text_color="white")
        azon_lbl.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Gmail or Mobile
        azon_gmail_lbl = ctk.CTkLabel(self, text="Gmail or Mobile", font=("Georgia bold", 12), text_color="white")
        azon_gmail_lbl.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.azon_gmail_ent = ctk.CTkEntry(self,
            font=("Georgia", 16), placeholder_text="Enter Gmail/Mobile", width=200)
        self.azon_gmail_ent.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Password
        azon_passwd_lbl = ctk.CTkLabel(self, text="Password", font=("Georgia bold", 12), text_color="white")
        azon_passwd_lbl.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.azon_passwd_ent = ctk.CTkEntry(self, show="*",
            font=("Georgia", 16), placeholder_text="Enter Password", width=200)
        self.azon_passwd_ent.grid(row=2, column=1, padx=10, pady=5, sticky="ew")


        # Toggle Show/Hide Password
        self.toggle_btn = ctk.CTkButton(self, text="", width=10, image=self.hide_img,
            fg_color="gray10", hover_color="gray15",
            command=lambda: self.toggle_passwd(self.azon_passwd_ent, self.toggle_btn))
        self.toggle_btn.grid(row=2, column=2, padx=10, pady=5)

        # Session ID
        azon_ssn_lbl = ctk.CTkLabel(self, text="Seesion ID", font=("Georgia bold", 12), text_color="white")
        azon_ssn_lbl.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.azon_ssn_id = ctk.StringVar()
        self.azon_ssn_ent = ctk.CTkEntry(self, font=("Georgia", 16),
            textvariable=self.azon_ssn_id, state="readonly", width=200, text_color="gray")
        self.azon_ssn_id.set("Login to Get SSN-AZON-ID")
        # self.azon_ssn_ent.configure(state="disabled")
        self.azon_ssn_ent.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Copy Text from a field
        self.copy_btn = ctk.CTkButton(self, text="", width=10, image=self.copy_img,
            fg_color="gray10", hover_color="gray15",
            command=lambda: self.copy_text(self.azon_ssn_ent))
        self.copy_btn.grid(row=3, column=2, padx=10, pady=5)

        # Login Button
        self.azon_login_btn = ctk.CTkButton(self,
            fg_color="gray10", hover_color="#a16a3f", text_color="#F4A261",
            text="Login 2 Azon", width=100, height=40, font=("Georgia bold", 16),
            command=lambda: self.get_azon_creds())
        self.azon_login_btn.grid(row=4, column=0, columnspan=3, padx=10, pady=20)

        # Create progress bar, but do not show it initially
        self.azon_progress_bar = ctk.CTkProgressBar(self,
            mode='indeterminate', width=300, progress_color="#F4A261", fg_color="gray10", bg_color="gray10")

        ctk.CTkLabel(self, text="").grid(row=5, column=0)

        # Flipkart Section
        fkart_lbl = ctk.CTkLabel(self, text="Flipkart", font=("Georgia bold", 16), text_color="white")
        fkart_lbl.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        fkart_gmail_lbl = ctk.CTkLabel(self, text="Gmail or Mobile", font=("Georgia bold", 12), text_color="white")
        fkart_gmail_lbl.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.fkart_gmail_ent = ctk.CTkEntry(self, font=("Georgia", 16),
            placeholder_text="Enter Gmail/Mobile", width=200)
        self.fkart_gmail_ent.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        # Session ID
        fkart_ssn_lbl = ctk.CTkLabel(self, text="Seesion ID", font=("Georgia bold", 12), text_color="white")
        fkart_ssn_lbl.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.fkart_ssn_id = ctk.StringVar()
        self.fkart_ssn_ent = ctk.CTkEntry(self, font=("Georgia", 16),
            textvariable=self.fkart_ssn_id, state="readonly", width=200, text_color="gray")
        self.fkart_ssn_id.set("Login to Get SSN-FKART-ID")
        # self.azon_ssn_ent.configure(state="disabled")
        self.fkart_ssn_ent.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        # Copy Text from a field
        self.copy_btn = ctk.CTkButton(self, text="", width=10, image=self.copy_img,
            fg_color="gray10", hover_color="gray15",
            command=lambda: self.copy_text(self.fkart_ssn_ent))
        self.copy_btn.grid(row=8, column=2, padx=10, pady=5)

        # Login Button
        self.fkart_login_btn = ctk.CTkButton(self,
            fg_color="gray10", hover_color="#a16a3f", text_color="#F4A261",
            text="Login 2 Fkart", width=100, height=40, font=("Georgia bold", 16),
            command=lambda: self.get_fkart_creds())
        self.fkart_login_btn.grid(row=9, column=0, columnspan=3, padx=10, pady=20)

        # Create progress bar, but do not show it initially
        self.fkart_progress_bar = ctk.CTkProgressBar(self,
            mode='indeterminate', width=300, progress_color="#F4A261", fg_color="gray10", bg_color="gray10")

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)


    def get_azon_creds(self) :
        email_phone = self.azon_gmail_ent.get()
        password = self.azon_passwd_ent.get()

        # Validate that both fields are filled
        if not email_phone or not password :
            # Show an error message box if inputs are empty
            errHead = "EMPTY-INPUT"
            errBody = "Please enter both Email/Mobile & Password."
            logics.log_error("fl_err.log", "frame-login.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)
            return

        # Create a thread to run the subprocess so it doesn't block the UI
        threading.Thread(target=self.azon_run_in_background, args=(
            os.path.dirname(__file__),
            os.path.join("..", "..", "Server", "azon_login.js"),
            {"EMAIL_PHONE": email_phone, "PASSWORD": password, "SSN_ID": logics.get_hashkey("SSN-AZON-")},
        )).start()


    def get_fkart_creds(self) :
        email_phone = self.fkart_gmail_ent.get()

        # Validate that both fields are filled
        if not email_phone :
            # Show an error message box if inputs are empty
            errHead = "EMPTY-INPUT"
            errBody = "Please enter both Email/Mobile"
            logics.log_error("fl_err.log", "frame-login.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)
            return

        # Create a thread to run the subprocess so it doesn't block the UI
        threading.Thread(target=self.fkart_run_in_background, args=(
            os.path.dirname(__file__),
            os.path.join("..", "..", "Server", "fkart_login.js"),
            {"EMAIL_PHONE": email_phone, "SSN_ID": logics.get_hashkey("SSN-FKART-")},
        )).start()


    def azon_run_in_background(self, dirname, filename, data) :
        self.show_loading_bar(self.azon_progress_bar, self.azon_login_btn, 4)
        self.azon_ssn_id.set("")
        logics.run_js_script(dirname, filename, data)
        self.hide_loading_bar(self.azon_progress_bar, self.azon_login_btn, 4)
        self.azon_ssn_id.set(data["SSN_ID"])


    def fkart_run_in_background(self, dirname, filename, data) :
        self.show_loading_bar(self.fkart_progress_bar, self.fkart_login_btn, 9)
        self.fkart_ssn_id.set("")
        logics.run_js_script(dirname, filename, data)
        self.hide_loading_bar(self.fkart_progress_bar, self.fkart_login_btn, 9)
        self.fkart_ssn_id.set(data["SSN_ID"])


    def hide_loading_bar(self, thisBar, thisBtn, rowIdx) :
        # Stop the progress bar after subprocess finishes
        thisBar.stop()
        # Remove progress bar from the grid
        thisBar.grid_forget()
        # Re-enable the Submit button after the subprocess finishes
        thisBtn.configure(state="normal")
        thisBtn.grid(row=rowIdx, column=0, columnspan=3, padx=10, pady=20)


    def show_loading_bar(self, thisBar, thisBtn, rowIdx) :
        # Disable the Submit Button to prevent multiple submissions
        thisBtn.grid_forget()
        # Show the loading indicator # Place progress bar in the grid
        thisBar.grid(row=rowIdx, column=0, columnspan=3, padx=10, pady=20)
        thisBar.start()


    def copy_text(self, entry) :
        text = entry.get()
        pyperclip.copy(text)


    def toggle_passwd(self, entry, button):
        if entry.cget("show") == "*" :
            entry.configure(show="")
            button.configure(image=self.show_img)
        else :
            entry.configure(show="*")
            button.configure(image=self.hide_img)
