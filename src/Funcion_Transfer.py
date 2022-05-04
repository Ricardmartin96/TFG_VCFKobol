import essentia.standard as es
import numpy as np

def transer_function (IR_input, IR_output, IR_ref):

    # Cogemos la posicion del max de las IR (cogiendo solo la parte positiva)
    pos_max_in = np.argmax(abs(IR_input))
    pos_max_out = np.argmax(abs(IR_output))
    pos_max_ref = np.argmax(abs(IR_ref))

    # Recortamos los 3 señales de manera que los picos esten alineados
    if pos_max_out > pos_max_in:
        dif1 = pos_max_out - pos_max_in
        IR_output = IR_output[dif1:len(IR_output)]
    else:
        dif1 = pos_max_in - pos_max_out
        IR_input = IR_input[dif1:len(IR_input)]

    if pos_max_ref > np.argmax(abs(IR_output)):
        dif = pos_max_ref - np.argmax(abs(IR_output))
        IR_ref = IR_ref[dif:len(IR_ref)]
    else:
        dif = np.argmax(abs(IR_output)) - pos_max_ref
        IR_output = IR_output[dif:len(IR_output)]

    # Para que input i output tengan el mismo tamaño y sean pares (para la FFT)
    if ((len(IR_input) > len(IR_ref)) and (len(IR_ref) > len(IR_output))) or (
            (len(IR_ref) > len(IR_input)) and (len(IR_input) > len(IR_output))):
        s = len(IR_output)
    elif ((len(IR_ref) > len(IR_output)) and (
            len(IR_output) > len(IR_input))) or (
            (len(IR_output) > len(IR_ref)) and (len(IR_ref) > len(IR_input))):
        s = len(IR_input)
    else:
        s = len(IR_ref)
    if s % 2 != 0:
        s = s - 1

    IR_input = IR_input[0:s]
    IR_output = IR_output[0:s]
    IR_ref = IR_ref[0:s]

    # Comprovamos que las IR están alienadas y tienen el mismo tamaño
    assert (len(IR_input) == len(IR_output))
    assert (len(IR_input) == len(IR_ref))
    assert (np.argmax(abs(IR_input)) == np.argmax(abs(IR_output)))
    assert (np.argmax(abs(IR_input)) == np.argmax(abs(IR_ref)))

    # Si es 0, lo ponemos a un valor muy pequeño, para evitar inf i nan en la TF
    IR_input[IR_input == 0] = np.finfo(float).eps  # 0 = num molt petit
    IR_output[IR_output == 0] = np.finfo(float).eps
    IR_ref[IR_ref == 0] = np.finfo(float).eps

    # Calculamos fft de in, out y ref y calculamos la funcion de transferencia(TF)
    spec = es.FFT(size=s)
    c2p = es.CartesianToPolar()

    IR_input_fft = spec(IR_input)
    IR_output_fft = spec(IR_output)
    IR_ref_fft = spec(IR_ref)

    trans_func_out = IR_output_fft / IR_input_fft
    TF_mag_out, TF_ang_out = c2p(trans_func_out)  # TF de la salida
    trans_func_ref = IR_ref_fft / IR_input_fft
    TF_mag_ref, TF_ang_ref = c2p(trans_func_ref)  # TF del bypass

    return TF_mag_out, TF_mag_ref