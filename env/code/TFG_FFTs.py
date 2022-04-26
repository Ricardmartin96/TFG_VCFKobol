import essentia.standard as es
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import spatial

# definimos algunos parametros globales
sr = 48000

# Cargamos los audios de entrada y salida
IR_input = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/'
                'IR_Loopback_sweepstat.wav',
       sampleRate=sr)()
IR_output = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/'
                'IR_0R_16kF_sweepstat.wav',
       sampleRate=sr)()

IR_ref = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/'
                'IR_Bypass_sweepstat.wav',
       sampleRate=sr)()

# Cogemos la posicion del max de las IR (cogiendo solo la parte positiva)
pos_max_in = np.argmax(abs(IR_input))
pos_max_out = np.argmax(abs(IR_output))
pos_max_ref = np.argmax(abs(IR_ref))

# Recortamos los 3 señales de manera que los picos esten alineados
if pos_max_out>pos_max_in:
    dif = pos_max_out - pos_max_in
    IR_output = IR_output[dif:len(IR_output)]
else:
    dif = pos_max_in - pos_max_out
    IR_input = IR_input[dif:len(IR_input)]

if pos_max_ref>pos_max_out:
    dif = pos_max_ref - pos_max_out
    IR_ref = IR_ref[dif:len(IR_ref)]
else:
    dif = pos_max_in - pos_max_ref
    IR_input = IR_input[dif:len(IR_input)]

# Para que input i output tengan el mismo tamaño y sean pares (para la FFT)
if (len(IR_input)>len(IR_ref))&(len(IR_ref)>len(IR_output)):
    s = len(IR_output)
elif (len(IR_ref)>len(IR_output))&(len(IR_output)>len(IR_input)):
    s = len(IR_input)
else: 
    s = len(IR_ref)
if s%2 != 0:
    s = s-1

IR_input = IR_input[0:s]
IR_output = IR_output[0:s]
IR_ref = IR_ref[0:s]

IR_input[IR_input == 0] = np.finfo(float).eps # 0 = num molt petit
IR_output[IR_output == 0] = np.finfo(float).eps
IR_ref[IR_ref == 0] = np.finfo(float).eps

spec = es.FFT(size=s)
c2p = es.CartesianToPolar()
IR_input_fft = spec(IR_input)
IR_output_fft = spec(IR_output)
IR_ref_fft = spec(IR_ref)

trans_func_out = IR_output_fft/IR_input_fft
TF_mag_out, TF_ang_out = c2p(trans_func_out)
trans_func_ref = IR_ref_fft/IR_input_fft
TF_mag_ref, TF_ang_ref = c2p(trans_func_ref)

N = len(IR_input_fft)
n = np.arange(N)
T = N/sr
freq = n/T

TF_mag_out = 20*np.log10(TF_mag_out) # Magnitut en dBs
TF_mag_ref = 20*np.log10(TF_mag_ref)-3 #Reducimos 3dBs para calculas la freq de corte
TF_min = np.min(TF_mag_out)
TF_max = np.max(TF_mag_out)

# PLOT RESULTS
fig, ax = plt.subplots()
plt.semilogx(freq, TF_mag_out, color='r')
plt.semilogx(freq, TF_mag_ref, color='b')
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 52000)
plt.ylim(TF_min,TF_max)
plt.title('Magnitud_TF')
red_patch = mpatches.Patch(color='red', label='TF_0R_16kF_sweepstat')
first_Leg = ax.legend(handles=[red_patch], loc='upper left')
ax.add_artist(first_Leg)
#black_patch = mpatches.Patch(color='black', label='Frequencia de corte')
#second_Leg = ax.legend(handles=[black_patch], loc='lower left')
#ax.add_artist(second_Leg)
blue_patch = mpatches.Patch(color='blue', label='TF_Bypass_sweepstat')
ax.legend(handles=[blue_patch], loc='upper right')

'''
Encontrar la frecuencia de corte como el punto de interseccion entre output y
bypass, habiendo reducido la magnitud del bypass 3 dBs:
https://stackoverflow.com/questions/28766692/intersection-of-two-graphs-in-python-find-the-x-value
Primero calcula la diferencia de magnitudes y los signos correspondientes 
usando np.sign. Aplicando np.diff las posiciones donde cambia el signo 
(cosa que ocurre cuando ambas gráficas se cortan).
Usar np.argwhere nos da los índices exactos.
'''
idx = np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref)))
a=24
pendent = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a]*1.25)]) # pendent en 1/3 d'octava
print('frequencia de corte:', idx[a]/10) # dividim per tenir la freq exacta
print('pendent:', pendent*3, 'dBs/octava') # operem per tenir el pendent/octava
#plt.plot(freq[idx[a]], TF_mag_out[idx[a]], 'ko')
plt.show()
'''
plt.subplot(2,1,2)
plt.semilogx(freq, TF_ang)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.xlim(10, 32000)
plt.ylim(-np.pi, np.pi)
plt.title('Phase_TF')
plt.tight_layout()
plt.show()

plt.subplot(2,1,1)
plt.semilogx(freq, 20*np.log10(np.abs(IR_input_fft)))
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 32000)
plt.ylim(-50,50)
plt.title('IR_input_fft')

plt.subplot(2,1,2)
plt.semilogx(freq,20*np.log10(np.abs(IR_output_fft)))
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.xlim(10, 32000)
plt.ylim(-50, 50)
plt.title('IR_output_fft')
plt.tight_layout()
plt.show()
'''


