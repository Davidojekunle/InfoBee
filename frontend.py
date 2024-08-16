# import os
# import customtkinter as ctk
# import requests
# from tkinter import filedialog, messagebox
# from typing import Dict, Any, List
# from PIL import Image, ImageTk
# import logging
# import webbrowser
# import threading
# from functools import lru_cache

# BASE_URL = "http://localhost:8000"  # Adjust this to match your API's base URL
# logger = logging.getLogger(__name__)

# class APIClient:
#     def __init__(self, token: str = None):
#         self.token = token
#         self.headers = {
#             "Authorization": f"Bearer {self.token}" if token else "",
#             "Content-Type": "application/json"
#         }
#     @staticmethod
#     def login(username: str, password: str) -> str:
#         url = f"{BASE_URL}/token"
#         data = {
#             "username": username,
#             "password": password
#         }
#         response = requests.post(url, data=data)
#         if response.status_code == 200:
#             return response.json()["access_token"]
#         else:
#             raise Exception(f"Login failed: {response.text}")

#     @staticmethod
#     def signup(username: str, email: str, password: str) -> Dict[str, Any]:
#         url = f"{BASE_URL}/user/signup"
#         data = {
#             "username": username,
#             "email": email,
#             "password": password
#         }
#         response = requests.post(url, json=data)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             raise Exception(f"Signup failed: {response.text}")

#     def get_file_list(self) -> List[Dict[str, Any]]:
#         """Fetch the list of files from the API."""
#         response = requests.get(f"{BASE_URL}/user/getfiles", headers=self.headers)
#         response.raise_for_status()
#         return response.json()
    
#     def get_file_list(self):
#         """Fetch the list of files from the API with caching."""
#         response = requests.get(f"{BASE_URL}/user/getfiles", headers=self.headers)
#         response.raise_for_status()
#         return response.json()


#     def upload_file(self, file_path: str) -> Dict[str, Any]:
        
#         if not os.path.exists(file_path):
#             raise ValueError(f"File not found: {file_path}")
        
#         try:
#             with open(file_path, 'rb') as file:
#                 file_name = os.path.basename(file_path)
#                 files = {'file': (file_name, file, 'application/octet-stream')}
                
#                 headers = self.headers.copy()
#                 # Remove Content-Type from headers as it's set automatically for multipart/form-data
#                 headers.pop('Content-Type', None)
                
#                 response = requests.post(
#                     f"{BASE_URL}/me/uploadfile",
#                     headers=headers,
#                     files=files
#                 )
            
#             response.raise_for_status()
#             return response.json()
        
#         except requests.exceptions.RequestException as e:
#             logger.error(f"Request failed: {str(e)}")
#             if hasattr(e, 'response') and e.response is not None:
#                 logger.error(f"Response status code: {e.response.status_code}")
#                 logger.error(f"Response content: {e.response.text}")
#             raise
        
#         except Exception as e:
#             logger.error(f"An unexpected error occurred: {str(e)}")
#             raise
#     def get_user_info(self) -> Dict[str, Any]:
#         """Fetch the user's information from the API."""
#         response = requests.get(f"{BASE_URL}/user/info", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

#     def update_user_info(self, updated_info: Dict[str, Any]) -> Dict[str, Any]:
#         """Update the user's information."""
#         response = requests.put(f"{BASE_URL}/user/info", headers=self.headers, json=updated_info)
#         response.raise_for_status()
#         return response.json()

#     def change_password(self, current_password: str, new_password: str) -> Dict[str, Any]:
#         """Change the user's password."""
#         data = {
#             "current_password": current_password,
#             "new_password": new_password
#         }
#         response = requests.post(f"{BASE_URL}/user/change-password", headers=self.headers, json=data)
#         response.raise_for_status()
#         return response.json()



#     def view_file(self, filename: str) -> Dict[str, Any]:
#         """View the contents of a specific file."""
#         response = requests.get(f"{BASE_URL}/user/files/{filename}", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

#     def analyze_file(self, filename: str) -> Dict[str, Any]:
#         """Initiate analysis for a specific file."""
#         response = requests.post(f"{BASE_URL}/user/analysis/{filename}", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

#     def delete_file(self, filename: str) -> Dict[str, Any]:
#         """Delete a specific file."""
#         response = requests.delete(f"{BASE_URL}/user/files/{filename}", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

#     def get_file_count(self) -> Dict[str, int]:
#         """Get the count of total and analyzed files."""
#         response = requests.get(f"{BASE_URL}/dashboard/file_count", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

#     def get_analysis_list(self) -> List[Dict[str, Any]]:
#         """Get the list of analyses."""
#         response = requests.get(f"{BASE_URL}/dashboard/analysis_list", headers=self.headers)
#         response.raise_for_status()
#         return response.json()
    
#     def get_analyzed_files(self) -> List[Dict[str, Any]]:
#         """Fetch the list of analyzed files from the API."""
#         response = requests.get(f"{BASE_URL}/user/analysis", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

