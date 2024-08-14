import customtkinter as ctk
import requests
from tkinter import messagebox

BASE_URL = "http://localhost:8000"  # Adjust this to match your API's base URL

class APIClient:
    @staticmethod
    def login(username, password):
        url = f"{BASE_URL}/token"
        data = {
            "username": username,
            "password": password
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Login failed: {response.text}")

    @staticmethod
    def signup(username, email, password):
        url = f"{BASE_URL}/user/signup"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Signup failed: {response.text}")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Login Screen")
        self.geometry("1200x700")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_login_frame()
        self.create_right_frame()

    def create_login_frame(self):
        self.login_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
        self.login_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        self.login_frame.grid_rowconfigure(4, weight=1)
        self.login_frame.grid_columnconfigure(0, weight=1)

        self.login_label = ctk.CTkLabel(self.login_frame, text="Sign In", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"), text_color="blue")
        self.login_label.grid(row=0, column=0, padx=40, pady=30, sticky="nw")

        self.username_frame = self.create_input_frame("Username")
        self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="nw")

        self.password_frame = self.create_input_frame("Password", show="•")
        self.password_frame.grid(row=2, column=0, padx=40, pady=(0, 10), sticky="nw")

        self.login_button = ctk.CTkButton(self.login_frame, text="Sign In", command=self.login_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        self.login_button.grid(row=5, column=0, padx=40, pady=(2, 20))

    def create_input_frame(self, label_text, show=None):
        frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(family="Helvetica", size=20), text_color="blue")
        label.grid(row=0, column=0, sticky="nw")
        entry = ctk.CTkEntry(frame, width=400, height=60, show=show, placeholder_text=f"enter your {label_text.lower()}", font=ctk.CTkFont(family="Helvetica", size=20))
        entry.grid(row=1, column=0)
        return frame

    def create_right_frame(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_rowconfigure(4, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.welcome_label = ctk.CTkLabel(self.right_frame, text="Welcome Back!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
        self.welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

        self.sub_label = ctk.CTkLabel(self.right_frame, text="Please Sign in to Continue.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        self.sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

        self.signup_label = ctk.CTkLabel(self.right_frame, text="New to Data Hive?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        self.signup_label.grid(row=2, column=0, padx=40, pady=(80, 0))

        self.signup_button = ctk.CTkButton(self.right_frame, text="Sign Up", command=self.show_signup_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        self.signup_button.grid(row=3, column=0, padx=40, pady=(30, 120))

    def login_event(self):
        username = self.username_frame.winfo_children()[1].get()
        password = self.password_frame.winfo_children()[1].get()
        
        try:
            token = APIClient.login(username, password)
            messagebox.showinfo("Login Successful", "You have successfully logged in!")
            self.destroy()
            from teste import DataHiveApp
            app = DataHiveApp(token)
            app.mainloop()
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def show_signup_page(self):
        self.destroy()
        SignUpApp().mainloop()

class SignUpApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sign Up Page")
        self.geometry("1200x700")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_signup_frame()
        self.create_right_frame()

    def create_signup_frame(self):
        self.signup_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
        self.signup_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        self.signup_frame.grid_rowconfigure(5, weight=1)
        self.signup_frame.grid_columnconfigure(0, weight=1)

        self.signup_label = ctk.CTkLabel(self.signup_frame, text="Sign Up", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"))
        self.signup_label.grid(row=0, column=0, padx=40, pady=30)

        self.username_frame = self.create_input_frame("Username")
        self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 20))

        self.email_frame = self.create_input_frame("Email")
        self.email_frame.grid(row=2, column=0, padx=40, pady=(0, 20))

        self.password_frame = self.create_input_frame("Password", show="•")
        self.password_frame.grid(row=3, column=0, padx=40, pady=(0, 20))

        self.signup_button = ctk.CTkButton(self.signup_frame, text="Sign Up", command=self.signup_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        self.signup_button.grid(row=4, column=0, padx=40, pady=(20, 20))

    def create_input_frame(self, label_text, show=None):
        frame = ctk.CTkFrame(self.signup_frame, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(family="Helvetica", size=20))
        label.grid(row=0, column=0, sticky="nw")
        entry = ctk.CTkEntry(frame, width=400, height=60, show=show, placeholder_text=f"enter your {label_text.lower()}", font=ctk.CTkFont(family="Helvetica", size=20))
        entry.grid(row=1, column=0)
        return frame

    def create_right_frame(self):
        self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_rowconfigure(4, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.welcome_label = ctk.CTkLabel(self.right_frame, text="Welcome to Data Hive!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
        self.welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

        self.sub_label = ctk.CTkLabel(self.right_frame, text="Please Sign up to get started.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        self.sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

        self.login_label = ctk.CTkLabel(self.right_frame, text="Already have an account?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        self.login_label.grid(row=2, column=0, padx=40, pady=(80, 0))

        self.login_button = ctk.CTkButton(self.right_frame, text="Sign In", command=self.show_login_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        self.login_button.grid(row=3, column=0, padx=40, pady=(30, 120))

    def signup_event(self):
        username = self.username_frame.winfo_children()[1].get()
        email = self.email_frame.winfo_children()[1].get()
        password = self.password_frame.winfo_children()[1].get()
        
        try:
            user = APIClient.signup(username, email, password)
            messagebox.showinfo("Signup Successful", "You have successfully signed up!")
            self.show_login_page()
        except Exception as e:
            messagebox.showerror("Signup Failed", str(e))

    def show_login_page(self):
        self.destroy()
        LoginApp().mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()