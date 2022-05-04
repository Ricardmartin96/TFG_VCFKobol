import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def resonance (sr, TF_mag_out, TF_mag_ref, IR_output, IR_ref):

    # Magnitut en dBs, restamos para compensar el gain extra y tenerlas a 0dBs
    TF_mag_out = 20*np.log10(TF_mag_out)-33
    TF_mag_ref_0 = 20*np.log10(TF_mag_ref)-2

    N = len(TF_mag_out)
    n = np.arange(N)
    T = N/sr
    freq = n/T

    if len(TF_mag_out) < len(TF_mag_ref):
        f = len(TF_mag_out)
    else:
        f = len(TF_mag_ref)

    TF_mag_out = TF_mag_out[0:f]
    TF_mag_ref = TF_mag_ref[0:f]

    assert (len(TF_mag_out) == len(TF_mag_ref))

    # Recorto para encontrar fc
    fcentral = np.argmax(TF_mag_out[40:32000])
    peak = np.max(TF_mag_out[40:32000])
    TF_mag_ref = TF_mag_ref_0 +peak-3 #Aumentamos para calcular la res

    # PLOT RESULTS
    fig, ax = plt.subplots(figsize=(10,5))
    plt.semilogx(freq, TF_mag_out, color='r')
    plt.semilogx(freq, TF_mag_ref, color='b')
    plt.xlabel('Freq (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.xlim(40, 32000)
    plt.ylim(-30,30)
    plt.title('Magnitud_TF')
    red_patch = mpatches.Patch(color='red', label='TF_'+str(IR_output))
    first_Leg = ax.legend(handles=[red_patch], loc='upper left')
    ax.add_artist(first_Leg)
    black_patch = mpatches.Patch(color='black', label='f1, fc y f2')
    second_Leg = ax.legend(handles=[black_patch], loc='lower left')
    ax.add_artist(second_Leg)
    blue_patch = mpatches.Patch(color='blue', label='TF_'+str(IR_ref))
    ax.legend(handles=[blue_patch], loc='lower right')

    '''
    Encontrar f1 y f2 como los punto de interseccion entre output y bypass aumentado. 
    Primero calcula la diferencia de magnitudes y los signos correspondientes 
    usando np.sign. Aplicando np.diff y np.argwhere conocemos las posiciones donde
    cambia el signo (cosa que ocurre cuando ambas gráficas se cortan).
    '''
    idx= np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
    # La funcion flatten convierte un array en un integer ( de [algo] a algo)
    a=26
    b=29

    # Calculamos los parámetros de la resonancia: f1, f2, fc, fres, gain y Q
    f1 = idx[a]
    f2 = idx[b]
    fres = np.sqrt(freq[f1]*freq[f2])
    Q = fres/(freq[f2]-freq[f1])
    gain = peak - 0

    plt.plot(freq[f1], TF_mag_out[f1], 'ko')
    plt.plot(freq[fcentral], TF_mag_out[fcentral], 'ko')
    plt.plot(freq[f2], TF_mag_out[f2], 'ko')

    plt.savefig('TF_'+str(IR_output)+'.png')

    return freq[f1], freq[f2], freq[fcentral], fres, peak, Q, gain






