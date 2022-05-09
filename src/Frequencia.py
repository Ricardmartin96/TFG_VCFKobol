import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json

def frequency(sr, TF_mag_out, TF_mag_ref, IR_output, output_file_freq,
                              reference_file, reg_ref, reg_out):

    assert(len(TF_mag_out)==len(IR_output))

    TF_mag_ref = TF_mag_ref[40:32000]
    TF_mag_ref = 20 * np.log10(abs(TF_mag_ref)) - reg_ref - 3

    for i in range (0,len(TF_mag_out)-1):
        TF_mag_out_def = list(TF_mag_out[i][0])
        TF_mag_out_def = 20*np.log10(TF_mag_out_def) - reg_out
        TF_mag_out_def = TF_mag_out_def[40:32000]

        N = len(TF_mag_out_def)
        n = np.arange(N)
        T = N / sr
        freq = n / T

        idx= np.argwhere(np.diff(np.sign(TF_mag_out_def - TF_mag_ref))).flatten()
        # La funcion flatten convierte un array en un integer ( de [algo] a algo)
        a=1
        # pendiente
        if (idx[a]<8000):
            pendiente = (TF_mag_out_def[idx[a]]-TF_mag_out_def[int(idx[a]*4)])/2
        elif (idx[a]>8000)and(idx[a]<16000):
            pendiente = (TF_mag_out_def[idx[a]]-TF_mag_out_def[int(idx[a]*2)])
        elif (idx[a]>16000)and(idx[a]<21000):
            pendiente = (TF_mag_out_def[idx[a]]-TF_mag_out_def[int(idx[a])*1.5])
        elif(idx[a]>21000):
            pendiente = (TF_mag_out_def[idx[a]]-TF_mag_out_def[int(idx[a])+100])

        fcorte = freq[idx[a]]

        output_file_freq_name = str(output_file_freq.stem).replace('IR_', '_',
                                                                   1)
        reference_file_name = str(reference_file.stem).replace('IR_', '_', 1)

        # PLOT RESULTS
        fig, ax = plt.subplots(figsize=(10, 4))
        plt.semilogx(freq, TF_mag_out_def, color='r')
        plt.semilogx(freq, TF_mag_ref, color='b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.xlim(40, 32000)
        plt.ylim(-30,30)
        plt.title('Magnitud_TF')
        red_patch = mpatches.Patch(color='red', label='TF' +
                                                      str(output_file_freq_name))
        first_Leg = ax.legend(handles=[red_patch], loc='upper left')
        ax.add_artist(first_Leg)
        black_patch = mpatches.Patch(color='black', label='f_corte:'+ str(fcorte))
        second_Leg = ax.legend(handles=[black_patch], loc='lower left')
        ax.add_artist(second_Leg)
        blue_patch = mpatches.Patch(color='blue', label='TF_'+str(reference_file_name))
        ax.legend(handles=[blue_patch], loc='lower right')
        plt.plot(freq[idx[a]], TF_mag_out_def[idx[a]], 'ko')

        plt.savefig("TF_"+ str(output_file_freq_name)+"{}.png".format(i))
        plt.close(fig)

        # STORE RESULTS IN JSON FILE
        dict1 = {
            "Resultados: ": {
                "Frecuencia de corte": str(fcorte),
                "Pendiente": str(pendiente),
            },
        }

        freq_file = open("Results_" + output_file_freq_name + "{}.json".format(i), "w")
        json.dump(dict1, freq_file, indent=6)
        freq_file.close()

    return fcorte, pendiente

