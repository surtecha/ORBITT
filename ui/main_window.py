import customtkinter as ctk

class MainWindow(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        
        self.tabview = ctk.CTkTabview(self, anchor="nw")
        self.tabview.pack(fill="both", expand=True, padx=0, pady=0)