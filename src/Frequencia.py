import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import json

def frequency(sr, TF_mag_out, TF_mag_ref, output_file_freq, reference_file):

    # Nos aseguramos que tengan la misma longitud y que esta sea par
    if (len(TF_mag_out) < len(TF_mag_ref)):
        s = len(TF_mag_out)
    else:
        s = len(TF_mag_ref)

    TF_mag_out = TF_mag_out[0:s]
    TF_mag_ref = TF_mag_ref[0:s]

    # Reducimos el nivel para que tenerla a 0dBs y -3 para calcular la fcorte
    TF_mag_ref = TF_mag_ref -3 #reg_ref - 3

    # Calculamos el eje x (pasamos de muestras a frecuencia)
    N = len(TF_mag_out)
    n = np.arange(N)
    T = N / sr
    freq = n / T

    # Calculamos la fc y el pendiente
    idx= np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
    a=1
    if (idx[a]<8000):
        pendiente = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a]*4)])\
                    /2
    elif (idx[a]>8000)and(idx[a]<16000):
        pendiente = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a]*2)])
    elif (idx[a]>16000)and(idx[a]<21000):
        pendiente = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a])*1.5])
    elif(idx[a]>21000):
        pendiente = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a])+100])

    fcorte = freq[idx[a]]

    # Eliminamos la IR_ del nombre
    output_file_freq_name = str(output_file_freq).replace('IR_', '_',
                                                               1)
    reference_file_name = str(reference_file).replace('IR_', '_', 1)

    # Ploteamos y guardamos los resultados
    fig, ax = plt.subplots(figsize=(10, 4))
    plt.semilogx(freq, TF_mag_out, color='r')
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
    black_patch = mpatches.Patch(color='black', label='f_corte:'+
                                                      str(fcorte))
    second_Leg = ax.legend(handles=[black_patch], loc='lower left')
    ax.add_artist(second_Leg)
    blue_patch = mpatches.Patch(color='blue', label='TF'+
                                                    str(reference_file_name))
    ax.legend(handles=[blue_patch], loc='lower right')
    plt.plot(freq[idx[a]], TF_mag_out[idx[a]], 'ko')

    plt.savefig("TF_"+str(output_file_freq_name)+".png".format())
    plt.close(fig)

    dict1 = {
        "Resultados: ": {
            "Frecuencia de corte": str(fcorte),
            "Pendiente": str(pendiente),
        },
    }

    freq_file = open("Results"+str(output_file_freq_name)+".json".format(),"w")
    json.dump(dict1, freq_file, indent=6)
    freq_file.close()

    return fcorte, pendiente

