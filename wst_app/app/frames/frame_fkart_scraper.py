import customtkinter as ctk
import tkinter.messagebox as messagebox
import pandas as pd
import threading
import os
import logics


class FkartScraperFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app  # Reference to MainApp
        self.create_widgets()


    def create_widgets(self):

        # ctk.CTkLabel(self, text="").grid(row=0, column=0)

        # Heading label (centered)
        heading_lbl = ctk.CTkLabel(self, text="Web Scraper Tool: Flipkart", font=("Georgia bold", 18), text_color="white")
        heading_lbl.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        # Session ID
        ssn_id_lbl = ctk.CTkLabel(self, text="Session ID:", font=("Georgia bold", 14), text_color="white")
        ssn_id_lbl.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ssn_id_ent = ctk.CTkEntry(self, font=("Georgia", 16), placeholder_text="Enter Session ID", width=200)
        self.ssn_id_ent.grid(row=1, column=1, padx=10, pady=5, sticky="ew", columnspan=3)

        # Base URL (multi-line textbox, height set to 5 rows)
        base_url_lbl = ctk.CTkLabel(self, text="Base URL:", font=("Georgia bold", 14), text_color="white")
        base_url_lbl.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.base_url_tbox = ctk.CTkTextbox(self, font=("Georgia bold", 12), height=75, width=200)
        self.base_url_tbox.grid(row=2, column=1, columnspan=3, rowspan=1, padx=10, pady=5, sticky="ew")

        # Product Name
        product_name_lbl = ctk.CTkLabel(self, text="Product Name:", font=("Georgia bold", 14), text_color="white")
        product_name_lbl.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.product_name_ent = ctk.CTkEntry(self, font=("Georgia", 16), placeholder_text="Enter Product Name", width=200)
        self.product_name_ent.grid(row=3, column=1, padx=10, pady=5, sticky="ew", columnspan=3)

        # Product Category: Combo-Box
        ctk.CTkLabel(self, text="Product Category:", font=("Georgia bold", 14), text_color="white")\
        .grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.catg_menu = ctk.CTkComboBox(self,
            font=("Georgia", 16), values=["Select Category"])
        self.catg_menu.grid(row=4, column=1, padx=10, pady=5, sticky="ew", columnspan=3)

        # New Category: Entry
        ctk.CTkLabel(self, text="New Category:", font=("Georgia bold", 14), text_color="white")\
        .grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.new_catg_ent = ctk.CTkEntry(self, font=("Georgia", 16), placeholder_text="Enter New Category (Optional)", width=200)
        self.new_catg_ent.grid(row=5, column=1, padx=10, pady=5, sticky="ew", columnspan=3)

        # Save As
        save_as_lbl = ctk.CTkLabel(self, text="Save As:", font=("Georgia bold", 14), text_color="white")
        save_as_lbl.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.save_as_ent = ctk.CTkEntry(self, font=("Georgia", 16), placeholder_text="Enter File Name (Optional)", width=200)
        self.save_as_ent.grid(row=6, column=1, padx=10, pady=5, sticky="ew", columnspan=3)

        # ctk.CTkLabel(self, text="").grid(row=6, column=0)
        ctk.CTkLabel(self,
            text="Advanced Settings", font=("Georgia bold", 14, "underline"), text_color="white")\
            .grid(row=7, column=0)

        # Scrape Mode Switch toggle
        smode_lbl = ctk.CTkLabel(self, text="Scrape Mode:", font=("Georgia bold", 14), text_color="white")
        smode_lbl.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.smode_var = ctk.StringVar(value="Testing")
        self.smode = ctk.CTkSwitch(self,
            font=("Georgia", 16), text=self.smode_var.get(),
            command=lambda: self.switch_toggle(self.smode, self.smode_var),
            variable=self.smode_var, onvalue="Deploy", offvalue="Testing")
        self.smode.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        # Based on Scrape Mode, Display the Category-Menu
        self.update_menu_option(self.smode_var.get())

        # Browser Visibility Switch toggle
        www_tgl_lbl = ctk.CTkLabel(self, text="Browser Visibility:", font=("Georgia bold", 14), text_color="white")
        www_tgl_lbl.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.www_tgl_var = ctk.StringVar(value="true")
        self.www_tgl = ctk.CTkSwitch(self,
            font=("Georgia", 16), text=self.www_tgl_var.get(),
            command=lambda: self.switch_toggle(self.www_tgl, self.www_tgl_var),
            variable=self.www_tgl_var, onvalue="true", offvalue="false")
        self.www_tgl.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        # Dataset File-Write-Speed
        write_speed_lbl = ctk.CTkLabel(self, text="File Write Speed\n(in rows):", font=("Georgia bold", 14), text_color="white")
        write_speed_lbl.grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.write_speed = ctk.CTkEntry(self, font=("Georgia", 16), placeholder_text="File Write Speed (in rows)", width=100)
        self.write_speed.grid(row=10, column=1, padx=10, pady=5, sticky="ew", columnspan=3)
        self.write_speed.insert(0, 15)

        # LIMITS
        pll_lbl = ctk.CTkLabel(self, text="Page Load Limit\n(in s):", font=("Georgia bold", 14), text_color="white")
        pll_lbl.grid(row=11, column=0, padx=10, pady=5, sticky="w")
        self.pll_ent = ctk.CTkEntry(self, font=("Georgia", 16), placeholder_text="(in s)", width=50)
        self.pll_ent.grid(row=11, column=1, padx=0, pady=5)#, sticky="ew")
        self.pll_ent.insert(0, 25)

        psl_lbl = ctk.CTkLabel(self, text="Page Scrape Limit\n(in s):", font=("Georgia bold", 14), text_color="white")
        psl_lbl.grid(row=11, column=2, padx=0, pady=5, sticky="w")
        self.psl_ent = ctk.CTkEntry(self, font=("Georgia", 16), placeholder_text="(in s)", width=50)
        self.psl_ent.grid(row=11, column=3, padx=0, pady=5)#, sticky="ew")
        self.psl_ent.insert(0, 4)

        # ctk.CTkLabel(self, text="").grid(row=12, column=0)

        # Generate Button
        self.generate_btn = ctk.CTkButton(
            self, text="Generate",  width=100, height=40, font=("Georgia bold", 16),
            fg_color="gray10", hover_color="#a16a3f", text_color="#F4A261",
            command=self.scrape_action)
        self.generate_btn.grid(row=12, column=0, pady=10, padx=10, columnspan=4)

        # Create progress bar, but do not show it initially
        self.progress_bar = ctk.CTkProgressBar(self,
            mode="indeterminate", width=300, progress_color="#F4A261", fg_color="gray10", bg_color="gray10")

        # Set weight for columns to allow them to expand equally
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(3, weight=1)


    def scrape_action(self):
        # process the base url
        prod_url = self.base_url_tbox.get("1.0", "end-1c").replace("\n", "").replace(" ", "").strip()
        catg_menu = self.catg_menu.get().strip()
        new_catg = self.new_catg_ent.get().strip()

        if (not catg_menu or catg_menu == "Select Category") and new_catg == "":
            errHead = "INVALID-FORM-INPUTS"
            errBody = "Please Choose a Valid Product-Category or Enter a New Catgeory"
            logics.log_error("fas_err.log", f"frame-fkart-scraper.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)
            return

        scrape_mode = self.smode_var.get()
        catg_name = (new_catg if new_catg else catg_menu).lower()
        save_as = self.save_as_ent.get().strip()
        if not save_as:
            save_as = ("final" if scrape_mode=="Deploy" else "test") + "_fkart_" + catg_name

        data = {
            "SSN_ID": self.ssn_id_ent.get().strip(),
            "PRODUCT_URL": prod_url,
            "PRODUCT_NAME": self.product_name_ent.get().strip(),
            "CATEGORY": catg_name,
            "SCRAPE_MODE": scrape_mode,
            "BROWSER_VIEW": self.www_tgl_var.get(),
            "WRITE_SPEED": self.write_speed.get().strip(),
            "PAGE_LOAD_LIMIT": self.pll_ent.get().strip(),
            "PAGE_SCRAPE_LIMIT": self.psl_ent.get().strip(),
            "FILE_NAME": save_as,
        }

        skip_info = ["FILE_NAME"]
        # Check if any of the fields are empty
        for key in data:
            if key in skip_info:
                continue

            if not data[key]:
                errHead = "MISSING-FORM-INPUTS"
                errBody = f"Please fill in all the Form Fields\n{key} Missing"
                logics.log_error("fas_err.log", f"frame-fkart-scraper.py", errHead, errBody)
                messagebox.showerror(errHead, errBody)
                return

        try:    # Validate "WRITE_SPEED" to ensure they are integers
            data["WRITE_SPEED"] = int(data["WRITE_SPEED"])
            data["PAGE_LOAD_LIMIT"] = int(data["PAGE_LOAD_LIMIT"])*1000
            data["PAGE_SCRAPE_LIMIT"] = int(data["PAGE_SCRAPE_LIMIT"])*1000

            if not (1 <= int(self.pll_ent.get())) :
                raise ValueError("PAGE-LOAD-LIMIT must be >= 1, Recommended: 10 or 30 !")

            if not (1 <= int(self.psl_ent.get())) :
                raise ValueError("PAGE-SCRAPE-LIMIT must be >= 1, Recommended: 2 or 4 !")

            if not (0 < data["WRITE_SPEED"] < 101) :
                raise ValueError("Write Speed must be: 0 < INTEGER < 101 !")

        except ValueError as e:
            errHead = e.__class__.__name__
            errBody = str(e)
            if str(e).startswith("invalid") :
                errHead = "INVALID-FORM-INPUTS"
                errBody = "Please Type Valid Numbers for Number-Fields"
            logics.log_error("fas_err.log", f"frame-fkart-scraper.py", errHead, errBody)
            messagebox.showerror(errHead, errBody)
            return


        # self.show_loading_bar()
        # Create a thread to run the subprocess so it doesn"t block the UI
        threading.Thread(target=self.run_in_background, args=(
            os.path.dirname(__file__),
            os.path.join("..", "..", "server", "fkart_scraper.js"),
            data,
        )).start()


    def run_in_background(self, dirname, filename, data) :
        self.show_loading_bar()
        logics.run_js_script(dirname, filename, data)
        self.hide_loading_bar()


    def hide_loading_bar(self) :
        # Stop the progress bar after subprocess finishes
        self.progress_bar.stop()
        # Remove progress bar from the grid
        self.progress_bar.grid_forget()
        # Re-enable the Submit button after the subprocess finishes
        self.generate_btn.configure(state="normal")
        self.generate_btn.grid(row=12, column=0, pady=10, padx=10, columnspan=4)


    def show_loading_bar(self) :
        # Disable the Submit Button to prevent multiple submissions
        self.generate_btn.grid_forget()
        # Show the loading indicator # Place progress bar in the grid
        self.progress_bar.grid(row=12, column=0, pady=10, padx=10, columnspan=4)
        self.progress_bar.start()


    def switch_toggle(self, switch, strVar) :
        switch.configure(text=strVar.get())
        self.update_menu_option(strVar.get())


    def update_menu_option(self, scrapeType):
        dbDir1 = os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "fkart")
        dbDir2 = os.path.join(os.path.dirname(__file__), "..", "..", "database", "fkart")
        options = ["Select Category"]
        tmp = []

        if scrapeType == "Deploy":
            tmp = self.get_unique_rows(os.path.join(dbDir1, "meta_data.csv"))
        elif scrapeType == "Testing":
            tmp = self.get_unique_rows(os.path.join(dbDir2, "meta_data.csv"))

        if tmp:
            options.extend(tmp)

        self.catg_menu.configure(values=options)
        self.catg_menu.set(options[0])


    def get_unique_rows(self, filePath):
        # Step 1: Check if the file exists
        if not os.path.exists(filePath):
            return

        try: # Step 2: Read the CSV file into a pandas DataFrame
            df = pd.read_csv(filePath)
        except Exception as e:
            print(f"Error reading the file: {e}")
            return

        # Step 3: Extract unique values from the 'Categories' column
        if 'Category' not in df.columns:
            print("Column 'Category' not found in the CSV file.")
            return

        unique_categories = df['Category'].dropna().unique().tolist()  # Drop NaN values and get unique values
        # df_unique = df.drop_duplicates(subset='Category')
        # Step 4: Optionally rewrite the file (if you want to keep unique rows only in the file)
        df_unique = df.drop_duplicates()
        df_unique.to_csv(filePath, index=False)
        # Step 5: Return the unique categories as a list
        return unique_categories
