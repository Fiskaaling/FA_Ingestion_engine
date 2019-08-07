# Hesin fílurin er til at minka um gui skrambul í bin_average fílinum
import numpy as np


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