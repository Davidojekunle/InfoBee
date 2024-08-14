import customtkinter as ctk

ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

app = ctk.CTk()
app.geometry("720x480")
app.title("DATA-HIVE")

# Left Side
frame_left = ctk.CTkFrame(master=app, width=200, height=480, corner_radius=0)
frame_left.place(x=0, y=0)
label_left = ctk.CTkLabel(master=frame_left, text="DATA-HIVE", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
label_left.place(x=10, y=20)

# Dashboard
button_dashboard = ctk.CTkButton(master=frame_left, text="🏠 Dashboard", font=ctk.CTkFont(size=14), width=150, height=30, corner_radius=5, fg_color="transparent")
button_dashboard.place(x=25, y=70)

# Right Side
frame_right = ctk.CTkFrame(master=app, width=520, height=480, corner_radius=0)
frame_right.place(x=200, y=0)

# User Greeting
label_greeting = ctk.CTkLabel(master=frame_right, text="Hi, username!", font=ctk.CTkFont(size=20, weight="bold"))
label_greeting.place(x=10, y=20)

# Uploaded Files
frame_uploaded_files = ctk.CTkFrame(master=frame_right, width=240, height=150, corner_radius=10)
frame_uploaded_files.place(x=10, y=70)

label_uploaded_files_count = ctk.CTkLabel(master=frame_uploaded_files, text="12", font=ctk.CTkFont(size=48, weight="bold"))
label_uploaded_files_count.place(x=80, y=20)

label_uploaded_files_text = ctk.CTkLabel(master=frame_uploaded_files, text="Your Uploaded Files", font=ctk.CTkFont(size=14))
label_uploaded_files_text.place(x=50, y=80)

# Upload Button
button_upload = ctk.CTkButton(master=frame_uploaded_files, text="⬆️ Upload", font=ctk.CTkFont(size=12), width=80, height=25, corner_radius=5, fg_color="transparent", text_color="white")
button_upload.place(x=100, y=110)

# Analyzed Files
frame_analyzed_files = ctk.CTkFrame(master=frame_right, width=240, height=150, corner_radius=10)
frame_analyzed_files.place(x=270, y=70)

label_analyzed_files_count = ctk.CTkLabel(master=frame_analyzed_files, text="13", font=ctk.CTkFont(size=48, weight="bold"))
label_analyzed_files_count.place(x=80, y=20)

label_analyzed_files_text = ctk.CTkLabel(master=frame_analyzed_files, text="Your Analyzed Files", font=ctk.CTkFont(size=14))
label_analyzed_files_text.place(x=50, y=80)

# Analyze Button
button_analyze = ctk.CTkButton(master=frame_analyzed_files, text="📊 Check Analysis", font=ctk.CTkFont(size=12), width=120, height=25, corner_radius=5, fg_color="transparent", text_color="white")
button_analyze.place(x=60, y=110)

# Subscription
label_subscription = ctk.CTkLabel(master=frame_right, text="Subscription : Free", font=ctk.CTkFont(size=16))
label_subscription.place(x=270, y=240)

# Payment Plans
frame_payment_plans = ctk.CTkFrame(master=frame_right, width=240, height=150, corner_radius=10)
frame_payment_plans.place(x=10, y=280)

label_payment_plans_title = ctk.CTkLabel(master=frame_payment_plans, text="💳 Payment Plans", font=ctk.CTkFont(size=18))
label_payment_plans_title.place(x=50, y=20)

button_view_plans = ctk.CTkButton(master=frame_payment_plans, text="View Plans", font=ctk.CTkFont(size=14), width=120, height=30, corner_radius=5, fg_color="transparent", text_color="white")
button_view_plans.place(x=60, y=70)

# Profile Information
frame_profile_info = ctk.CTkFrame(master=frame_right, width=240, height=150, corner_radius=10)
frame_profile_info.place(x=270, y=280)

label_profile_info_title = ctk.CTkLabel(master=frame_profile_info, text="👤 Profile Information", font=ctk.CTkFont(size=18))
label_profile_info_title.place(x=50, y=20)

button_view_profile = ctk.CTkButton(master=frame_profile_info, text="View Profile", font=ctk.CTkFont(size=14), width=120, height=30, corner_radius=5, fg_color="transparent", text_color="white")
button_view_profile.place(x=60, y=70)

app.mainloop()
