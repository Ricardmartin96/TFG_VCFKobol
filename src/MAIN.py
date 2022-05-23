import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Transfer_Function import transfer_function
from pathlib import Path

# definimos un parametro global y una funcion de essentia
sr = 48000
mean = es.Mean()

# Definimos un directorio y la lista de arxivos que contiene
data_dir = Path("./AUDIOS_TFG/IRs_separadas/Pregunta_1/Ampmin/")
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
                                           'Pregunta_1/Ampmin/' +
                                           str(input_file.name),
                                 sampleRate=sr)()
    elif "Bypass" in child.stem:
        reference_file = child
        IR_ref = es.MonoLoader(filename= './AUDIOS_TFG/IRs_separadas/'
                                           'Pregunta_1/Ampmin/' +
                                         (reference_file.name),
                               sampleRate=sr)()
    if "_0R_" in child.stem:
        output_file_freq = child
        IR_output_freq = es.MonoLoader(filename= './AUDIOS_TFG/IRs_separadas/'
                                           'Pregunta_1/Ampmin/' +
                                                 str(output_file_freq.name),
                                       sampleRate=sr)()
        output_file_freq_names.append(output_file_freq.stem)
        IR_output_freq_list.append(IR_output_freq)
    else:
        output_file_res = child
        IR_output_res = es.MonoLoader(filename= './AUDIOS_TFG/IRs_separadas/'
                                           'Pregunta_1/Ampmin/' +
                                                str(output_file_res.name),
                                      sampleRate=sr)()
        output_file_res_names.append(output_file_res.stem)
        IR_output_res_list.append(IR_output_res)

# CALCULAR TF DEL BYPASS
TF_mag_ref, TF_ang_ref = transfer_function(IR_input, IR_ref)

# Reducimos el nivel de la region plana para compensar la ganancia extra
TF_mag_ref = TF_mag_ref - mean(TF_mag_ref[500:2000])

# CALCULAR TF DE SALIDAS CON RES = 0 y PARAMETROS DE FRECUENCIA
for i in range(0,len(IR_output_freq_list)-1):
    TF_mag_out_freq, TF_ang_out_freq = transfer_function(IR_input,
                                                         IR_output_freq_list[i])

    # Reducimos el nivel de la region plana para compensar la ganancia extra
    TF_mag_out_freq = TF_mag_out_freq - mean(TF_mag_out_freq[40:90])

    fcorte, pendiente = frequency(sr, TF_mag_out_freq, TF_mag_ref,
                                  output_file_freq_names[i],
                                  reference_file.name)


# CALCULAR TF DE SALIDAS CON RES != 0 Y PARAMETROS DE RESONANCIA
for i in range(0,len(IR_output_res_list)-1):
    TF_mag_out_res, TF_ang_out_res = transfer_function(
        IR_input, IR_output_res_list[i])

    TF_mag_out_res = TF_mag_out_res - mean(TF_mag_out_res[40:90])

    f1, f2, fcentral, fres, peak, Q = resonance(sr, TF_mag_out_res,
                                                      TF_mag_ref,
                                                      output_file_res_names[i],
                                                      reference_file.name)