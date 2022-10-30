import mariadb
import sys

class DBConnection:
    USER = "studienarbeit"
    HOST = "127.0.0.1"
    DATABASE = "datensatzNine"
    DB = None
    CURSOR = None
    
    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.DB = mariadb.connect(
                user = self.USER,
                host = self.HOST,
                database = self.DATABASE
            )
            self.CURSOR = self.DB.cursor()
        except mariadb.Error as e:
            print(f"Error connecting: {e}")
            self.DB = None
            self.CURSOR = None
    
    def addDatensatz(self, word: str, speaker_id: int, audio_length: float, frequencies, amplitudes):
        # print(f"Word: {word}, SpeakerID: {speaker_id}, AudioLength: {audio_length}", end=";")
        dataset_id = None
        self.CURSOR.execute(
            f"SELECT * FROM datensatz WHERE word LIKE '{word}' AND speakerID = {speaker_id} AND length = {audio_length}"
        )
        if self.CURSOR.rowcount == 1:
            dataset_id = self.CURSOR.next()[0]

        else:
            self.CURSOR.execute(
                f"INSERT INTO datensatz (word, speakerID, length) VALUES ('{word}', {speaker_id}, {audio_length})"
            )
            self.DB.commit()
            dataset_id = self.CURSOR.lastrowid
        
        if dataset_id is not None:
            # print(f"Dataset ID: {dataset_id}", end = ";")
            for frequency in frequencies:
                # print(f"Add frequency: {frequency}", end = ";")
                try:
                    self.CURSOR.execute(
                        f"INSERT INTO frequenz (datensatzId, frequenz, amplitude) VALUES ({dataset_id}, {frequency}, {amplitudes[frequencies.index(frequency)]})"
                    )
                    self.DB.commit()
                    # print("Insert successful")
                except mariadb.IntegrityError as e:
                    print(f"Insert failed: {e}")
    
    def getFrequencies(self):
        self.CURSOR.execute(
            f"SELECT frequenz, amplitude, datensatzId FROM frequenz ORDER BY frequenz"
        )
        frequenz = []
        amplitude = []
        datensatzId = []
        for pair in self.CURSOR:
            frequenz.append(pair[0])
            amplitude.append(pair[1])
            datensatzId.append(pair[2])
        return frequenz, amplitude, datensatzId
