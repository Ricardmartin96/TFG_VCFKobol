import essentia.standard as es
from Transfer_Function import transfer_function
from Frequencia import frequency
from Resonancia import resonance

mean = es.Mean()
sr = 48000

loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs_separadas/Pregunta_9/Variable/Ampmin/IR_CV_res_7V_sweepvar_ampmin.wav', sampleRate=sr)
IR_output = loader()
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs_separadas/Pregunta_1/Ampmin/IR_Bypass_sweepvar_ampmin.wav', sampleRate=sr)
IR_ref = loader()
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs_separadas/Pregunta_1/Ampmin/IR_Loopback_sweepvar_ampmin.wav', sampleRate=sr)
IR_input = loader()

TF_mag_out, TF_ang_out = transfer_function (IR_input, IR_output)
TF_mag_ref, TF_ang_ref = transfer_function (IR_input, IR_ref)

TF_mag_out = TF_mag_out - mean(TF_mag_out[40:90])
TF_mag_ref = TF_mag_ref - mean(TF_mag_ref[500:2000])

#fcorte, pendiente = frequency(sr, TF_mag_out, TF_mag_ref,'IR_CV_freq_7V_sweepvar_ampmin.wav','IR_Bypass_sweepvar_ampmin')
f1, f2, fcentral, fres, peak, Q = resonance(sr, TF_mag_out, TF_mag_ref, 'IR_CV_res_7V_sweepvar_ampmin','IR_Bypass_sweepvar_ampmin')
