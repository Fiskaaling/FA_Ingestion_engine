def insert_gui_par(setup_dict, par):
    for key in par:
        if key == 'Language':
            temp = par[key].get().strip().lower()
            if temp in ['fo', 'en']:
                setup_dict[key] = temp.upper()
            else:
                raise ValueError('Language skal vera FO ella EN')
        elif key == 'N':
            temp = int(par[key].get())
            if temp > 0:
                setup_dict[key] = temp
            else:
                raise ValueError('N kann ikki vera <=0')
        elif key == 'dpi':
            temp = int(par[key].get())
            if temp > 0:
                setup_dict[key] = temp
            else:
                raise ValueError('dpi kann ikki vera <= 0')
        elif key == 'top_mid_bot_layer':
            temp = par[key].get().strip().lower()
            if temp == 'false':
                setup_dict[key] = False
            else:
                temp = [int(x) for x in temp.split()]
                mybool = len(temp) == 3
                for i in temp:
                    mybool = mybool and i > 0
                if mybool:
                    setup_dict[key] = temp
                else:
                    raise ValueError('%s er ikki godt nokk' % key)
        elif key == 'Hov_hadd':
            setup_dict[key] = int(par[key].get())
        elif key == 'Hov_rat':
            temp = par[key].get().strip().lower()
            temp = [int(x) for x in temp.split()]
            setup_dict[key] = temp
        elif key == 'tidal_oll_Frqs':
            setup_dict[key] = par[key].get().strip().split()
        elif key == 'minmax':
            temp = par[key].get().strip().lower()
            if temp == 'true':
                setup_dict[key] = True
            elif temp == 'false':
                setup_dict[key] = False
            else:
                raise ValueError('%s skal entin verða True ella False' % key)
        else:
            raise ValueError('har er eingin parametur sum eitur %s' % key)


