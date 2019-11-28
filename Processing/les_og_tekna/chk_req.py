def chk_req(variable, value, v_dic):
    if variable == 'latmax':
        v_dic['req']['latmax'] = float(value)
    elif variable == 'latmin':
        v_dic['req']['latmin'] = float(value)
    elif variable == 'lonmin':
        v_dic['req']['lonmin'] = float(value)
    elif variable == 'lonmax':
        v_dic['req']['lonmax'] = float(value)
    else:
        return False
    return True
