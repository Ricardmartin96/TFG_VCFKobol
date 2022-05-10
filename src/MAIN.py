import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Funcion_Transfer import transer_function
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

data_dir = Path("./AUDIOS_TFG/IRs_separadas/Preguntas_2,3i4/")
wav_files = list(data_dir.rglob("*.wav"))

# definimos algunos parametros globales
sr = 48000

IR_input = None
IR_output_freq = None
IR_output_res = None
IR_ref = None
reference_file = None
output_file_freq = None
output_file_res = None

IR_output_freq_list = []
IR_output_res_list = []
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

TF_mag_out_freq, TF_mag_ref, reg_ref, reg_out = \
    transer_function(IR_input,IR_output_freq_list, IR_ref)
'''
print('out: ', reg_out)
print('ref: ', reg_ref)
TF_mag_out_freq_def = list(TF_mag_out_freq[0][0][50:32000])
TF_mag_ref = TF_mag_ref[50:32000]
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

#print(TF_mag_out_freq[21][1])# 1a pos: sortida, 2a pos: magnitut o fase
fcorte, pendiente = frequency(sr, TF_mag_out_freq, TF_mag_ref,
                              IR_output_freq_list, output_file_freq,
                              reference_file, reg_ref, reg_out)

f1, f2, fcentral, fres, peak, Q, gain = resonance(sr, TF_mag_out_res,
                                                  TF_mag_ref,
                                                  IR_output_res_list,
                                                  output_file_res,
                                                  reference_file,
                                                  reg_ref, reg_out)

'''
output_file_freq.stem agafa el nom de l'últim arxiu que te _0R_. Per guardar 
cada fig amb el seu nom corresponent, caldria fer totes les crides a funcions 
del main dintre del for de wav_list. Pero aixo no es posible perque per cada 
iteracio nomes hi ha un arxiu, o input, o output o referencia. Lu mateix pasa 
amb output_file_res. I passa amb el savefig i al guardar resultats en un .json
COM HO FAIG???
'''