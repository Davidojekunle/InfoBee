import customtkinter as ctk
from PIL import Image, ImageTk


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

def create_dashboard():
    # Initialize the main window
    app = ctk.CTk()
    app.geometry("1200x700")
    app.title("Data-Hive Dashboard")
    app.resizable(False, False)

    # Set the color scheme
    ctk.set_default_color_theme("dark-blue")

    # Create main frame
    main_frame = ctk.CTkFrame(app, fg_color="#E5E5E5")
    main_frame.pack(fill="both", expand=True)

    # Create sidebar
    sidebar = ctk.CTkFrame(main_frame, width=250, fg_color="#3B3BFF", corner_radius=0)
    sidebar.pack(side="left", fill="y")

    # Sidebar content
    logo_label = ctk.CTkLabel(sidebar, text="DATA- HIVE", font=("Arial", 24, "bold"), text_color="white")
    logo_label.pack(pady=(30, 50))

    dashboard_button = ctk.CTkButton(sidebar, text="🏠 dashboard", fg_color="#D3D3D3", text_color="black", hover_color="#BEBEBE")
    dashboard_button.pack(pady=10)

    # Content area
    content_area = ctk.CTkFrame(main_frame, fg_color="#E5E5E5")
    content_area.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # Header
    header_frame = ctk.CTkFrame(content_area, fg_color="#E5E5E5")
    header_frame.pack(fill="x", pady=(0, 20))

    welcome_label = ctk.CTkLabel(header_frame, text="Hi, username!", font=("Arial", 20, "bold"))
    welcome_label.pack(side="left")

    subscription_label = ctk.CTkLabel(header_frame, text="subscription : Free", font=("Arial", 16))
    subscription_label.pack(side="right")

    # File statistics
    stats_frame = ctk.CTkFrame(content_area, fg_color="#E5E5E5")
    stats_frame.pack(fill="x", pady=20)

    upload_frame = HoverFrame(stats_frame, fg_color="white", corner_radius=15)
    upload_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), ipady=20)

    upload_count = ctk.CTkLabel(upload_frame, text="12", font=("Arial", 48, "bold"))
    upload_count.pack(pady=(30, 10))

    upload_label = ctk.CTkLabel(upload_frame, text="Your Uploaded Files", font=("Arial", 18))
    upload_label.pack()

    upload_button = ctk.CTkButton(upload_frame, text="upload⬆", fg_color="#90EE90", text_color="black", hover_color="#7CFC00", font=("Arial", 16), height=40)
    upload_button.pack(pady=30)

    analyze_frame = HoverFrame(stats_frame, fg_color="white", corner_radius=15)
    analyze_frame.pack(side="right", fill="both", expand=True, padx=(20, 0), ipady=20)

    analyze_count = ctk.CTkLabel(analyze_frame, text="13", font=("Arial", 48, "bold"))
    analyze_count.pack(pady=(30, 10))

    analyze_label = ctk.CTkLabel(analyze_frame, text="Your analyzed files", font=("Arial", 18))
    analyze_label.pack()

    analyze_button = ctk.CTkButton(analyze_frame, text="check analysis", fg_color="#6495ED", hover_color="#4169E1", font=("Arial", 16), height=40)
    analyze_button.pack(pady=30)

    # Additional sections
    additional_frame = ctk.CTkFrame(content_area, fg_color="#E5E5E5")
    additional_frame.pack(fill="x", pady=20)

    payment_frame = HoverFrame(additional_frame, fg_color="#E0FFE0", corner_radius=15)
    payment_frame.pack(side="left", fill="both", expand=True, padx=(0, 20), ipady=20)

    payment_label = ctk.CTkLabel(payment_frame, text="Payment Plans", font=("Arial", 24, "bold"))
    payment_label.pack(pady=(30, 20))

    view_plans_button = ctk.CTkButton(payment_frame, text="View Plans", fg_color="#32CD32", hover_color="#228B22", font=("Arial", 16), height=40)
    view_plans_button.pack(pady=(10, 30))

    profile_frame = HoverFrame(additional_frame, fg_color="white", corner_radius=15)
    profile_frame.pack(side="right", fill="both", expand=True, padx=(20, 0), ipady=20)

    profile_label = ctk.CTkLabel(profile_frame, text="Profile Information", font=("Arial", 24, "bold"))
    profile_label.pack(pady=(30, 20))

    view_profile_button = ctk.CTkButton(profile_frame, text="View Profile", fg_color="#9370DB", hover_color="#8A2BE2", font=("Arial", 16), height=40)
    view_profile_button.pack(pady=(10, 30))

    return app

if __name__ == "__main__":
    app = create_dashboard()
    app.mainloop()



