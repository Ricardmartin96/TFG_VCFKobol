import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np

# definimos algunos parametros globales
sr = 48000

# Cargamos los audios de entrada y salida
IR_input = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/'
                'IR_Loopback_sweepstat.wav',
       sampleRate=sr)()
IR_output = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/'
                'IR_128F_6R_sweepstat.wav',
       sampleRate=sr)()

# Ploteamos las IR
'''
fig, ax = plt.subplots(nrows=2, ncols=1)
ax[0].plot(IR_input, color='b')
ax[0].set_title("Input IR")
ax[1].plot(IR_output, color='r')
ax[1].set_title("Output IR")
plt.tight_layout()
print(len(IR_input))
print(len(IR_output))
plt.show()
exit()
'''
# Cogemos la posicion del max de las IR (cogiendo solo la parte positiva)
pos_max_in = np.argmax(abs(IR_input))
pos_max_out = np.argmax(abs(IR_output))

# Recortamos el senyal de manera que el maximo esté en la misma posicion
if pos_max_out>pos_max_in:
    dif = pos_max_out - pos_max_in
    IR_output = IR_output[dif:len(IR_output)]
else:
    dif = pos_max_in - pos_max_out
    IR_input = IR_input[dif:len(IR_input)]

# Para que input i output tengan el mismo tamaño y sean pares (para la FFT)
if len(IR_input)>len(IR_output):
    s = len(IR_output)
else:
    s = len(IR_input)

if s%2 != 0:
    s = s-1
else:
    s=s

IR_input=IR_input[0:s]
IR_output=IR_output[0:s]

print('pos_max_in', np.argmax(abs(IR_input)))
print('pos_max_out', np.argmax(abs(IR_output)))
print('len_in', len(IR_input))
print('len_out', len(IR_output))

IR_input[IR_input == 0] = np.finfo(float).eps # 0 = num molt petit
IR_output[IR_output == 0] = np.finfo(float).eps

spec = es.FFT(size=len(IR_input))
c2p = es.CartesianToPolar()

IR_input_fft = spec(IR_input)
IR_output_fft = spec(IR_output)
trans_func = IR_output_fft/IR_input_fft
TF_mag, TF_ang = c2p(trans_func)

N = len(TF_mag)
n = np.arange(N)
T = N/sr
freq = n/T

TF_mag = 20*np.log10(TF_mag) # Magnitut en dBs
TF_min = np.min(TF_mag)
TF_max = np.max(TF_mag)

plt.subplot(2,1,1)
plt.semilogx(freq, TF_mag)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 32000)
plt.ylim(TF_min,TF_max+30)
plt.title('Magnitud_TF')

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
plt.ylim(-50,30)
plt.title('IR_input_fft')

plt.subplot(2,1,2)
plt.semilogx(freq,20*np.log10(np.abs(IR_output_fft)))
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.xlim(10, 32000)
plt.ylim(-50, 30)
plt.title('IR_output_fft')
plt.tight_layout()
plt.show()



