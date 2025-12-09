import customtkinter as ctk
from ui.sidebar import Sidebar
from ui.topbar import create_menubar
from ui.main_window import MainWindow

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Orbital Retrieval and Behaviour Inspection Tool for TLEs")
        self.state("zoomed")

        create_menubar(self)

        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")

        self.main_window = MainWindow(self)
        self.main_window.pack(side="right", fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()