#     def get_full_analysis(self, analysis_id: int) -> Dict[str, Any]:
#         """Fetch the full analysis for a specific file."""
#         response = requests.get(f"{BASE_URL}/user/analysis/{analysis_id}", headers=self.headers)
#         response.raise_for_status()
#         return response.json()
    
#     def get_subscription_plans(self) -> List[Dict[str, Any]]:
#         """Fetch the list of subscription plans from the API."""
#         response = requests.get(f"{BASE_URL}/subscriptions/view", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

#     def pay_for_subscription(self, sub_type: str) -> Dict[str, Any]:
#         """Initiate payment for a subscription."""
#         response = requests.post(f"{BASE_URL}/pay/{sub_type}", headers=self.headers)
#         response.raise_for_status()
#         return response.json()
#     def create_visualizations(self, file_name: str) -> Dict[str, Any]:
#         """Create visualizations for a file."""
#         response = requests.post(f"{BASE_URL}/user/visuals/{file_name}", headers=self.headers)
#         response.raise_for_status()
#         return response.json()
    
#     def get_file_count(self) -> Dict[str, int]:
#         """Get the count of total and analyzed files."""
#         response = requests.get(f"{BASE_URL}/dashboard/file_count", headers=self.headers)
#         response.raise_for_status()
#         return response.json()
    
#     def get_user_subscription(self) -> Dict[str, Any]:
#         """Get the user's current subscription information."""
#         response = requests.get(f"{BASE_URL}/user/subscription", headers=self.headers)
#         response.raise_for_status()
#         return response.json()

# class LoginApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("Login Screen")
#         self.geometry("1200x700")
#         self.resizable(False, False)

#         self.grid_columnconfigure(1, weight=1)
#         self.grid_rowconfigure(0, weight=1)

#         self.create_login_frame()
#         self.create_right_frame()

#     def create_login_frame(self):
#         self.login_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
#         self.login_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
#         self.login_frame.grid_rowconfigure(4, weight=1)
#         self.login_frame.grid_columnconfigure(0, weight=1)

#         self.login_label = ctk.CTkLabel(self.login_frame, text="Sign In", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"), text_color="blue")
#         self.login_label.grid(row=0, column=0, padx=40, pady=30, sticky="nw")

#         self.username_frame = self.create_input_frame("Username")
#         self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="nw")

#         self.password_frame = self.create_input_frame("Password", show="•")
#         self.password_frame.grid(row=2, column=0, padx=40, pady=(0, 10), sticky="nw")

#         self.login_button = ctk.CTkButton(self.login_frame, text="Sign In", command=self.login_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
#         self.login_button.grid(row=5, column=0, padx=40, pady=(2, 20))

#     def create_input_frame(self, label_text, show=None):
#         frame = ctk.CTkFrame(self.login_frame, fg_color="transparent")
#         label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(family="Helvetica", size=20), text_color="black")
#         label.grid(row=0, column=0, sticky="nw")
#         entry = ctk.CTkEntry(frame, width=400, height=60, show=show, placeholder_text=f"enter your {label_text.lower()}", font=ctk.CTkFont(family="Helvetica", size=20))
#         entry.grid(row=1, column=0)
#         return frame

#     def create_right_frame(self):
#         self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
#         self.right_frame.grid(row=0, column=1, sticky="nsew")
#         self.right_frame.grid_rowconfigure(4, weight=1)
#         self.right_frame.grid_columnconfigure(0, weight=1)

#         self.welcome_label = ctk.CTkLabel(self.right_frame, text="Welcome Back!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
#         self.welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

#         self.sub_label = ctk.CTkLabel(self.right_frame, text="Please Sign in to Continue.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
#         self.sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

#         self.signup_label = ctk.CTkLabel(self.right_frame, text="New to Data Hive?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
#         self.signup_label.grid(row=2, column=0, padx=40, pady=(80, 0))

#         self.signup_button = ctk.CTkButton(self.right_frame, text="Sign Up", command=self.show_signup_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
#         self.signup_button.grid(row=3, column=0, padx=40, pady=(30, 120))

#     def login_event(self):
#         username = self.username_frame.winfo_children()[1].get()
#         password = self.password_frame.winfo_children()[1].get()
        
#         try:
#             token = APIClient.login(username, password)
#             messagebox.showinfo("Login Successful", "You have successfully logged in!")
#             self.destroy()
#             DataHiveApp(token, username).mainloop()
#         except Exception as e:
#             messagebox.showerror("Login Failed", str(e))

#     def show_signup_page(self):
#         self.destroy()
#         SignUpApp().mainloop()

# class SignUpApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title("Sign Up Page")
#         self.geometry("1200x700")
#         self.resizable(False, False)

#         self.grid_columnconfigure(1, weight=1)
#         self.grid_rowconfigure(0, weight=1)

#         self.create_signup_frame()
#         self.create_right_frame()

#     def create_signup_frame(self):
#         self.signup_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#E0E0E0")
#         self.signup_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
#         self.signup_frame.grid_rowconfigure(5, weight=1)
#         self.signup_frame.grid_columnconfigure(0, weight=1)

