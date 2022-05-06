import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Funcion_Transfer import transer_function
import json
from pathlib import Path

data_dir = Path("./AUDIOS_TFG/IRs_separadas/Pregunta_1/")
wav_files = list(data_dir.rglob("*.wav"))

for child in wav_files:
    if "Loopback" in child.stem:
        input_file = child
    elif "Bypass" in child.stem:
        reference_file = child
    elif "0Res" in child.stem:
        output_file_freq = child
    else:
        output_file_res = child

    # definimos algunos parametros globales
    sr = 48000

    # Cargamos los audios de entrada y salida
    IR_input = es.MonoLoader(
        filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'+input_file.name,
        sampleRate=sr)()
    IR_output_freq = es.MonoLoader(
        filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'+output_file_freq.name,
        sampleRate=sr)()
    IR_output_res = es.MonoLoader(
        filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'+output_file_res.name,
        sampleRate=sr)()
    IR_ref = es.MonoLoader(
        filename='./AUDIOS_TFG/IRs_separadas/Pregunta_1/'+reference_file.name,
        sampleRate=sr)()

    TF_mag_out_freq, TF_mag_ref, reg_freq = transer_function(IR_input,
                                                             IR_output_freq,
                                                             IR_ref)
    TF_mag_out_res, TF_mag_ref, reg_res = transer_function(IR_input,
                                                           IR_output_res,
                                                           IR_ref)

    fcorte, pendiente = frequency(sr, TF_mag_out_freq, TF_mag_ref,
                                  IR_output_freq, IR_ref)
    f1, f2, fcentral, fres, peak, Q, gain = resonance(sr, TF_mag_out_res,
                                                      TF_mag_ref, IR_output_res,
                                                      IR_ref)

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
    freq_file = open("Results_"+IR_output_freq.stem+".json", "w")
    json.dump(dict1, freq_file, indent=6)
    freq_file.close()

    res_file = open("Results_"+IR_output_res.stem+".json", "w")
    json.dump(dict2, res_file, indent=6)
    res_file.close()
