import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfreqz
import soundfile as sf
from scipy.signal import sosfilt

# Add 3rd filter for tweeter/mids
# Upgrade to Linkwitz-Riley filters
# Add frequency response plot of real audio before and after

# - Frequency Response Graph


f = np.linspace(20, 20000, 1000) #Frequency axis - 20Hz to 20kHz
fs = 48000 #Sampling rate

#Crossover frequency 
fc = 90

#Filter Design - x order butterworth
def butterworth_crossover(fc, order, fs):
    Nyquist = fs/2
    Wn = fc / Nyquist #Normalised cutoff frequency
    lp = butter(order, Wn, btype ='low', output ='sos')
    hp = butter(order, Wn, btype='high', output='sos')
    return lp, hp

#Filter Design - x order Linkwitz-Riley
def lr_crossover(fc, order, fs):
    lp_sos, hp_sos = butterworth_crossover(fc, order, fs)
    lp = np.vstack([lp_sos, lp_sos]) #np.vstack function used to apply the butterworth filter twice
    hp = np.vstack([hp_sos, hp_sos]) #this in turn creates a functional LR filter for HP and LP
    return lp, hp

#Choice of filter and order for user
def terminal_filterchoice():

    print('Choose filter types:')
    print('(1) Butterworth')
    print('(2) Linkwitz-Riley')
    filter_choice = input()

    print("Choose filter order: ")
    if filter_choice == '1':
        print ("1, 2, 3, 4 ,5, 6, 7, 8")
        order_choice = int(input())
        lp, hp = butterworth_crossover(fc, order_choice, fs) 
    elif filter_choice == '2':
        print("2, 4, 6, 8")
        order_choice = int(input())
        lp, hp = lr_crossover(fc, order_choice, fs)
    return lp, hp

lp_sos, hp_sos = terminal_filterchoice()

#Get frequency response
#h_hp , h_lp = butterworth_crossover(fc, 4, fs)

w, h_lp = sosfreqz(lp_sos, worN=1000, fs=fs)
w, h_hp = sosfreqz(hp_sos, worN=1000, fs=fs)

#Convert to dB
lp_db = 20 * np.log10(np.abs(h_lp))
hp_db = 20 * np.log10(np.abs(h_hp))

plt.figure(figsize=(10,6))
plt.plot(w, lp_db, label='Subwoofer (low-pass)')
plt.plot(w, hp_db, label='Tops (high-pass)')
plt.xscale('log')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.title('Crossover Filter Response')
plt.grid(True, which='both')
plt.ylim(-60, 5)
plt.xlim(20, 20000)
plt.axvline(x=fc, color='grey', linestyle='--', label=f'Crossover: {fc}Hz')
plt.axhline(y=-6, color='red', linestyle=':', label='-6dB reference')
plt.legend()

combined = 20 * np.log10(np.abs(np.abs(h_lp) + np.abs(h_hp)))
plt.plot(w, combined, label='Combined', linestyle='--', color='green')

plt.show()

# - Audio File Filter Processing
filename = 'jungler.wav'
def audio_process(filename):
    audio, file_sr = sf.read('jungler.wav') # Load audio file
    if audio.ndim == 2:
        audio = audio[:, 0] # Turn mono (duplicate left ear)    
    if file_sr != fs: # Resample warning
        print(f"Warning: file sample rate ({file_sr}Hz) doesn't match fs ({fs}Hz)")
    return audio

# Apply filters to audio
sub_out = sosfilt(lp_sos, audio)
tops_out = sosfilt(hp_sos, audio)

# Save outputs

sf.write('sub_out.wav', sub_out, file_sr)
sf.write('tops_out.wav', tops_out, file_sr)


print("Done - sub_out.wav and tops_out.wav saved")