#         self.signup_label = ctk.CTkLabel(self.signup_frame, text="Sign Up", font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"), text_color="black")
#         self.signup_label.grid(row=0, column=0, padx=40, pady=30)

#         self.username_frame = self.create_input_frame("Username")
#         self.username_frame.grid(row=1, column=0, padx=40, pady=(0, 20))

#         self.email_frame = self.create_input_frame("Email")
#         self.email_frame.grid(row=2, column=0, padx=40, pady=(0, 20))

#         self.password_frame = self.create_input_frame("Password", show="•")
#         self.password_frame.grid(row=3, column=0, padx=40, pady=(0, 20))

#         self.signup_button = ctk.CTkButton(self.signup_frame, text="Sign Up", command=self.signup_event, width=400, height=60, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
#         self.signup_button.grid(row=4, column=0, padx=40, pady=(20, 20))

#     def create_input_frame(self, label_text, show=None):
#         frame = ctk.CTkFrame(self.signup_frame, fg_color="transparent")
#         label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(family="Helvetica", size=20), text_color="black")
#         label.grid(row=0, column=0, sticky="nw")
#         entry = ctk.CTkEntry(frame, width=400, height=60, show=show, placeholder_text=f"enter your {label_text.lower()}", font=ctk.CTkFont(family="Helvetica", size=20))
#         entry.grid(row=1, column=0)
#         return frame

#     def create_right_frame(self):
#         self.right_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#1a237e")
#         self.right_frame.grid(row=0, column=1, sticky="nsew")
#         self.right_frame.grid_rowconfigure(4, weight=1)
#         self.right_frame.grid_columnconfigure(0, weight=1)

#         self.welcome_label = ctk.CTkLabel(self.right_frame, text="Welcome to Data Hive!", font=ctk.CTkFont(family="Helvetica", size=48, weight="bold"), text_color="white")
#         self.welcome_label.grid(row=0, column=0, padx=40, pady=(120, 30))

#         self.sub_label = ctk.CTkLabel(self.right_frame, text="Please Sign up to get started.", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
#         self.sub_label.grid(row=1, column=0, padx=40, pady=(0, 60))

#         self.login_label = ctk.CTkLabel(self.right_frame, text="Already have an account?", font=ctk.CTkFont(family="Helvetica", size=24), text_color="white")
#         self.login_label.grid(row=2, column=0, padx=40, pady=(80, 0))

#         self.login_button = ctk.CTkButton(self.right_frame, text="Sign In", command=self.show_login_page, fg_color="white", text_color="#1a237e", width=250, height=50, font=ctk.CTkFont(family="Helvetica", size=24, weight="bold"))
#         self.login_button.grid(row=3, column=0, padx=40, pady=(30, 120))

#     def signup_event(self):
#         username = self.username_frame.winfo_children()[1].get()
#         email = self.email_frame.winfo_children()[1].get()
#         password = self.password_frame.winfo_children()[1].get()
        
#         try:
#             user = APIClient.signup(username, email, password)
#             messagebox.showinfo("Signup Successful", "You have successfully signed up!")
#             self.show_login_page()
#         except Exception as e:
#             messagebox.showerror("Signup Failed", str(e))
#     def create_visualizations(self, file_name: str) -> Dict[str, Any]:
#         """Create visualizations for a file."""
#         response = requests.post(f"{BASE_URL}/user/visuals/{file_name}", headers=self.headers)
#         response.raise_for_status()
#         return response.json()
#     def show_login_page(self):
#         self.destroy()
#         LoginApp().mainloop()
    
# class DataHiveApp(ctk.CTk):
#     def __init__(self, token, username):
#         super().__init__()
#         self.token = token
#         self.username = username
#         self.api_client = APIClient(token)
#         self.title("DATA-HIVE")
#         self.geometry("1200x700")
#         self.resizable(False, False)

#         # Configure grid
#         self.grid_columnconfigure(1, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         # Create header
#         self.header = ctk.CTkFrame(self, height=50, fg_color="white", corner_radius=0)
#         self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
#         greeting = ctk.CTkLabel(self.header, text=f"Hi, {self.username}!", text_color="black")
#         greeting.pack(side="left", padx=20)
#         self.subscription_label = ctk.CTkLabel(self.header, text="", text_color="black")
#         self.subscription_label.pack(side="right", padx=20)
       
#         # Update subscription info
#         self.update_subscription_info()
#     def update_subscription_info(self):
#         try:
#             subscription_info = self.api_client.get_user_subscription()
#             subscription_type = subscription_info.get("plan_name", "Free")
#             self.subscription_label.configure(text=f"Subscription: {subscription_type}")
#         except Exception as e:
#             print(f"Failed to fetch subscription info: {str(e)}")
#             self.subscription_label.configure(text="Subscription: Unknown")

#         # Create sidebar
#         self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color="#1a237e")
#         self.sidebar.grid(row=1, column=0, sticky="nsw", padx=0, pady=0)

