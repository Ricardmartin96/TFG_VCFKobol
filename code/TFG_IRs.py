import essentia.standard as es
# SCRIPT PARA SEPARAR LAS IRs DE LOS ARCHIVOS DE SALIDA

# Cargamos el audio necesario
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs/Pregunta_1/IR_16F_10Res_sweepvar.wav', sampleRate=48000)
IR_audio = loader()

# Detección de picos
peaks = es.PeakDetection(maxPeaks=3, minPeakDistance=0.14,
                         threshold=0.03)
peaks_pos, peaks_amp = peaks(IR_audio)
# pasamos a muestras (PeakDetection devuelve posiciones de 0 a 1)
peaks_pos = peaks_pos*len(IR_audio)

# Definimos T como el intervalo entre dos IR (dos picos)
T = peaks_pos[2] - peaks_pos[1]

# Cogemos solo la IR que nos interesa
IR_sep = IR_audio[int(peaks_pos[2] - (T/2)): int(peaks_pos[2] + (T/2))]

file = es.MonoWriter(filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
                              'IR_16F_10Res_sweepvar_ampmin.wav', format='wav',
                     sampleRate=48000)
file(IR_sep)

