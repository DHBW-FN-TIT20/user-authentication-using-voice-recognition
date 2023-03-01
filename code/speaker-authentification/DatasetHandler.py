import os
import librosa

class DatasetHandler:

    def __init__(self, basepath):
        self.basepath = basepath

    def filepath(self, speaker_index, file_index):
        # print(os.path.join(self.basepath, f"Speaker{speaker_index:04}", f"Speaker{speaker_index:02}_{file_index:04}.wav"))
        return os.path.join(self.basepath, f"Speaker{speaker_index:04}", f"Speaker{speaker_index:02}_{file_index:04}.wav")