#         # Add app name to sidebar
#         app_name = ctk.CTkLabel(self.sidebar, text="DATA- HIVE", font=("Helvetica", 24, "bold"), text_color="white")
#         app_name.pack(pady=(20, 40), padx=20)

#         # Add sidebar buttons
#         # Add sidebar buttons
#         self.sidebar_buttons = []
#         for text, page in [("Dashboard", DashboardPage), 
#                         ("My Files", MyFilesPage), 
#                         ("Analysis", AnalysisPage), 
#                         ("Visuals", VisualsPage),
#                         ("Payment", PaymentPage),
#                         ("Profile", ProfilePage),
#                         ("Twitter Insights", TwitterInsightsPage)]:  # Add this line
#             button = ctk.CTkButton(self.sidebar, text=text, 
#                                 command=lambda p=page: self.show_frame(p),
#                                 fg_color="transparent", text_color="white",
#                                 hover_color="#3949ab", anchor="w")
#             button.pack(pady=10, padx=20, fill="x")
#             self.sidebar_buttons.append(button)

#         # Add logout button
#         logout_button = ctk.CTkButton(self.sidebar, text="Log Out", 
#                                       command=self.logout,
#                                       fg_color="transparent", text_color="white",
#                                       hover_color="#3949ab", anchor="w")
#         logout_button.pack(pady=10, padx=20, fill="x")

#         # Create main content area
#         self.main_content = ctk.CTkFrame(self, fg_color="white", corner_radius=0)
#         self.main_content.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
#         self.main_content.grid_columnconfigure(0, weight=1)
#         self.main_content.grid_rowconfigure(0, weight=1)
#         self.stop_auto_update = threading.Event()
#         self.auto_update_thread = threading.Thread(target=self.auto_update)
#         self.auto_update_thread.start()
#         # Create and add frames to the main content area
#         # Create and add frames to the main content area
#         self.frames = {}
#         for F in (DashboardPage, MyFilesPage, AnalysisPage, VisualsPage, PaymentPage, ProfilePage, TwitterInsightsPage):  # Add TwitterInsightsPage here
#             frame = F(self.main_content, self)
#             self.frames[F] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         # Show the initial frame
#         self.show_frame(DashboardPage)
#         self.stop_auto_update = threading.Event()
#         self.auto_update_thread = threading.Thread(target=self.auto_update)
#         self.auto_update_thread.start()
#     def auto_update(self):
#         while not self.stop_auto_update.is_set():
#             self.update_all_pages()
#             self.stop_auto_update.wait(60)

#     def update_all_pages(self):
#         for frame in self.frames.values():
#             if hasattr(frame, 'update_content'):
#                 frame.update_content()
#     def show_frame(self, cont):
#         frame = self.frames[cont]
#         frame.tkraise()
        
#         # Update the content of the frame
#         if hasattr(frame, 'update_content'):
#             frame.update_content()
        
#         # Highlight the current button
#         for button in self.sidebar_buttons:
#             if button.cget("text") == frame.__class__.__name__.replace("Page", ""):
#                 button.configure(fg_color="#3949ab")  # Highlight color
#             else:
#                 button.configure(fg_color="transparent")
#     def logout(self):
#         self.stop_auto_update.set()
#         self.auto_update_thread.join()
#         self.destroy()
#         LoginApp().mainloop()
    

# class DashboardPage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.api_client = APIClient(controller.token)
        
#         # File statistics
#         files_frame = ctk.CTkFrame(self, fg_color="transparent")
#         files_frame.pack(pady=20, padx=60, fill="x", expand=True)

#         self.uploaded_files = ctk.CTkFrame(files_frame, fg_color="light gray")
#         self.uploaded_files.pack(side="left", expand=True, pady=20, padx=(0, 10), fill="both")

#         self.analyzed_files = ctk.CTkFrame(files_frame, fg_color="light gray")
#         self.analyzed_files.pack(side="right", expand=True, pady=20, padx=(10, 0), fill="both")

#         # Update file counts
#         self.update_file_counts()

#         ctk.CTkButton(self.uploaded_files, text="Upload", fg_color="#4CAF50", hover_color="#45a049", command=self.upload_file).pack(pady=(0, 20))
#         ctk.CTkButton(self.analyzed_files, text="Check Analysis", fg_color="#3F51B5", hover_color="#303F9F", command=lambda: controller.show_frame(AnalysisPage)).pack(pady=(0, 20))

#         # Payment Plans and Profile Information
#         bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
#         bottom_frame.pack(pady=20, padx=60, fill="x", expand=True)

#         plans_frame = ctk.CTkFrame(bottom_frame, fg_color="#E8F5E9")
#         plans_frame.pack(side="left", expand=True, pady=20, padx=(0, 10), fill="both")
#         ctk.CTkLabel(plans_frame, text="Payment Plans", font=("Roboto", 24, "bold"), text_color="#2E7D32").pack(pady=(20, 10))
#         ctk.CTkButton(plans_frame, text="View Plans", fg_color="#4CAF50", hover_color="#45a049", command=lambda: controller.show_frame(PaymentPage)).pack(pady=(10, 20))

