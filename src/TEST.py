import essentia.standard as es
import matplotlib.pyplot as plt
import numpy as np
from Transfer_Function import transfer_function
from Flat_Region import flat_reg

sr = 48000
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs_separadas/Preguntas_2,3i4/IR_256F_2R_sweepstat.wav', sampleRate=48000)
IR_output = loader()

loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs_separadas/Preguntas_2,3i4/IR_Loopback_sweepstat.wav', sampleRate=48000)
IR_input = loader()


TF_mag, TF_ang = transfer_function (IR_input, IR_output)

N = len(TF_mag)
n = np.arange(N)
T = N / sr
freq = n / T
plt.semilogx(freq, TF_mag)
plt.xlim(40, 32000)
plt.show()
