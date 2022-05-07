import essentia.standard as es
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def frequency(sr, TF_mag_out, TF_mag_ref, IR_output, IR_ref, output_file_freq,
                              reference_file):

    assert(len(TF_mag_out)==len(IR_output))

    for i in range (0,len(TF_mag_out)):
        TF_mag_out = list(TF_mag_out[i][0])

        # Magnitut en dBs, restamos para compensar el gain extra y tenerlas a 0dBs
        TF_mag_out = 20*np.log10(TF_mag_out)
        TF_mag_ref = 20*np.log10(TF_mag_ref)

        # Recorto para encontrar fc
        TF_mag_ref = TF_mag_ref - 3 #Reducimos para calcular la freq de corte

        if len(TF_mag_out)<len(TF_mag_ref):
            f = len(TF_mag_out)
        else:
            f = len(TF_mag_ref)

        TF_mag_out = TF_mag_out[0:f]
        TF_mag_ref = TF_mag_ref[0:f]

        assert (len(TF_mag_out)==len(TF_mag_ref))

        N = len(TF_mag_out)
        n = np.arange(N)
        T = N / sr
        freq = n / T

        idx= np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
        # La funcion flatten convierte un array en un integer ( de [algo] a algo)
        a=67
        pendiente = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a]+20)])
        # pendent
        fcorte = freq[idx[a]]

        # PLOT RESULTS
        fig, ax = plt.subplots(figsize=(10,4))
        plt.semilogx(freq, TF_mag_out, color='r')
        plt.semilogx(freq, TF_mag_ref, color='b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('Amplitude (dB)')
        plt.xlim(40, 32000)
        plt.ylim(-30,30)
        plt.title('Magnitud_TF')
        red_patch = mpatches.Patch(color='red', label='TF_' +
                                                      'output_file_freq[i].stem')
        first_Leg = ax.legend(handles=[red_patch], loc='upper left')
        ax.add_artist(first_Leg)
        black_patch = mpatches.Patch(color='black', label='f_corte:'+ str(fcorte))
        second_Leg = ax.legend(handles=[black_patch], loc='lower left')
        ax.add_artist(second_Leg)
        blue_patch = mpatches.Patch(color='blue', label='TF_'+str(reference_file.stem))
        ax.legend(handles=[blue_patch], loc='lower right')
        plt.plot(freq[idx[a]], TF_mag_out[idx[a]], 'ko')

        plt.savefig('TF_'+'output_file_freq[i].stem' +'.png')

    return fcorte, pendiente
