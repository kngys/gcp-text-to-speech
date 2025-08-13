class TTSManager:
    def __init__(self):
        self.providers = {}
        self.active_provider = None

    def register_provider(self, name, provider):
        self.providers[name] = provider

    def set_active_provider(self, name):
        if name not in self.providers:
            raise ValueError(f"TTS provider '{name}' not registered.")
        self.active_provider = self.providers[name]

    def synthesize(self, mode, input_path, lang, voice, output_path, engine=None):
        if not self.active_provider:
            raise RuntimeError("No active TTS provider selected.")
        if mode == "text":
            self.active_provider.synthesize_text(input_path, lang, voice, output_path, engine)
        elif mode == "ssml":
            self.active_provider.synthesize_ssml(input_path, lang, voice, output_path, engine)
        else:
            raise ValueError(f"Unknown synthesis mode: {mode}")

    def get_languages(self):
        if not self.active_provider:
            return []
        return self.active_provider.list_languages()

    def get_voices(self, lang):
        if not self.active_provider:
            return []
        return self.active_provider.list_voices(lang)
    
    def get_engines(self, lang, voice):
        if not self.active_provider:
            return []
        return self.active_provider.list_engines(lang, voice)


