from tkinter import filedialog

def vel_data(frame, setup_dict):
    temp = filedialog.askdirectory(title='Hvar er dataði')
    setup_dict['path']['data'].set(temp)

def vel_dest(frame, setup_dict):
    temp = filedialog.askdirectory(title='Hvar skal LaTeX mappan')
    setup_dict['path']['dest'].set(temp)

def vel_mynd(frame, setup_dict):
    print(setup_dict['N'])
    temp = filedialog.askopenfilename(title='Velfil',
                                       filetypes=(("all files", "*.*"), ("png files", "*.png")))
    setup_dict['path']['mynd'].set(temp)
