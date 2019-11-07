# Hendan kodan er gjørd í stórum hasti. Má gjøgnumhyggjast áðrenn hon verður nýtt í production
# Basically, not use me
import subprocess
import pandas
import os
import fileinput

filename = '2019-09-11.csv'

data = pandas.read_csv(filename, header=None)
turdato = filename.split('.')[0]
print(turdato)

if not os.path.exists('./Lokalt_Data/' + turdato + '/8_Bin_Average_slava/'):
    print('Ger lokala mappu')
    os.mkdir('./Lokalt_Data/' + turdato + '/8_Bin_Average_slava')
    os.mkdir('./Lokalt_Data/' + turdato + '/9_ASCII_Out_slava')

print(data)
print('test')

for index, fn in enumerate(data.iloc[:,0]):
    print(index)
    filnavn = fn
    print(filnavn)
    print(data.iloc[index, 1])
    if data.iloc[index, 1] == -1:
        continue
    with fileinput.FileInput('/home/johannus/.wine/drive_c/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/BinAvg(1mcustomstart).psa', inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace('-77', str(data.iloc[index, 1])), end='')

    subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                     "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/8_Bin_Average(1m-customstart).txt",
                     str('Z:' + os.getcwd() + '/Lokalt_Data/' + turdato + '/7_Window_Filter/' + filnavn + '.cnv'),
                     str('Z:' + os.getcwd() + '/Lokalt_Data/' + turdato + '/8_Bin_Average_slava'), '#m'])
    subprocess.call(['wine', 'C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/SBEBatch.exe',
                     "C:/Program Files (x86)/Sea-Bird/SBEDataProcessing-Win32/Settings/9_ASCII_Out.txt",
                     str('Z:' + os.getcwd() + '/Lokalt_Data/' + turdato + '/8_Bin_Average_slava/' + filnavn + '.cnv'),
                     str('Z:' + os.getcwd() + '/Lokalt_Data/' + turdato + '/9_ASCII_Out_slava'), '#m'])

print('done')

