import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json

def frequency(sr, TF_mag_out, TF_mag_ref, output_file_freq, reference_file):

    # Reducimos el nivel 3 dBs para calcular la fcorte
    TF_mag_ref = TF_mag_ref - 3

    # Calculamos la fc y el pendiente
    fcorte = np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
    fcorte = fcorte[0]

    if fcorte < 80000:
        pendiente = (TF_mag_out[int(fcorte)]-TF_mag_out[int(fcorte*4)])/2
    elif (fcorte>80000)and(fcorte<210000):
        pendiente = (TF_mag_out[int(fcorte)]-TF_mag_out[int(fcorte*2)])
    elif fcorte>210000:
        pendiente = (TF_mag_out[int(fcorte)]-TF_mag_out[int(fcorte)+6000])

    # Eliminamos la IR_ del nombre
    output_file_freq_name = str(output_file_freq).replace('IR_', '_', 1)
    reference_file_name = str(reference_file).replace('IR_', '_', 1)

    # Calculamos un vector de frecuencias para el plot
    N = len(TF_mag_out)
    n = np.arange(N)
    T = N / sr
    freq = n / T

    # Ploteamos y guardamos los resultados
    fig, ax = plt.subplots(figsize=(10, 4))
    plt.semilogx(freq, TF_mag_out, color='r')
    plt.semilogx(freq, TF_mag_ref, color='b')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.xlim(10, 52000)
    plt.ylim(-30,30)
    plt.title('Magnitud_TF')
    red_patch = mpatches.Patch(color='red', label='TF' +
                                                 str(output_file_freq_name))
    first_Leg = ax.legend(handles=[red_patch], loc='upper left')
    ax.add_artist(first_Leg)
    black_patch = mpatches.Patch(color='black', label='f_corte:'+
                                                      str(freq[fcorte]))
    second_Leg = ax.legend(handles=[black_patch], loc='lower left')
    ax.add_artist(second_Leg)
    blue_patch = mpatches.Patch(color='blue', label='TF'+
                                                    str(reference_file_name))
    ax.legend(handles=[blue_patch], loc='lower right')
    plt.plot(freq[fcorte], TF_mag_out[fcorte], 'ko')
    
    plt.savefig("TF"+str(output_file_freq_name)+".png".format())
    plt.close(fig)
    
    dict1 = {
        "Resultados: ": {
            "Frecuencia de corte": str(freq[fcorte]) + 'Hz',
            "Pendiente": str(pendiente) + 'dB/octava',
        }
    }

    freq_file = open("Results"+str(output_file_freq_name)+".json".format(),"w")
    json.dump(dict1, freq_file, indent=6)
    freq_file.close()

    return freq[fcorte], pendiente

