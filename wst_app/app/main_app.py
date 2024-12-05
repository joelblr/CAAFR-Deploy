
import customtkinter as ctk
from frames.frame_login import LoginFrame
from frames.frame_azon_scraper import AzonScraperFrame
from frames.frame_fkart_scraper import FkartScraperFrame
from frames.frame_ssn_hist import SessionHistoryFrame


class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper App")
        self.root.geometry("720x600") # W x H
        self.root.resizable(False, False)

        # Set the app theme to dark mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize the current frame as None
        self.current_frame = None
        self.current_nav_button = None  # Track the current navigation button


        # Initialize frames (for Login, Azon Scraper, Fkart Scraper)
        self.frames = {}
        self.frames['login'] = LoginFrame(self.root, self)
        self.frames['amazon_scraper'] = AzonScraperFrame(self.root, self)
        self.frames['flipkart_scraper'] = FkartScraperFrame(self.root, self)
        self.frames['ssn_hist'] = SessionHistoryFrame(self.root, self)


        # # Navigation Bar
        # self.nav_bar = ctk.CTkFrame(self.root, width=200, height=540, fg_color="#2C2F37")  # Dark background for navbar
        self.nav_bar = ctk.CTkFrame(self.root, width=200, height=540, fg_color="#2C2F37")  # Dark background for navbar
        self.nav_bar.grid(row=0, column=0, sticky="news", padx=10, pady=10)
        # Set up navbar with button-like labels
        self.nav_buttons = {}
        self.create_nav_buttons()
        # self.navbar = self.create_nav_bar()


        # Grid configuration to make sure the layout expands
        self.root.grid_rowconfigure(0, weight=1)  # Make sure row 0 takes available vertical space
        self.root.grid_columnconfigure(0, weight=0)  # Sidebar column doesn't need to stretch horizontally
        self.root.grid_columnconfigure(1, weight=1)  # Main content area should take up all horizontal space


        # # Default starting frame is the LoginFrame
        self.show_frame('login')
        self.show_frame('ssn_hist')

    def create_nav_buttons(self):

        nav_button_data = [
            ("Login", "login"),
            ("Amazon Scraper", "amazon_scraper"),
            ("Flipkart Scraper", "flipkart_scraper"),
            ("Session History", "ssn_hist")
        ]

        for idx, (text, frame_name) in enumerate(nav_button_data):
            button = ctk.CTkButton(
                self.nav_bar, text=text, font=("Georgia bold", 16),
                border_width=0, width=180, height=40, anchor="w",
                # fg_color="#333333", 
                text_color="#40E0D0", 
                fg_color="transparent", 
                hover_color="gray10",
                command=lambda frame_name=frame_name: self.show_frame(frame_name),
            )
            button.grid(row=idx, column=0, padx=5, pady=5, sticky="w")
            self.nav_buttons[frame_name] = button


    # def show_frame(self, frame_class):
    def show_frame(self, frame_name):

        # Highlight the active nav bar item
        # self.highlight_active_nav_item(frame_class)
        self.highlight_active_nav_item(frame_name)

        """Hide all frames and show the selected frame"""
        # Hide all frames first
        for frame in self.frames.values():
            frame.grid_forget()

        # Show the selected frame
        self.frames[frame_name].grid(row=0, column=1, sticky="news", padx=10, pady=10)  # Show the selected frame


    # def highlight_active_nav_item(self, frame_class):
    def highlight_active_nav_item(self, frame_name):
        """
        Highlights the active nav item by changing its background color to yellowish gold.
        """
        if self.current_nav_button:
            # Reset the text color of the previous active button
            self.current_nav_button.configure(fg_color="transparent", text_color="#40E0D0")

        # Find the nav item corresponding to the active frame class
        self.current_nav_button = self.nav_buttons[frame_name]


        # Change the active button's background color to yellowish gold and text color to dark?
        self.current_nav_button.configure(fg_color="#F4A261", text_color="#FFFFFF")  # Text color changed to dark
        # self.current_nav_button.configure(fg_color="#F4A261", text_color="#333333")  # Text color changed to dark
