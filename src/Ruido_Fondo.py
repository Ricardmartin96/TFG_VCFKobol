import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np

# Definimos un parametro global
sr = 48000

# Importamos audios
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/tone_10k.wav', sampleRate=sr)
tone = loader()
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/Bypass_tone10k.wav', sampleRate=sr)
bypass = loader()

# Nos aseguramos que ambos audios tengan la misma longitud y esta sea par
if len(tone)>len(bypass):
    s = len(bypass)
else:
    s = len(tone)
if s%2 != 0:
    s = s-1
tone = tone[0:s]
bypass = bypass[0:s]

# Calculamos la FFT
spec = es.FFT(size=s)
c2p = es.CartesianToPolar()

tone_fft = spec(tone)
tone_mag, tone_ang = c2p(tone_fft)
bypass_fft = spec(bypass)
bypass_mag, bypass_ang = c2p(bypass_fft)

# Calculamos el ruido de fondo
back_noise = 20*np.log10(tone_mag/bypass_mag)

# PLoteamos los resultados
N = len(back_noise)
n = np.arange(N)
T = N/sr
freq = n/T
plt.semilogx(freq,back_noise)
plt.xlim(10,32000)
plt.ylim(-20,70)
plt.show()