import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np

sr = 48000
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/tone_100.wav', sampleRate=sr)
tone = loader()

loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/Bypass_tone100.wav', sampleRate=sr)
bypass = loader()

# Nos aseguramos que ambos audios tienen el mismo tamaño y que tienen tamaño par
if len(tone)>len(bypass):
    s = len(bypass)
else:
    s = len(tone)
if s%2 != 0:
    s = s-1
tone = tone[0:s]
bypass = bypass[0:s]

spec = es.FFT(size=s)
c2p = es.CartesianToPolar()

tone_fft = spec(tone)
tone_mag, tone_ang = c2p(tone_fft)
bypass_fft = spec(bypass)
bypass_mag, bypass_ang = c2p(bypass_fft)
back_noise = 20*np.log10(tone_mag/bypass_mag)

N = len(back_noise)
n = np.arange(N)
T = N/sr
freq = n/T

tone_mag = 20*np.log10(tone_mag)
bypass_mag = 20*np.log10(bypass_mag)

plt.subplot(3,1,1)
plt.semilogx(freq, tone_mag)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 22000)
plt.ylim(-20,70)
plt.title('Magnitud_Tone')

plt.subplot(3,1,2)
plt.semilogx(freq, bypass_mag)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 22000)
plt.ylim(-20,70)
plt.title('Magnitud_Bypass')

plt.subplot(3,1,3)
plt.semilogx(freq, back_noise)
plt.xlabel('Freq (Hz)')
plt.ylabel('Amplitude (dB)')
plt.xlim(10, 22000)
plt.ylim(-20,70)
plt.title('Magnitud_Noise')
plt.tight_layout()
plt.show()



