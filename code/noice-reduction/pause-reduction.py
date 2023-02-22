import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
import soundfile as sf
import scipy
import os
import math
import random
import pandas as pd
from tabulate import tabulate
from pydub import AudioSegment
from pydub.silence import split_on_silence

class AudioPreprocessor:

    @staticmethod
    def int_to_float(array, type=np.float32):
        """
        Change np.array int16 into np.float32
        Parameters
        ----------
        array: np.array
        type: np.float32
        Returns
        -------
        result : np.array
        """

        if array.dtype == type:
            return array

        if array.dtype not in [np.float16, np.float32, np.float64]:
            if np.max(np.abs(array)) == 0:
                array = array.astype(np.float32)
                array[:] = 0
            else:
                array = array.astype(np.float32) / np.max(np.abs(array))

        return array

    @staticmethod
    def float_to_int(array, type=np.int16, divide_max_abs=True):
        """
        Change np.array float32 / float64 into np.int16
        Parameters
        ----------
        array: np.array
        type: np.int16
        Returns
        -------
        result : np.array
        """

        if array.dtype == type:
            return array

        if array.dtype not in [np.int16, np.int32, np.int64]:
            if np.max(np.abs(array)) == 0:
                array[:] = 0
                array = type(array * np.iinfo(type).max)
            else:
                if divide_max_abs:
                    array = type(array / np.max(np.abs(array)) * np.iinfo(type).max)
                else:
                    array = type(array * np.iinfo(type).max)
        return array

    @staticmethod
    def norm_mel(y, sr):
        mel = librosa.feature.melspectrogram(y=y, sr = sr, n_mels = 80)
        return np.log10(np.maximum(mel, 1e-10)).T

    @staticmethod
    def plot(y, sr):
        mel = AudioPreprocessor.norm_mel(y, sr)
        fig, axs = plt.subplots(2, figsize=(10, 8))
        axs[0].plot(y)
        im = axs[1].imshow(np.rot90(mel), aspect='auto', interpolation='none')
        fig.colorbar(mappable=im, shrink=0.65, orientation='horizontal', ax=axs[1])

    @staticmethod
    def remove_silence(y, sr):

        threshold = 0.02
        pause_length_in_ms = 100
        counter_below_threshold = 0
        indices_to_remove = []
        keep_at_start_and_end = 10
        
        for i, amp in enumerate(y):
            if abs(amp) < threshold:
                counter_below_threshold += 1
            else:
                if counter_below_threshold > pause_length_in_ms:
                    for index in range(i-counter_below_threshold+keep_at_start_and_end, i-keep_at_start_and_end):
                        indices_to_remove.append(index)
                counter_below_threshold = 0

        if counter_below_threshold > pause_length_in_ms:
            for index in range(len(y)-counter_below_threshold+keep_at_start_and_end, len(y)-keep_at_start_and_end):
                indices_to_remove.append(index)

        y_ = np.delete(y, indices_to_remove)

        sf.write("/Users/johannes/repos/sa-hs-lb-jb/code/noice-reduction/removed_silence.wav", y_, sr)
        AudioPreprocessor.plot(y_, sr)
        return y_, sr
        

def main():
    y, sr = librosa.load("/Users/johannes/repos/sa-hs-lb-jb/code/noice-reduction/download.wav")
    AudioPreprocessor.plot(y=y, sr=sr)
    AudioPreprocessor.remove_silence(y=y, sr=sr)
    plt.show()

if __name__ == '__main__':
    main()