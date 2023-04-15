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
def draw_topoplot(impedance_data, canvas):
    # Clear canvas
    canvas.delete("all")

    # Draw topoplot
    radius = 20
    max_impedance = max(impedance_data)

    if max_impedance == 0:
        max_impedance = 1  # 최대 임피던스 값이 0인 경우를 처리합니다.

    for i, imp in enumerate(impedance_data):
        x, y = pos_2d[i]
        x = int((x + 1) * 150)
        y = int((y + 1) * 150)
        intensity = int(255 * imp / max_impedance)
        color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)



def update_topoplot(board, canvas):
    sample = board.get_new_sample()  # 변경된 부분
    impedance_data = impedance_measure(sample, canvas)
    draw_topoplot(impedance_data, canvas)
    canvas.after(1000, update_topoplot, board, canvas)
def main():
    q = Queue()

    def on_new_sample(sample):
        q.put(sample)

    def update_topoplot():
        if not q.empty():
            sample = q.get()
            impedance_data = impedance_measure(sample, canvas)
            draw_topoplot(impedance_data, canvas)
        root.after(100, update_topoplot)

    def start_board_stream():
        board.start_stream(on_new_sample)

    root = tk.Tk()
    root.title("Topoplot")

    frame = Frame(root)
    frame.pack()

    canvas = Canvas(frame, width=300, height=300)
    canvas.pack()

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
