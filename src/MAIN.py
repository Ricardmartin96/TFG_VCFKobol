import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Funcion_Transfer import transer_function
import json
from pathlib import Path

'''
If you’ve never used this module before or just aren’t sure which 
class is right for your task, Path is most likely what you need. 
It instantiates a concrete path for the platform the code is 
running on
'''
data_dir = Path("./AUDIOS_TFG/IRs_separadas/Pregunta_1/")
#print(list(data_dir.glob('**/*.py'))) # show .py files
#print(data_dir.parts) # separa cada part del directori
#print(data_dir.parents[0]) # show AUDIOS_TFG/IRs_separated
#print(data_dir.parents[1]) # show AUDIOS_TFG
#print(data_dir.stem) # show filename without .wav (PER LES FIG I JSON)
# si el directori es la carpeta, stem dona el nom d'aquesta carpeta
# , no dels seus arxius
#print(Path.cwd()) # show current directory
#print(data_dir.exists())

wav_files = list(data_dir.rglob("*.wav")) # store .wav files
for child in wav_files: #data_dir.iterdir():
    if "Loopback" in child.stem:
        input_file = child
        print('IR_input', input_file)
    elif "Bypass" in child.stem:
        reference_file = child
        print('IR_ref', reference_file)
    else:
        output_file = child
        print('IR_output', output_file)

data_dir.mkdir(exist_ok=True, parent=True)
exit()
'''
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