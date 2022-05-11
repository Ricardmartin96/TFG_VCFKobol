import essentia.standard as es
import numpy as np

# Definimos un parametro global
sr = 48000

# Importamos audios
loader = es.MonoLoader(filename='./AUDIOS_TFG/Preg_5i6/Bypass_tone10k.wav',
                       sampleRate=sr)
bypass = loader()

loader = es.MonoLoader(filename='./AUDIOS_TFG/Preg_5i6/Noise.wav',
                       sampleRate=sr)
noise = loader()

# Calculamos el SNR
rms = es.RMS()

bypass_rms = rms(bypass)
noise_rms = rms(noise)
snr = 20*np.log10(bypass_rms/noise_rms) + 15

# Calculamos el rango dinamico
bypass_peak = np.max(bypass)
dr = 20*np.log10(bypass_peak/noise_rms)+15 # dynamic range

# Mostramos los resultados
print('RMS_tone (dB): ', 20*np.log10(bypass_rms))
print('RMS_noise (dB): ', 20*np.log10(noise_rms))
print('SNR (dB): ', snr)
print('peak (dB): ', 20*np.log10(bypass_peak))
print('Dynamic Range (dB): ', dr)

