import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np

loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/tone_10k.wav', sampleRate=48000)
tone = loader()


loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/Bypass_tone10k.wav', sampleRate=48000)
bypass = loader()

w = es.Windowing(type = 'hann')
spectrum = es.Spectrum()  # magnitude spectrum
bypass = bypass[0:722000]

tone_fft = spectrum(w(tone))
bypass_fft = spectrum(w(bypass))
noise = bypass_fft - tone_fft

plt.plot(10*np.log(np.abs(noise))) # log to plot in dB's
plt.title('FFT Noise Tone 10kHz')
plt.xlabel('samples') # plot gives half the total samples because of fft
plt.ylabel('dB')
plt.show()

