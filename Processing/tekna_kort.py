from tkinter import *
from tkinter import messagebox

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Frame.pack(self, side=BOTTOM)
        self.init_window()

    def init_window(self):
        self.master.title("Fiskaaling - Tekna Kort")
        self.pack(fill=BOTH, expand=1)

        # tools_frame = Frame(self, relief=RAISED, borderwidth=1)
        main_frame = Frame(self, borderwidth=1)
        main_frame.pack(fill=BOTH, expand=False, side=TOP)

    def client_exit(self):
        exit()


def teknakort():
    print('farts')


    root = Tk()
    root.geometry("1200x800")
    app = Window(root)
    menu_frame = Frame(app, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    menu_frame.pack(fill=X, expand=False, anchor=N)
    load_btn = Button(menu_frame, text='Les inn').pack(side=LEFT)
    save_btn = Button(menu_frame, text='Goym').pack(side=LEFT)
    nytt_kort = Button(menu_frame, text='Nýtt Kort', command=lambda: nyttkort(text_list)).pack(side=LEFT)
    tekna_btn = Button(menu_frame, text='Tekna Kort').pack(side=LEFT)
    content_frame = Frame(app, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    content_frame.pack(fill=BOTH, expand=True, anchor=N)

    map_frame = Frame(content_frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    map_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)

    list_frame = Frame(content_frame, borderwidth=1, highlightbackground="green", highlightcolor="green", highlightthickness=1)
    list_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
    text_list = Text(list_frame)
    text_list.pack(fill=BOTH, expand=True)

def nyttkort(text):
    nyttkort_text = "clf \nNW_Lat=62.36\nNW_Lon=-7.878598"
    if len(text.get("1.0", END)) > 1:
        if messagebox.askyesno("Ávaring", "Vilt tú yvurskriva núverani kort?"):
            text.delete(1.0, END)
            text.insert(INSERT, nyttkort_text)
    else:
        text.insert(INSERT, nyttkort_text)
