from google.cloud import texttospeech
import html

def synthesize_text(text_file_path):
    """
    Synthesizes audio from plaintext.
    """

    with open(text_file_path) as f:
        text_input = f.read()

    client = texttospeech.TextToSpeechClient.from_service_account_file("gcp_key.json")
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

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

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

def synthesize_ssml(ssml_file_path: str):
    """
    Synthesizes audio from ssml.
    """

    with open(ssml_file_path) as f:
        ssml_input = f.read()

    client = texttospeech.TextToSpeechClient.from_service_account_file("gcp_key.json")
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

    with open("ssml_output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "ssml_output.mp3"')

if __name__ == "__main__":
    #synthesize_ssml("text_input.ssml")
    synthesize_text("text_input.txt")
