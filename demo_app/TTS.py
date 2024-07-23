from gtts import gTTS
import os

class TextToSpeech:
    def __init__(self, lang='ko'):
        self.lang = lang

    def convert_text_to_speech(self, text, output_file):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(output_file)
