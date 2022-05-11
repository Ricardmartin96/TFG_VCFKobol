import essentia.standard as es
import numpy as np

def transer_function (IR_input, IR_output, IR_ref):

    IR_output_fft=[]
    trans_func_out=[]
    TF_mag_out=[]

    c2p = es.CartesianToPolar()
    der = es.Derivative()
    mean = es.Mean()

    # Iteramos sobre las salidas
    for i in range (0, len(IR_output)):

        # Alineamos las IRs
        pos_max_in = np.argmax(abs(IR_input))
        pos_max_out = np.argmax(abs(IR_output[i]))
        pos_max_ref = np.argmax(abs(IR_ref))

        if pos_max_out > pos_max_in:
            dif1 = pos_max_out - pos_max_in
            IR_output[i] = IR_output[i][dif1:len(IR_output[i])]
        else:
            dif1 = pos_max_in - pos_max_out
            IR_input = IR_input[dif1:len(IR_input)]

        if pos_max_ref > np.argmax(abs(IR_output[i])):
            dif = pos_max_ref - np.argmax(abs(IR_output[i]))
            IR_ref = IR_ref[dif:len(IR_ref)]
        else:
            dif = np.argmax(abs(IR_output[i])) - pos_max_ref
            IR_output[i] = IR_output[i][dif:len(IR_output[i])]

        # Nos aseguramos que tengan la misma longitud y que esta sea par
        if ((len(IR_input) > len(IR_ref)) and (len(IR_ref) > len(IR_output[i])))\
                or ((len(IR_ref) > len(IR_input))
                    and (len(IR_input) > len(IR_output[i]))):
            s = len(IR_output[i])
        elif ((len(IR_ref) > len(IR_output[i]))
              and (len(IR_output[i]) > len(IR_input))) \
                or ((len(IR_output[i]) > len(IR_ref))
                    and (len(IR_ref) > len(IR_input))):
            s = len(IR_input)
        elif (len(IR_input)==len(IR_ref))and(len(IR_input)<len(IR_output[i])):
            s = len(IR_input)
        elif (len(IR_input)==len(IR_ref))and(len(IR_input)>len(IR_output[i])):
            s = len(IR_output[i])
        else:
            s = len(IR_ref)
        if s % 2 != 0:
            s = s - 1

        IR_input = IR_input[0:s]
        IR_output[i] = IR_output[i][0:s]
        IR_ref = IR_ref[0:s]

        # Si es 0, lo ponemos a un valor muy proximo a 0
        IR_input[IR_input == 0] = np.finfo(float).eps
        IR_output[i][IR_output[i] == 0] = np.finfo(float).eps
        IR_ref[IR_ref == 0] = np.finfo(float).eps

        # Calculamos fft y funcion de transferencia(TF) de salida y bypass
        spec = es.FFT(size=s)

        IR_input_fft = spec(IR_input)
        IR_output_fft.append(spec(IR_output[i]))
        IR_ref_fft = spec(IR_ref)

        trans_func_out.append(IR_output_fft[i] / IR_input_fft)

        TF_mag_out.append(c2p(trans_func_out[i])) # TF de la salida
        # devuelve una tupla (1a pos: salida, 2a pos: magnitud o fase)

        trans_func_ref = IR_ref_fft / IR_input_fft
        TF_mag_ref, TF_ang_ref = c2p(trans_func_ref)  # TF del bypass

    # Calculamos el nivel de la region plana de cada TF
    '''
    for i in range(0,len(TF_mag_ref)-1):
        #TF_mag_out_def = list(TF_mag_out[i][0])
        pos_der = np.argwhere(der(TF_mag_ref)<0.5)
        reg=[]
        for i in range(0,len(pos_der)-1):
            if pos_der[i]==pos_der[i+1]:
                reg.append(TF_mag_ref[pos_der[i]])
    op2:
    reg_ref = np.argwhere(np.diff(TF_mag_ref)<0.5)
    reg_ref = mean(TF_mag_ref[reg_ref])
    '''
    TF_mag_ref_der = der(TF_mag_ref)
    TF_mag_out_der = der(TF_mag_out[i][0])
    flat_ref = []
    flat_out = []

    for j in range(0, len(TF_mag_ref_der) - 1):
        if (TF_mag_ref_der[j] < 0.5)and((TF_mag_ref_der[j+1]-TF_mag_ref_der[j])
                                        <0.25):
            flat_ref.append(TF_mag_ref[j])
    reg_ref = mean(np.array(flat_ref))

    for j in range(0, len(TF_mag_out_der) - 1):
        if (TF_mag_out_der[j] < 0.5)and((TF_mag_out_der[j+1]-TF_mag_out_der[j])
                                        <0.25):
            flat_out.append(TF_mag_out[i][0][j])
    reg_out = mean(np.array(flat_out))

    return TF_mag_out, TF_mag_ref, reg_ref, reg_out