#         profile_frame = ctk.CTkFrame(bottom_frame, fg_color="light gray")
#         profile_frame.pack(side="right", expand=True, pady=20, padx=(10, 0), fill="both")
#         ctk.CTkLabel(profile_frame, text="Profile Information", font=("Roboto", 24, "bold"), text_color="black").pack(pady=(20, 10))
#         ctk.CTkButton(profile_frame, text="View Profile", fg_color="#3F51B5", hover_color="#303F9F", command=lambda: controller.show_frame(ProfilePage)).pack(pady=(10, 20))

#         # Recent Activity
#         activity_frame = ctk.CTkFrame(self, fg_color="transparent")
#         activity_frame.pack(pady=20, padx=60, fill="both", expand=True)
#         ctk.CTkLabel(activity_frame, text="Recent Activity", font=("Roboto", 24, "bold"), text_color="black").pack(pady=(0, 10), anchor="w")
        
#         # Placeholder for recent activity list
#         activity_list = ctk.CTkFrame(activity_frame, fg_color="light gray")
#         activity_list.pack(fill="both", expand=True, pady=(0, 20))
#         ctk.CTkLabel(activity_list, text="No recent activity", font=("Roboto", 18), text_color="gray").pack(pady=20)
#     def update_file_counts(self):
#         try:
#             file_counts = self.api_client.get_file_count()
            
#             for widget in self.uploaded_files.winfo_children():
#                 widget.destroy()
#             for widget in self.analyzed_files.winfo_children():
#                 widget.destroy()

#             ctk.CTkLabel(self.uploaded_files, text=str(file_counts["total_files"]), font=("Roboto", 36, "bold"), text_color="black").pack(pady=(20, 0))
#             ctk.CTkLabel(self.uploaded_files, text="Your Uploaded Files", font=("Roboto", 18), text_color="black").pack(pady=(0, 20))

#             ctk.CTkLabel(self.analyzed_files, text=str(file_counts["analyzed_files"]), font=("Roboto", 36, "bold"), text_color="black").pack(pady=(20, 0))
#             ctk.CTkLabel(self.analyzed_files, text="Your Analyzed Files", font=("Roboto", 18), text_color="black").pack(pady=(0, 20))

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch file counts: {str(e)}")
#     def upload_file(self):
#         # Call the upload_file method from MyFilesPage
#         my_files_page = self.controller.frames[MyFilesPage]
#         my_files_page.upload_file()
    
# class MyFilesPage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.api_client = APIClient(controller.token)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         # Title
#         title_label = ctk.CTkLabel(self, text="My Files", font=("Helvetica", 32, "bold"), text_color="black")
#         title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="w")

#         # File list frame
#         self.file_list_frame = ctk.CTkFrame(self)
#         self.file_list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
#         self.file_list_frame.grid_columnconfigure(0, weight=1)
#         self.file_list_frame.grid_rowconfigure(0, weight=1)

#         # Scrollable frame for file list
#         self.scrollable_frame = ctk.CTkScrollableFrame(self.file_list_frame)
#         self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)

#         # File options frame
#         self.file_options_frame = ctk.CTkFrame(self)
#         self.file_options_frame.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)

#         # Upload button
#         self.upload_button = ctk.CTkButton(self, text="Upload File", command=self.upload_file)
#         self.upload_button.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="e")

#         # Populate file list
#         self.populate_file_list()
#         self.file_list = []
#         self.current_page = 0
#         self.files_per_page = 20

#     def populate_file_list(self):
#         # Clear existing widgets
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()

#         try:
#             # Fetch the updated file list
#             files = self.api_client.get_file_list()

#             # Create a button for each file
#             for i, file in enumerate(files):
#                 file_button = ctk.CTkButton(self.scrollable_frame, text=file["filename"], 
#                                             command=lambda f=file["filename"]: self.show_file_options(f))
#                 file_button.grid(row=i, column=0, pady=5, padx=10, sticky="ew")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch file list: {str(e)}")

#     def next_page(self):
#         self.current_page += 1
#         self.populate_file_list()

#     def prev_page(self):
#         self.current_page = max(0, self.current_page - 1)
#         self.populate_file_list()

#     def populate_file_list(self):
#         # Clear existing widgets
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()

#         try:
#             # Fetch file list from API
#             files = self.api_client.get_file_list()

#             # Create a button for each file
#             for i, file in enumerate(files):
#                 file_button = ctk.CTkButton(self.scrollable_frame, text=file["filename"], 
#                                             command=lambda f=file["filename"]: self.show_file_options(f))
#                 file_button.grid(row=i, column=0, pady=5, padx=10, sticky="ew")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch file list: {str(e)}")

#     def show_file_options(self, filename):
#         # Clear existing widgets in file options frame
#         for widget in self.file_options_frame.winfo_children():
#             widget.destroy()

