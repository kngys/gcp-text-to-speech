import boto3
import os
from .tts_provider import TTSProvider

class AmazonTTSProvider(TTSProvider):
    def __init__(self):
        self.client = boto3.client("polly", region_name="ap-southeast-1")
    
    def synthesize_text(self, input_path, lang, voice, output_path):
        with open(input_path) as f:
            text = f.read()

        response = self.client.synthesize_speech(LanguageCode=lang, OutputFormat="mp3", VoiceId=voice, Text=text)
        with open(output_path, "wb") as out:
            out.write(response["AudioStream"].read())

    def synthesize_ssml(self, input_path, lang, voice, output_path):
        with open(input_path) as f:
            ssml = f.read()

        response = self.client.synthesize_speech(LanguageCode=lang, OutputFormat="mp3", VoiceId=voice, Text=ssml, TextType="ssml")
        with open(output_path, "wb") as out:
            out.write(response["AudioStream"].read())

    def list_languages(self):
        voices = self.client.describe_voices()["Voices"]
        return sorted({v["LanguageCode"] for v in voices if v["LanguageCode"].startswith("en-")})

    def list_voices(self, lang):
        voices = self.client.describe_voices(LanguageCode=lang)["Voices"]
        return [{
            "name": v["Id"],
            "gender": v["Gender"],
            "ssml_support": True
        } for v in voices]
    


    

