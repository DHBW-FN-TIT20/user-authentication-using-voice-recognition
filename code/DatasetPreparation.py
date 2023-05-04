import os
from pathlib import Path
import librosa
import numpy as np
import soundfile as sf

# base_path = "/home/henry/Downloads/archive/50_speakers_audio_data"
# target_path = "/home/henry/Downloads/audio_dataset"

base_path = os.path.join(os.path.dirname(__file__), "data", "50_speakers_audio_data")
target_path = os.path.join(os.path.dirname(__file__), "data", "audio_dataset")

def rename_files(base_path):
    # get all folder names in base_path
    folders = os.listdir(base_path)

    # loop through all folders
    for folder in folders:
        # get speaker number (last two digits of folder name)
        speaker_number = int(folder[-2:])

        # replace folder 50 with 22 (missing folder)
        if speaker_number == 50:
            speaker_number = 22
        
        # rename folder
        os.rename(os.path.join(base_path, folder), os.path.join(base_path, f"Speaker{speaker_number:04}"))

        # get all files in folder
        files = os.listdir(os.path.join(base_path, f"Speaker{speaker_number:04}"))

        # loop through all files
        for file in files:
            # get file number
            file_number = int(file.split("_")[-1].split(".")[0])

            # rename file
            os.rename(os.path.join(base_path, f"Speaker{speaker_number:04}", file), os.path.join(base_path, f"Speaker{speaker_number:04}", f"Speaker{speaker_number:02}_{file_number:04}.wav"))

def create_dataset(sourcePath, target_path):
    """
    sourcePath: path to the 50_speaker_audio_data folder
    target_path: custom new folder to save the dataset
    """
    used_speaker_numbers = [11, 12, 13, 14, 15, 17, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33, 37, 38, 39]

    new_speaker_index = 0

    for speaker_number in used_speaker_numbers:
        speaker_source_path = os.path.join(sourcePath, f"Speaker{speaker_number:04}")

        target_folder = os.path.join(target_path, f"Speaker{new_speaker_index:04}")
        # mkdir if not exists
        if not os.path.exists(target_folder):
            Path(target_folder).mkdir(parents=True, exist_ok=True)

        # count files in folder
        files = os.listdir(speaker_source_path)
        file_count = len(files)

        # TRAINING DATA
        # combine files 0 - file_count - 4
        # create float32 array
        training_data = np.array([], dtype=np.float32)
        sr = 0
        for i in range(file_count - 4):
            # load file
            file_path = os.path.join(speaker_source_path, f"Speaker{speaker_number:02}_{i:04}.wav")
            y, sr = librosa.load(file_path)
            training_data = np.append(training_data, y)
            
        # save file
        target_file_path = os.path.join(target_folder, f"Training_Speaker{new_speaker_index:02}.wav")
        sf.write(target_file_path, training_data, sr, subtype='PCM_24')
        print(f"New speaker {new_speaker_index:02} with {len(training_data)/sr/60:.2f} minutes of training data.")


        # VALIDATION DATA
        val_file_index = 0
        for i in range(file_count - 4, file_count - 1):
            # load file
            file_path = os.path.join(speaker_source_path, f"Speaker{speaker_number:02}_{i:04}.wav")
            y, sr = librosa.load(file_path)
            
            current_limit = 15*sr
            while current_limit < len(y):
                # save file
                target_file_path = os.path.join(target_folder, f"Validation_Speaker{new_speaker_index:02}_{val_file_index:04}.wav")
                sf.write(target_file_path, y[current_limit - 15*sr:current_limit], sr, subtype='PCM_24')

                current_limit += 15*sr
                val_file_index += 1

        new_speaker_index += 1

def split_to_eight_min(sourcePath):
    for i in range(20):
        file_path = os.path.join(sourcePath, f"Speaker{i:04}", f"Training_Speaker{i:02}.wav")

        y, sr = librosa.load(file_path)

        current_limit = 8*60*sr
        print(current_limit)

        j = 0
        sf.write(os.path.join(sourcePath, f"Speaker{i:04}", f"Training_Speaker{i:02}_{j:02}.wav"), y[0:current_limit], sr, subtype='PCM_24')
        j += 1
        sf.write(os.path.join(sourcePath, f"Speaker{i:04}", f"Training_Speaker{i:02}_{j:02}.wav"), y[current_limit:], sr, subtype='PCM_24')
       
if __name__ == "__main__":
    # create_dataset(base_path, target_path)
    split_to_eight_min(target_path)