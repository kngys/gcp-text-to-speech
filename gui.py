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
        self.root.geometry("600x400")

        self.synth_mode = tk.StringVar(value="text")
        self.language = tk.StringVar()
        self.voice = tk.StringVar()
        
        # Load or select authentication key file 
        ttk.Label(self.root, text="Select Key File:").pack()
        self.key_entry = ttk.Entry(self.root, width=50)
        self.key_entry.pack()
        ttk.Button(self.root, text="Browse", command=self.browse_key_file).pack(pady=5)
        config = load_config()
        key_path = config.get("gcp_key_path", "")
        self.key_entry.insert(0, key_path)
        self.key_entry.icursor(tk.END)
        self.key_entry.xview_moveto(1)

        # Select input file
        ttk.Label(self.root, text="Select Input File:").pack()
        self.input_entry = ttk.Entry(self.root, width=50)
        self.input_entry.pack()
        ttk.Button(self.root, text="Browse", command=self.browse_input_file).pack(pady=5)

        # Select output path
        ttk.Label(self.root, text="Select Output Location:").pack()
        self.output_entry = ttk.Entry(self.root, width=50)
        self.output_entry.pack()
        ttk.Button(self.root, text="Browse", command=self.browse_output_file).pack(pady=5)

        # Select mode
        ttk.Label(self.root, text="Select Mode:").pack()
        ttk.Radiobutton(self.root, text="Text", variable=self.synth_mode, value="text").pack()
        ttk.Radiobutton(self.root, text="SSML", variable=self.synth_mode, value="ssml").pack()

        #Select Language and Voice
        dropdown_frame = tk.Frame(self.root)
        dropdown_frame.pack(pady=10)

        self.lang_set = fetch_en_languages(key_path)
        ttk.Label(dropdown_frame, text="Select Language:").pack(side="left", padx=5)
        self.language_combo = ttk.Combobox(dropdown_frame, textvariable=self.language, values=list(self.lang_set))
        self.language_combo.pack(side="left", padx=5)
        ttk.Label(dropdown_frame, text="Select Voice:").pack(side="left", padx=5)
        self.voice_combo = ttk.Combobox(dropdown_frame, width=45, textvariable=self.voice)
        self.voice_combo.pack(side="left", padx=5)
        self.language_combo.bind("<<ComboboxSelected>>", self.update_voice_list)

        # Synthesize 
        ttk.Button(self.root, text="Synthesize", command=self.run_synthesis).pack(pady=10)

    def browse_key_file(self):
        key_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if key_path:
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key_path)
            self.key_entry.icursor(tk.END)
            self.key_entry.xview_moveto(1)
            save_config({"gcp_key_path": key_path})


    def browse_input_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text and SSML Files", "*.txt *.ssml")])
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
        key_path = self.key_entry.get()
        voices = fetch_voices(key_path, selected_lang)
        self.voice_combo['values'] = voices

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
