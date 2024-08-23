import os
import pandas as pd
from misc.faLog import log_print

# Checks when CTD pump turns on and off
def pumpstatus(mappa, filur):
    parent_folder = mappa.split('Processed')[0]
    raw_folder = f'{parent_folder}RAW/'
    raw_file = f'{filur[0:7]}.xml'
    raw_file_path = f'{raw_folder}{raw_file}'

    if os.path.exists(raw_file_path):
        print(f'Lesur raw fíl: {raw_file}')
        raw_data = pd.read_csv(raw_file_path, skiprows=185, skipfooter=3, 
                               header=None, names=['hex'],
                               dtype='str', engine='python')
        raw_data['hex'] = raw_data['hex'].str.replace("\t\t","")
        # Pump on signaled by first character being 0 when off and 1 when on
        pump_on = raw_data.index[raw_data['hex'].str.startswith('1')][0]
        pump_off = raw_data.index[raw_data['hex'].str.startswith('1')][-1]

        log_print('Pump ' + str(pump_on))
        return [pump_on, pump_off]
    
    else:
        raise FileNotFoundError('Eingin raw fílur funnin') 