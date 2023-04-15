from pyOpenBCI import OpenBCICyton
import numpy as np
import mne
import tkinter as tk
from tkinter import Canvas, Frame

CHANNEL_MAPPING = {
    'Fp1': 1,
    'Fp2': 2,
    'F3': 3,
    'F4': 4,
    # ...
}

CHANNELS_TO_MEASURE = ['Fp1', 'Fp2', 'F3', 'F4']

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
    # This is a simple example of drawing circles with different colors
    # based on impedance_data. You can modify this code to create a more
    # complex topoplot visualization.
    radius = 20
    max_impedance = max(impedance_data)

    for i, imp in enumerate(impedance_data):
        x, y = pos_2d[i]
        x = int((x + 1) * 150)
        y = int((y + 1) * 150)
        intensity = int(255 * imp / max_impedance)
        color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

def update_topoplot(board, canvas):
    sample = board.get_board_data()
    impedance_data = impedance_measure(sample, canvas)
    draw_topoplot(impedance_data, canvas)
    canvas.after(1000, update_topoplot, board, canvas)

def main():
    root = tk.Tk()
    root.title("Topoplot")

    frame = Frame(root)
    frame.pack()

    canvas = Canvas(frame, width=300, height=300)
    canvas.pack()

    board = OpenBCICyton(port='COM4', daisy=True)
    board.start_stream()
    update_topoplot(board, canvas)

    root.mainloop()

if __name__ == "__main__":
    main()
# 사이보드를 연결하고 스트리밍을 시작합니다.
board = OpenBCICyton(port='COM4', daisy=True)  # 시리얼 포트를 사용하여 연결합니다. 포트 번호는 사용자의 시스템에 맞게 변경해야 합니다.
board.start_stream(impedance_measure_and_topoplot)
