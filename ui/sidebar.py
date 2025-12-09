import customtkinter as ctk

class Sidebar(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=250, corner_radius=0)

        self.pack_propagate(False)
        