import tkinter as tk

def create_menubar(app):
    menubar = tk.Menu(app)

    insertmenu = tk.Menu(menubar, tearoff=0)
    insertmenu.add_command(label="Insert Local TLE", command=app.insert_local_tle)
    insertmenu.add_command(label="Insert from SpaceTrack")
    menubar.add_cascade(label="Insert", menu=insertmenu)

    loginmenu = tk.Menu(menubar, tearoff=0)
    loginmenu.add_command(label="Login to Spacetrack")
    menubar.add_cascade(label="Login", menu=loginmenu)

    app.config(menu=menubar)
    return menubar