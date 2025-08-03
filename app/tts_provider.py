class TTSProvider:
    def synthesize_text(self, input_path, lang, voice, output_path):
        raise NotImplementedError("synthesize_text must be implemented by subclass")

    def synthesize_ssml(self, input_path, lang, voice, output_path):
        raise NotImplementedError("synthesize_ssml must be implemented by subclass")

    def list_languages(self):
        raise NotImplementedError("list_languages must be implemented by subclass")

    def list_voices(self, lang):
        raise NotImplementedError("list_voices must be implemented by subclass")

