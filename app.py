from google.cloud import texttospeech

def synthesize():
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

if __name__ == "__main__":
    synthesize()
