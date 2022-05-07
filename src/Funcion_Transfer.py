import essentia.standard as es
import numpy as np

def transer_function (IR_input, IR_output, IR_ref):

    IR_output_fft=[]
    trans_func_out=[]
    TF_mag_out=[]
    TF_ang_out=[]

    c2p = es.CartesianToPolar()

    for i in range (0, len(IR_output)):
        # Cogemos la posicion del max de las IR (cogiendo solo la parte positiva)
        pos_max_in = np.argmax(abs(IR_input))
        pos_max_out = np.argmax(abs(IR_output[i])) # valor absolut i max d'un array
        pos_max_ref = np.argmax(abs(IR_ref))

        # Recortamos los 3 señales de manera que los picos esten alineados
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

        # Para que input i output tengan el mismo tamaño y sean pares (para la FFT)
        if ((len(IR_input) > len(IR_ref)) and (len(IR_ref) > len(IR_output[i]))) or (
                (len(IR_ref) > len(IR_input)) and (len(IR_input) > len(IR_output[i]))):
            s = len(IR_output[i])
        elif ((len(IR_ref) > len(IR_output[i])) and (
                len(IR_output[i]) > len(IR_input))) or (
                (len(IR_output[i]) > len(IR_ref)) and (len(IR_ref) > len(IR_input))):
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

        # Comprovamos que las IR están alienadas y tienen el mismo tamaño
        assert (len(IR_input) == len(IR_output[i]))
        assert (len(IR_input) == len(IR_ref))
        assert (np.argmax(abs(IR_input)) == np.argmax(abs(IR_output[i])))
        assert (np.argmax(abs(IR_input)) == np.argmax(abs(IR_ref)))

        # Si es 0, lo ponemos a un valor muy pequeño, para evitar inf i nan en la TF
        IR_input[IR_input == 0] = np.finfo(float).eps  # 0 = num molt petit
        IR_output[i][IR_output[i] == 0] = np.finfo(float).eps
        IR_ref[IR_ref == 0] = np.finfo(float).eps

        # Calculamos fft de in, out y ref y calculamos la funcion de transferencia(TF)
        spec = es.FFT(size=s)

        IR_input_fft = spec(IR_input)
        IR_output_fft.append(spec(IR_output[i]))
        IR_ref_fft = spec(IR_ref)

        trans_func_out.append(IR_output_fft[i] / IR_input_fft)

        TF_mag_out.append(c2p(trans_func_out[i])) # TF de la salida
        # retorna una tupla: 1a pos: sortida, 2a pos: magnitut o fase

        trans_func_ref = IR_ref_fft / IR_input_fft
        TF_mag_ref, TF_ang_ref = c2p(trans_func_ref)  # TF del bypass

        # Calculamos la región plana de cada TF
        '''
        der = es.Derivative()
        pos_der = np.argwhere(der(TF_mag_out)<0.5)
        reg=0
        for i in range(0,len(pos_der)-1):
            dif = TF_mag_out[pos_der[i]] - TF_mag_out[pos_der[i+1]]
            if dif<1:
                reg = TF_mag_out[pos_der[i]]
        
        reg=[]
        for j in range (0, len(TF_mag_out[i])-1):
            if (TF_mag_out[i]-TF_mag_out[i+1])<0.1:
                reg.append(TF_mag_out[i])
        mean = es.Mean()
        reg = mean(np.array(reg))
    '''
    return TF_mag_out, TF_mag_ref