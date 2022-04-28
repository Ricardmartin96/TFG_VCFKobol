import essentia as e
import essentia.standard as es
import numpy as np
import matplotlib.pyplot as plt

sr = 48000
loader = es.MonoLoader(filename='./AUDIOS_TFG/Preg_5i6/Bypass_tone10k.wav',
                       sampleRate=sr)
bypass = loader()

loader = es.MonoLoader(filename='./AUDIOS_TFG/Preg_5i6/Noise.wav',
                       sampleRate=sr)
noise = loader()

rms = es.RMS()

bypass_rms = rms(bypass)
noise_rms = rms(noise)
snr = 20*np.log10(bypass_rms/noise_rms) +15
# sumamos 15 dBs porque el audio está referenciado a -12dB FS rms
# mas los 3dB de diferencia producidos en los tonos por los cables desbalanceados

bypass_peak = np.max(bypass)
dr = 20*np.log10(bypass_peak/noise_rms)+15 # dynamic range

print('RMS_tone (dB): ', 20*np.log10(bypass_rms))
print('RMS_noise (dB): ', 20*np.log10(noise_rms))
print('SNR (dB): ', snr)
print('peak (dB): ', 20*np.log10(bypass_peak))
print('Dynamic Range (dB): ', dr)

