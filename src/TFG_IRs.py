import essentia.standard as es
import matplotlib.pyplot as plt
# SCRIPT PARA SEPARAR LAS IRs DE LOS ARCHIVOS DE SALIDA

# Cargamos el audio necesario
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs/Preguntes_2,3i4/IR_allF_0R_sweepstat.wav', sampleRate=48000)
IR_audio = loader()
'''
plt.plot(IR_audio)
plt.show()
exit()
'''
# Detección de picos
peaks = es.PeakDetection(maxPeaks=11, minPeakDistance=0.064,
                         threshold=0.0002)
peaks_pos, peaks_amp = peaks(IR_audio)
# pasamos a muestras (PeakDetection devuelve posiciones de 0 a 1)
peaks_pos = peaks_pos*len(IR_audio)
print(peaks_pos)
# Definimos T como el intervalo entre dos IR (dos picos)
T = peaks_pos[2] - peaks_pos[1]

# Cogemos solo la IR que nos interesa
IR_sep = IR_audio[int(peaks_pos[10] - (T/2)): int(peaks_pos[10] + (T/2))]

plt.plot(IR_sep)
plt.show()

file = es.MonoWriter(filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/'
                              'IR_0R_16F_sweepstat.wav', format='wav',
                     sampleRate=48000)
file(IR_sep)

