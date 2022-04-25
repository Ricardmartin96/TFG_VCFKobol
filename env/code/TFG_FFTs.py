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
                'IR_0R_16F_sweepstat.wav',
       sampleRate=sr)()

IR_ref = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/'
                'IR_Bypass_sweepstat.wav',
       sampleRate=sr)()

# Ploteamos las IR
'''
fig, ax = plt.subplots(nrows=3, ncols=1)
ax[0].plot(IR_input, color='b')
ax[0].set_title("Input IR")
ax[1].plot(IR_output, color='r')
ax[1].set_title("Output IR")
ax[2].plot(IR_ref, color='k')
ax[2].set_title("Reference IR")
plt.tight_layout()
plt.show()
exit()
'''
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
'''
print('pos_max_in', np.argmax(abs(IR_input)))
print('pos_max_out', np.argmax(abs(IR_output)))
print('pos_max_ref', np.argmax(abs(IR_ref)))
print('len_in', len(IR_input))
print('len_out', len(IR_output))
print('len_ref', len(IR_ref))
print('s', s)
exit()
'''
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
plt.xlim(10, 32000)
plt.ylim(TF_min,TF_max)
plt.title('Magnitud_TF')
red_patch = mpatches.Patch(color='red', label='TF_0R_16F_sweepstat')
first_Leg = ax.legend(handles=[red_patch], loc='upper left')
ax.add_artist(first_Leg)
blue_patch = mpatches.Patch(color='blue', label='TF_Bypass_sweepstat')
ax.legend(handles=[blue_patch], loc='upper right')

'''
Encontrar la frecuencia de corte como el punto de interseccion entre output y
bypass, habiendo reducido la magnitud del bypass 3 dBs:
https://stackoverflow.com/questions/28766692/intersection-of-two-graphs-in-python-find-the-x-value
First it calculates f - g and the corresponding signs using np.sign. Applying 
np.diff reveals all the positions, where the sign changes.
Using np.argwhere gives us the exact indices.
'''
idx = np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref)))
print('frequencia de corte:', idx[1]/10)
plt.plot(freq[idx[1]], TF_mag_out[idx[1]], 'ko')
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


