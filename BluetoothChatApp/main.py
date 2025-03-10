import sys
import os
import uuid

try:
    import tkinter as tk
except ImportError:
    print("Error: tkinter module not found. Please install it before running this script.")
    sys.exit(1)

from database.database import init_db
from gui.gui import ChatApp, LoginWindow
from bluetooth_manager import BluetoothManager

# Initialize directories
def init_dirs():
    os.makedirs("assets/images", exist_ok=True)
    os.makedirs("assets/videos", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    os.makedirs("database", exist_ok=True)
    os.makedirs("gui", exist_ok=True)
    print("PAMM app initialized")
    print("Directories initialized.")

# Generate a unique UUID for the Bluetooth service
def get_bluetooth_uuid():
    return str(uuid.uuid4())

if __name__ == "__main__":
    init_dirs()
    init_db()
    bluetooth_uuid = get_bluetooth_uuid()
    print(f"Bluetooth Service UUID: {bluetooth_uuid}")
    bluetooth_manager = BluetoothManager(bluetooth_uuid)
    root = tk.Tk()
    login_window = LoginWindow(root, bluetooth_manager)
    root.mainloop()
 