import numpy as np
import matplotlib.pyplot as plt
import essentia.standard as es
import scipy.optimize
from Transfer_Function import transfer_function
from sklearn.metrics import mean_squared_error
import json

sr = 48000
mean = es.Mean()

# FUNCIONES

# Definimos la ecuacion de la curva logaritmica
def logFunc(x, a, b):
    return a + b*np.log10(x)

# Definimos la ecuacion de la curva lineal
def linFunc(x, a, b):
    return a*x + b

# Definimos la ecuacion de la curva exponencial
def expFunc(x, a, t, b):
    return a * np.exp(-t * x) + b

# MAIN
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs_separadas/Preguntas_2,3i4/IR_4096F_0R_sweepstat.wav',
                       sampleRate=sr)
IR_output = loader()
loader = es.MonoLoader(audioStream=0, downmix="mix", filename='./AUDIOS_TFG' 
                '/IRs_separadas/Preguntas_2,3i4/IR_Loopback_sweepstat.wav',
                       sampleRate=sr)
IR_input = loader()

# Calculamos la TF, sin recortar, y restamos nivel para que este a 0 dB
TF_mag_out, TF_ang_out = transfer_function (IR_input, IR_output)
TF_mag_out = TF_mag_out - mean(TF_mag_out[40:90])

# Calculamos el vector del eje x y nos aseguramos que no contiene zeros
N = len(TF_mag_out)
n = np.arange(N)
T = N / sr
freq = n / T
freq[freq == 0] = np.finfo(float).eps

# Obtenemos los coeficientes para la curva logaritmica
log_coef, _ = scipy.optimize.curve_fit(logFunc, freq, TF_mag_out)
a, b = log_coef

# Ajustamos la curva LOGARITMICA
plt.subplot(3,1,1)
plt.plot(freq, TF_mag_out, color='r')
plt.plot(freq, logFunc(freq, a, b), color='b')
plt.title('Fitted Logarithmic Curve')
plt.xlim(10,22000)
plt.ylim(-75,75)
mse_log = mean_squared_error(TF_mag_out, logFunc(freq, a, b))

# Obtenemos los coeficientes para la curva lineal
lin_coef, _ = scipy.optimize.curve_fit(linFunc, freq, TF_mag_out)
a, b = lin_coef

# # Ajustamos la curva LINEAL
plt.subplot(3,1,2)
plt.plot(freq, TF_mag_out, color='r')
plt.plot(freq, linFunc(freq, a, b), color='b')
plt.title('Fitted Lineal Curve')
plt.xlim(10,22000)
plt.ylim(-75,75)
mse_lin = mean_squared_error(TF_mag_out, linFunc(freq, a, b))

# Obtenemos los coeficientes para la curva exponencial
exp_coef, _ = scipy.optimize.curve_fit(expFunc, freq, TF_mag_out)
a, t, b = exp_coef

# Ajustamos la curva EXPONENCIAL
plt.subplot(3,1,3)
plt.plot(freq, TF_mag_out, color='r')
plt.plot(freq, expFunc(freq, a, t, b), color='b')
plt.title("Fitted Exponential Curve")
plt.xlim(10,22000)
plt.ylim(-75,75)
mse_exp = mean_squared_error(TF_mag_out, expFunc(freq, a, t, b))

# Ajustamos los plots y guardamos los resultados en .png y en .json
plt.tight_layout()
plt.savefig("Filter_Response" + '_4096F_0R_sweepstat' + ".png".format())

dict = {
        "Resultados: ": {
            "MSE_log": str(mse_log),
            "MSE_lin": str(mse_lin),
            "MSE_exp": str(mse_exp),
        }
    }

file = open("Results" + '_4096F_0R_sweepstat' + ".json".format(),"w")
json.dump(dict, file, indent=6)
file.close()