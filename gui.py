import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
from app.tts_manager import TTSManager
from app.google_tts import GoogleTTSProvider
from app.amazon_tts import AmazonTTSProvider
from config import load_config, save_config
import os

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Synthesizer")
        self.root.geometry("900x620+60+30")

        self.synth_mode = tk.StringVar(value="text")
        self.language = tk.StringVar()
        self.voice = tk.StringVar()
        self.engine = tk.StringVar()
        self.provider = tk.StringVar()
        self.config = load_config()
        self.tts_manager = TTSManager()
        self.key_path = self.config.get("gcp_key_path", "")

        # Select provider 
        ttk.Label(self.root, text="Select TTS Provider:").pack(pady=5)
        self.provider_combo = ttk.Combobox(self.root, textvariable=self.provider, state="readonly")
        self.provider_combo['values'] = [GoogleTTSProvider.NAME, AmazonTTSProvider.NAME]
        self.provider_combo.pack(pady=5)
        self.provider_combo.bind("<<ComboboxSelected>>", self.set_provider)
        self.tts_manager.register_provider(AmazonTTSProvider.NAME, AmazonTTSProvider())
        
        # Load or select authentication key file 
        self.key_frame = tk.Frame(self.root)
        self.key_frame.pack(pady=5)
        ttk.Label(self.key_frame, text="Select Key File:").pack(pady=5)
        self.key_entry = ttk.Entry(self.key_frame, width=50)
        self.key_entry.pack(pady=5)
        self.key_browse_button = ttk.Button(self.key_frame, text="Browse", command=self.browse_key_file)
        self.key_browse_button.pack(pady=5) 
        self.key_entry.insert(0, self.key_path)
        self.key_entry.icursor(tk.END)
        self.key_entry.xview_moveto(1)
        
        self.key_entry.configure(state="disabled")
        self.key_browse_button.configure(state="disabled")
      
        # Select mode
        mode_frame = tk.Frame(self.root)
        mode_frame.pack()
        ttk.Label(mode_frame, text="Select Mode:").pack(pady=5)
        ttk.Radiobutton(mode_frame, text="Text", variable=self.synth_mode, value="text", command=self.update_voice_list).pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="SSML", variable=self.synth_mode, value="ssml", command=self.update_voice_list).pack(side="left", padx=5)

        # Select input file
        ttk.Label(self.root, text="Select Input File:").pack(pady=5)
        self.input_entry = ttk.Entry(self.root, width=50)
        self.input_entry.pack(pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_input_file).pack(pady=5)

        # Select output path
        ttk.Label(self.root, text="Select Output Location:").pack(pady=5)
        self.output_entry = ttk.Entry(self.root, width=50)
        self.output_entry.pack(pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_output_file).pack(pady=5) 

        # Select Language, Voice and Engine
        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack(pady=10)

        ttk.Label(dropdown_frame, text="Select Language:").pack(side="left", padx=5)
        self.language_combo = ttk.Combobox(dropdown_frame, width=10, textvariable=self.language, state="readonly")
        self.language_combo.pack(side="left", padx=5)
        ttk.Label(dropdown_frame, text="Select Voice:").pack(side="left", padx=5)
        self.voice_combo = ttk.Combobox(dropdown_frame, height=10, width=40, textvariable=self.voice, state="readonly")
        self.voice_combo.pack(side="left", padx=5)
        self.language_combo.bind("<Button-1>", lambda event: self.load_languages())
        self.language_combo.bind("<<ComboboxSelected>>", self.update_voice_list)
        self.voice_combo.bind("<<ComboboxSelected>>", self.update_engine_list)
        ttk.Label(dropdown_frame, text="Select Engine:").pack(side="left", padx=5)
        self.engine_combo = ttk.Combobox(dropdown_frame, width=20, textvariable=self.engine, state="readonly")
        self.engine_combo.pack(side="left", padx=5)
        self.engine_combo.configure(state="disabled")

        # Synthesize 
        ttk.Button(self.root, text="Synthesize", width=20, command=self.run_synthesis).pack(pady=20)

        self.load_provider_config()

    def initialize_provider_from_key(self, key_path):
        if not os.path.exists(key_path):
            messagebox.showwarning("Invalid Key", "The key file path in config.json is invalid.")
            return

        self.tts_manager.register_provider(GoogleTTSProvider.NAME, GoogleTTSProvider(key_path))
        self.tts_manager.set_active_provider(GoogleTTSProvider.NAME)
        self.load_languages()
        self.update_voice_list()

    def load_provider_config(self):
        provider = self.config.get("provider", "")
        self.provider.set(provider)
        self.provider_combo.set(provider)

        if provider == GoogleTTSProvider.NAME:
            self.key_path = self.config.get("gcp_key_path", "")
            self.language.set(self.config.get("gcp_language", ""))
            self.voice.set(self.config.get("gcp_voice", ""))
            self.key_entry.configure(state="normal")
            self.key_browse_button.configure(state="normal")
            if self.key_path:
                self.initialize_provider_from_key(self.key_path)
        elif provider == AmazonTTSProvider.NAME:
            self.language.set(self.config.get("aws_language", ""))
            self.voice.set(self.config.get("aws_voice", ""))
            self.engine.set(self.config.get("aws_engine", ""))
            self.tts_manager.set_active_provider(AmazonTTSProvider.NAME)
            self.engine_combo.configure(state="readonly")
            self.load_languages()
            self.update_voice_list()
            self.update_engine_list()
        else:
            self.language.set("")
            self.voice.set("")
            self.engine.set("")

    def save_provider_config(self):
        provider = self.provider.get()
        self.config["provider"] = provider

        lang = self.language.get()
        voice_name = self.voice.get()
        engine = self.engine.get()

        if provider == GoogleTTSProvider.NAME:
            self.config["gcp_key_path"] = self.key_entry.get()
            self.config["gcp_language"] = lang
            self.config["gcp_voice"] = voice_name
        elif provider == AmazonTTSProvider.NAME:
            self.config["aws_language"] = lang
            self.config["aws_voice"] = voice_name
            self.config["aws_engine"] = engine

        save_config(self.config)

    def set_provider(self, event=None):

        selected_provider = self.provider.get()

        if selected_provider == GoogleTTSProvider.NAME:
            self.key_entry.configure(state="normal")
            self.key_browse_button.configure(state="normal")
            self.engine_combo.configure(state="disabled")
            if self.key_path:
                self.initialize_provider_from_key(self.key_path)
        else:
            self.engine_combo.configure(state="normal")
            self.key_entry.configure(state="disabled")
            self.key_browse_button.configure(state="disabled")
            self.tts_manager.set_active_provider(selected_provider)

        self.language.set("")
        self.language_combo.set("")
        self.voice.set("")
        self.voice_combo.set("")
    
    def browse_key_file(self):
        self.key_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        
        if self.key_path:
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, self.key_path)
            self.key_entry.icursor(tk.END)
            self.key_entry.xview_moveto(1)
            self.config["gcp_key_path"] = self.key_path
            save_config(self.config)
            self.tts_manager.register_provider(GoogleTTSProvider.NAME, GoogleTTSProvider(self.key_path))
            self.tts_manager.set_active_provider(GoogleTTSProvider.NAME)
            self.load_languages()
    
    def load_languages(self):
        try:
            self.lang_set = self.tts_manager.get_languages()
            self.language_combo['values'] = list(self.lang_set)
            self.update_voice_list()  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load languages:\n{e}")

    def browse_input_file(self):
        synth_mode = self.synth_mode.get()
        if synth_mode == "text":
            filetype = [("Text Files", "*.txt")]
        else: 
            filetype = [("SSML Files", "*.ssml")]
        
        path = filedialog.askopenfilename(filetypes=filetype)
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)
            self.input_entry.icursor(tk.END)
            self.input_entry.xview_moveto(1)
    
    def browse_output_file(self):
        filetypes = [("MP3 Files", "*.mp3")]
        output_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=filetypes)
        if output_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_path)
            self.output_entry.icursor(tk.END)
            self.output_entry.xview_moveto(1)

    def update_voice_list(self, event=None):
        selected_lang = self.language.get()
        if not selected_lang:
            return
        
        selected_voice = self.voice.get()
        try:
            voice_list = self.tts_manager.get_voices(selected_lang)
            if self.synth_mode.get() == "ssml":
                voice_list = [v for v in voice_list if v['ssml_support']]
                formatted_voices = [f"{v['name']} ({v['gender']})" for v in voice_list]
                if selected_voice not in formatted_voices:
                    self.voice.set("")
                    self.voice_combo.set("")
                    messagebox.showinfo("Voice Not Supported", "The selected voice does not support SSML.") 
            else:
                formatted_voices = [f"{v['name']} ({v['gender']})" for v in voice_list]
                if selected_voice not in formatted_voices:
                    self.voice.set("")
                    self.voice_combo.set("")

            self.voice_combo['values'] = formatted_voices

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load voices:\n{e}")

    def update_engine_list(self, event=None):

        if self.provider.get() == AmazonTTSProvider.NAME: 
            selected_lang = self.language.get()
            selected_voice = self.voice.get()
            selected_engine = self.engine.get()

            try:
                engine_list = self.tts_manager.get_engines(selected_lang, selected_voice)
                self.engine_combo['values'] = engine_list
                if selected_engine and selected_engine not in engine_list:
                        self.engine.set("")
                        self.engine_combo.set("")
                        messagebox.showinfo("Engine Not Supported", "The selected voice does not support the selected engine.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load engines:\n{e}")

    def run_synthesis(self):
        key_path = self.key_entry.get()
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        mode = self.synth_mode.get()
        lang = self.language.get()
        voice_name = self.voice.get().split(' ')[0]
        engine = self.engine.get().lower()

        if self.provider.get() == GoogleTTSProvider.NAME and not key_path:
            messagebox.showwarning("No key selected.", "Please select a key for authentication.")
            return

        if not input_path:
            messagebox.showwarning("No input file selected.", "Please select an input file for synthesis.")
            return
        
        if not output_path:  
            messagebox.showwarning("Location or name of output file not specified.", "Please specify location and name of output file.")
            return

        try:
            provider = self.tts_manager.active_provider
            self.save_provider_config()
            save_config(self.config)
            self.tts_manager.synthesize(mode, input_path, lang, voice_name, output_path, engine)

            file_name = os.path.basename(output_path)
            messagebox.showinfo("Success", f"Audio saved as {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")


def start_gui():
    root = ThemedTk(theme="plastik")
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
