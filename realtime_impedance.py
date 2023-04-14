from pyOpenBCI import OpenBCICyton

# 이전에 정의한 변수와 함수들은 그대로 유지합니다.
import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.viz import plot_topomap

# 채널 매핑 및 측정할 채널 정의
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
def filter_impedance(v, low_freq=5, high_freq=345, fs=250):
    filtered_v = mne.filter.filter_data(v, fs, low_freq, high_freq, method='iir')
    return filtered_v


def get_rms(v):
    return np.std(v)
#     return (v.max()-v.min())/(2*np.sqrt(2))




# 채널 위치 정보를 가져옵니다.
montage = mne.channels.make_standard_montage('standard_1020')
pos = montage.get_positions()['ch_pos']
# 콜백 함수 정의
def impedance_measure_and_topoplot(sample):
    eeg, aux = sample.channels_data, sample.aux_data
    eeg = filter_impedance(eeg)
    impedance_values = []
    
    for channel_name in CHANNELS_TO_MEASURE:
        channel_number = CHANNEL_MAPPING[channel_name]
        z = get_z(eeg[channel_number - 1])
        impedance_values.append(z)
        print(f'Channel {channel_name}: {z / 1000:.2f} kOhm')

    # 임피던스 값을 Topoplot에 표시합니다.
    impedance_data = np.array([impedance_values[CHANNEL_MAPPING[ch] - 1] for ch in CHANNELS_TO_MEASURE])
    plot_topomap(impedance_data, pos, cmap='inferno', contours=0, show=False)
    plt.pause(1)
    plt.clf()

# 사이보드를 연결하고 스트리밍을 시작합니다.
board = OpenBCICyton(port='COM4', daisy=True)  # 시리얼 포트를 사용하여 연결합니다. 포트 번호는 사용자의 시스템에 맞게 변경해야 합니다.
board.start_stream(impedance_measure_and_topoplot)