import tkinter.messagebox as messagebox
import datetime as dt
import FA_DB_Interface.miscleitamatingar.db_ting as db

def update(setup_dict):
    #TODO kolonnir skal umskrivast
    kolonnir = ['mátingar.' + x for x in db.getcol(setup_dict)]
    tabellir = ['mátingar', 'instrumentir']
    wherecall = ['mátingar.Mátari = instrumentir.navn']
    where = []

    instrument = setup_dict['tk_inst'].get()
    slag = setup_dict['tk_slag'].get()
    if instrument != 'Øll':
        where.append(instrument)
        wherecall.append('mátingar.Mátari = %s')
    elif slag != 'Øll':
        where.append(slag)
        wherecall.append('instrumentir.Slag = %s')

    #Startdato
    wherecall.append('mátingar.Start_tid BETWEEN %s AND %s')
    where += Startendtime(setup_dict)

    innihald = db.getmatinger2(kolonnir, tabellir, wherecall, where, setup_dict)
    return kolonnir, innihald


def Startendtime(setup_dict):
    try:
        Start = get_tid(setup_dict['dato']['Startdato'])
    except:
        messagebox.showerror('Feilur', 'Feilur í startdato vit brúka 1 jan í 1900')
        Start = dt.datetime(1900, 1, 1)
    try:
        Endi = get_tid(setup_dict['dato']['Enddato'])
    except:
        messagebox.showerror('Feilur', 'Feilur í startdato vit brúka 1 jan í 2200')
        Endi = dt.datetime(2200, 1, 1)
    return [Start, Endi]

def get_tid(time):
    return dt.datetime(int(time['Ár'].get()), int(time['M'].get()), int(time['D'].get()))
