import essentia.standard as es
from Resonancia import resonance
from Frequencia import frequency
from Funcion_Transfer import transer_function

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

TF_mag_out_freq, TF_mag_ref = transer_function(IR_input, IR_output_freq, IR_ref)
TF_mag_out_res, TF_mag_ref = transer_function(IR_input, IR_output_res, IR_ref)

fcorte, pendiente = frequency(sr, TF_mag_out_freq, TF_mag_ref, IR_output_freq, IR_ref)
print('fcorte', fcorte)
print('pendiente', pendiente)

f1, f2, fcentral, fres, peak, Q, gain = resonance(sr, TF_mag_out_res, TF_mag_ref, IR_output_res, IR_ref)
print('f1', f1)
print('f2', f2)
print('fcentral', fcentral)
print('fres', fres)
print('peak', peak)
print('Q', Q)
print('gain', gain)