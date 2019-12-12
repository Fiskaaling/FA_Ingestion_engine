import os
from misc.faLog import log_w, log_print

def pumpstatus(mappa, filur):
    parent_folder = os.path.dirname(os.path.dirname(mappa))
    if os.path.isdir(parent_folder + '/RAW/'):
        raw_filar = os.listdir(parent_folder + '/RAW/')
        raw_filnavn = '-1'
        hesin_filur = filur.upper()[:]
        for raw_file in raw_filar:  # Hettar finnur rætta xml fílin
            if raw_file[0:7].upper() == hesin_filur[0:7]:
                print('Alright')
                raw_filnavn = raw_file
        if raw_filnavn == '-1':
            log_w('Eingin raw fílur funnin')
            return
        # raw_filnavn = raw_filar[filur]
        print('Lesur raw fíl: ' + raw_filnavn)
        with open(parent_folder + '/RAW/' + raw_filnavn, 'r') as raw_file:
            raw_data = raw_file.read()
        raw_data = raw_data.split('*END*')
        raw_data = raw_data[1].split('\n')
        pump_on = -1
        pump_off = -1
        lastLine = 0
        for i, line in enumerate(raw_data):
            if line:
                if line[0] == '1' and lastLine == '0':
                    pump_on = i
                elif line[0] == '0' and lastLine == '1':
                    pump_off = i
                lastLine = line[0]
        log_print('Pump ' + str(pump_on))

        return [pump_on, pump_off]