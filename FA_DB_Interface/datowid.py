from tkinter import *

def datowid(Date_frame):
    for _ in [0]:
        dato = {'Startdato': {}, 'Enddato': {}}
        i = 0
        j = 0
        Label(Date_frame, text=list(dato.keys())[0]).grid(row=i, column=j, columnspan=2)
        i += 1
        Label(Date_frame, text='Ár').grid(row=i, column=j)
        j += 1
        dato[list(dato.keys())[0]]['Ár'] = Entry(Date_frame, width=4)
        dato[list(dato.keys())[0]]['Ár'].grid(row=i, column=j)
        j += 1
        Label(Date_frame, text='M').grid(row=i, column=j)
        j += 1
        dato[list(dato.keys())[0]]['M'] = Entry(Date_frame, width=2)
        dato[list(dato.keys())[0]]['M'].grid(row=i, column=j)
        j += 1
        Label(Date_frame, text='D').grid(row=i, column=j)
        j += 1
        dato[list(dato.keys())[0]]['D'] = Entry(Date_frame, width=2)
        dato[list(dato.keys())[0]]['D'].grid(row=i, column=j)
        i += 1
        j = 0
        Label(Date_frame, text=list(dato.keys())[1]).grid(row=i, column=j, columnspan=2)
        i += 1
        Label(Date_frame, text='Ár').grid(row=i, column=j)
        j += 1
        dato[list(dato.keys())[1]]['Ár'] = Entry(Date_frame, width=4)
        dato[list(dato.keys())[1]]['Ár'].grid(row=i, column=j)
        j += 1
        Label(Date_frame, text='M').grid(row=i, column=j)
        j += 1
        dato[list(dato.keys())[1]]['M'] = Entry(Date_frame, width=2)
        dato[list(dato.keys())[1]]['M'].grid(row=i, column=j)
        j += 1
        Label(Date_frame, text='D').grid(row=i, column=j)
        j += 1
        dato[list(dato.keys())[1]]['D'] = Entry(Date_frame, width=2)
        dato[list(dato.keys())[1]]['D'].grid(row=i, column=j)
    return dato