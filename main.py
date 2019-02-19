# -*- coding: utf-8 -*-
from tkinter import *
from tkinter import font
import Processing.tekna_kort
import tkinter.ttk as ttk
import Ingestion.streymmatari
import Ingestion.LV
import Ingestion.LV_Aldumátingar
import Strfbotni.strbotni
import Ingestion.oxygenkeda
import Ingestion.RDI.fra_botni
import Ingestion.Botnkort.tilCsv
import Ingestion.CTD.init
import vatnstoduanalysa.vatnstoduanalysa
import Ingestion.seaguard.seaguard as seaguard
import FA_DB_Interface.init
import subprocess
from Ingestion.Aanderaa import init as AADI
import sys

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

    @staticmethod
    def client_exit(self):
        exit()


def OnDoubleClick(event, tree):
    minimize = 1
    item = tree.identify('item', event.x, event.y)
    item = tree.item(item, "text")
    if clo:
        item = sys.argv[1]
    else:
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
    elif item == 'Aldumátingar':
        Ingestion.LV_Aldumátingar.Alduplt(RightFrame, root)
    elif item == 'Vatnstoduanalysa':
        vatnstoduanalysa.vatnstoduanalysa.load(RightFrame, root)
    elif item == 'seaguard':
        seaguard.load(RightFrame, root)
    else:
        minimize = 0
        minimize += Ingestion.oxygenkeda.check_click(item, RightFrame, root)
        minimize += Ingestion.RDI.fra_botni.check_click(item, RightFrame, root)
        minimize += Ingestion.Botnkort.tilCsv.check_click(item, RightFrame, root)
        minimize += Ingestion.CTD.init.check_click(item, RightFrame, root)
        minimize += FA_DB_Interface.init.check_click(item, RightFrame, root)
        minimize += AADI.check_click(item, RightFrame, root)


    if minimize:
        mintree()

def mintree():
    ingestion_listbox.pack_forget()
    condens.pack_forget()
    expandButton = Button(ingestion_subframe, text='>', command=lambda: visTree(expandButton))
    expandButton.pack(side=LEFT, expand=1, fill=Y)
    Ingestion_frame.config(width=100)
    Ingestion_frame.pack(expand=False)


def visTree(expandButton):
    expandButton.pack_forget()
    condens.pack(side=RIGHT, fill=Y)
    ingestion_listbox.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
    Ingestion_frame.pack(expand=True)
    del expandButton

# Teknar main gui
root = Tk()
root.geometry("1200x800")

if subprocess.check_output('whoami') == b'johannus\n': # 4K bullshit, Alt er forbanna lítið
    root.geometry("3000x1600")
    print(root.tk.call('tk', 'scaling', 3))
    f = font.Font(size=10)
    root.option_add("*Font", f)
    style = ttk.Style(root)
    style.configure('Treeview', rowheight=45)
    style.configure('Treeview.Heading', font=f)
    style.configure(".", font=f)


app = Window(root)
# Teknar vinstru frame (har instrumentini eru)
Ingestion_frame = Frame(app)
Ingestion_frame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)
Label(Ingestion_frame, text='Ingestion').pack(side=TOP)
# Teknar høgru frame
RightFrame = Frame(app)
RightFrame.pack(fill=BOTH, expand=True, side=LEFT, anchor=N)

ingestion_subframe = Frame(Ingestion_frame)
ingestion_subframe.pack(fill=BOTH, expand=True, side=TOP, anchor=W)
# Ger objekti ið inniheldur listan av instumentum
ingestion_listbox = ttk.Treeview(ingestion_subframe)
scrollbar = Scrollbar(ingestion_subframe, orient=VERTICAL)
scrollbar.config(command=ingestion_listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)

# Byrjar at fylla ting inní listan

ingestion_listbox.insert("", 0, text='Tekna Kort')
ingestion_listbox.insert("", 0, text='Vatnstoduanalysa')
ingestion_listbox.insert("", 0, text='seaguard')
LV = ingestion_listbox.insert("", 0, text='Landsverk')


# Rudduligari máti at gera hettar uppá, ikki implementera allastaðni enn
Ingestion.streymmatari.init(ingestion_listbox)
Ingestion.RDI.fra_botni.init(ingestion_listbox)
Ingestion.oxygenkeda.init(ingestion_listbox)
Ingestion.Botnkort.tilCsv.init(ingestion_listbox)
Ingestion.CTD.init.init(ingestion_listbox)
FA_DB_Interface.init.init(ingestion_listbox)
AADI.init(ingestion_listbox)

alduboya = ingestion_listbox.insert("", 0, text='Alduboya')

ingestion_listbox.bind("<Double-1>", lambda event, arg=ingestion_listbox: OnDoubleClick(event, arg))

ingestion_listbox.insert(LV, "end", text='Veðurstøðir')
ingestion_listbox.insert(LV, "end", text='Aldumátingar')
ingestion_listbox.insert(LV, "end", text='Vatnstøða')

#ingestion_listbox.insert(END, 'Test')
condens = Button(ingestion_subframe, text='<', command=lambda: mintree())
condens.pack(side=RIGHT, fill=Y)
ingestion_listbox.pack(fill=BOTH, expand=True, side=TOP, anchor=W)

if sys.argv:
    print(sys.argv)
    print(sys.argv[1])
    OnDoubleClick(0, 0, True)

root.mainloop()

