import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np


# definimos algunos parametros globales
sr = 48000

# Cargamos los audios de entrada y salida
IR_input = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
                'IR_Loopback_sweepvar_ampmax.wav',
       sampleRate=sr)()
IR_output = es.MonoLoader(
       filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
                'IR_16F_0Res_sweepvar_ampmax.wav',
       sampleRate=sr)()

# Ploteamos las IR
# fig, ax = plt.subplots(nrows=2, ncols=1)
# ax[0].plot(IR_input, color='b')
# ax[0].set_title("Input IR")
# ax[1].plot(IR_output, color='r')
# ax[1].set_title("Output IR")
# plt.tight_layout()
# plt.show()

IR_input=IR_input[0:959930]
IR_output=IR_output[0:959930]

print(f"duration: {959930/sr}[s]")
print(len(IR_input))
print(len(IR_output))

print(np.argmax(abs(IR_input)))
print(np.argmax(abs(IR_output)))

#IR_input[IR_input == 0] = np.finfo(float).eps # 0 = num molt petit
#IR_output[IR_output == 0] = np.finfo(float).eps

spec = es.FFT(size=len(IR_input))
c2p = es.CartesianToPolar()

IR_input_fft = spec(IR_input)
IR_output_fft = spec(IR_output)
FFT_TF = IR_output_fft/IR_input_fft
impRes_mag, impRes_ang = c2p(FFT_TF)

N = len(impRes_mag)
n = np.arange(N)
T = N/sr
freq = n/T

impRes_mag = 20*np.log10(impRes_mag)
TF_min = np.min(impRes_mag)
TF_max = np.max(impRes_mag)

plt.subplot(2,1,1)
plt.semilogx(freq, impRes_mag)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 32000)
#plt.ylim(TF_min,TF_max+30)
plt.title('Magnitud_FFT_TF_IR_CV_res_10V_sweepvar')

plt.subplot(2,1,2)
plt.semilogx(freq, impRes_ang)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude')
plt.xlim(10, 32000)
plt.ylim(-np.pi, np.pi)
plt.title('Phase_FFT_TF_IR_CV_res_10V_sweepvar')
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
#plt.ylim(TF_min, TF_max)
plt.title('IR_output_fft')
plt.tight_layout()
plt.show()



