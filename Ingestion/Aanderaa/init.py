from Ingestion.Aanderaa import plotta_boyudata

def init(ingestion_listbox):
    boya = ingestion_listbox.insert("", 0, text='Aandreaa')
    ingestion_listbox.insert(boya, 0, text="Plotta boyu data")


def check_click(item, RightFrame, root):
    toReturn = 1
    if item == 'Plotta boyu data':
        plotta_boyudata.csvPlot(RightFrame, root)
    else:
        toReturn = 0
    return toReturn
