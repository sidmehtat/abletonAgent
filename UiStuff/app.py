import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from als_parser import SPLICE_FOLDER, parse_project
from packager import package


class App:
    def __init__(self, root):
        self.root = root
        self.splice_folder = SPLICE_FOLDER
        self.current_project = None

        root.title("Ableton Packager")
        root.geometry("700x500")

        tk.Label(root, text="Remember to hit Collect All and Save on the .als file for best results.",
                 font=("Helvetica", 14, "bold")).pack(anchor="w", padx=10, pady=10)

        self.splice_label = tk.Label(root, text="Splice folder: " + str(self.splice_folder))
        self.splice_label.pack(anchor="w", padx=10)

        self.spliceButton = tk.Button(root, text="Choose Splice folder", command=self.on_splice)
        self.spliceButton.pack(anchor="w", padx=10, pady=5)

        self.alsOneFileButton = tk.Button(root, text="Select file", command=self.on_select)
        self.alsOneFileButton.pack(anchor="w", padx=10, pady=5)

        self.output = tk.Text(root)
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def on_splice(self):
        print("spliceButton pressed")
        folder = filedialog.askdirectory(title="Choose your Splice folder", initialdir=Path.home())
        if folder:
            self.splice_folder = Path(folder)
            self.splice_label.config(text="Splice folder: " + folder)
            print("Splice folder set to", folder)
            if self.current_project:
                self.start_scan(self.current_project)

    def on_select(self):
        print("alsOneFileButton pressed")
        path = filedialog.askopenfilename(title="Choose an Ableton project",
                                          initialdir=Path.home() / "Documents",
                                          filetypes=[("Ableton project", "*.als")])
        if path:
            self.current_project = path
            self.start_scan(path)

    def start_scan(self, path):
        self.show(path + "\n\nWorking...")
        threading.Thread(target=self.scan, args=(path,), daemon=True).start()

    def scan(self, path):
        try:
            result = parse_project(path, self.splice_folder)
            copied = package(result)
            text = path + "\n\nCopied to " + copied["folder"] + ":\n"
            for name in copied["copied"]:
                text += "  " + name + "\n"
            text += "\nThird-party plugins:\n"
            for p in result["plugins"]:
                text += "  " + p["name"] + " (" + p["format"] + ") on " + p["track"] + "\n"
            print("copied", len(copied["copied"]), "files")
        except Exception as e:
            text = "Error: " + str(e)
            print(text)
        self.root.after(0, self.show, text)

    def show(self, text):
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)


def run():
    root = tk.Tk()
    App(root)
    root.mainloop()
