import datetime
import subprocess
import json
import os
import tkinter.messagebox as messagebox


errlogDir = os.path.join(os.path.dirname(__file__), "..", "Logs", "Errors")
def log_error(category, srcFile, errHead, errBody) :

    filepath = os.path.join(errlogDir, category)
    if not os.path.exists(errlogDir):
        os.makedirs(errlogDir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    head = errHead
    body = errBody

    with open(filepath, "a") as f:
        f.write(f"{timestamp}\n")
        f.write(f"ERROR:\t{head}@{srcFile}\n")
        f.write(f"{body}\n\n")
    return


infologDir = os.path.join(os.path.dirname(__file__), "..", "Logs", "Events")
def log_info(category, srcFile, infoHead, infoBody) :

    filepath = os.path.join(infologDir, category)
    if not os.path.exists(infologDir):
        os.makedirs(infologDir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d | %H:%M:%S")
    head = infoHead
    body = infoBody

    with open(filepath, "a") as f:
        f.write(f"{timestamp}\n")
        f.write(f"INFO:\t{head}@{srcFile}\n")
        f.write(f"{body}\n")
    return


def get_hashkey(prefix) :
    """Function to generate hashkeys."""
    now = datetime.datetime.now()
    # yyy/mm/dd_HH:MM:SS
    hashkey = now.strftime("%Y%m%d-%H%M%S")
    return prefix+hashkey


def run_js_script(backend_dir, js_file, data):
    """Function to run a JS script with provided JSON data and backend directory."""
    # Construct the full path to the JS file dynamically
    js_file_path = os.path.join(backend_dir, js_file)
    # Check if the file exists
    if not os.path.exists(js_file_path):
        print(f"Error: {js_file} not found in {backend_dir}")
        return

    # Serialize data to a JSON string
    data_json = json.dumps(data)
    # Construct the command to call the JS file using Node.js
    command = ['node', js_file_path, data_json]
    try:
        # Run the command Synchronously
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Capture outputs for debugging
        stdout, stderr = result.stdout, result.stderr

        # Check if there are errors in the Node.js process
        if stderr:
            log_error(f"njs_err.log", f"{js_file}", f"ERROR?", f"{stderr}")
            messagebox.showerror("Error", f"Error in {js_file_path}: {stderr}")
        else:
            log_info("infos.log", f"{js_file}", f"INFO", f"{stdout}")
            messagebox.showinfo("Info", f"Info:\n{stdout}")

    except Exception as e:
        log_error(f"others_err.log", f"{js_file}", f"{e.__class__.__name__}", f"{str(e)}")
        messagebox.showerror("Error", f"Error running {js_file_path}: {e}")

    return
