

def init(ingestion_listbox):
    streymmatingar_stationert = ingestion_listbox.insert("", 0, text="RDI streymmátinar frá botni")
    ingestion_listbox.insert(streymmatingar_stationert, "end", text='Vind korrilation')
    ingestion_listbox.insert(streymmatingar_stationert, "end", text='Countour plot')

def check_click(item, RightFrame, root):
    if item == 'Vind korrilation':
        vk()

def vk():
    print('farts')