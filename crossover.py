import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfreqz
import soundfile as sf


#Frequency axis - 20Hz to 20kHz
f = np.linspace(20, 20000, 1000)
fs = 48000

#Crossover frequency 
fc = 90

#Normalise to Nyquist
Nyquist = fs/2
Wn = fc / Nyquist

#Filter Design - 4th order butterworth
lp_sos = butter(4, Wn, btype ='low', output ='sos')
hp_sos = butter(4, Wn, btype='high', output='sos')

#Get frequency response
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
plt.legend()

combined = 20 * np.log10(np.abs(np.abs(h_lp) + np.abs(h_hp)))
plt.plot(w, combined, label='Combined', linestyle='--', color='green')

plt.show()

# Load audio file
audio, file_sr = sf.read('jungler.wav')
if audio.ndim == 2:
    audio = audio[:, 0]

# Resample warning
if file_sr != fs:
    print(f"Warning: file sample rate ({file_sr}Hz) doesn't match fs ({fs}Hz)")

# Apply filters to audio
from scipy.signal import sosfilt
sub_out = sosfilt(lp_sos, audio)
tops_out = sosfilt(hp_sos, audio)

# Save outputs

sf.write('sub_out.wav', sub_out, file_sr)
sf.write('tops_out.wav', tops_out, file_sr)


print("Done - sub_out.wav and tops_out.wav saved")