import essentia.standard as es
import matplotlib.pyplot as plt

# Importamos audio
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG/'
                       'IRs/Preguntas_2,3i4/IR_16F_allR_sweepstat.wav',
                       sampleRate=48000)
IR_audio = loader()

# Detectamos la posicion y amplitud de los picos (IRs)
peaks = es.PeakDetection(maxPeaks=11, minPeakDistance=0.064, threshold=0.0002)
peaks_pos, peaks_amp = peaks(IR_audio)

# Pasamos a muestras
peaks_pos = peaks_pos*len(IR_audio)

# Definimos T como el intervalo entre dos IR
T = peaks_pos[2] - peaks_pos[1]

# Cogemos solo la IR que nos interesa
IR_sep = IR_audio[int(peaks_pos[0] - (T/2)): int(peaks_pos[0] + (T/2))]

# Guardamos el nuevo archivo
file = es.MonoWriter(filename='./AUDIOS_TFG/IRs_separadas/Preguntas_2,3y4/'
                              'IR_16F_0R_sweepstat.wav', format='wav',
                     sampleRate=48000)
file(IR_sep)

