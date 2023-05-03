import os

class DatasetHandler:
    def __init__(self, base_path) -> None:
        self.base_path = base_path

    def get_training_file_path(self, speaker_index) -> str:
        return os.path.join(self.base_path, f"Speaker{speaker_index:04}", f"Training_Speaker{speaker_index:02}.wav")

    def get_validation_file_path(self, speaker_index, file_index) -> str:
        return os.path.join(self.base_path, f"Speaker{speaker_index:04}", f"Validation_Speaker{speaker_index:02}_{file_index:04}.wav")