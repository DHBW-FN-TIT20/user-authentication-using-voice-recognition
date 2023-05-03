import numpy as np

class AudioPreprocessor:
    @staticmethod
    def int_to_float(array, type=np.float32):
        pass

    @staticmethod
    def float_to_int(array, type=np.int16, divide_max_abs=True):
        pass

    @staticmethod
    def remove_noise(y, sr):
        pass

    @staticmethod
    def remove_silence(y):
        pass

    @staticmethod
    def create_frames(y, frame_size, overlap):
        pass

    @staticmethod
    def window_frames(frames, window_function=np.hanning):
        pass