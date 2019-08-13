# Hesin fílurin er til at minka um gui skrambul í bin_average fílinum
import os
import numpy as np
from tkinter import Label, TOP, W
import pandas as pd

def refresh_qframe(Quality_frame, list_of_casts, parent_folder, filnavn, mappunavn_dict):
    textsize = 16  # TODO: Set hettar í ein settings fíl
    metadata = []
    for widget in Quality_frame.winfo_children(): # Tømur quality frame
        widget.destroy()
    for cast in list_of_casts:
        casttext = cast
        if os.path.exists(parent_folder + '/ASCII_Downcast/metadata/' + cast.split('.')[0] + '_metadata.csv'):
            cast_metadata_df = pd.read_csv(parent_folder + '/ASCII_Downcast/metadata/' + cast.split('.')[0] + '_metadata.csv', index_col=False)
            cast_metadata_keys = cast_metadata_df.key
            cast_metadata_values = cast_metadata_df.value
            cast_metadata = {}
            for i, key in enumerate(cast_metadata_keys):
                cast_metadata[key] = cast_metadata_values[i]

            if cast == filnavn[mappunavn_dict['filur']]:
                metadata = cast_metadata

            if float(cast_metadata['cast_quality']) < 0:
                casttext += ' -'
            else:
                casttext += ' ✓'
        if os.path.exists(parent_folder + '/ASCII_Downcast/metadata/' + cast.split('.')[0] + '_do_not_use_.csv'):
            casttext += ' X'
        if cast == filnavn[mappunavn_dict['filur']]:
            Label(Quality_frame, text=casttext, font=("Courier", textsize, 'underline')).pack(side=TOP, anchor=W)
        else:
            Label(Quality_frame, text=casttext, font=("Courier", textsize)).pack(side=TOP, anchor=W)
    return metadata


def kanna_events(event_dict, log_w):
    if event_dict['soak_start'] == -1:
        log_w('Ávaring! Soak Start er ikki funnið')
        event_dict['soak_start'] = 50
    if event_dict['soak_stop'] == -1:
        log_w('Ávaring! Soak Stop er ikki funnið')
        event_dict['soak_stop'] = 100
    if event_dict['downcast_start'] == -1:
        log_w('Ávaring! Downcast Start er ikki funnið')
        event_dict['downcast_start'] = 150
    if event_dict['downcast_stop'] == -1:
        log_w('Ávaring! Downcast Stop er ikki funnið')
        event_dict['downcast_stop'] = 200
    if event_dict['upcast_stop'] == -1:
        log_w('Ávaring! Upcast Stop er ikki funnið')
        event_dict['upcast_stop'] = 250


def zoom_in(selected_event, ax, event_dict, depth):
    time_fulllength = event_dict['time_fulllength']
    if selected_event == 0:
        ax.set_xlim(time_fulllength[event_dict['soak_start']] - 5, time_fulllength[event_dict['soak_start']] + 5)
        ax.set_ylim(np.min(depth[event_dict['soak_start'] - (5 * 16):event_dict['soak_start'] + (5 * 16)]) - 0.5, np.max(depth[event_dict['soak_start'] - (5 * 16):event_dict['soak_start'] + (5 * 16)]) + 0.5)
    if selected_event == 1:
        ax.set_xlim(time_fulllength[event_dict['soak_stop']] - 5, time_fulllength[event_dict['soak_stop']] + 5)
        ax.set_ylim(np.min(depth[event_dict['soak_stop'] - (5 * 16):event_dict['soak_stop'] + (5 * 16)]) - 0.5,
                    np.max(depth[event_dict['soak_stop'] - (5 * 16):event_dict['soak_stop'] + (5 * 16)]) + 0.5)
    if selected_event == 2:
        ax.set_xlim(time_fulllength[event_dict['downcast_start']] - 5, time_fulllength[event_dict['downcast_start']] + 5)
        ax.set_ylim(np.min(depth[event_dict['downcast_start'] - (5 * 16):event_dict['downcast_start'] + (5 * 16)]) - 0.5,
                    np.max(depth[event_dict['downcast_start'] - (5 * 16):event_dict['downcast_start'] + (5 * 16)]) + 0.5)
    if selected_event == 3:
        ax.set_xlim(time_fulllength[event_dict['downcast_stop']] - 5, time_fulllength[event_dict['downcast_stop']] + 5)
        ax.set_ylim(np.min(depth[event_dict['downcast_stop'] - (5 * 16):event_dict['downcast_stop'] + (5 * 16)]) - 0.5,
                    np.max(depth[event_dict['downcast_stop'] - (5 * 16):event_dict['downcast_stop'] + (5 * 16)]) + 0.5)
    if selected_event == 4:
        ax.set_xlim(time_fulllength[event_dict['upcast_stop']] - 5, time_fulllength[event_dict['upcast_stop']] + 5)
        ax.set_ylim(np.min(depth[event_dict['upcast_stop'] - (5 * 16):event_dict['upcast_stop'] + (5 * 16)]) - 0.5,
                    np.max(depth[event_dict['upcast_stop'] - (5 * 16):event_dict['upcast_stop'] + (5 * 16)]) + 0.5)


def update_annotations(selected_event, ax, event_dict, maxd):
    time_fulllength = event_dict['time_fulllength']
    if selected_event == 0:
        annotation = ax.annotate('Soak Start',
                                 xy=(time_fulllength[event_dict['soak_start']], maxd + 1),
                                 xytext=(time_fulllength[event_dict['soak_start']], maxd + 2),
                                 xycoords='data',
                                 textcoords='data',
                                 ha='center',
                                 arrowprops=dict(arrowstyle="->"))
    elif selected_event == 1:
        annotation = ax.annotate('Soak Stop',
                                 xy=(time_fulllength[event_dict['soak_stop']], maxd + 1),
                                 xytext=(time_fulllength[event_dict['soak_stop']], maxd + 2),
                                 xycoords='data',
                                 textcoords='data',
                                 ha='center',
                                 arrowprops=dict(arrowstyle="->"))
    elif selected_event == 2:
        annotation = ax.annotate('Downcast Start',
                                 xy=(time_fulllength[event_dict['downcast_start']], maxd + 1),
                                 xytext=(time_fulllength[event_dict['downcast_start']], maxd + 2),
                                 xycoords='data',
                                 textcoords='data',
                                 ha='center',
                                 arrowprops=dict(arrowstyle="->"))
    elif selected_event == 3:
        annotation = ax.annotate('Downcast Stop',
                                 xy=(time_fulllength[event_dict['downcast_stop']], maxd + 1),
                                 xytext=(time_fulllength[event_dict['downcast_stop']], maxd + 2),
                                 xycoords='data',
                                 textcoords='data',
                                 ha='center',
                                 arrowprops=dict(arrowstyle="->"))
    elif selected_event == 4:
        annotation = ax.annotate('Upcast Stop',
                                 xy=(time_fulllength[event_dict['upcast_stop']], maxd + 1),
                                 xytext=(time_fulllength[event_dict['upcast_stop']], maxd + 2),
                                 xycoords='data',
                                 textcoords='data',
                                 ha='center',
                                 arrowprops=dict(arrowstyle="->"))
    return annotation
