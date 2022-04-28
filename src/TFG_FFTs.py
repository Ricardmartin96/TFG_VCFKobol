import essentia.standard as es
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import spatial
from scipy.signal import argrelextrema

# definimos algunos parametros globales
sr = 48000

# Cargamos los audios de entrada y salida
IR_input = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
                'IR_Loopback_sweepvar_ampmax.wav',
       sampleRate=sr)()
IR_output = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
                'IR_512F_5Res_sweepvar_ampmax.wav',
       sampleRate=sr)()

IR_ref = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
                'IR_Bypass_sweepvar_ampmax.wav',
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

if pos_max_ref>pos_max_in:
    dif = pos_max_ref - pos_max_in
    IR_ref = IR_ref[dif:len(IR_ref)]
else:
    dif = pos_max_in - pos_max_ref
    IR_input = IR_input[dif:len(IR_input)]

# Para que input i output tengan el mismo tamaño y sean pares (para la FFT)
if ((len(IR_input)>len(IR_ref))and(len(IR_ref)>len(IR_output))) or ((len(IR_ref)>len(IR_input))and(len(IR_input)>len(IR_output))):
    s = len(IR_output)
elif ((len(IR_ref)>len(IR_output))and(len(IR_output)>len(IR_input))) or ((len(IR_output)>len(IR_ref))and(len(IR_ref)>len(IR_input))):
    s = len(IR_input)
else:
    s = len(IR_ref)
if s%2 != 0:
    s = s-1

IR_input = IR_input[0:s]
IR_output = IR_output[0:s]
IR_ref = IR_ref[0:s]
'''
print('len_in', len(IR_input))
print('len_out', len(IR_output))
print('len_ref', len(IR_ref))
print('pic_in',  np.argmax(abs(IR_input)))
print('pic_out',  np.argmax(abs(IR_output)))
print('pic_ref',  np.argmax(abs(IR_ref)))
exit()
'''
# Si es 0, lo ponemos a un valor muy pequeño, para evitar inf i nan en la TF
IR_input[IR_input == 0] = np.finfo(float).eps # 0 = num molt petit
IR_output[IR_output == 0] = np.finfo(float).eps
IR_ref[IR_ref == 0] = np.finfo(float).eps

# Calculamos fft de in, out y ref y calculamos la funcion de transferencia(TF)
spec = es.FFT(size=s)
c2p = es.CartesianToPolar()
IR_input_fft = spec(IR_input)
IR_output_fft = spec(IR_output)
IR_ref_fft = spec(IR_ref)

trans_func_out = IR_output_fft/IR_input_fft
TF_mag_out, TF_ang_out = c2p(trans_func_out) # TF de la salida
trans_func_ref = IR_ref_fft/IR_input_fft
TF_mag_ref, TF_ang_ref = c2p(trans_func_ref) # TF del bypass

N = len(TF_mag_out)
n = np.arange(N)
T = N/sr
freq = n/T

TF_mag_out = 20*np.log10(TF_mag_out)-13 # Magnitut en dBs, restamos para compensar el gain extra

# Estimu el valor de pic i fc de la resonancia
maxs = argrelextrema(TF_mag_out, np.greater)
maxs = list(maxs)
fc = maxs[0][580]
pic = TF_mag_out[fc]+7-3 # resto 3 dBs (f1 i f2 son les f que estan a -3dB del pic)

TF_mag_ref = 20*np.log10(TF_mag_ref)+pic #Aumentamos para calcular la res
#TF_min = np.min(TF_mag_out)
#TF_max = np.max(TF_mag_out)

# PLOT RESULTS
fig, ax = plt.subplots()
plt.semilogx(freq, TF_mag_out, color='r')
plt.semilogx(freq, TF_mag_ref, color='b')
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 32000)
plt.ylim(-30,pic+10)
plt.title('Magnitud_TF')
red_patch = mpatches.Patch(color='red', label='TF_512F_5R_sweepvar_ampmax')
first_Leg = ax.legend(handles=[red_patch], loc='upper left')
ax.add_artist(first_Leg)
black_patch = mpatches.Patch(color='black', label='f1, fc y f2')
second_Leg = ax.legend(handles=[black_patch], loc='lower left')
ax.add_artist(second_Leg)
blue_patch = mpatches.Patch(color='blue', label='TF_Bypass_sweepvar_ampmax')
ax.legend(handles=[blue_patch], loc='lower right')

'''
Encontrar la frecuencia de corte como el punto de interseccion entre output y
bypass, habiendo reducido la magnitud del bypass 3 dBs:
Primero calcula la diferencia de magnitudes y los signos correspondientes 
usando np.sign. Aplicando np.diff conocemos las posiciones donde cambia el signo 
(cosa que ocurre cuando ambas gráficas se cortan).
Usar np.argwhere nos da los índices exactos.
'''
idx= np.argwhere(np.diff(np.sign(TF_mag_out - TF_mag_ref))).flatten()
# La funcion flatten convierte un array en un integer ( de [algo] a algo)
a=50
b=70
# pendent = (TF_mag_out[idx[a]]-TF_mag_out[int(idx[a]*4)]) # pendent
#print('frequencia de corte:', freq[idx[a]])
# print('pendent:', pendent/2, 'dBs/octava') # operem per tenir el pendent/octava

# Calculamos los parámetros de la resonancia: f1, f2, fc, Q
f1 = idx[a]
f2 = idx[b]
#res = TF_mag_out[int(freq[f1]):int(freq[f2])]
fres = np.sqrt(freq[f1]*freq[f2])
Q = fres/(freq[f2]-freq[f1])
gain = (TF_mag_out[int(fres)]+10)-0 # El nivell rms de la sortida es 0

#Printamos los parámetros de la resonancia: f1, f2, fc, Q
print('f1:', freq[f1])
print('f2:', freq[f2])
print('fc:', fc)
print('fres:', fres)
print('Q:', Q )
print('gain (dB)', gain)

plt.plot(freq[f1], TF_mag_out[f1], 'ko')
plt.plot(fc, TF_mag_out[fc]+10, 'ko')
plt.plot(freq[f2], TF_mag_out[f2], 'ko')
plt.show()

'''
#plt.subplot(2,1,2)
plt.semilogx(freq, TF_ang_out)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.xlim(10, 42000)
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


