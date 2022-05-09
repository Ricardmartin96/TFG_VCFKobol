import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def resonance (sr, TF_mag_out, TF_mag_ref, IR_output, output_file_res,
                              reference_file):

    assert (len(TF_mag_out) == len(IR_output))

    for i in range(0, len(TF_mag_out)-1):
        TF_mag_out_def = list(TF_mag_out[i][0])

        # Magnitut en dBs, restamos para compensar el gain extra y tenerlas a 0dBs
        TF_mag_out_def = 20*np.log10(TF_mag_out_def)-33
        TF_mag_ref = 20*np.log10(abs(TF_mag_ref))-2

        if len(TF_mag_out_def) < len(TF_mag_ref):
            f = len(TF_mag_out_def)
        else:
            f = len(TF_mag_ref)

        TF_mag_out_def = TF_mag_out_def[0:f]
        TF_mag_ref = TF_mag_ref[0:f]

        assert (len(TF_mag_out_def) == len(TF_mag_ref))

        N = len(TF_mag_out_def)
        n = np.arange(N)
        T = N / sr
        freq = n / T

        # Recorto para encontrar fc
        fcentral = np.argmax(TF_mag_out_def[40:32000])
        peak = np.max(TF_mag_out_def[40:32000])
        TF_mag_ref = TF_mag_ref +peak-3 #Aumentamos para calcular la res

        # PLOT RESULTS
        fig, ax = plt.subplots(figsize=(10,5))
        plt.semilogx(freq, TF_mag_out_def, color='r')
        plt.semilogx(freq, TF_mag_ref, color='b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.xlim(40, 32000)
        plt.ylim(-30,30)
        plt.title('Magnitud_TF')
        red_patch = mpatches.Patch(color='red', label='TF_' +
                                                      str(output_file_res.stem))
        first_Leg = ax.legend(handles=[red_patch], loc='upper left')
        ax.add_artist(first_Leg)
        black_patch = mpatches.Patch(color='black', label='f1,'+'fc'+'('+
                                                          str(fcentral)+')'+
                                                          ' y f2')
        second_Leg = ax.legend(handles=[black_patch], loc='lower left')
        ax.add_artist(second_Leg)
        blue_patch = mpatches.Patch(color='blue', label='TF_' +
                                                        str(reference_file.stem))
        ax.legend(handles=[blue_patch], loc='lower right')

        idx= np.argwhere(np.diff(np.sign(TF_mag_out_def - TF_mag_ref))).flatten()
        # La funcion flatten convierte un array en un integer ( de [algo] a algo)
        a=0
        b=0

        # Calculamos los parámetros de la resonancia: f1, f2, fc, fres, gain y Q
        f1 = 200 #idx[a]
        f2 = 220 #idx[b]
        fres = np.sqrt(freq[f1]*freq[f2])
        Q = fres/(freq[f2]-freq[f1])
        gain = peak - 0

        plt.plot(freq[f1], TF_mag_out_def[f1], 'ko')
        plt.plot(freq[fcentral], TF_mag_out_def[fcentral], 'ko')
        plt.plot(freq[f2], TF_mag_out_def[f2], 'ko')

        plt.savefig("TF_" + str(output_file_res.stem) + "{}.png".format(i))
        plt.close(fig)

    return freq[f1], freq[f2], freq[fcentral], fres, peak, Q, gain






