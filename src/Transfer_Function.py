import essentia.standard as es
import numpy as np

def transfer_function (IR_input, IR_output):

    c2p = es.CartesianToPolar()

    # Alineamos las IRs
    pos_max_in = np.argmax(abs(IR_input))
    pos_max_out = np.argmax(abs(IR_output))

    if pos_max_out > pos_max_in:
        dif1 = pos_max_out - pos_max_in
        IR_output = IR_output[dif1:len(IR_output)]
    else:
        dif1 = pos_max_in - pos_max_out
        IR_input = IR_input[dif1:len(IR_input)]

    # Nos aseguramos que tengan la misma longitud y que esta sea par
    if len(IR_input) < len(IR_output):
        s = len(IR_input)
    else:
        s = len(IR_output)

    if s % 2 != 0:
        s = s - 1

    IR_input = IR_input[0:s]
    IR_output = IR_output[0:s]

    # Si es 0, lo ponemos a un valor muy proximo a 0
    IR_input[IR_input == 0] = np.finfo(float).eps
    IR_output[IR_output == 0] = np.finfo(float).eps

    # Calculamos fft y funcion de transferencia (TF) del output
    spec = es.FFT(size=s)

    IR_input_fft = spec(IR_input)
    IR_output_fft = spec(IR_output)

    trans_func = IR_output_fft / IR_input_fft
    TF_mag, TF_ang = c2p(trans_func)
    TF_mag = 20*np.log10(TF_mag) # Obtenemos la magnitud de la TF

    # Recortamos la TF para tener la region sin ruido
    TF_mag = TF_mag[400:320000]

    return TF_mag, TF_ang



