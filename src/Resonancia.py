import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json

def resonance (sr, TF_mag_out, TF_mag_ref, output_file_res, reference_file):

    # Nos aseguramos que tengan la misma longitud y que esta sea par
    if (len(TF_mag_out) < len(TF_mag_ref)):
        s = len(TF_mag_out)
    else:
        s = len(TF_mag_ref)

    TF_mag_out = TF_mag_out[0:s]
    TF_mag_ref = TF_mag_ref[0:s]

    # Calculamos el eje x (pasamos de muestras a frecuencia)
    N = len(TF_mag_out)
    n = np.arange(N)
    T = N / sr
    freq = n / T

    # Encontramos fcentral y su pico
    fcentral = np.argmax(TF_mag_out)
    peak = np.max(TF_mag_out)

    # Aumentamos el bypass para calcular f1 y f2
    TF_mag_ref = TF_mag_ref +peak - 3

    # Calculamos los parametros de la resonancia
    idx = np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
    a = 1
    b = 2
    f1 = 20000 #idx[a]
    f2 = 21000 #idx[b]
    fres = np.sqrt(freq[f1] * freq[f2])
    Q = fres / (freq[f2] - freq[f1])
    gain = peak - TF_mag_ref[fcentral]

    # Eliminamos la IR_ del nombre
    output_file_res_name = str(output_file_res).replace('IR_', '_',
                                                               1)
    reference_file_name = str(reference_file).replace('IR_', '_', 1)

    # Ploteamos y guardamos resultados
    fig, ax = plt.subplots(figsize=(10,5))
    plt.semilogx(freq, TF_mag_out, color='r')
    plt.semilogx(freq, TF_mag_ref, color='b')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.xlim(40, 32000)
    plt.ylim(-30,30)
    plt.title('Magnitud_TF')
    red_patch = mpatches.Patch(color='red', label='TF' +
                                                  str(output_file_res_name))
    first_Leg = ax.legend(handles=[red_patch], loc='upper left')
    ax.add_artist(first_Leg)
    black_patch = mpatches.Patch(color='black', label='f1,'+'fc'+'('+
                                                      str(fcentral)+')'+
                                                      ' y f2')
    second_Leg = ax.legend(handles=[black_patch], loc='lower left')
    ax.add_artist(second_Leg)
    blue_patch = mpatches.Patch(color='blue', label='TF' +
                                                    str(reference_file_name))
    ax.legend(handles=[blue_patch], loc='lower right')
    plt.plot(freq[f1], TF_mag_out[f1], 'ko')
    plt.plot(freq[fcentral], TF_mag_out[fcentral], 'ko')
    plt.plot(freq[f2], TF_mag_out[f2], 'ko')

    plt.savefig("TF_" + str(output_file_res_name) + ".png".format())
    plt.close(fig)

    dict2 = {
        "Resultados: ": {
            "F1": str(f1),
            "F2": str(f2),
            "Frecuencia central": str(fcentral),
            "Frecuencia de resonancia": "40000",
            "Pico": str(peak),
            "Factor Q": str(Q),
            "Ganancia": str(gain),
        },
    }

    res_file = open("Results" + output_file_res_name + ".json".format(), "w")
    json.dump(dict2, res_file, indent=6)
    res_file.close()

    return freq[f1], freq[f2], freq[fcentral], fres, peak, Q, gain






