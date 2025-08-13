from google.cloud import texttospeech
import os
from .tts_provider import TTSProvider

class GoogleTTSProvider(TTSProvider):
    def __init__(self, key_path):
        self.key_path = key_path
        self.client = texttospeech.TextToSpeechClient.from_service_account_file(key_path)

    def synthesize_text(self, input_path, lang, voice, output_path, engine=None):
        with open(input_path) as f:
            text = f.read()

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(language_code=lang, name=voice)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = self.client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
        with open(output_path, "wb") as out:
            out.write(response.audio_content)

    def synthesize_ssml(self, input_path, lang, voice, output_path, engine=None):
        with open(input_path) as f:
            ssml = f.read()

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
        voice_params = texttospeech.VoiceSelectionParams(language_code=lang, name=voice)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = self.client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)
        with open(output_path, "wb") as out:
            out.write(response.audio_content)

    def list_languages(self):
        voices = self.client.list_voices().voices
        return sorted({lang for v in voices for lang in v.language_codes if lang.startswith("en-")})

    def list_voices(self, lang):
        voices = self.client.list_voices(language_code=lang).voices
        return [{
            "name": v.name,
            "gender": v.ssml_gender.name,
            "ssml_support": not "Chirp" in v.name
        } for v in voices]
    
    def list_engines(self, lang, voice):
        return []

