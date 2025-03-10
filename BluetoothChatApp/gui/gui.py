import tkinter as tk
from tkinter import messagebox
from database.database import register_user, login_user

class ChatApp:
    def __init__(self, root, bluetooth_manager):
        self.root = root
        self.bluetooth_manager = bluetooth_manager
        self.root.title("Bluetooth Chat App")
        self.root.geometry("400x600")
        
        self.chat_frame = tk.Frame(self.root, bg="#ECE5DD")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
        
        self.text_box = tk.Text(self.chat_frame, state=tk.DISABLED, wrap=tk.WORD, bg="#DCF8C6")
        self.text_box.pack(fill=tk.BOTH, expand=True)
        
        self.entry_frame = tk.Frame(self.root, bg="#ffffff")
        self.entry_frame.pack(fill=tk.X)
        
        self.entry_field = tk.Entry(self.entry_frame, font=("Arial", 14))
        self.entry_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.send_button = tk.Button(self.entry_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10)
        
        self.bluetooth_manager.start_server()
        self.root.after(1000, self.check_for_messages)

    def send_message(self):
        message = self.entry_field.get()
        if message:
            self.display_message("You", message)
            self.bluetooth_manager.send_message(message)
            self.entry_field.delete(0, tk.END)
        
    def display_message(self, sender, message):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, f"{sender}: {message}\n")
        self.text_box.config(state=tk.DISABLED)
        self.text_box.yview(tk.END)

    def check_for_messages(self):
        message = self.bluetooth_manager.receive_message()
        if message:
            self.display_message("Other", message)
        self.root.after(1000, self.check_for_messages)

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("300x200")

        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Register", command=self.register)
        self.register_button.pack(pady=20)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            register_user(username, password)
            messagebox.showinfo("Success", "User registered successfully!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Please enter both username and password")

class LoginWindow:
    def __init__(self, root, bluetooth_manager):
        self.root = root
        self.bluetooth_manager = bluetooth_manager
        self.root.title("Login")
        self.root.geometry("300x200")

        self.username_label = tk.Label(self.root, text="Username")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=20)

        self.register_button = tk.Button(self.root, text="Register", command=self.open_register_window)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            main_app(self.bluetooth_manager)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def open_register_window(self):
        register_window = tk.Toplevel(self.root)
        RegisterWindow(register_window)

def main_app(bluetooth_manager):
    root = tk.Tk()
    app = ChatApp(root, bluetooth_manager)
    root.mainloop()

if __name__ == "__main__":
    init_dirs()
    init_db()
    bluetooth_uuid = get_bluetooth_uuid()
    print(f"Bluetooth Service UUID: {bluetooth_uuid}")
    root = tk.Tk()
    bluetooth_manager = BluetoothManager(bluetooth_uuid)
    login_window = LoginWindow(root, bluetooth_manager)
    root.mainloop()
