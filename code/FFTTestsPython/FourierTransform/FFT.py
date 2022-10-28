# sampling a sine wave programmatically
import wave
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

ifile = wave.open("untitled.wav")
samples = ifile.getnframes()
audio = ifile.readframes(samples)
fs = ifile.getframerate()
# Convert buffer to float32 using NumPy
audio_as_np_int16 = np.frombuffer(audio, dtype=np.int16)
audio_as_np_float32 = audio_as_np_int16.astype(np.float32)
# Normalise float32 array so that values are between -1.0 and +1.0
max_int16 = 2**15
audio_normalised = audio_as_np_float32 / max_int16

TIME = np.linspace(0, len(audio_normalised) / fs, num=len(audio_normalised))

plt.plot(TIME, audio_normalised)
plt.show()
# TODO: Use audio_nomalised instead of y for fourier

# sampling information
Fs = 44100 # sample rate
T = 1/Fs # sampling period
t = 0.4 # seconds of sampling
N = Fs*t # total points in signal

#fourier transform audio ifile
audio_fft = np.fft.fft(audio_normalised)[0:int(N/2)]/N
audio_fft[1:] = 2*audio_fft[1:]
Pxx_audio_fft = np.abs(audio_fft)
f = Fs*np.arange((N/2))/N; # frequency vector

# plotting
fig,ax = plt.subplots()
plt.plot(f,Pxx_audio_fft,linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
plt.show()

# signal information
freq = 440 # in hertz, the desired natural frequency
freq2 = 160
freq3 = 5
omega = 2*np.pi*freq # angular frequency for sine waves
omega2 = 2*np.pi*freq2
omega3 = 2*np.pi*freq3

t_vec = np.arange(N)*T # time vector for plotting
y = np.sin(omega*t_vec)
y += 2*np.sin(omega2*t_vec)
y += np.sin(omega3*t_vec)

plt.plot(t_vec,y)
plt.show()

# fourier transform and frequency domain
#
Y_k = np.fft.fft(y)[0:int(N/2)]/N # FFT function from numpy
test = Y_k
Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
Pxx = np.abs(Y_k) # be sure to get rid of imaginary part

f = Fs*np.arange((N/2))/N; # frequency vector

# plotting
fig,ax = plt.subplots()
plt.plot(f,Pxx,linewidth=1)
ax.set_xscale('log')
ax.set_yscale('log')
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
plt.show()

# fftx = test[range(int(len(test)/2))]
# freq_fftx = np.linspace(0,2/T,len(fftx))
# plt.plot(freq_fftx,abs(fftx)**2)
# plt.show()

for coef, freq in zip(Pxx, f):
    if coef:
        if (coef > 0.1):
            print('{c:>6} * exp(2 pi i t * {f})'.format(c=coef, f=freq))