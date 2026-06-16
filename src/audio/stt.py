from faster_whisper import WhisperModel


class SpeechToText:

    def __init__(
        self,
        model_size: str = "base"
    ):

        self.model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(
        self,
        audio_path: str
    ) -> str:

        segments, _ = self.model.transcribe(
            audio_path
        )

        text = " ".join(
            segment.text
            for segment in segments
        )

        return text.strip()