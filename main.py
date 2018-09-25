from tkinter import *
import Processing.tekna_kort
import tkinter.ttk as ttk

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

ingestion_subframe = Frame(Ingestion_frame)
ingestion_subframe.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

ingestion_listbox = ttk.Treeview(ingestion_subframe)
scrollbar = Scrollbar(ingestion_subframe, orient=VERTICAL)
scrollbar.config(command=ingestion_listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)



ingestion_listbox["columns"]=("one","two")
ingestion_listbox.column("one", width=100 )
ingestion_listbox.column("two", width=100)
ingestion_listbox.heading("one", text="coulmn A")
ingestion_listbox.heading("two", text="column B")


#ingestion_listbox.insert(END, 'Test')
ingestion_listbox.pack(fill=BOTH, expand=True, side=TOP, anchor=W)


Label(Processing_frame, text='Processing').pack(side=TOP)
TeknaKort_Btn = Button(Processing_frame, text='Tekna Kort', command=lambda: Processing.tekna_kort.teknakort())
TeknaKort_Btn.pack(side=TOP)

root.mainloop()

