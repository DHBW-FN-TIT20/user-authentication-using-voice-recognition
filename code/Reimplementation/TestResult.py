class TestResult:
    def __init__(self, speaker_id: int, sample_id: int, correspondence: dict[int, float]):
        self.speaker_id: int = speaker_id
        self.sample_id: int = sample_id
        self.correspondence: dict[int, float] = correspondence