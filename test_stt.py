from src.audio.stt import SpeechToText


stt = SpeechToText()

text = stt.transcribe(
    "question.wav"
)

print(text)