import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json

def resonance (sr, TF_mag_out, TF_mag_ref, IR_output, output_file_res,
                              reference_file, reg_ref, reg_out):

    # Recortamos el bypass para tener la region sin ruido
    TF_mag_ref = TF_mag_ref[40:32000]

    # Reducimos el nivel para que tenerla a 0dBs
    TF_mag_ref = 20 * np.log10(abs(TF_mag_ref)) - reg_ref

    # Iteramos sobre las salidas
    for i in range(0, len(TF_mag_out)-1):

        # Cogemos la magnitud de la salida i, la reducimos y la recortamos
        TF_mag_out_def = list(TF_mag_out[i][0])
        TF_mag_out_def = 20*np.log10(TF_mag_out_def) - reg_out
        TF_mag_out_def = TF_mag_out_def[40:32000]

        # Calculamos el eje x (pasamos de muestras a frecuencia)
        N = len(TF_mag_out_def)
        n = np.arange(N)
        T = N / sr
        freq = n / T

        # Recorto para encontrar fc
        fcentral = np.argmax(TF_mag_out_def[40:32000])
        peak = np.max(TF_mag_out_def[40:32000])

        # Aumentamos el bypass para calcular f1 y f2
        TF_mag_ref = TF_mag_ref +peak - 3

        # Calculamos los parametros de la resonancia
        idx = np.argwhere(np.diff(np.sign(TF_mag_out_def - TF_mag_ref))).\
            flatten()
        a = 1
        b = 2
        f1 = idx[a]
        f2 = idx[b]
        fres = np.sqrt(freq[f1] * freq[f2])
        Q = fres / (freq[f2] - freq[f1])
        gain = peak - TF_mag_ref[fcentral]

        # Eliminamos la IR_ del nombre
        output_file_res_name = str(output_file_res.stem).replace('IR_', '_',
                                                                   1)
        reference_file_name = str(reference_file.stem).replace('IR_', '_', 1)

        # Ploteamos y guardamos resultados
        fig, ax = plt.subplots(figsize=(10,5))
        plt.semilogx(freq, TF_mag_out_def, color='r')
        plt.semilogx(freq, TF_mag_ref, color='b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.xlim(40, 32000)
        plt.ylim(-30,30)
        plt.title('Magnitud_TF')
        red_patch = mpatches.Patch(color='red', label='TF_' +
                                                      str(output_file_res_name))
        first_Leg = ax.legend(handles=[red_patch], loc='upper left')
        ax.add_artist(first_Leg)
        black_patch = mpatches.Patch(color='black', label='f1,'+'fc'+'('+
                                                          str(fcentral)+')'+
                                                          ' y f2')
        second_Leg = ax.legend(handles=[black_patch], loc='lower left')
        ax.add_artist(second_Leg)
        blue_patch = mpatches.Patch(color='blue', label='TF_' +
                                                        str(reference_file_name))
        ax.legend(handles=[blue_patch], loc='lower right')
        plt.plot(freq[f1], TF_mag_out_def[f1], 'ko')
        plt.plot(freq[fcentral], TF_mag_out_def[fcentral], 'ko')
        plt.plot(freq[f2], TF_mag_out_def[f2], 'ko')

        plt.savefig("TF_" + str(output_file_res_name) + "{}.png".format(i))
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

        res_file = open("Results_" + output_file_res_name + "{}.json".format(i),
                        "w")
        json.dump(dict2, res_file, indent=6)
        res_file.close()

    return freq[f1], freq[f2], freq[fcentral], fres, peak, Q, gain






