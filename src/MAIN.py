import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Funcion_Transfer import transer_function
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# definimos un parametro global
sr = 48000

# Definimos un directorio y la lista de arxivos que contiene
data_dir = Path("./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/")
wav_files = list(data_dir.rglob("*.wav"))

# Declaramos ciertas variables para poder reusarlas fuera de los ifs
IR_input = None
IR_output_freq = None
IR_output_res = None
IR_ref = None
reference_file = None
output_file_freq = None
output_file_res = None

IR_output_freq_list = []
IR_output_res_list = []

# Iteramos sobre los archivos del directorio y los clasificamos
for child in wav_files:
    if "Loopback" in child.stem:
        input_file = child
        IR_input = es.MonoLoader(filename='./AUDIOS_TFG/IRs_separadas/'
                                                'Preguntas_2,3i4/' +
                                                str(input_file.name),
                                 sampleRate=sr)()
    elif "Bypass" in child.stem:
        reference_file = child
        IR_ref = es.MonoLoader(filename='./AUDIOS_TFG/IRs_separadas/'
                                                'Preguntas_2,3i4/' +
                                                str(reference_file.name),
                               sampleRate=sr)()
    elif "_0R_" in child.stem:
        output_file_freq = child
        IR_output_freq = es.MonoLoader(filename='./AUDIOS_TFG/IRs_separadas/'
                                                'Preguntas_2,3i4/' +
                                                str(output_file_freq.name),
                                       sampleRate=sr)()
        IR_output_freq_list.append(IR_output_freq)
    else:
        output_file_res = child
        IR_output_res = es.MonoLoader(filename='./AUDIOS_TFG/IRs_separadas/'
                                                'Preguntas_2,3i4/' +
                                                str(output_file_res.name),
                                      sampleRate=sr)()
        IR_output_res_list.append(IR_output_res)

# Calculamos las TF y comprovamos que estan a 0dBs
TF_mag_out_freq, TF_mag_ref, reg_ref, reg_out = \
    transer_function(IR_input,IR_output_freq_list, IR_ref)
'''
print('out: ', reg_out)
print('ref: ', reg_ref)
TF_mag_out_freq_def = list(TF_mag_out_freq[0][0][40:32000])
TF_mag_ref = TF_mag_ref[40:32000]
N = len(TF_mag_ref)
n = np.arange(N)
T = N / sr
freq = n / T
plt.semilogx(freq, TF_mag_ref - reg_ref)
plt.semilogx(freq, np.array(TF_mag_out_freq_def) - reg_out)
plt.xlim(10, 42000)
plt.ylim(-30, 30)
plt.show()
exit()
'''

TF_mag_out_res, TF_mag_ref,  reg_ref, reg_out = \
    transer_function(IR_input, IR_output_res_list, IR_ref)

# Calculamos parametros de frecuencia y resonancia
fcorte, pendiente = frequency(sr, TF_mag_out_freq, TF_mag_ref,
                              IR_output_freq_list, output_file_freq,
                              reference_file, reg_ref, reg_out)

f1, f2, fcentral, fres, peak, Q, gain = resonance(sr, TF_mag_out_res,
                                                  TF_mag_ref,
                                                  IR_output_res_list,
                                                  output_file_res,
                                                  reference_file,
                                                  reg_ref, reg_out)

