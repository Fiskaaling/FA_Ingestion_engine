from tkinter import *
import Processing.tekna_kort

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Frame.pack(self, side=BOTTOM)
        self.init_window()

    def init_window(self):
        self.master.title("Fiskaaling Ingestion Engine")
        self.pack(fill=BOTH, expand=1)

        #tools_frame = Frame(self, relief=RAISED, borderwidth=1)
        main_frame = Frame(self, borderwidth=1)
        main_frame.pack(fill=BOTH, expand=False, side = TOP)


    def client_exit(self):
        exit()


root = Tk()
root.geometry("1200x800")
app = Window(root)

Ingestion_frame = Frame(app)
Ingestion_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
Label(Ingestion_frame, text='Ingestion').pack(side=TOP)

Processing_frame = Frame(app)
Processing_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
Label(Processing_frame, text='Processing').pack(side=TOP)
TeknaKort_Btn = Button(Processing_frame, text='Tekna Kort', command=lambda: Processing.tekna_kort.teknakort())
TeknaKort_Btn.pack(side=TOP)

root.mainloop()

