"""
Setup.py will gather the username that controls ALSA,
a unique name for the control (I use the room name),
the broker address of the MQTT server and
the path to where the python app resides.
It makes a .config file for the the python app
it creates a systemd/system service file,
enables the service and starts it.
Any problems, blame it on the 83 year old programmer
Douglas Wyman
"""

import tkinter as tk
import json
from tkinter import messagebox
import sys
import os
import subprocess
def valid_computer_char(inchar):
    """
    Validate the computer name
    """
    print(inchar.isalnum() or inchar in "-_")
    return inchar.isalnum() or inchar in "-_"


def valid_path_char(inchar):
    """
    # Address: digits and dots only (simple IPv4-style check)
    """
    return inchar.isalnum() or inchar in "-_/"

def valid_address_char(inchar):
    """
    # Address: digits and dots only (simple IPv4-style check)
    """
    return inchar.isdigit() or inchar == "."

def valid_user_char(inchar):
    """
    # Address: digits and dots only (simple IPv4-style check)

    """
    return inchar.isalnum()

def make_key_handler(validator):
    """
    handle key checking
    """
    def handler(event):
        inchar = event.char
        # Ignore control keys
        if len(inchar) == 0 or ord(inchar) < 32:
            return ""

        if not validator(inchar):
            messagebox.showwarning("Invalid character", f"'{inchar}' is not allowed.")
            return "break"

        update_save_button()
        return handler

def update_save_button(*args):
    """
    # -----------------------------
    # Save button logic
    # -----------------------------
    """
    name = COMPUTER_VAR.get().strip()
    addr = ADDRESS_VAR.get().strip()

    if name and addr:
        SAVE_BUTTON.config(state="normal")
    else:
        SAVE_BUTTON.config(state="disabled")

def save():
    """
    This block saves the .config file
    """
    print("ADDRESS_VAR:", ADDRESS_VAR, type(ADDRESS_VAR))
    print("COMPUTER_VAR:", COMPUTER_VAR, type(COMPUTER_VAR))

    print("ADDRESS_VAR.get():", ADDRESS_VAR.get(), type(ADDRESS_VAR.get()))
    print("COMPUTER_VAR.get():", COMPUTER_VAR.get(), type(COMPUTER_VAR.get()))

    data = {
        "broker_address": ADDRESS_VAR.get(),
        "computer_name": COMPUTER_VAR.get()
    }
    print("DATA:", data, type(data))

    with open("rpi_volume.conf", "w") as conffile:
        json.dump(data, conffile, indent=4)

    messagebox.showinfo("Saved Config File",\
    "config data \n Broker Address as " +  str(ADDRESS_VAR.get()) + "\n Computer name as " + COMPUTER_VAR.get())
    #root.withdraw()

    template_file = os.getcwd() + "/rpi-volume.service.template"

    user_name = USER_VAR.get()
    script_path = PATH_VAR.get() + "/rpi_vol_control.py"
    working_dir = os.path.dirname(script_path)
    try:
        with open(template_file, "r") as bp_file:
            template = bp_file.read()
    except exception as myerr:
        print(myerr)
    service_text = template.replace("{{SCRIPT_PATH}}", script_path)\
                           .replace("{{WORKING_DIR}}", working_dir)\
                           .replace("{{user_id}}", user_name)
    try:
        with open("rpi-volume.service", "w") as svc_file:
            svc_file.write(service_text)
    except exception as myerr:
        print(myerr)

    mytext = "Service file created as rpi-volume.service\n"
    mytext += "Service User set as " + user_name + "\nFile location saves as " + working_dir
    mytext += "\nExecute command as " + script_path
    messagebox.showinfo("Saved", mytext)
    msg = "sudo cp rpi-volume.service /etc/systemd/system/rpi-volume.service"
    subprocess.run(msg, shell=True, check=True)
    messagebox.showinfo("Service setup", "Copied rpi-volume.service\n To /etc/systemd/system/rpi-volume.service")

    subprocess.run("sudo systemctl daemon-reload", shell=True, check=True)
    subprocess.run("sudo systemctl enable rpi-volume.service", shell=True, check=True)
    subprocess.run("sudo systemctl start rpi-volume.service", shell=True, check=True)
#     print("sudo systemctl daemon-reload")
#     print("  sudo systemctl enable rpi-volume.service")
#     print("  sudo systemctl start rpi-volume.service")
    messagebox.showinfo("Started rpi-volume", "The service should be running, check")
    sys.exit()
# -----------------------------
# GUI setup
# -----------------------------
root = tk.Tk()
root.title("User, Computer, Address and Path")

USER_VAR = tk.StringVar()
COMPUTER_VAR = tk.StringVar()
ADDRESS_VAR = tk.StringVar()
PATH_VAR = tk.StringVar()

COMPUTER_VAR.trace_add("write", update_save_button)
ADDRESS_VAR.trace_add("write", update_save_button)

# User name entry
TMPNAME = os.getlogin()
tk.Label(root, text="User Name that will run rpi_vol_control.py:").pack(anchor="w", padx=10)
USER_ENTRY = tk.Entry(root, textvariable=USER_VAR, width=20)
USER_ENTRY.insert(0, TMPNAME)
USER_ENTRY.pack(padx=10, pady=5)
USER_ENTRY.bind("<Key>", make_key_handler(valid_user_char))

# Computer name entry
tk.Label(root, text="A Unique Name Identifying The Control:").pack(anchor="w", padx=10)
COMPUTER_ENTRY = tk.Entry(root, textvariable=COMPUTER_VAR, width=20)
COMPUTER_ENTRY.pack(padx=10, pady=5)
COMPUTER_ENTRY.bind("<Key>", make_key_handler(valid_computer_char))

# Address entry
tk.Label(root, text="Broker IP Address:").pack(anchor="w", padx=10)
ADDRESS_ENTRY = tk.Entry(root, textvariable=ADDRESS_VAR, width=40)
ADDRESS_ENTRY.pack(padx=10, pady=5)
ADDRESS_ENTRY.bind("<Key>", make_key_handler(valid_address_char))

# Path entry
TMP_PATH = os.getcwd()
tk.Label(root, text="Full Path to rpi_vol_control.py :").pack(anchor="w", padx=10)
PATH_ENTRY = tk.Entry(root, textvariable=PATH_VAR, width=40)
PATH_ENTRY.insert(0, TMP_PATH)
PATH_ENTRY.pack(padx=10, pady=5)
PATH_ENTRY.bind("<Key>", make_key_handler(valid_path_char))

# Save button
SAVE_BUTTON = tk.Button(root, text="Save", state="disabled", command=save)
SAVE_BUTTON.pack(pady=15)

root.mainloop()