#         # Add file options
#         ctk.CTkLabel(self.file_options_frame, text=f"Options for {filename}", font=("Helvetica", 18, "bold")).pack(pady=10)
#         ctk.CTkButton(self.file_options_frame, text="View File", command=lambda: self.view_file(filename)).pack(pady=5)
#         ctk.CTkButton(self.file_options_frame, text="Analyze File", command=lambda: self.analyze_file(filename)).pack(pady=5)
#         ctk.CTkButton(self.file_options_frame, text="Delete File", command=lambda: self.delete_file(filename)).pack(pady=5)

#     def upload_file(self):
#         file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
#         if file_path:
#             try:
#                 response = self.api_client.upload_file(file_path)
#                 messagebox.showinfo("Upload Successful", f"File {os.path.basename(file_path)} uploaded successfully")
#                 self.populate_file_list()  # Refresh the file list
#             except Exception as e:
#                 messagebox.showerror("Upload Failed", f"Failed to upload file: {str(e)}")

#     def view_file(self, filename):
#         try:
#             response = self.api_client.view_file(filename)
#             # Here you would typically open a new window to display the file contents
#             messagebox.showinfo("File Contents", response['contents'])
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to view file: {str(e)}")

#     def analyze_file(self, filename):
#         try:
#             response = self.api_client.analyze_file(filename)
#             messagebox.showinfo("Analysis", f"Analysis for {filename} initiated. Results: {response['summary_statistics']}")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to analyze file: {str(e)}")

#     def delete_file(self, filename):
#         if messagebox.askyesno("Delete File", f"Are you sure you want to delete {filename}?"):
#             try:
#                 self.api_client.delete_file(filename)
#                 messagebox.showinfo("Delete File", f"{filename} deleted successfully")
#                 self.populate_file_list()  # Refresh the file list
                
#                 # Clear file options frame
#                 for widget in self.file_options_frame.winfo_children():
#                     widget.destroy()
#             except Exception as e:
#                 messagebox.showerror("Error", f"Failed to delete file: {str(e)}")

#     def update_content(self):
#         self.populate_file_list()
        

# class AnalysisPage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.api_client = APIClient(controller.token)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         title_label = ctk.CTkLabel(self, text="Analysis", font=("Helvetica", 32, "bold"), text_color="black")
#         title_label.grid(row=0, column=0, pady=20, padx=20, sticky="w")

#         # Create scrollable frame for analysis list
#         self.scrollable_frame = ctk.CTkScrollableFrame(self)
#         self.scrollable_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
#         self.scrollable_frame.grid_columnconfigure(0, weight=1)

#         # Populate analysis list
#         self.populate_analysis_list()

#     def populate_analysis_list(self):
#         # Clear existing widgets
#         for widget in self.scrollable_frame.winfo_children():
#             widget.destroy()

#         try:
#             # Fetch analyzed files from API
#             analyzed_files = self.api_client.get_analyzed_files()

#             # Create a frame for each analyzed file
#             for i, file in enumerate(analyzed_files):
#                 file_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="light gray")
#                 file_frame.grid(row=i, column=0, pady=10, padx=10, sticky="ew")
#                 file_frame.grid_columnconfigure(1, weight=1)

#                 ctk.CTkLabel(file_frame, text=file["file_name"], font=("Helvetica", 16, "bold"), text_color="black").grid(row=0, column=0, pady=5, padx=10, sticky="w")
#                 ctk.CTkLabel(file_frame, text=file["summary"], wraplength=400, justify="left", text_color="black").grid(row=1, column=0, pady=5, padx=10, sticky="w")
#                 ctk.CTkButton(file_frame, text="View All", command=lambda f=file: self.view_full_analysis(f["analysis_id"])).grid(row=1, column=1, pady=5, padx=10, sticky="e")

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch analyzed files: {str(e)}")

#     def view_full_analysis(self, analysis_id):
#         try:
#             full_analysis = self.api_client.get_full_analysis(analysis_id)
            
#             # Create a new window to display the full analysis
#             analysis_window = ctk.CTkToplevel(self)
#             analysis_window.title(f"Full Analysis - {full_analysis['file_name']}")
#             analysis_window.geometry("600x400")

#             # Create a scrollable text widget to display the full analysis
#             text_widget = ctk.CTkTextbox(analysis_window, wrap="word")
#             text_widget.pack(expand=True, fill="both", padx=20, pady=20)

#             # Insert the full analysis text
#             text_widget.insert("1.0", full_analysis['summary_statistics'])
#             text_widget.configure(state="disabled")  # Make the text widget read-only

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch full analysis: {str(e)}")
#     def update_content(self):
#         self.populate_analysis_list()

# class VisualsPage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.api_client = APIClient(controller.token)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         title_label = ctk.CTkLabel(self, text="Visuals", font=("Helvetica", 32, "bold"), text_color="black")
#         title_label.grid(row=0, column=0, pady=(20, 10), padx=20, sticky="w")

