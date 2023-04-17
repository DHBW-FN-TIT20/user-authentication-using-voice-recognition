import os

basePath = "/home/henry/Downloads/archive/50_speakers_audio_data"

# get all folder names in basePath
folders = os.listdir(basePath)

# loop through all folders
for folder in folders:
    # get speaker number (last two digits of folder name)
    speaker_number = int(folder[-2:])

    # replace folder 50 with 22 (missing folder)
    if speaker_number == 50:
        speaker_number = 22
    
    # rename folder
    os.rename(os.path.join(basePath, folder), os.path.join(basePath, f"Speaker{speaker_number:04}"))

    # get all files in folder
    files = os.listdir(os.path.join(basePath, f"Speaker{speaker_number:04}"))

    # loop through all files
    for file in files:
        # get file number
        file_number = int(file.split("_")[-1].split(".")[0])

        # rename file
        os.rename(os.path.join(basePath, f"Speaker{speaker_number:04}", file), os.path.join(basePath, f"Speaker{speaker_number:04}", f"Speaker{speaker_number:02}_{file_number:04}.wav"))