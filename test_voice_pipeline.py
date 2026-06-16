from src.audio.stt import SpeechToText
from src.audio.tts import TextToSpeech


stt = SpeechToText()
tts = TextToSpeech()

text = stt.transcribe(
    "question.wav"
)

print(text)

tts.speak(text)