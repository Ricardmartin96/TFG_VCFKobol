import essentia.standard as es
import essentia as e
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

def flat_reg(TF_mag, sr):
    mean = es.Mean()
    der = es.Derivative()

    N = len(TF_mag)
    n = np.arange(N)
    T = N / sr
    freq = n / T

# https: // matplotlib.org / 3.5.0 / gallery / user_interfaces / canvasagg.html
    fig = Figure(figsize=(2, 1), dpi=80)
    canvas = FigureCanvasAgg(fig)
    plt.semilogx(freq, TF_mag, color='r')
    plt.xlim(40, 32000)
    canvas.draw()
    TF_mag_freq = np.asarray(canvas.buffer_rgba())
    TF_mag_freq = TF_mag_freq.flatten()
    # retorna una imatge en blanc

    flat_dB_list=[]
    for i in range (0, len(TF_mag_freq)-1):
        if (TF_mag_freq[i] - TF_mag_freq[i+1])<1:
            flat_dB_list.append(TF_mag_freq[i])
    flat_dB = mean(e.array(flat_dB_list))

    '''
    TF_mag_freq_der = der(TF_mag_freq)
    flat_dB_list = []

    for j in range(0, len(TF_mag_freq_der) - 1):
        if (TF_mag_freq_der[j]<0.5) and ((TF_mag_freq_der[j+1] -
                                          TF_mag_freq_der[j]) < 0.25):
            flat_dB_list.append(TF_mag_freq[j])
    flat_dB = mean(np.array(flat_dB_list))
    '''
    return flat_dB