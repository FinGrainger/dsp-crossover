import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfreqz
import soundfile as sf
from scipy.signal import sosfilt
from scipy.signal import welch

# Add 3rd filter for tweeter/mids
# Upgrade to Linkwitz-Riley filters
# Add frequency response plot of real audio before and after

# - Frequency Response Graph

f = np.linspace(20, 20000, 1000) #Frequency axis - 20Hz to 20kHz
fs = 44100 #Sampling rate
fc = 900 #Crossover frequency 

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
def filter_choice():

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

    print("lp, hp, both or none(1,2,3,4)")
    choice_filter = int(input())
    if choice_filter == 1:
        return lp, None
    elif choice_filter == 2:
        return None, hp
    elif choice_filter == 3:
        return lp, hp
    else:
        return None, None
        


def plot_response(lp_sos, hp_sos):
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

filename = 'jungler.wav' #Temp file
def audio_process(filename):
    audio, file_fs = sf.read('jungler.wav') # Load audio file
    if audio.ndim == 2:
        audio = audio[:, 0] # Turn mono (duplicate left ear)    
    if file_fs != fs: # Resample warning
        print(f"Warning: file sample rate ({file_fs}Hz) doesn't match fs ({fs}Hz)")
    return audio, file_fs
audio, file_fs = audio_process(filename)

 # - Plotting audio spectrum, possible use of filters
def plot_spectrum(audio, file_fs,lp_sos=None, hp_sos=None, title='audio spectrum'):

    def Plot_filter_welch(filter):
        filtered_audio = sosfilt(filter, audio) #Applies the filter to the audio
        spectrum_freqs_filtered, spectrum_power_filtered = welch(filtered_audio, fs=file_fs, nperseg=4096) #Runs welch method on filtered audio
        spectrum_mag_filtered = 10 * np.log10(spectrum_power_filtered) #Converting power to dB
        spectrum_mag_filtered = spectrum_mag_filtered - np.max(spectrum_mag_filtered) #Normalising spectrum, loudest point is 0dB
        plt.plot(spectrum_freqs_filtered, spectrum_mag_filtered, label='LP Filtered Audio', color='yellow')

    plt.figure(figsize=(10,6))
    
    print('Do you want to use Welch method? (y/n)')
    yn = input()
    if yn == 'y':
        
        spectrum_freqs, spectrum_power = welch(audio, fs=file_fs, nperseg=4096) #Welch method returns a smoother curve, overlapping segments of audio
        spectrum_mag = 10 * np.log10(spectrum_power)  
        spectrum_mag = spectrum_mag - np.max(spectrum_mag)  #Normalising the spectrum               
    else:
        spectrum_result = np.fft.rfft(audio) #Fast fourier transform
        spectrum_freqs = np.fft.rfftfreq(len(audio), d=1/file_fs) #Real fast fourier transform for audio
        spectrum_mag = 20 * np.log10(np.abs(spectrum_result)) #Magnitude of the spectrum
        spectrum_mag = spectrum_mag - np.max(spectrum_mag)
    

    if lp_sos is not None: #Checks if none
        w, h_lp = sosfreqz(lp_sos, worN=1000, fs=file_fs) 
        lp_db = 20 * np.log10(abs(h_lp)) #Convert to dB
        plt.plot(w, lp_db, label='Low Pass Filter')#Plotting filters

        Plot_filter_welch(lp_sos)

    if hp_sos is not None:
        w, h_hp = sosfreqz(hp_sos, worN=1000, fs=file_fs)
        hp_db = 20 * np.log10(abs(h_hp))
        plt.plot(w, hp_db, label='High Pass Filter')

        Plot_filter_welch(hp_sos)
        

    plt.xscale('log')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Crossover Filter Response')
    plt.grid(True, which='both')
    plt.ylim(-120, 5)
    plt.xlim(20, 20000)
    plt.axvline(x=fc, color='grey', linestyle='--', label=f'Crossover: {fc}Hz')
    plt.plot(spectrum_freqs, spectrum_mag, label='Audio')
    plt.legend()
    plt.show()


#lp_sos, hp_sos = terminal_filterchoice()
#plot_response(lp_sos, hp_sos)
lp, hp = filter_choice()
audio, file_fs = audio_process(filename)
plot_spectrum(audio, file_fs, lp, hp)

#h_hp , h_lp = butterworth_crossover(fc, 4, fs)

# Apply filters to audio
#sub_out = sosfilt(lp_sos, audio)
#tops_out = sosfilt(hp_sos, audio)

# Save outputs

#sf.write('sub_out.wav', sub_out, file_fs)
#sf.write('tops_out.wav', tops_out, file_fs)


#print("Done - sub_out.wav and tops_out.wav saved")