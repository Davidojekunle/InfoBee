import customtkinter as ctk
from PIL import Image, ImageTk

# Dashboard Frame Class
class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(1, weight=1)
        
        # Sidebar
        self._create_sidebar()

        # Main Content Area
        self._create_content()

    def _create_sidebar(self):
        """Create and layout the sidebar components."""
        self.sidebar = ctk.CTkFrame(self)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        # User Information
        self.name_label = ctk.CTkLabel(self.sidebar, text="John Doe")
        self.name_label.pack(pady=10)
        
        # Profile Picture (placeholder)
        self.profile_pic = ctk.CTkLabel(self.sidebar, text="Profile Picture")
        self.profile_pic.pack(pady=10)
        
        # Search Box
        self.search_box = ctk.CTkEntry(self.sidebar, placeholder_text="Search...")
        self.search_box.pack(pady=10, padx=5, fill="x")
        
    def _create_content(self):
        """Create and layout the main content components."""
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_columnconfigure(1, weight=1)
        
        # Payment Widget
        self.payment_widget = ctk.CTkFrame(self.content)
        self.payment_widget.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        ctk.CTkLabel(self.payment_widget, text="Payment Widget").pack()
        
        # Critical Graphs
        self._create_graphs()
        
        # Upload Button
        self.upload_x = ctk.CTkButton(self.content, text="Upload to X")
        self.upload_x.grid(row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        
        # Payment Options
        self._create_payment_options()
    
    def _create_graphs(self):
        """Create and layout the graph components."""
        self.graph1 = ctk.CTkFrame(self.content)
        self.graph1.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        ctk.CTkLabel(self.graph1, text="Critical Graph 1").pack()
        
        self.graph2 = ctk.CTkFrame(self.content)
        self.graph2.grid(row=1, column=1, pady=10, padx=10, sticky="nsew")
        ctk.CTkLabel(self.graph2, text="Critical Graph 2").pack()
    
    def _create_payment_options(self):
        """Create and layout the payment options components."""
        self.payment_options = ctk.CTkFrame(self.content)
        self.payment_options.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        ctk.CTkLabel(self.payment_options, text="Payment Options").pack()
        ctk.CTkButton(self.payment_options, text="Personal").pack(side="left", padx=5)
        ctk.CTkButton(self.payment_options, text="Business").pack(side="right", padx=5)

# My Files Frame Class
class MyFilesFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # File List
        self.file_list = ctk.CTkTextbox(self)
        self.file_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # CRUD Buttons
        self._create_crud_buttons()

    def _create_crud_buttons(self):
        """Create and layout the CRUD operation buttons."""
        self.crud_frame = ctk.CTkFrame(self)
        self.crud_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkButton(self.crud_frame, text="Create").pack(side="left", padx=5)
        ctk.CTkButton(self.crud_frame, text="Update").pack(side="left", padx=5)
        ctk.CTkButton(self.crud_frame, text="Delete").pack(side="left", padx=5)

# Main Application Class
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Data Analyst Dashboard")
        self.geometry("1000x600")
        
        # Layout configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Notebook (Tab View)
        self.notebook = ctk.CTkTabview(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Tabs
        self.dashboard_tab = self.notebook.add("Dashboard")
        self.my_files_tab = self.notebook.add("My Files")
        
        # Frames
        self.dashboard_frame = DashboardFrame(self.dashboard_tab)
        self.dashboard_frame.pack(fill="both", expand=True)
        
        self.my_files_frame = MyFilesFrame(self.my_files_tab)
        self.my_files_frame.pack(fill="both", expand=True)

# Application Entry Point
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()