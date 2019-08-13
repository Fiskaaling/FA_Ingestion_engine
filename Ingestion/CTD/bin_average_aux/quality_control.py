import numpy as np
from tkinter import Label, TOP, W
from scipy import stats
import datetime
import misc.git_toolbox as gitTB
from misc.faLog import *

def qcontrol(Quality_subframe, depth, event_dict, pump_on, filnavn):
    # TODO: Ger so at min kvalitetur er -10 og mesti er +10 og vektra ymsku parametrarnir eitt sindur betur
    textsize = 16 # TODO: Set hettar í ein settings fíl
    for widget in Quality_subframe.winfo_children(): # Tømur quality frame
        widget.destroy()
    time_fulllength = event_dict['time_fulllength']
    cast_quality=0
    downcast_quality=0
    upcast_quality=0

    # TODO: kanna um ymsku tingini eru funnin?
    # Soaking stabilitetur
    soakvar = np.var(depth[event_dict['soak_start']:event_dict['soak_stop']])
    print('Sample variansur á soak er: ' + str(soakvar))
    cast_quality -= min(soakvar, 1)
    # Downcast stabilitetur
    downcast_diff = np.diff(depth[event_dict['downcast_start']:event_dict['downcast_stop']])
    downcast_slope = -1
    if len(downcast_diff)>1:
        downcast_slope, intercept, downcast_r_value, p_value, std_err = stats.linregress(time_fulllength[event_dict['downcast_start']:event_dict['downcast_stop']], depth[event_dict['downcast_start']:event_dict['downcast_stop']])
        print('Downcast R value: ' + str(downcast_r_value))
    # Upcast stabilitetur
    # Fitta linju og rokna error
    slope, intercept, upcast_r_value, p_value, std_err = stats.linregress(time_fulllength[event_dict['downcast_stop']:event_dict['upcast_stop']], depth[event_dict['downcast_stop']:event_dict['upcast_stop']])
    upcast_r_value = abs(upcast_r_value)
    print('Upcast R value: ' + str(upcast_r_value))
    # Pumpa tendrar
    if pump_on == -1:
        Label(Quality_subframe, text='Pumpan tendraði ikki', font=("Helvetica", textsize), bg="red").pack(side=TOP, anchor=W)
        cast_quality -= 100
    elif (time_fulllength[pump_on] + 10 < time_fulllength[event_dict['downcast_start']])\
            and (time_fulllength[event_dict['soak_start']] < time_fulllength[pump_on] < time_fulllength[event_dict['soak_stop']]):
        Label(Quality_subframe, text='Pumpan tendraði til tíðuna', font=("Courier", textsize), bg="lightgreen").pack(side=TOP, anchor=W)
        cast_quality += 1
    else:
        Label(Quality_subframe, text='Pumpan tendraði ikki tá hon burdi', font=("Helvetica", textsize),
              bg="red").pack(side=TOP, anchor=W)
        cast_quality -= 1
    # Soak tíð og varians
    if time_fulllength[event_dict['soak_stop']] - time_fulllength[event_dict['soak_start']] > 60:
        Label(Quality_subframe, text='Soak er nóg miki langt', font=("Courier", textsize), bg="lightgreen").pack(
            side=TOP, anchor=W)
        cast_quality += 1
        if soakvar < 0.1:
            Label(Quality_subframe, text='Variansurin á soak er OK', font=("Courier", textsize), bg="lightgreen").pack(
                side=TOP, anchor=W)
        else:
            Label(Quality_subframe, text='Variansurin á soak er høgur', font=("Helvetica", textsize), bg="orange").pack(
                side=TOP,
                anchor=W)
    else:
        Label(Quality_subframe, text='Soak er ikki nóg langt', font=("Helvetica", textsize), bg="red").pack(side=TOP,
                                                                                                          anchor=W)
        cast_quality -= 1

    if len(downcast_diff) > 1:
        if np.min(downcast_diff) >= 0:
            Label(Quality_subframe, text='Downcast fer ikki upp', font=("Courier", textsize), bg="lightgreen").pack(side=TOP, anchor=W)
            downcast_quality += 1
        else:
            Label(Quality_subframe, text='Downcast fer upp', font=("Helvetica", textsize), bg="red").pack(side=TOP,anchor=W)
            downcast_quality -= 1

        if downcast_r_value > 0.99:
            Label(Quality_subframe, text='Downcast er stabilt', font=("Courier", textsize), bg="lightgreen").pack(side=TOP, anchor=W)
        else:
            Label(Quality_subframe, text='Downcast er ikki stabilt', font=("Helvetica", textsize), bg="red").pack(side=TOP, anchor=W)
        downcast_quality += downcast_r_value

        if upcast_r_value > 0.97:
            Label(Quality_subframe, text='Upcast er stabilt', font=("Courier", textsize), bg="lightgreen").pack(side=TOP, anchor=W)
        else:
            Label(Quality_subframe, text='Upcast er ikki stabilt', font=("Helvetica", textsize), bg="red").pack(side=TOP, anchor=W)
        upcast_quality += upcast_r_value

        if 0.5 < downcast_slope < 1:
            Label(Quality_subframe, text='Downcast ferð er ok', font=("Courier", textsize), bg="lightgreen").pack(side=TOP, anchor=W)
            downcast_quality += 1
        else:
            if downcast_slope < 0.5:
                Label(Quality_subframe, text='Downcast ferð er ov lág', font=("Helvetica", textsize), bg="red").pack(side=TOP, anchor=W)
            else:
                Label(Quality_subframe, text='Downcast ferð er ov høg', font=("Helvetica", textsize), bg="red").pack(side=TOP, anchor=W)
            downcast_quality -= 1

    text, is_dirty = gitTB.get_info()
    if is_dirty:
        Label(Quality_subframe, text='Git commit broytingar', font=("Helvetica", textsize), bg="red").pack(side=TOP, anchor=W)
        cast_quality -= 1
    else:
        Label(Quality_subframe, text='Git er ok', font=("Helvetica", textsize), bg="lightgreen").pack(side=TOP, anchor=W)

    if 'Master' not in text:
        Label(Quality_subframe, text='Git koyrur ikki á Master branch', font=("Helvetica", textsize), bg="orange").pack(side=TOP, anchor=W)

    cast_quality = cast_quality + downcast_quality + upcast_quality

    Label(Quality_subframe, text='Kvalitetur: ' + str(np.round(cast_quality+downcast_quality+upcast_quality,2)), font=("Helvetica", textsize)).pack(side=TOP, anchor=W)
    datetimestring = filnavn.split()
    measurement_time = datetime.datetime.strptime(datetimestring[0], '%Y-%m-%dt%H%M%S') + datetime.timedelta(0,time_fulllength[event_dict['downcast_start']])
    print(measurement_time)

    Label(Quality_subframe, text=('―' * 40), font=("Courier", 8)).pack(side=TOP, anchor=W) ## Seperator
    Label(Quality_subframe, text='Soaktid: ' + str(time_fulllength[event_dict['soak_stop']] - time_fulllength[event_dict['soak_start']]) + ' sek', font=("Courier", textsize-4)).pack(side=TOP, anchor=W)
    Label(Quality_subframe, text='Soakdypið:' + str(np.round(np.mean(depth[event_dict['soak_start']:event_dict['soak_stop']]), 3)) + ' m', font=("Courier", textsize-4)).pack(side=TOP, anchor=W)
    Label(Quality_subframe, text='Støðsta dýpið: ' + str(np.round(max(depth), 2)) + ' m', font=("Courier", textsize - 4)).pack(side=TOP, anchor=W)
    Label(Quality_subframe, text='Downcast ferð: ' + str(np.round(downcast_slope, 2)) + ' m/s', font=("Courier", textsize - 4)).pack(side=TOP, anchor=W)

    summary = {'downcast_quality': downcast_quality, 'upcast_quality': upcast_quality, 'cast_quality': cast_quality, 'soak_time': time_fulllength[event_dict['soak_stop']] - time_fulllength[event_dict['soak_start']],
               'soak_depth': np.mean(depth[event_dict['soak_start']:event_dict['soak_stop']]), 'soak_var': soakvar, 'downcast_time': measurement_time, 'downcast_speed': downcast_slope, 'max_depth': max(depth)}

    return summary