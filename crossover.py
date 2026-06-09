import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfreqz
import soundfile as sf
from scipy.signal import sosfilt
from scipy.signal import welch
import matplotlib.ticker as ticker

# Add 3rd filter for tweeter/mids

def main():
    
    filename = 'jungler.wav' #Temp file
    new_graph = True
    while new_graph is True:

        fs = 44100 #Sampling rate

        print('Choose Crossover Frequency:')
        fc = int(input()) #Crossover frequency 

        print('1 - Process Audio')
        print('2 - Frossover Filter Response')
        choice = input()
        lp, hp = filter_choice(fc, fs)
        if choice == '1':
            plot_graph(fc, lp, hp, filename)
        elif choice == '2':
            plot_response(lp, hp, fc, fs)
    
        print("Plot Another (y/n)")
        if input() == 'y':
            new_graph = True
        else:
            new_graph = False

    #plot_graph()

# - Filter - x order butterworth
def butterworth_crossover(fc, order, fs):
    Nyquist = fs/2
    Wn = fc / Nyquist #Normalised cutoff frequency
    lp = butter(order, Wn, btype ='low', output ='sos')
    hp = butter(order, Wn, btype='high', output='sos')
    return lp, hp

# - Filter - x order Linkwitz-Riley
def lr_crossover(fc, order, fs):
    lp_sos, hp_sos = butterworth_crossover(fc, order, fs)
    lp = np.vstack([lp_sos, lp_sos]) #np.vstack function used to apply the butterworth filter twice
    hp = np.vstack([hp_sos, hp_sos]) #this in turn creates a functional LR filter for HP and LP
    return lp, hp

# - Choice of filter and order for user
def filter_choice(fc, fs):

    print('Choose filter types:')
    print('(1) Butterworth')
    print('(2) Linkwitz-Riley')
    filter_type = input()

    print("Choose filter order: ")
    if filter_type == '1':
        print ("1, 2, 3, 4 ,5, 6, 7, 8")
        order_type = int(input())
        lp, hp = butterworth_crossover(fc, order_type, fs) 
    elif filter_type == '2':
        print("2, 4, 6, 8")
        order_type = int(input())
        lp, hp = lr_crossover(fc, order_type, fs)

    print("lp, hp, both or none(1,2,3,4)")
    filter_pass = int(input())
    if filter_pass == 1:
        return lp, None
    elif filter_pass == 2:
        return None, hp
    elif filter_pass == 3:
        return lp, hp
    else:
        return None, None
        
# - Plot response on flat curve
def plot_response(lp_sos, hp_sos, fc, fs):
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
    save_graph(plt.gcf())
    plt.show()

# - Audio file filter processing

def audio_process(filename):
    audio, file_fs = sf.read(filename) # Load audio file
    if audio.ndim == 2:
        audio = audio[:, 0] # Turn mono (duplicate left ear)    
    return audio, file_fs



