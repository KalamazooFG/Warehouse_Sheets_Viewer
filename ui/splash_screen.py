import tkinter as tk
from tkinter import ttk

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Loading")
        self.geometry("300x150")
        self.overrideredirect(True)
        self.center_window()

        self.label = ttk.Label(self, text="Starting...", font=("Helvetica", 12))
        self.label.pack(pady=20)

        self.progress = ttk.Progressbar(self, length=200, mode="determinate")
        self.progress.pack(pady=10)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')

    def update_status(self, message, progress):
        self.label.config(text=message)
        self.progress["value"] = progress
        self.update_idletasks()
