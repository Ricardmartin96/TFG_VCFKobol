import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json

def resonance (sr, TF_mag_out, TF_mag_ref, output_file_res, reference_file):

    # Encontramos fcentral y su pico
    fcentral = np.argmax(TF_mag_out)
    peak = np.max(TF_mag_out)

    # Aumentamos el bypass para calcular f1 y f2
    TF_mag_ref = TF_mag_ref + peak - 3

    # Calculamos los parametros de la resonancia
    idx = np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
    a = 0
    b = len(idx)-1
    f1 = idx[a]
    f2 = idx[b]
    fres = np.sqrt(f1 * f2)
    Q = fres / (f2 - f1)

    # Eliminamos la IR_ del nombre
    output_file_res_name = str(output_file_res).replace('IR_', '_', 1)
    reference_file_name = str(reference_file).replace('IR_', '_', 1)

    N = len(TF_mag_out)
    n = np.arange(N)
    T = N / sr
    freq = n / T

    # Ploteamos y guardamos resultados
    fig, ax = plt.subplots(figsize=(10,5))
    plt.semilogx(freq, TF_mag_out, color='r')
    plt.semilogx(freq, TF_mag_ref, color='b')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.xlim(10, 32000)
    plt.ylim(-30,30)
    plt.title('Magnitud_TF')
    red_patch = mpatches.Patch(color='red', label='TF' +
                                                  str(output_file_res_name))
    first_Leg = ax.legend(handles=[red_patch], loc='upper left')
    ax.add_artist(first_Leg)
    black_patch = mpatches.Patch(color='black', label='f1,'+'fc'+'('+
                                                      str(freq[fcentral])+')'+
                                                      ' y f2')
    second_Leg = ax.legend(handles=[black_patch], loc='lower left')
    ax.add_artist(second_Leg)
    blue_patch = mpatches.Patch(color='blue', label='TF' +
                                                    str(reference_file_name))
    ax.legend(handles=[blue_patch], loc='lower right')
    plt.plot(freq[f1], TF_mag_out[f1], 'ko')
    plt.plot(freq[fcentral], TF_mag_out[fcentral], 'ko')
    plt.plot(freq[f2], TF_mag_out[f2], 'ko')

    plt.savefig("TF" + str(output_file_res_name) + ".png".format())
    plt.close(fig)

    dict2 = {
        "Resultados: ": {
            "F1": str(freq[f1]),
            "F2": str(freq[f2]),
            "Frecuencia central": str(freq[fcentral]),
            "Frecuencia de resonancia": str(freq[int(fres)]),
            "Pico o ganancia": str(peak),
            "Factor Q": str(Q),
        },
    }

    res_file = open("Results" + output_file_res_name + ".json".format(), "w")
    json.dump(dict2, res_file, indent=6)
    res_file.close()

    return freq[f1], freq[f2], freq[fcentral], fres, peak, Q






