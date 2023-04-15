import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
 from pyOpenBCI import OpenBCICyton
import numpy as np
import mne
import tkinter as tk
from tkinter import Canvas, Frame
import threading
from queue import Queue

CHANNEL_MAPPING = {
    'Fp1': 1,
    'Fp2': 2,
    'F3': 3,
    'F4': 4,
    "Fz":5
    # ...
}

CHANNELS_TO_MEASURE = ['Fp1', 'Fp2', 'F3', 'F4','Fz']

def get_z(v):
    rms = get_rms(v)
    z = (1e-6 * rms * np.sqrt(2) / 6e-9) - 2200
    if z < 0:
        return 0
    return z

def filter_impedance(v, low_freq=5, high_freq=45, fs=250):
    v = np.array(v, dtype=float)
    filtered_v = mne.filter.filter_data(v, fs, low_freq, high_freq, method='iir')
    return filtered_v

def get_rms(v):
    return np.std(v)

montage = mne.channels.make_standard_montage('standard_1020')
pos_3d = montage.get_positions()['ch_pos']
pos_2d = np.array([[x, y] for ch, (x, y, z) in pos_3d.items() if ch in CHANNELS_TO_MEASURE])

def impedance_measure(sample, canvas):
    eeg, aux = sample.channels_data, sample.aux_data
    eeg = filter_impedance(eeg)
    impedance_values = []

    for channel_name in CHANNELS_TO_MEASURE:
        channel_number = CHANNEL_MAPPING[channel_name]
        z = get_z(eeg[channel_number - 1])
        impedance_values.append(z)

    return impedance_values
def draw_topoplot(impedance_data, channel_names, montage_name='standard_1020', cmap='coolwarm'):
    # Create a dictionary mapping channel names to impedance values
    ch_impedance_dict = {ch: imp for ch, imp in zip(channel_names, impedance_data)}

    # Create a new MNE info object with the specified channel names and the standard 10-20 montage
    info = mne.create_info(channel_names, sfreq=250, ch_types='eeg')
    info.set_montage(montage_name)

    # Create an MNE Evoked object with the impedance values as data
    evoked = mne.EvokedArray(np.array([list(ch_impedance_dict.values())]).T, info, tmin=0)

    # Plot the topomap
    fig, ax = plt.subplots(figsize=(5, 5))
    plot_topomap(evoked.data[:, 0], evoked.info, axes=ax, cmap=cmap, show=True)
def update_topoplot(board, fig, ax):
    sample = board.get_new_sample()
    impedance_data = impedance_measure(sample, canvas)
    draw_topoplot(impedance_data, fig, ax)
    root.after(1000, update_topoplot, board, fig, ax)
def main():
    q = Queue()

    def on_new_sample(sample):
        q.put(sample)

    def update_topoplot():
        if not q.empty():
            sample = q.get()
            impedance_data = impedance_measure(sample, canvas)
            draw_topoplot(impedance_data, fig, ax)
        root.after(100, update_topoplot)

    def start_board_stream():
        board.start_stream(on_new_sample)

    root = tk.Tk()
    root.title("Topoplot")

    frame = Frame(root)
    frame.pack()

    # Create a Figure and an Axes object for the topomap plot
    fig, ax = plt.subplots(figsize=(5, 5))

    # Create a FigureCanvasTkAgg object and embed it into the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    board = OpenBCICyton(port='COM4', daisy=True)

    board_thread = threading.Thread(target=start_board_stream)
    board_thread.daemon = True
    board_thread.start()

    update_topoplot()

    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        board.stop_stream()
        board_thread.join()

if __name__ == "__main__":
    main()
