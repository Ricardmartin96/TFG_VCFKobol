import essentia as e
import essentia.standard as es

def compute_snr(audio, threshold, sampleRate = 48000,
                 broadbad_correction=False):
    frame_size = 512

    snr = es.SNR(frameSize=frame_size, noiseThreshold=threshold,
                 useBroadbadNoiseCorrection=broadbad_correction)

    snr_spectral_list = []
    for frame in es.FrameGenerator(audio,frameSize=frame_size,
                                   hopSize=frame_size // 2):
        snr_instant, snr_av, snr_spectral = snr(frame)
        snr_spectral_list.append(snr_spectral)

    snr_spectral = e.array(snr_spectral_list).T

    return snr_av, snr_spectral

loader = es.MonoLoader(audioStream=0, downmix="mix",
                       filename='./AUDIOS_TFG/Preg_5i6/Bypass_tone100.wav',
                       sampleRate=48000)
audio = loader()
threshold = -50
snr_average, snr_inst = compute_snr(audio, threshold)

print (snr_average, 'snr average')
print (snr_inst, 'snr in each instant')


