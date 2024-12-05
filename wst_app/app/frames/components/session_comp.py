
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import pyperclip
import os
import sys

# Get the absolute path of the base directory (going up 3 levels)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# Add base_dir to sys.path to allow importing logics
sys.path.append(base_dir)
# Import logics.py after modifying sys.path
import logics


class SessionFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, file_names, tag, **kwargs):
        super().__init__(master, **kwargs)

        self.tag = tag
        self.addComponents(file_names)


    def addComponents(self, file_names):
        self.delComponents()
        for i, val in enumerate(file_names) :
            # Dynamically creating SessionKeysComponent for each string (file_name)
            session_component = SessionKeysComponent(
                master=self, file_name=val, tag=self.tag,
                width=200,
                height=100
            )
            session_component.grid(row=i, column=0, padx=20, pady=5, sticky="ew")

    def delComponents(self):
        for widget in self.winfo_children() :
            widget.destroy()



class SessionKeysComponent(ctk.CTkFrame):

    extn = ".json"
    cacheDir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Server", "Cache")

    def __init__(self, master, file_name, tag, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.tag = tag
        self.configure(fg_color="gray20")

        # Create and place the input field (disabled entry)
        self.file_name = ctk.StringVar(value=file_name)
        self.ssn_ent = ctk.CTkEntry(self, font=("Georgia", 16),
            textvariable=self.file_name, state="readonly", width=300, text_color="gray")
        self.ssn_ent.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Load and resize images for buttons
        dirname = os.path.join(os.path.dirname(__file__), "..", "..", "Images")
        copy_img = ctk.CTkImage(Image.open(os.path.join(dirname, "copy-icon2.png")))
        bin_img = ctk.CTkImage(Image.open(os.path.join(dirname, "bin-icon2.png")))

        # Copy Text from a field
        self.copy_btn = ctk.CTkButton(self, text="", width=10, image=copy_img,
            fg_color="gray10", hover_color="gray15",
            command=self.copy_to_clipboard)
        self.copy_btn.grid(row=0, column=1, padx=10, pady=5)

        # Deletes SessionKey
        self.del_btn = ctk.CTkButton(self, text="", width=10, image=bin_img,
            fg_color="gray10", hover_color="gray15",
            command=self.confirm_delete_file)
        self.del_btn.grid(row=0, column=2, padx=10, pady=5)        


    def confirm_delete_file(self):
        """Prompt for confirmation before deleting the file"""
        # Show a confirmation dialog
        result = messagebox.askyesno(
            title="Confirm Deletion",
            message=f"Are you sure you want to Delete the Cache: '{self.file_name.get()}'?"
        )
        
        if result:  # If the user clicks 'Yes'
            self.delete_file()


    def delete_file(self):
        """Deletes the file from the current directory"""
        file_path = os.path.join(self.cacheDir, self.tag, self.file_name.get()+self.extn)

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                infoHead = "DELETED-SUCCESS"
                infoBody = f"File '{file_path}' Deleted"
                messagebox.showinfo(infoHead, infoBody)
                logics.log_info("ssn-hist-info.log", f"{file_path}", infoHead, infoBody)
                self.destroy()
            except Exception as e:
                errHead = e.__class__.__name__
                errBody = str(e)
                messagebox.showerror(errHead, errBody)
                logics.log_error("ssn-hist-err.log", "frame-ssn-hist.py", errHead, errBody)
        else:
            errHead = "FILE-NOT-FOUND"
            errBody = f"Couldn't Delete the File\n{file_path}"
            messagebox.showerror(errHead, errBody)
            logics.log_error("ssn-hist-err.log", "frame-ssn-hist.py", errHead, errBody)


    def copy_to_clipboard(self):
        """Copies the content of the input field to clipboard"""
        pyperclip.copy(self.file_name.get())
        # messagebox.showinfo("Copied", f"File name '{self.file_name.get()}' copied to clipboard.")


# Example usage
if __name__ == "__main__":
    # Create a sample window
    root = ctk.CTk()
    myFrame = SessionFrame(
        root,
        [f"Azon {i}" for i in range(1, 101)],
        width=400, height=400  # Adjust frame size as needed
    )
    myFrame.grid(row=0, column=0)#, sticky="nsew")

    myFrame = SessionFrame(
        root,
        [f"Fkart {i}" for i in range(1, 101)],
        width=400, height=400  # Adjust frame size as needed
    )
    myFrame.grid(row=1, column=0)#, sticky="nsew")

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    root.mainloop()
