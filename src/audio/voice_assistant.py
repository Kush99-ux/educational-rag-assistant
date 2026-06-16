from src.audio.stt import SpeechToText
from src.audio.tts import TextToSpeech

from src.llm.rag_pipeline import (
    RAGPipeline
)


class VoiceAssistant:

    def __init__(
        self,
        rag_pipeline: RAGPipeline
    ):

        self.rag_pipeline = (
            rag_pipeline
        )

        self.stt = (
            SpeechToText()
        )

        self.tts = (
            TextToSpeech()
        )

    def answer_audio(
        self,
        audio_path: str
    ):

        question = (
            self.stt.transcribe(
                audio_path
            )
        )

        response = (
            self.rag_pipeline.answer(
                question
            )
        )

        self.tts.speak(
            response.answer
        )

        return {
            "question": question,
            "answer": response.answer,
            "sources": response.sources
        }