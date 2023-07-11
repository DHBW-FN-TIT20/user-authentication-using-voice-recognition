import numpy as np
import librosa
import noisereduce as nr

class AudioPreprocessor:
    
    @staticmethod
    def int_to_float(array, type=np.float32):
        """
        Change np.array int16 into np.float32 Parameters
        Author: Husein Zolkepli
        Source: https://github.com/huseinzol05/malaya-speech/blob/master/malaya_speech/utils/astype.py
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
        Change np.array float32 / float64 into np.int16 Parameters
        Author: Husein Zolkepli
        Source: https://github.com/huseinzol05/malaya-speech/blob/master/malaya_speech/utils/astype.py
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
    def remove_noise(y, sr):
        # prop_decrease 0.8 only reduces noise by 0.8 -> sound quality is better than at 1.0
        y_ = nr.reduce_noise(y=y, sr=sr, prop_decrease=0.8)

        return y_

    @staticmethod
    def remove_silence(y):
        threshold = 0.005
        pause_length_in_ms = 200
        keep_at_start_and_end = 50
        counter_below_threshold = 0
        indices_to_remove = []
        
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

        return y_

    @staticmethod
    def create_frames(y, frame_size, overlap):
        frames = []
        
        if overlap >= frame_size or frame_size <= 0 or overlap < 0:
            return frames

        index = 0
        
        while index + frame_size < y.shape[0]:
            frames.append(y[index: index + frame_size])
            index = index + frame_size - overlap
        
        return frames

    @staticmethod
    def window_frames(frames, window_function=np.hanning):
        windowed_frames = []

        for frame in frames:
            windowed_frames.append(frame * window_function(frame.shape[0]))

        return windowed_frames

    @staticmethod
    def load_preprocessed_frames(filepath=None, y=None, sr=None):
        if filepath is None and (y is None or sr is None):
            raise ValueError("Either filepath or y and sr must be given.")
        
        if y is None or sr is None:
            y, sr = librosa.load(filepath)

        y = AudioPreprocessor.remove_noise(y=y, sr=sr)
        y = AudioPreprocessor.remove_silence(y=y)

        frames = AudioPreprocessor.create_frames(y=y, frame_size=1000, overlap=100)
        windowed_frames = AudioPreprocessor.window_frames(frames=frames)

        return windowed_frames