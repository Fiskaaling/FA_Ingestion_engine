from tkinter import *
import Processing.tekna_kort
import tkinter.ttk as ttk
import Ingestion.streymmatari
import Ingestion.LV
import Strfbotni.strbotni
import Ingestion.oxygenkeda

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        Frame.pack(self, side=BOTTOM)
        self.init_window()

    def init_window(self):
        self.master.title("Fiskaaling Ingestion Engine")
        self.pack(fill=BOTH, expand=1)
        main_frame = Frame(self, borderwidth=1)
        main_frame.pack(fill=BOTH, expand=False, side=TOP)

    def client_exit(self):
        exit()


def OnDoubleClick(event, tree):
    item = tree.identify('item', event.x, event.y)
    item = tree.item(item, "text")
    if item == 'Tekna Kort':
        Processing.tekna_kort.teknakort()
    elif item == 'Rokna quiver data':
        Ingestion.streymmatari.roknaQuiver(RightFrame, root)
    elif item == 'Veðurstøðir':
        Ingestion.LV.vedurstodirPlt(RightFrame, root)
    elif item == 'Rokna miðal streym':
        Ingestion.streymmatari.roknaMidalstreym(RightFrame, root)
    elif item == 'Countour plot':
        Strfbotni.strbotni.botnmatPlt(RightFrame, root)
    elif item == 'Decimering':
        Ingestion.oxygenkeda.decimering(RightFrame, root)


global root
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
LV = ingestion_listbox.insert("", 0, text='Landsverk')

streymmatingar_stationert = ingestion_listbox.insert("", 0, text="Streymmátinar frá botni")

Ingestion.streymmatari.init(ingestion_listbox)
Ingestion.oxygenkeda.init(ingestion_listbox)

ctd = ingestion_listbox.insert("", 0, text='CTD')
alduboya = ingestion_listbox.insert("", 0, text='Alduboya')

ingestion_listbox.insert(ctd, "end", text='Les data frá CTD')
ingestion_listbox.insert(streymmatingar_stationert, "end", text='Countour plot')
ingestion_listbox.bind("<Double-1>", lambda event, arg=ingestion_listbox: OnDoubleClick(event, arg))

ingestion_listbox.insert(LV, "end", text='Veðurstøðir')
ingestion_listbox.insert(LV, "end", text='Aldumátingar')
ingestion_listbox.insert(LV, "end", text='Vatnstøða')

#ingestion_listbox.insert(END, 'Test')
ingestion_listbox.pack(fill=BOTH, expand=True, side=TOP, anchor=W)


root.mainloop()

