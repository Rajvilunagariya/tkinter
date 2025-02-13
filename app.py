import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import webbrowser

user_database = {}

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="login_db"
        )
        return connection
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return None

def open_social_link(platform):
    if platform == "facebook":
        webbrowser.open("https://www.facebook.com")
    elif platform == "twitter":
        webbrowser.open("https://www.twitter.com")
    elif platform == "google":
        webbrowser.open("https://www.google.com")

def fetch_user_data():
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT username, pass FROM login")
        for row in cursor.fetchall():
            user_database[row['username']] = row['pass']
        cursor.close()
        connection.close()

def save_user_to_database(username, password):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO login (username, pass) VALUES (%s, %s)", (username, password))
        connection.commit()
        cursor.close()
        connection.close()

class FoodApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Ordering App")
        self.root.geometry("500x900")
        self.root.resizable(True, True)
        self.fetch_user_data()
        self.login_page()

    def fetch_user_data(self):
        try:
            fetch_user_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch user data: {e}")

    def login_page(self):
        self.root.title("Login Page")
        self.root.resizable(True, True)

        bg_image = Image.open("E:/MSCIT-BIA-sem2/python/image/back.jpg")  
        bg_image = bg_image.resize((2000, 1000), Image.Resampling.LANCZOS)
        self.bg = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.frame = tk.Frame(self.root, bd=0, bg="#ffffff", highlightbackground="#ffffff", highlightthickness=1)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=600)
        self.frame.config(highlightthickness=2, highlightcolor="#eeeeee")

        tk.Label(
            self.frame, text="Login", font=("Arial", 22, "bold"), bg="#ffffff", fg="#333333"
        ).pack(pady=15)

        tk.Label(
            self.frame, text="Username", font=("Arial", 12), bg="#ffffff", fg="#333333"
        ).pack(pady=5, anchor="w", padx=30)
        self.username_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#f0f0f0", bd=0)
        self.username_entry.pack(pady=5, ipadx=5, ipady=5, fill="x", padx=30)

        tk.Label(
            self.frame, text="Password", font=("Arial", 12), bg="#ffffff", fg="#333333"
        ).pack(pady=5, anchor="w", padx=30)
        self.password_entry = tk.Entry(
            self.frame, font=("Arial", 12), bg="#f0f0f0", bd=0, show="*"
        )
        self.password_entry.pack(pady=5, ipadx=5, ipady=5, fill="x", padx=30)

        forget_password = tk.Label(
            self.frame,
            text="Forgot Password?",
            font=("Arial", 10, "italic"),
            bg="#ffffff",
            fg="#0066cc",
            cursor="hand2",
        )
        forget_password.pack(pady=5, anchor="e", padx=30)
        forget_password.bind("<Button-1>", self.forgot_password_handler)

        login_button = tk.Button(
            self.frame,
            text="LOGIN",
            font=("Arial", 14, "bold"),
            bg="#0066cc",
            fg="#ffffff",
            bd=0,
            command=self.login_handler,
        )
        login_button.pack(pady=20, ipadx=10, ipady=10, fill="x", padx=30)

        tk.Label(
            self.frame,
            text="Or Sign Up Using",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#999999",
        ).pack(pady=10)

        social_frame = tk.Frame(self.frame, bg="#ffffff")
        social_frame.pack(pady=5)
        
        self.add_social_icon(social_frame, "E:/MSCIT-BIA-sem2/python/image/facebook.png")
        self.add_social_icon(social_frame, "E:/MSCIT-BIA-sem2/python/image/twitter.png")
        self.add_social_icon(social_frame, "E:/MSCIT-BIA-sem2/python/image/google.png")

        signup_label = tk.Label(
            self.frame,
            text="SIGN UP",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#0066cc",
            cursor="hand2",
        )
        signup_label.pack(pady=15)
        signup_label.bind("<Button-1>", self.registration_page)

    def add_social_icon(self, parent, icon_path):
        """Helper function to add social icons."""
        icon = Image.open(icon_path)
        icon = icon.resize((40, 40), Image.Resampling.LANCZOS)
        icon_tk = ImageTk.PhotoImage(icon)
        platform = icon_path.split('/')[-1].split('.')[0].lower()
        button = tk.Button(
            parent,
            image=icon_tk,
            bg="#ffffff",
            bd=0,
            cursor="hand2",
            command=lambda: open_social_link(platform),
        )
        button.image = icon_tk  # Prevent garbage collection
        button.pack(side="left", padx=10)

    def login_handler(self):
        """Handle login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in user_database and user_database[username] == password:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.home()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    def forgot_password_handler(self, event=None):
        """Handle forgot password."""
        self.frame.destroy()

        self.frame = tk.Frame(self.root, bg="#ffffff", bd=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=550)
        self.frame.config(highlightthickness=2, highlightcolor="#eeeeee")

        # Forgot Password Label
        tk.Label(
            self.frame, text="Forgot Password", font=("Arial", 22, "bold"), bg="#ffffff", fg="#333333"
        ).pack(pady=15)

        # Username Entry
        tk.Label(
            self.frame, text="Username", font=("Arial", 12), bg="#ffffff", fg="#333333"
        ).pack(pady=5, anchor="w", padx=30)
        username_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#f0f0f0", bd=0)
        username_entry.pack(pady=5, ipadx=5, ipady=5, fill="x", padx=30)

        # New Password Entry
        tk.Label(
            self.frame, text="New Password", font=("Arial", 12), bg="#ffffff", fg="#333333"
        ).pack(pady=5, anchor="w", padx=30)
        new_password_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#f0f0f0", bd=0, show="*")
        new_password_entry.pack(pady=5, ipadx=5, ipady=5, fill="x", padx=30)

        # Confirm Password Entry
        tk.Label(
            self.frame, text="Confirm Password", font=("Arial", 12), bg="#ffffff", fg="#333333"
        ).pack(pady=5, anchor="w", padx=30)
        confirm_password_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#f0f0f0", bd=0, show="*")
        confirm_password_entry.pack(pady=5, ipadx=5, ipady=5, fill="x", padx=30)

        # Reset Password Button
        reset_button = tk.Button(
            self.frame,
            text="RESET PASSWORD",
            font=("Arial", 14, "bold"),
            bg="#0066cc",
            fg="#ffffff",
            bd=0,
            command=lambda: self.reset_password(username_entry.get(), new_password_entry.get(), confirm_password_entry.get()),
        )
        reset_button.pack(pady=20, ipadx=10, ipady=10, fill="x", padx=30)

        # Back to Login Link
        login_label = tk.Label(
            self.frame,
            text="Back to Login",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#0066cc",
            cursor="hand2",
        )
        login_label.pack(pady=15)
        login_label.bind("<Button-1>", lambda e: self.login_page())

    def reset_password(self, username, new_password, confirm_password):
        """Reset the user's password."""
        if not username or not new_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required!")
            return
        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        if username not in user_database:
            messagebox.showerror("Error", "Username does not exist!")
            return

        user_database[username] = new_password
        connection = connect_to_database()
        if connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE login SET pass = %s WHERE username = %s", (new_password, username))
            connection.commit()
            cursor.close()
            connection.close()
        messagebox.showinfo("Success", "Password reset successful!")
        self.login_page()

    def registration_page(self, event=None):
        """Display registration page."""
        self.frame.destroy()

        self.frame = tk.Frame(self.root, bg="#ffffff", bd=0)
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=550)
        self.frame.config(highlightthickness=2, highlightcolor="#eeeeee")

        # Registration Label
        tk.Label(
            self.frame, text="Register", font=("Arial", 22, "bold"), bg="#ffffff", fg="#333333"
        ).pack(pady=15)

        # Username Entry
        tk.Label(
            self.frame, text="Username", font=("Arial", 12), bg="#ffffff", fg="#333333"
        ).pack(pady=5, anchor="w", padx=30)
        username_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#f0f0f0", bd=0)
        username_entry.pack(pady=5, ipadx=5, ipady=5, fill="x", padx=30)

        # Password Entry
        tk.Label(
            self.frame, text="Password", font=("Arial", 12), bg="#ffffff", fg="#333333"
        ).pack(pady=5, anchor="w", padx=30)
        password_entry = tk.Entry(self.frame, font=("Arial", 12), bg="#f0f0f0", bd=0, show="*")
        password_entry.pack(pady=5, ipadx=5, ipady=5, fill="x", padx=30)

        # Register Button
        register_button = tk.Button(
            self.frame,
            text="REGISTER",
            font=("Arial", 14, "bold"),
            bg="#0066cc",
            fg="#ffffff",
            bd=0,
            command=lambda: self.register_user(username_entry.get(), password_entry.get()),
        )
        register_button.pack(pady=20, ipadx=10, ipady=10, fill="x", padx=30)

        # Back to Login Link
        login_label = tk.Label(
            self.frame,
            text="Back to Login",
            font=("Arial", 10),
            bg="#ffffff",
            fg="#0066cc",
            cursor="hand2",
        )
        login_label.pack(pady=15)
        login_label.bind("<Button-1>", lambda e: self.login_page())

    def register_user(self, username, password):
        """Register a new user."""
        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty!")
            return
        if username in user_database:
            messagebox.showerror("Error", "Username already exists!")
        else:
            user_database[username] = password
            save_user_to_database(username, password)
            messagebox.showinfo("Success", "Registration successful!")
            self.login_page()

    

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodApp(root)
    root.mainloop()