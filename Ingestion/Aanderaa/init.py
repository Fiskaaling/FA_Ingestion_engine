from Ingestion.Aanderaa import plotta_boyudata

def init(ingestion_listbox):
    boya = ingestion_listbox.insert("", 0, text='Aandreaa')
    ingestion_listbox.insert(boya, 0, text="Plotta boyu data")


def check_click(item, RightFrame, root):
    toReturn = 0
    if item == 'Plotta boyu data':
        plotta_boyudata.csvPlot(RightFrame, root)
    else:
        toReturn = 1
    return toReturn
