import essentia.standard as es
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def frequency(sr, TF_mag_out, TF_mag_ref, IR_output, IR_ref):
    rms = es.RMS()

    TF_mag_out_eq = rms(TF_mag_out[40:440])
    TF_mag_ref_eq = rms(TF_mag_ref[40:440])

    # Magnitut en dBs, restamos para compensar el gain extra y tenerlas a 0dBs
    TF_mag_out = 20*np.log10(TF_mag_out) - 20*np.log10(TF_mag_out_eq)-2
    TF_mag_ref = 20*np.log10(TF_mag_ref)- TF_mag_ref_eq

    # Recorto para encontrar fc
    TF_mag_ref = TF_mag_ref - 3 #Reducimos para calcular la freq de corte

    N = len(TF_mag_out)
    n = np.arange(N)
    T = N/sr
    freq = n/T

    if len(TF_mag_out)<len(TF_mag_ref):
        f = len(TF_mag_out)
    else:
        f = len(TF_mag_ref)

    TF_mag_out=TF_mag_out[0:f]
    TF_mag_ref = TF_mag_ref[0:f]

    assert (len(TF_mag_out)==len(TF_mag_ref))

    '''
    Encontrar la frecuencia de corte como el punto de interseccion entre output y
    bypass. Primero calcula la diferencia de magnitudes y los signos correspondientes 
    usando np.sign. Aplicando np.diff y np.argwhere conocemos las posiciones donde 
    cambia el signo (cosa que ocurre cuando ambas gráficas se cortan).
    '''
    idx= np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
    # La funcion flatten convierte un array en un integer ( de [algo] a algo)
    a=67
    pendiente = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a]*4)])/2 # pendent
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
    red_patch = mpatches.Patch(color='red', label='TF_'+str(IR_output))
    first_Leg = ax.legend(handles=[red_patch], loc='upper left')
    ax.add_artist(first_Leg)
    black_patch = mpatches.Patch(color='black', label='f_corte:'+ str(fcorte))
    second_Leg = ax.legend(handles=[black_patch], loc='lower left')
    ax.add_artist(second_Leg)
    blue_patch = mpatches.Patch(color='blue', label='TF_'+str(IR_ref))
    ax.legend(handles=[blue_patch], loc='lower right')
    plt.plot(freq[idx[a]], TF_mag_out[idx[a]], 'ko')

    plt.savefig('TF_'+str(IR_output)+'.png')

    return fcorte, pendiente