def plot_spectrum(audio, file_fs, fc, lp_sos=None, hp_sos=None,):
    
    def welch_choice():

        print('Do you want to use Welch method? (y/n)')
        yn = input()
        if yn == 'y':

            use_welch = True
        else:
            use_welch = False
        return use_welch
    
    use_welch = welch_choice();
    if use_welch:
        _, unfiltered_power = welch(audio, fs=file_fs, nperseg=4096)
        raw_max = 10 * np.log10(np.max(unfiltered_power))
    else:
        raw_max = 20 * np.log10(np.max(np.abs(np.fft.rfft(audio))))

    def plot_filter_spectrum(use_welch, filter_color, signal_label, filter=None):
        if filter is not None:
            filtered_audio = sosfilt(filter, audio) #Applies the filter to the signal
        else:
            filtered_audio = audio
        if use_welch: #Checks whether welch or FFT method
            spectrum_freqs, spectrum_power = welch(filtered_audio, fs=file_fs, nperseg=4096) #Applies the welch method (reduces noice/makes signal smoother)
            spectrum_mag = 10*np.log10(spectrum_power) #Converting to magnitude (10log10 due to welch method using power)
        else:
            spectrum_result = np.fft.rfft(filtered_audio)  #Applies real FFT (discards negative values), returns a complex array of frequencies
            spectrum_freqs = np.fft.rfftfreq(len(audio), d=1/file_fs) #Generates the corresponding frequency axis for each bin
            spectrum_mag = 20*np.log10(np.abs(spectrum_result)) #Converting to magnitude
        spectrum_mag = spectrum_mag - raw_max #Normalising (loudest point at 0dB)
        plt.plot(spectrum_freqs, spectrum_mag, label=signal_label, color=filter_color)    
            
    def get_spectrum(use_welch):
        if use_welch:
            spectrum_freqs, spectrum_power = welch(audio, fs=file_fs, nperseg=4096)
            spectrum_mag = 10*np.log10(spectrum_power)
        else:
            spectrum_result = np.fft.rfft(audio)
            spectrum_freqs = np.fft.rfftfreq(len(audio), d=1/file_fs)
            spectrum_mag = 20*np.log10(np.abs(spectrum_result))
        raw_max = np.max(spectrum_mag)
        spectrum_mag = spectrum_mag-raw_max
        return spectrum_freqs, spectrum_mag, raw_max


   
    
    def plot_filters(use_welch, lp_sos=None, hp_sos=None,):

        if lp_sos is not None: #Checks if none
            w, h_lp = sosfreqz(lp_sos, worN=1000, fs=file_fs) 
            lp_db = 20 * np.log10(abs(h_lp)) #Convert to dB
            plt.plot(w, lp_db, label='Low Pass Filter')#Plotting filters

            plot_filter_spectrum(use_welch, 'yellow', 'LP Audio', lp_sos)

        if hp_sos is not None:
            w, h_hp = sosfreqz(hp_sos, worN=1000, fs=file_fs)
            hp_db = 20 * np.log10(abs(h_hp))
            plt.plot(w, hp_db, label='High Pass Filter')

            plot_filter_spectrum(use_welch, 'blue', 'HP Audio', hp_sos)
    
    plt.figure(figsize=(10,6))  
    plot_filter_spectrum(use_welch, 'green', 'Unfiltered Audio')
    plot_filters(use_welch, lp_sos, hp_sos)       
    
    
    plt.xscale('log')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.title('Crossover Filter Response')
    plt.grid(True, which='both')
    plt.ylim(-120, 5)
    plt.xlim(20, 20000)
    plt.axvline(x=fc, color='grey', linestyle='--', label=f'Crossover: {fc}Hz')
   
    
    ax = plt.gca()
    ax.set_xticks([20, 30, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])
    ax.get_xaxis().set_major_formatter(ticker.ScalarFormatter())
        
    save_graph(plt.gcf())
        
    print('Do you want to save audio (y/n)')
    yn = input()
    if yn == 'y':
        
        if lp_sos is not None:
            audio_saving(lp_sos, audio, 'Low Pass Sample', file_fs)
        if hp_sos is not None:
            audio_saving(hp_sos, audio, 'High Pass Sample', file_fs)


    plt.legend()
    plt.show() 

# - Plots the final frequency response
def plot_graph(fc, lp, hp, filename):
    audio, file_fs = audio_process(filename)
    plot_spectrum(audio, file_fs, fc, lp, hp)
    
# - Saves filtered audio
def audio_saving(filter, audio, filter_type, file_fs):
    sample = sosfilt(filter, audio)
    sf.write(f'{filter_type}.wav', sample, file_fs)

def save_graph(f):
    print ('Do you want to save graph (y/n)')
    yn = input()
    if yn == ('y'):
        print("Name: ")
        name = input()
        f.savefig(f'{name}.png')
    
main()