import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Transfer_Function import transfer_function
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# definimos un parametro global y una funcion de essentia
sr = 48000
mean = es.Mean()

# Definimos un directorio y la lista de arxivos que contiene
data_dir = Path("./AUDIOS_TFG/IRs_separadas/Preguntas_2,3y4/")
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
output_file_freq_names = []
output_file_res_names = []

# Iteramos sobre los archivos del directorio y los clasificamos
for child in wav_files:
    if "Loopback" in child.stem:
        input_file = child
        IR_input = es.MonoLoader(filename= './AUDIOS_TFG/IRs_separadas/'
                                           'Preguntas_2,3y4/' +
                                           str(input_file.name),
                                 sampleRate=sr)()
    elif "Bypass" in child.stem:
        reference_file = child
        IR_ref = es.MonoLoader(filename= './AUDIOS_TFG/IRs_separadas/'
                                           'Preguntas_2,3y4/' +
                                         (reference_file.name),
                               sampleRate=sr)()
    if "_0R_" in child.stem:
        output_file_freq = child
        IR_output_freq = es.MonoLoader(filename= './AUDIOS_TFG/IRs_separadas/'
                                           'Preguntas_2,3y4/' +
                                                 str(output_file_freq.name),
                                       sampleRate=sr)()
        output_file_freq_names.append(output_file_freq.stem)
        IR_output_freq_list.append(IR_output_freq)
    else:
        output_file_res = child
        IR_output_res = es.MonoLoader(filename= './AUDIOS_TFG/IRs_separadas/'
                                           'Preguntas_2,3y4/' +
                                                str(output_file_res.name),
                                      sampleRate=sr)()
        output_file_res_names.append(output_file_res.stem)
        IR_output_res_list.append(IR_output_res)

# CALCULAR TF DEL BYPASS
TF_mag_ref, TF_ang_ref = transfer_function(IR_input, IR_ref)

# Reducimos el nivel de la region plana para compensar la ganancia extra
TF_mag_ref = TF_mag_ref - mean(TF_mag_ref[500:2000])

'''
# CALCULAR TF DE SALIDAS CON RES = 0 y PARAMETROS DE FRECUENCIA
fcorte_lista=[]
for i in range(0,len(IR_output_freq_list)-1):
    TF_mag_out_freq, TF_ang_out_freq = transfer_function(IR_input,
                                                         IR_output_freq_list[i])

    # Reducimos el nivel de la region plana para compensar la ganancia extra
    TF_mag_out_freq = TF_mag_out_freq - mean(TF_mag_out_freq[40:90])

    fcorte, pendiente = frequency(sr, TF_mag_out_freq, TF_mag_ref,
                                  output_file_freq_names[i],
                                  reference_file.name)

    fcorte_lista.append(fcorte)

# PLoteamos todas las frecuencias de corte
fcorte_lista = np.asarray(fcorte_lista)
fcorte_lista = np.sort(fcorte_lista, axis=None)
labels=['16F', '32F', '64F', '128F', '256F', '512F', '1024F', '2048F', '4096F']

for i in range(0,len(fcorte_lista)):
    plt.plot(labels[i],  fcorte_lista[i], 'ko')

plt.plot(labels,  fcorte_lista, color='r')
plt.xlabel('Posiciones del potenciometro de Frecuencia')
plt.ylabel('Frecuencias de corte (Hz)')
plt.savefig("Frecuencias_de_corte_sweepstat" + ".png".format())
'''

# CALCULAR TF DE SALIDAS CON RES != 0 Y PARAMETROS DE RESONANCIA
peak_list=[]
for i in range(0,len(IR_output_res_list)-1):
    TF_mag_out_res, TF_ang_out_res = transfer_function(
        IR_input, IR_output_res_list[i])

    TF_mag_out_res = TF_mag_out_res - mean(TF_mag_out_res[40:90])
    '''
    f1, f2, fcentral, fres, peak, Q = resonance(sr, TF_mag_out_res,
                                                      TF_mag_ref,
                                                      output_file_res_names[i],
                                                      reference_file.name)
    '''
    peak = np.max(TF_mag_out_res)
    peak_list.append(peak)

# Ploteamos todos los picos
peak_list.pop(110)
peak_list = np.asarray(peak_list)
peak_list = np.sort(peak_list, axis=None)
labels = ['1R', '2R', '3R', '4R', '5R', '6R', '7R', '8R', '9R', '10R']
labels = np.repeat(labels,11) # Hay 11 frecuencias de corte

for i in range(0,len(peak_list)-1):
    plt.plot(labels[i],  peak_list[i], 'ko')

plt.plot(labels,  peak_list, color='r')
plt.xlabel('Posiciones del potenciometro de Resonancia')
plt.ylabel('Valores de picos (dB)')
plt.savefig("Resonancias_sweepstat" + ".png".format())