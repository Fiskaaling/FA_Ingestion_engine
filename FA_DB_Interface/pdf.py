import miscMatingar.skrivapdf as skriva
import os

os.chdir('..')
fil = skriva.birjan()
fil += skriva.DepID('  Kúgv  ')
fil += skriva.tveycol('bein:', 4, 'kolvar', 2)
fil += skriva.eincol('litur:', 'flekkut svart hvítur')
fil += skriva.endi()

print(fil)

navn = 'hey.pdf'

skriva.makepdf(fil, navn, 'FA_DB_Interface/miscMatingar')
