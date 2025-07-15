import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
from app import synthesize_text, synthesize_ssml
from config import load_config, save_config
import os

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Synthesizer")
        self.root.geometry("400x400")
        self.synth_mode = tk.StringVar(value="text")

        # Load or select authentication key file 
        ttk.Label(self.root, text="Select GCP Key File:").pack()
        self.key_entry = ttk.Entry(self.root, width=40)
        self.key_entry.pack()
        ttk.Button(self.root, text="Browse", command=self.browse_key_file).pack(pady=5)
        config = load_config()
        key_path = config.get("gcp_key_path", "")
        self.key_entry.insert(0, key_path)

        # Select input file
        ttk.Label(self.root, text="Choose File:").pack()
        self.input_entry = ttk.Entry(self.root, width=40)
        self.input_entry.pack()
        ttk.Button(self.root, text="Browse", command=self.browse_input_file).pack(pady=5)

        # Select output path
        ttk.Label(self.root, text="Choose Output Location:").pack()
        self.output_entry = ttk.Entry(self.root, width=40)
        self.output_entry.pack()
        ttk.Button(self.root, text="Browse", command=self.browse_output_file).pack(pady=5)

        # Select mode
        ttk.Label(self.root, text="Choose Mode:").pack()
        ttk.Radiobutton(self.root, text="Text", variable=self.synth_mode, value="text").pack()
        ttk.Radiobutton(self.root, text="SSML", variable=self.synth_mode, value="ssml").pack()

        # Synthesize 
        ttk.Button(self.root, text="Synthesize", command=self.run_synthesis).pack(pady=10)

    def browse_key_file(self):
        key_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if key_path:
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key_path)
            save_config({"gcp_key_path": key_path})


    def browse_input_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text and SSML Files", "*.txt *.ssml")])
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)
    
    def browse_output_file(self):
        filetypes = [("MP3 Files", "*.mp3")]
        output_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=filetypes)
        if output_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, output_path)


    def run_synthesis(self):
        key_path = self.key_entry.get()
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        mode = self.synth_mode.get()

        if not key_path:
            messagebox.showwarning("No key selected.", "Please select a key for authentication.")
            return

        if not input_path:
            messagebox.showwarning("No file selected.", "Please select a file for synthesis.")
            return

        try:
            if mode == "text":
                synthesize_text(input_path, key_path, output_path)
            else:
                synthesize_ssml(input_path, key_path, output_path)
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
