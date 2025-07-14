import tkinter as tk
from tkinter import filedialog, messagebox
from app import synthesize_text, synthesize_ssml  

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text-to-Speech Synthesizer")
        self.root.geometry("400x200")
        self.synth_mode = tk.StringVar(value="text")

        # Select authentication key file 
        tk.Label(self.root, text="Select GCP Key File:").pack()
        self.key_entry = tk.Entry(self.root, width=40)
        self.key_entry.pack()
        tk.Button(self.root, text="Browse", command=self.browse_key_file).pack(pady=5)


        # Select input file
        tk.Label(self.root, text="Choose File:").pack()
        self.file_entry = tk.Entry(self.root, width=40)
        self.file_entry.pack()
        tk.Button(self.root, text="Browse", command=self.browse_file).pack(pady=5)

        # Select mode
        tk.Label(self.root, text="Choose Mode:").pack()
        tk.Radiobutton(self.root, text="Text", variable=self.synth_mode, value="text").pack()
        tk.Radiobutton(self.root, text="SSML", variable=self.synth_mode, value="ssml").pack()

        # Synthesize 
        tk.Button(self.root, text="Synthesize", command=self.run_synthesis).pack(pady=10)

    def browse_key_file(self):
        key_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if key_path:
            self.key_entry.delete(0, tk.END)
            self.key_entry.insert(0, key_path)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text and SSML Files", "*.txt *.ssml")])
        if path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, path)

    def run_synthesis(self):
        key_path = self.key_entry.get()
        path = self.file_entry.get()
        mode = self.synth_mode.get()

        if not key_path:
            messagebox.showwarning("No key selected.", "Please select a key for authentication.")
            return

        if not path:
            messagebox.showwarning("No file selected.", "Please select a file for synthesis.")
            return

        try:
            if mode == "text":
                synthesize_text(path, key_path)
                messagebox.showinfo("Success", "Audio file saved as output.mp3")
            else:
                synthesize_ssml(path, key_path)
                messagebox.showinfo("Success", "Audio saved as ssml_output.mp3")
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

def start_gui():
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_gui()
