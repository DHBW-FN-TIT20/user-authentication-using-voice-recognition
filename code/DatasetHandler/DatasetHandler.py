import os

class DatasetHandler:
    def __init__(self, base_path) -> None:
        self.base_path = base_path

    def get_speaker_file_path(self, speaker_index, file_index):
        return os.path.join(self.base_path, f"Speaker{speaker_index:04}", f"Speaker{speaker_index:02}_{file_index:04}.wav")