#         # Image display area (scrollable)
#         self.image_frame = ctk.CTkScrollableFrame(self)
#         self.image_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
#         self.image_frame.grid_columnconfigure(0, weight=1)

#         # Controls frame
#         controls_frame = ctk.CTkFrame(self)
#         controls_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
#         controls_frame.grid_columnconfigure(1, weight=1)

#         # File selection dropdown
#         self.file_var = ctk.StringVar()
#         self.file_dropdown = ctk.CTkOptionMenu(controls_frame, variable=self.file_var, values=["Select a file"])
#         self.file_dropdown.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="w")

#         # Visualize button
#         self.visualize_button = ctk.CTkButton(controls_frame, text="Visualize", command=self.visualize_data)
#         self.visualize_button.grid(row=0, column=1, pady=10, sticky="e")

#         # Populate the file dropdown
#         self.populate_file_list()

    
#     def update_content(self):
#         self.populate_file_list()

#     def populate_file_list(self):
#         try:
#             files = self.api_client.get_file_list()
#             file_names = [file["filename"] for file in files]
#             self.file_dropdown.configure(values=["Select a file"] + file_names)
#             self.file_var.set("Select a file")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch file list: {str(e)}")

#     def visualize_data(self):
#         selected_file = self.file_var.get()
#         if selected_file == "Select a file":
#             messagebox.showwarning("Warning", "Please select a file to visualize.")
#             return

#         try:
#             # Get the image paths from the API
#             response = self.api_client.create_visualizations(selected_file)
#             visualizations = response.get("visualizations", [])

#             # Clear previous images
#             for widget in self.image_frame.winfo_children():
#                 widget.destroy()

#             # Display each image
#             for i, viz in enumerate(visualizations):
#                 image_path = viz.get("image_path")
#                 if image_path and os.path.exists(image_path):
#                     image = Image.open(image_path)
#                     image.thumbnail((600, 461))  # Adjust size as needed
#                     photo = ImageTk.PhotoImage(image)

#                     image_label = ctk.CTkLabel(self.image_frame, image=photo, text="")
#                     image_label.image = photo  # Keep a reference to avoid garbage collection
#                     image_label.grid(row=i, column=0, pady=10, padx=10, sticky="nsew")

#                     # Add a description label
#                     desc_label = ctk.CTkLabel(self.image_frame, text=f"Visualization: {viz.get('visualization_type', 'Unknown')}", font=("Helvetica", 12))
#                     desc_label.grid(row=i+1, column=0, pady=(0, 20), padx=10, sticky="n")

#             if not visualizations:
#                 no_viz_label = ctk.CTkLabel(self.image_frame, text="No visualizations available for this file.", font=("Helvetica", 16))
#                 no_viz_label.grid(row=0, column=0, pady=20, padx=10, sticky="nsew")

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to visualize data: {str(e)}")

#     def update_content(self):
#         self.populate_file_list()
    
# class PaymentPage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.api_client = APIClient(controller.token)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         title_label = ctk.CTkLabel(self, text="Payment", font=("Helvetica", 32, "bold"), text_color="black")
#         title_label.grid(row=0, column=0, pady=20, padx=20, sticky="w")

#         # Create a frame for subscription plans
#         self.plans_frame = ctk.CTkFrame(self)
#         self.plans_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
#         self.plans_frame.grid_columnconfigure(0, weight=1)

#         # Populate subscription plans
#         self.populate_subscription_plans()

#     def populate_subscription_plans(self):
#         try:
#             # Fetch subscription plans from API
#             plans = self.api_client.get_subscription_plans()

#             # Create a frame for each plan
#             for i, plan in enumerate(plans):
#                 plan_frame = ctk.CTkFrame(self.plans_frame, fg_color="light gray")
#                 plan_frame.grid(row=i, column=0, pady=10, padx=10, sticky="ew")
#                 plan_frame.grid_columnconfigure(1, weight=1)

#                 ctk.CTkLabel(plan_frame, text=plan["plan_name"], font=("Helvetica", 16, "bold"), text_color="black").grid(row=0, column=0, pady=5, padx=10, sticky="w")
#                 ctk.CTkLabel(plan_frame, text=f"Price: ₦{plan['price']}", text_color="black").grid(row=1, column=0, pady=5, padx=10, sticky="w")
#                 ctk.CTkLabel(plan_frame, text=f"Features: {plan['features']}", wraplength=300, justify="left", text_color="black").grid(row=2, column=0, pady=5, padx=10, sticky="w")
#                 ctk.CTkButton(plan_frame, text="Subscribe", command=lambda p=plan["plan_name"]: self.subscribe_to_plan(p)).grid(row=3, column=0, pady=5, padx=10, sticky="w")

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch subscription plans: {str(e)}")

#     def subscribe_to_plan(self, plan_name):
#         try:
#             # Make a POST request to initiate payment
#             response = self.api_client.pay_for_subscription(plan_name)
            
