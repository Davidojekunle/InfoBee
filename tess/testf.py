import customtkinter as ctk
import requests
from tkinter import messagebox

BASE_URL = "http://localhost:8000"  # Adjust this to match your API's base URL

class APIClient:
    @staticmethod
    def login(username, password):
        url = f"{BASE_URL}/token"
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception(f"Login failed: {response.text}")

    @staticmethod
    def signup(username, email, password):
        url = f"{BASE_URL}/user/signup"
        data = {"username": username, "email": email, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Signup failed: {response.text}")

class BaseApp(ctk.CTk):
    def __init__(self, title, geometry="1200x700"):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def create_input_frame(self, parent, label_text, show=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(family="Helvetica", size=20))
        label.grid(row=0, column=0, sticky="nw")
        entry = ctk.CTkEntry(frame, width=400, height=60, show=show, placeholder_text=f"enter your {label_text.lower()}", font=ctk.CTkFont(family="Helvetica", size=20))
        entry.grid(row=1, column=0)
        return frame

class HoverFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.original_color = kwargs.get('fg_color', 'white')

    def on_enter(self, event):
        self.configure(border_width=2, border_color="#3B3BFF")

    def on_leave(self, event):
        self.configure(border_width=0)

class LoginApp(BaseApp):
    def __init__(self):
        super().__init__("Login Screen")
        self.create_login_frame()
        self.create_right_frame()

    def create_login_frame(self):
        login_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
        login_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        login_frame.grid_rowconfigure(4, weight=1)
        login_frame.grid_columnconfigure(0, weight=1)

        login_label = ctk.CTkLabel(login_frame, text="Sign In", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"), text_color="blue")
        login_label.grid(row=0, column=0, padx=40, pady=30, sticky="nw")

        self.username_frame = self.create_input_frame(login_frame, "Username")
        self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="nw")

        self.password_frame = self.create_input_frame(login_frame, "Password", show="•")
        self.password_frame.grid(row=2, column=0, padx=40, pady=(0, 10), sticky="nw")

        login_button = ctk.CTkButton(login_frame, text="Sign In", command=self.login_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        login_button.grid(row=5, column=0, padx=40, pady=(2, 20))

    def create_right_frame(self):
        right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(4, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        welcome_label = ctk.CTkLabel(right_frame, text="Welcome Back!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
        welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

        sub_label = ctk.CTkLabel(right_frame, text="Please Sign in to Continue.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

        signup_label = ctk.CTkLabel(right_frame, text="New to Data Hive?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        signup_label.grid(row=2, column=0, padx=40, pady=(80, 0))

        signup_button = ctk.CTkButton(right_frame, text="Sign Up", command=self.show_signup_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        signup_button.grid(row=3, column=0, padx=40, pady=(30, 120))

    def login_event(self):
        username = self.username_frame.winfo_children()[1].get()
        password = self.password_frame.winfo_children()[1].get()
        try:
            token = APIClient.login(username, password)
            messagebox.showinfo("Login Successful", "You have successfully logged in!")
            self.destroy()
            DataHiveApp(token, username).mainloop()
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def show_signup_page(self):
        self.destroy()
        SignUpApp().mainloop()

class SignUpApp(BaseApp):
    def __init__(self):
        super().__init__("Sign Up Page")
        self.create_signup_frame()
        self.create_right_frame()

    def create_signup_frame(self):
        signup_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
        signup_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        signup_frame.grid_rowconfigure(5, weight=1)
        signup_frame.grid_columnconfigure(0, weight=1)

        signup_label = ctk.CTkLabel(signup_frame, text="Sign Up", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"))
        signup_label.grid(row=0, column=0, padx=40, pady=30)

        self.username_frame = self.create_input_frame(signup_frame, "Username")
        self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 20))

        self.email_frame = self.create_input_frame(signup_frame, "Email")
        self.email_frame.grid(row=2, column=0, padx=40, pady=(0, 20))

        self.password_frame = self.create_input_frame(signup_frame, "Password", show="•")
        self.password_frame.grid(row=3, column=0, padx=40, pady=(0, 20))

        signup_button = ctk.CTkButton(signup_frame, text="Sign Up", command=self.signup_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        signup_button.grid(row=4, column=0, padx=40, pady=(20, 20))

    def create_right_frame(self):
        right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
        right_frame.grid(row=0, column=1, sticky="nsew")
        right_frame.grid_rowconfigure(4, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        welcome_label = ctk.CTkLabel(right_frame, text="Welcome to Data Hive!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
        welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

        sub_label = ctk.CTkLabel(right_frame, text="Please Sign up to get started.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

        login_label = ctk.CTkLabel(right_frame, text="Already have an account?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
        login_label.grid(row=2, column=0, padx=40, pady=(80, 0))

        login_button = ctk.CTkButton(right_frame, text="Sign In", command=self.show_login_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
        login_button.grid(row=3, column=0, padx=40, pady=(30, 120))

    def signup_event(self):
        username = self.username_frame.winfo_children()[1].get()
        email = self.email_frame.winfo_children()[1].get()
        password = self.password_frame.winfo_children()[1].get()
        try:
            APIClient.signup(username, email, password)
            messagebox.showinfo("Signup Successful", "Account created successfully!")
            self.show_login_page()
        except Exception as e:
            messagebox.showerror("Signup Failed", str(e))

    def show_login_page(self):
        self.destroy()
        LoginApp().mainloop()

class DataHiveApp(BaseApp):
    def __init__(self):
        super().__init__()
        self.title("DATA-HIVE")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create header
        self.header = ctk.CTkFrame(self, height=50, fg_color="white", corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        greeting = ctk.CTkLabel(self.header, text="Hi, username!", text_color="black")
        greeting.pack(side="left", padx=20)
        subscription = ctk.CTkLabel(self.header, text="subscription: Free", text_color="black")
        subscription.pack(side="right", padx=20)

        # Create sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1a237e")
        self.sidebar.grid(row=1, column=0, sticky="nsw", padx=0, pady=0)

        # Add app name to sidebar
        app_name = ctk.CTkLabel(self.sidebar, text="DATA- HIVE", font=("Helvetica", 24, "bold"), text_color="white")
        app_name.pack(pady=(20, 40), padx=20)

        # Add sidebar buttons
        self.sidebar_buttons = []
        for text, page in [("Dashboard", DashboardPage), 
                           ("My Files", MyFilesPage), 
                           ("Analysis", AnalysisPage), 
                           ("Visuals", VisualsPage)]:
            button = ctk.CTkButton(self.sidebar, text=text, 
                                   command=lambda p=page: self.show_frame(p),
                                   fg_color="transparent", text_color="white",
                                   hover_color="#3949ab", anchor="w")
            button.pack(pady=10, padx=20, fill="x")
            self.sidebar_buttons.append(button)

        # Create main content area
        self.main_content = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
        self.main_content.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_rowconfigure(0, weight=1)

        # Create and add frames to the main content area
        self.frames = {}
        for F in (DashboardPage, MyFilesPage, AnalysisPage, VisualsPage):
            frame = F(self.main_content, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the initial frame
        self.show_frame(DashboardPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        # File statistics
        files_frame = ctk.CTkFrame(self, fg_color="transparent")
        files_frame.pack(pady=20, padx=60, fill="x", expand=True)

        uploaded_files = ctk.CTkFrame(files_frame, fg_color="light gray")
        uploaded_files.pack(side="left", expand=True, pady=20, padx=(0, 10), fill="both")
        ctk.CTkLabel(uploaded_files, text="12", font=("Roboto", 36, "bold"), text_color="black").pack(pady=(20, 0))
        ctk.CTkLabel(uploaded_files, text="Your Uploaded Files", font=("Roboto", 18), text_color="black").pack(pady=(0, 20))
        ctk.CTkButton(uploaded_files, text="Upload", fg_color="#4CAF50", hover_color="#45a049").pack(pady=(0, 20))


        analyzed_files = ctk.CTkFrame(files_frame, fg_color="light gray")
        analyzed_files.pack(side="right", expand=True, pady=20, padx=(10, 0), fill="both")
        ctk.CTkLabel(analyzed_files, text="13", font=("Roboto", 36, "bold"), text_color="black").pack(pady=(20, 0))
        ctk.CTkLabel(analyzed_files, text="Your Analyzed Files", font=("Roboto", 18), text_color="black").pack(pady=(0, 20))
        ctk.CTkButton(analyzed_files, text="Check Analysis", fg_color="#3F51B5", hover_color="#303F9F").pack(pady=(0, 20))

        # Payment Plans and Profile Information
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(pady=20, padx=60, fill="x", expand=True)

        plans_frame = ctk.CTkFrame(bottom_frame, fg_color="#E8F5E9")
        plans_frame.pack(side="left", expand=True, pady=20, padx=(0, 10), fill="both")
        ctk.CTkLabel(plans_frame, text="Payment Plans", font=("Roboto", 24, "bold"), text_color="#2E7D32").pack(pady=(20, 10))
        ctk.CTkButton(plans_frame, text="View Plans", fg_color="#4CAF50", hover_color="#45a049").pack(pady=(10, 20))

        profile_frame = ctk.CTkFrame(bottom_frame, fg_color="light gray")
        profile_frame.pack(side="right", expand=True, pady=20, padx=(10, 0), fill="both")
        ctk.CTkLabel(profile_frame, text="Profile Information", font=("Roboto", 24, "bold"), text_color="black").pack(pady=(20, 10))
        ctk.CTkButton(profile_frame, text="View Profile", fg_color="#3F51B5", hover_color="#303F9F").pack(pady=(10, 20))


    def upload_file(self):
        # Implement file upload functionality
        pass

    def check_analysis(self):
        # Implement analysis check functionality
        pass

class MyFilesPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        label = ctk.CTkLabel(self, text="UPLOADED FILES:", font=("Roboto", 24))
        label.pack(pady=10, padx=10)

        
            

class AnalysisPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        label = ctk.CTkLabel(self, text="ANALYSIS FILES:", font=("Roboto", 24))
        label.pack(pady=10, padx=10)

class VisualsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        label = ctk.CTkLabel(self, text="VISUALS:", font=("Roboto", 24))
        label.pack(pady=10, padx=10)


if __name__ == "__main__":
    app = DataHiveApp()
    app.mainloop()