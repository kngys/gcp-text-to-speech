from google.cloud import texttospeech
import html

def synthesize_text():
    """
    Synthesises audio from plaintext.
    """

    client = texttospeech.TextToSpeechClient.from_service_account_file("gcp_key.json")
    synthesis_input = texttospeech.SynthesisInput(text="Hello, world!")
    voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", name="en-US-Standard-C"
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











    





if __name__ == "__main__":
    synthesize()
