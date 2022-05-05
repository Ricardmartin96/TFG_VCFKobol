import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Funcion_Transfer import transer_function
import json
from pathlib import Path

# p = Path("./") #AUDIOS_TFG/IRs_separated/Pregunta_1")
p = Path('/etc')
q = p / 'init.d' / 'reboot'

q.is_dir()
print(q)
exit()
'''
data_dir = "whatever/1/2"
data_dir = Path("whatever/1/2")
data_dir.parent
parent.parent
data_dir.exists()
data_dir.mkdir(exist_ok=True, parent=True)
data_dir.rglob()
data_dir.rglob("*.wav")
input_dir = Path("./AUDIOS_TFG/IRs_..../IR_Loopbak_sweep_....wav")

wav_list = data_dir.rglob("*.wav")
for wav_path in wav_list:
if "loopback" in wav_path.stem:
loopback_file = wav_path
RSF KOBOL'S VCF PROJECT

# definimos algunos parametros globales
sr = 48000

# Cargamos los audios de entrada y salida
IR_input = es.MonoLoader(
    filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
             'IR_Loopback_sweepvar_ampmax.wav',
    sampleRate=sr)()
IR_output_freq = es.MonoLoader(
    filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
             'IR_64F_0Res_sweepvar_ampmax.wav',
    sampleRate=sr)()

IR_output_res = es.MonoLoader(
    filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
             'IR_64F_5Res_sweepvar_ampmax.wav',
    sampleRate=sr)()

IR_ref = es.MonoLoader(
    filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'
             'IR_Bypass_sweepvar_ampmax.wav',
    sampleRate=sr)()

TF_mag_out_freq, TF_mag_ref, reg_freq = transer_function(IR_input, IR_output_freq, IR_ref)
TF_mag_out_res, TF_mag_ref, reg_res = transer_function(IR_input, IR_output_res, IR_ref)

fcorte, pendiente = frequency(sr, TF_mag_out_freq, TF_mag_ref, IR_output_freq, IR_ref)
f1, f2, fcentral, fres, peak, Q, gain = resonance(sr, TF_mag_out_res, TF_mag_ref, IR_output_res, IR_ref)

# python object(dictionary) to be dumped
dict1 = {
    "emp1": {
        "Frecuencia de corte": str(fcorte),
        "Pendiente": str(pendiente),
    },
}

dict2 = {
    "emp2": {
        "F1": str(f1),
        "F2": str(f2),
        "Frecuencia central": str(fcentral),
        "Frecuencia de resonancia": "40000",
        "Pico": str(peak),
        "Factor Q": str(Q),
        "Ganancia": str(gain),
    },
}

# the json file where the output must be stored
freq_file = open("Results_"+str(IR_output_freq)+".json", "w")
json.dump(dict1, freq_file, indent=6)
freq_file.close()

res_file = open("Results_"+str(IR_output_res)+".json", "w")
json.dump(dict2, res_file, indent=6)
res_file.close()
'''