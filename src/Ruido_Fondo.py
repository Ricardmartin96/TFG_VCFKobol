import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np

# Definimos un parametro global
sr = 48000

# Importamos audios
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/tone_100.wav', sampleRate=sr)
tone = loader()
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG'
                      '/Preg_5i6/Bypass_tone100.wav', sampleRate=sr)
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
freq = np.linspace(0, sr/2, len(back_noise))
plt.semilogx(freq,back_noise)
plt.title('Magnitud_Ruido_Fondo_100 Hz')
plt.xlabel('Frecuencia (Hz)')
plt.ylabel('Amplitud (dB)')
plt.xlim(10, 28000)
plt.ylim(-20,70)
plt.show()