#             # Check if payment initiation was successful
#             if "payment_url" in response:
#                 # Open the payment URL in the default web browser
#                 webbrowser.open(response["payment_url"])
#                 messagebox.showinfo("Payment Initiated", "Please complete the payment in your web browser.")
                
#                 # Update subscription info after successful payment
#                 self.controller.update_subscription_info()
#             else:
#                 messagebox.showerror("Error", "Failed to initiate payment. Please try again.")

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to subscribe to plan: {str(e)}")

        

# class ProfilePage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller
#         self.api_client = APIClient(controller.token)

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         title_label = ctk.CTkLabel(self, text="Profile", font=("Helvetica", 32, "bold"), text_color="black")
#         title_label.grid(row=0, column=0, pady=20, padx=20, sticky="w")

#         # Create a frame for user information
#         self.info_frame = ctk.CTkFrame(self)
#         self.info_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
#         self.info_frame.grid_columnconfigure(1, weight=1)

#         # Populate user information
#         self.populate_user_info()

#     def populate_user_info(self):
#         try:
#             # Fetch user information from API
#             user_info = self.api_client.get_user_info()

#             # Display user information
#             ctk.CTkLabel(self.info_frame, text="Username:", font=("Helvetica", 16, "bold")).grid(row=0, column=0, pady=5, padx=10, sticky="w")
#             self.username_var = ctk.StringVar(value=user_info["username"])
#             ctk.CTkEntry(self.info_frame, textvariable=self.username_var, state="disabled").grid(row=0, column=1, pady=5, padx=10, sticky="ew")

#             ctk.CTkLabel(self.info_frame, text="Email:", font=("Helvetica", 16, "bold")).grid(row=1, column=0, pady=5, padx=10, sticky="w")
#             self.email_var = ctk.StringVar(value=user_info["email"])
#             ctk.CTkEntry(self.info_frame, textvariable=self.email_var).grid(row=1, column=1, pady=5, padx=10, sticky="ew")

#             # Add buttons for updating profile and changing password
#             ctk.CTkButton(self.info_frame, text="Update Profile", command=self.update_profile).grid(row=2, column=0, columnspan=2, pady=20, padx=10, sticky="ew")
#             ctk.CTkButton(self.info_frame, text="Change Password", command=self.show_change_password_dialog).grid(row=3, column=0, columnspan=2, pady=(0, 20), padx=10, sticky="ew")

#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to fetch user information: {str(e)}")

#     def update_profile(self):
#         try:
#             updated_info = {
#                 "email": self.email_var.get()
#             }
#             response = self.api_client.update_user_info(updated_info)
#             messagebox.showinfo("Success", "Profile updated successfully")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to update profile: {str(e)}")

#     def show_change_password_dialog(self):
#         dialog = ctk.CTkToplevel(self)
#         dialog.title("Change Password")
#         dialog.geometry("300x200")

#         ctk.CTkLabel(dialog, text="Current Password:").pack(pady=(20, 5))
#         current_password = ctk.CTkEntry(dialog, show="*")
#         current_password.pack(pady=5)

#         ctk.CTkLabel(dialog, text="New Password:").pack(pady=5)
#         new_password = ctk.CTkEntry(dialog, show="*")
#         new_password.pack(pady=5)

#         ctk.CTkButton(dialog, text="Change Password", command=lambda: self.change_password(current_password.get(), new_password.get(), dialog)).pack(pady=20)

#     def change_password(self, current_password, new_password, dialog):
#         try:
#             response = self.api_client.change_password(current_password, new_password)
#             messagebox.showinfo("Success", "Password changed successfully")
#             dialog.destroy()
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to change password: {str(e)}")

# class TwitterInsightsPage(ctk.CTkFrame):
#     def __init__(self, parent, controller):
#         super().__init__(parent)
#         self.controller = controller

#         self.grid_columnconfigure(0, weight=1)
#         self.grid_rowconfigure(1, weight=1)

#         title_label = ctk.CTkLabel(self, text="Twitter Insights", font=("Helvetica", 32, "bold"), text_color="black")
#         title_label.grid(row=0, column=0, pady=20, padx=20, sticky="w")

#         content_frame = ctk.CTkFrame(self)
#         content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
#         content_frame.grid_columnconfigure(0, weight=1)
#         content_frame.grid_rowconfigure(0, weight=1)

#         coming_soon_label = ctk.CTkLabel(content_frame, text="Coming Soon!", font=("Helvetica", 24, "bold"), text_color="black")
#         coming_soon_label.grid(row=0, column=0, pady=20, padx=20)

#         description_label = ctk.CTkLabel(content_frame, text="This feature will use Selenium to automate tweet collection for insights, providing more awareness. Stay tuned for updates!", 
#                                          font=("Helvetica", 16), text_color="black", wraplength=600, justify="center")
#         description_label.grid(row=1, column=0, pady=20, padx=20)

#     def update_content(self):
#         # This method can be empty for now, but it's good to have it for consistency with other pages
#         pass 

# # Run the application
# if __name__ == "__main__":
#     LoginApp().mainloop()
