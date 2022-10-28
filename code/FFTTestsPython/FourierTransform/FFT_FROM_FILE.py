import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from os import walk
import dbConnection

def getTimeAndAudioFromFile(filepath):
    ifile = wave.open(filepath)
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

    return TIME, audio_normalised

def plot(x, y):
    plt.style.use('ggplot')
    plt.plot(x, y)
    plt.show()

def plotPoints(x, y):
    plt.plot(x,y,'s', markersize="1")
    plt.show()

def plotFrequecy(x, y):
    plt.style.use('ggplot')
    fig,ax = plt.subplots()
    plt.plot(x,y,linewidth=1)
    ax.set_xscale('log')
    ax.set_yscale('log')
    plt.ylabel('Amplitude')
    plt.xlabel('Frequency [Hz]')
    plt.show()

def fft(x, y):
    # sampling information
    Fs = 44100 # sample rate
    T = 1/Fs # sampling period
    N = len(x) # total points in signal
    if (N % 2 == 1):
        N -= 1
    t = N/Fs # seconds of sampling
    print(int(N), N, len(x))

    #fourier transform audio ifile
    Y_f = np.fft.fft(y)[0:int(N/2)]/N
    Y_f[1:] = 2*Y_f[1:]
    Pxx = np.abs(Y_f)
    f = Fs*np.arange((N/2))/N; # frequency vector
    # print(f)
    return f, Pxx

def getValuesFromFTT(f, Pxx, border):
    values = []
    coefs = []
    for coef, freq in zip(Pxx, f):
        if coef:
            if (coef > border):
                # print('{c:>6} * exp(2 pi i t * {f})'.format(c=coef, f=freq))
                values.append(freq)
                coefs.append(coef)
    return values, coefs

def createCurveWithValues(freqs, amps, name):
    curve = None
    Fs = 44100/4
    T = 1/Fs
    t = 4
    N = Fs * t
    t_vec = np.arange(N)*T
    for freq in freqs:
        print(freq)
        omega = 2*np.pi*freq # angular frequency for sine waves

        t_vec = np.arange(N)*T # time vector for plotting
        if curve is None:
            curve = amps[freqs.index(freq)]*np.sin(omega*t_vec)
        else:
            curve += amps[freqs.index(freq)]*np.sin(omega*t_vec)
    plot(t_vec, curve)
    write(name + 'test.wav', 44100, curve)
    return t_vec, curve

def outputPlotFromDB(connection):
    values = connection.getFrequencies()
    plotPoints(values[0], values[1])
    plotPoints(values[2], values[0])

    index1 = 0
    i = 1
    f_list = []
    cluster = []
    count = []
    for element in values[0]:
        if element > i*100 + 5 :
            f_list.append(values[0][index1:values[0].index(element)])
            count.append(len(values[0][index1:values[0].index(element)]))
            cluster.append(i*100+5)
            index1 = values[0].index(element) + 1
            i += 1
    
    # print(f_list)
    # print(count)
    plot(cluster, count)

def main():
    folderpath = "../archive/augmented_dataset/augmented_dataset/zero"
    filenames = next(walk(folderpath), (None, None, []))[2]
    connection = dbConnection.DBConnection()
    
    # for filepath in filenames:
    #     print(filepath)
    #     values = getTimeAndAudioFromFile(folderpath + "/" + filepath)
    #     fft_values = fft(values[0], values[1])
    #     freqs = getValuesFromFTT(fft_values[0], fft_values[1], 0.001)
    #     # plot(values[0], values[1])
    #     # plotFrequecy(fft_values[0], fft_values[1])
    #     # print(np.max(values[0]))
    #     # print(filepath[:filepath.rfind(".")])
    #     connection.addDatensatz("zero", int(filepath[:filepath.rfind(".")]), np.max(values[0]), freqs[0], freqs[1])

    outputPlotFromDB(connection)




        
    # print(len(values[0]), " ", len(values[1]))
    # index = 0;
    # while values[0][index] < 2:
    #     index += 1
    # print(len(values[0][1:index]))
    # plot(values[0][1:index], values[1][1:index])
    # ftt_values = fft(values[0][1:index], values[1][1:index])
    # plotFrequecy(ftt_values[0], ftt_values[1])
    # border = input("Border: ")
    # freqs = getValuesFromFTT(ftt_values[0], ftt_values[1], float(border))
    # newCurve = createCurveWithValues(freqs[0], freqs[1], filepath)
    # fft_2 = fft(newCurve[0], newCurve[1])
    # plotFrequecy(fft_2[0], fft_2[1])
    # freqs_2 = getValuesFromFTT(fft_2[0], fft_2[1], 0.01)
    # createCurveWithValues(freqs_2[0], freqs_2[1], filepath + "2")





if __name__ == "__main__":
    main()