import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
from app import synthesize_text, synthesize_ssml, fetch_en_languages, fetch_voices
from config import load_config, save_config
import os

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Synthesizer")
        self.root.geometry("650x500")

        self.synth_mode = tk.StringVar(value="text")
        self.language = tk.StringVar()
        self.voice = tk.StringVar()
        self.config = load_config()
        
        # Load or select authentication key file 
        ttk.Label(self.root, text="Select Key File:").pack(pady=5)
        self.key_entry = ttk.Entry(self.root, width=50)
        self.key_entry.pack(pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_key_file).pack(pady=5) 
        self.key_path = self.config.get("gcp_key_path", "")
        self.key_entry.insert(0, self.key_path)
        self.key_entry.icursor(tk.END)
        self.key_entry.xview_moveto(1)

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

        # Select Language and Voice
        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack(pady=10)

        ttk.Label(dropdown_frame, text="Select Language:").pack(side="left", padx=5)
        self.language_combo = ttk.Combobox(dropdown_frame, textvariable=self.language, state="readonly")
        self.language_combo.pack(side="left", padx=5)
        ttk.Label(dropdown_frame, text="Select Voice:").pack(side="left", padx=5)
        self.voice_combo = ttk.Combobox(dropdown_frame, width=45, textvariable=self.voice, state="readonly")
        self.voice_combo.pack(side="left", padx=5)
        self.language_combo.bind("<<ComboboxSelected>>", self.update_voice_list)

        last_lang = self.config.get("gcp_language", "")
        last_voice = self.config.get("gcp_voice", "")
        self.language.set(last_lang)
        self.language_combo.set(last_lang)
        self.voice.set(last_voice)
        self.voice_combo.set(last_voice)
                
        # Synthesize 
        ttk.Button(self.root, text="Synthesize", width=20, command=self.run_synthesis).pack(pady=10)

    def browse_key_file(self):
        self.key_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if self.key_path:
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, self.key_path)
            self.key_entry.icursor(tk.END)
            self.key_entry.xview_moveto(1)
            self.config["gcp_key_path"] = self.key_path
            save_config(self.config)
            self.load_languages()
    
    def load_languages(self):
            self.lang_set = fetch_en_languages(self.key_path)
            self.language_combo['values'] = list(self.lang_set)


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
        synth_mode = self.synth_mode.get()
        selected_lang = self.language.get()
        selected_voice = self.voice.get()
        key_path = self.key_entry.get()
        voice_list = fetch_voices(key_path, selected_lang)

        if synth_mode == "ssml":
            voice_list = [v for v in voice_list if v['ssml_support']]
            voice_names = [v['name'] for v in voice_list]
            if selected_voice not in voice_names:
                self.voice.set("")
                self.voice_combo.set("")
                messagebox.showinfo("Voice Not Supported", "The previously selected voice does not support SSML.")
            
        formatted_voices = [f"{v['name']} ({v['gender']})" for v in voice_list]
        self.voice_combo['values'] = formatted_voices

    def run_synthesis(self):
        key_path = self.key_entry.get()
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        mode = self.synth_mode.get()
        lang = self.language.get()
        voice_name = self.voice.get().split(' ')[0]

        if not key_path:
            messagebox.showwarning("No key selected.", "Please select a key for authentication.")
            return

        if not input_path:
            messagebox.showwarning("No input file selected.", "Please select an input file for synthesis.")
            return
        
        if not output_path:  
            messagebox.showwarning("Location or name of output file not specified.", "Please specify location and name of output file.")
            return

        try:
            if mode == "text":
                synthesize_text(input_path, key_path, output_path, lang, voice_name)
            else:
                synthesize_ssml(input_path, key_path, output_path, lang, voice_name)

            self.config["gcp_key_path"] = key_path
            self.config["gcp_language"] = lang
            self.config["gcp_voice"] = voice_name
            save_config(self.config)

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
