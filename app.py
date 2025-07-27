from google.cloud import texttospeech
import html
import os

def synthesize_text(input_file_path, key_file_path, output_file_path):
    """
    Synthesizes audio from plaintext.
    """

    with open(input_file_path) as f:
        text_input = f.read()

    client = texttospeech.TextToSpeechClient.from_service_account_file(key_file_path)
    synthesis_input = texttospeech.SynthesisInput(text=text_input)
    voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Chirp-HD-D"
    )
    audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        file_name = os.path.basename(output_file_path)
        print(f'Audio saved to file "{file_name}"')

def text_to_ssml(input_file: str) -> str:
    """
    Converts plaintext to Speech Synthesis Markup Language (SSML).
    """

    with open(input_file) as f:
        raw_lines = f.read()

    # Replace HTML special characters 
    escaped_lines = html.escape(raw_lines)

    # Convert plaintext to SSML
    ssml = "<speak>{}</speak>".format(
        escaped_lines.replace("\n", '\n<break time="2s"/>')
    )

    return ssml

def synthesize_ssml(input_file_path, key_file_path, output_file_path):
    """
    Synthesizes audio from ssml.
    """

    with open(input_file_path) as f:
        ssml_input = f.read()

    client = texttospeech.TextToSpeechClient.from_service_account_file(key_file_path)
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_input)

    voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Neural2-I"
    )
    audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=1.0
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        file_name = os.path.basename(output_file_path)
        print(f'Audio saved to file "{file_name}"') 

def fetch_languages(key_file_path):
    
    client = texttospeech.TextToSpeechClient.from_service_account_file(key_file_path)
    voices = client.list_voices().voices

    lang_set = set() 
    for voice in voices:
        for lang in voice.language_codes:
            lang_set.add(lang)
    return sorted(lang_set)

def fetch_voices(key_file_path, lang):

    client = texttospeech.TextToSpeechClient.from_service_account_file(key_file_path)
    voices = client.list_voices(language_code=lang).voices

    voice_options = []
    for voice in voices:
        voice_desc = f"{voice.name} ({voice.ssml_gender.name})"
        voice_options.append(voice_desc)
    return voice_options 