import customtkinter as ctk
import main_app
import os


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        dirname = os.path.join(os.path.dirname(__file__), 'Images')
        self.iconbitmap(os.path.join(dirname, "icon.ico"))
        main_app.MainApp(self)

        self.bind("<Control-w>", self.close_app)
        self.bind("<Alt-F4>", self.close_app)

    def close_app(self, event=None):
        self.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()
