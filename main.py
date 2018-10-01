from tkinter import *
import Processing.tekna_kort
import tkinter.ttk as ttk
import Ingestion.streymmatari

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
        main_frame.pack(fill=BOTH, expand=False, side=TOP)


    def client_exit(self):
        exit()


def OnDoubleClick(event, tree):
    item = tree.identify('item', event.x, event.y)
    if tree.item(item, "text") == 'Tekna Kort':
        Processing.tekna_kort.teknakort()
    elif tree.item(item, "text") == 'Rokna quiver data':
        Ingestion.streymmatari.roknaQuiver(RightFrame)



root = Tk()
root.geometry("1200x800")
app = Window(root)

Ingestion_frame = Frame(app)
Ingestion_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
Label(Ingestion_frame, text='Ingestion').pack(side=TOP)

RightFrame = Frame(app)
RightFrame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)

ingestion_subframe = Frame(Ingestion_frame)
ingestion_subframe.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

ingestion_listbox = ttk.Treeview(ingestion_subframe)
scrollbar = Scrollbar(ingestion_subframe, orient=VERTICAL)
scrollbar.config(command=ingestion_listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)

ingestion_listbox.insert("", 0, text='Tekna Kort')
ctd = ingestion_listbox.insert("", 0, text='CTD')
ingestion_listbox.insert(ctd, "end", text='Les data frá CTD')

streymmatingar = ingestion_listbox.insert("", 0, text="Streymmátingar")
ingestion_listbox.insert(streymmatingar, "end", text='Kopiera data frá feltteldu')
ingestion_listbox.insert(streymmatingar, "end", text='Evt. Reprocessera')
ingestion_listbox.insert(streymmatingar, "end", text='Exportera csv fílar')
ingestion_listbox.insert(streymmatingar, "end", text='Rokna quiver data')
ingestion_listbox.insert(streymmatingar, "end", text='Tekna Kort')
ingestion_listbox.bind("<Double-1>", lambda event, arg=ingestion_listbox: OnDoubleClick(event, arg))

#ingestion_listbox.insert(END, 'Test')
ingestion_listbox.pack(fill=BOTH, expand=True, side=TOP, anchor=W)


root.mainloop()

