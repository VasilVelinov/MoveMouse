import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import math
from threading import Thread
import ctypes


class MouseMovementApp:
    def __init__(self, master):
        self.master = master
        master.title("Mouse Movement App")

        self.welcome_label = ttk.Label(master, text="Welcome to Mouse Movement App!", font=("Helvetica", 12, "bold"))
        self.radius_label = ttk.Label(master, text="Radius:")
        self.radius_entry = ttk.Entry(master, state='write')
        self.radius_entry.insert(0, "50")  # Default radius value
        self.speed_label = ttk.Label(master, text="Speed:")
        self.speed_entry = ttk.Entry(master, state='write')
        self.speed_entry.insert(0, "0.001")  # Default speed value
        self.start_button = ttk.Button(master, text="Start", command=self.start_mouse_movement)
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_mouse_movement)
        self.status_label = ttk.Label(master, text="Status: Idle")

        self.countdown_progress = ttk.Progressbar(master, length=200, mode="determinate")
        self.countdown_label = ttk.Label(master, text="Countdown: 15")
        self.signature_label = ttk.Label(master, text="@ Vasil Velinov", font=("Helvetica", 8, "bold"))

        self.welcome_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.radius_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.radius_entry.grid(row=1, column=1, padx=10, pady=10)
        self.speed_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.speed_entry.grid(row=2, column=1, padx=10, pady=10)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.stop_button.grid(row=5, column=0, columnspan=2, pady=10)
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10)
        self.countdown_progress.grid(row=7, column=0, columnspan=2, pady=10)
        self.countdown_label.grid(row=8, column=0, columnspan=2, pady=10)
        self.signature_label.grid(row=9, column=0, columnspan=2, pady=10)

        self.mouse_movement_thread = None
        self.is_running = False

    def start_mouse_movement(self):
        radius = float(self.radius_entry.get())
        speed = float(self.speed_entry.get())
        self.status_label["text"] = "Status: Running"
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002) # Prevent display and system sleep
        self.is_running = True
        self.mouse_movement_thread = Thread(target=self.move_mouse, args=(radius, speed))
        self.mouse_movement_thread.start()

    def stop_mouse_movement(self):
        self.status_label["text"] = "Status: Stopped"
        # Allow sleep on Windows
        ctypes.windll.kernel32.SetThreadExecutionState(0x00000002)  # Revert sleep prevention
        self.is_running = False

    def move_mouse(self, radius, speed):
        while self.is_running:
            for countdown in range(15, 0, -1):
                self.countdown_label["text"] = f"Countdown: {countdown}"
                self.countdown_progress["value"] = (countdown / 15) * 100
                self.master.update()
                time.sleep(1)

            self.countdown_label["text"] = "Countdown: 15"  # Reset countdown label
            self.countdown_progress["value"] = 0  # Reset progress bar
            current_x, current_y = pyautogui.position()

            # Jitter the mouse position slightly
            for _ in range(5):  # Repeat to ensure activity
                pyautogui.moveTo(current_x + 1, current_y + 1)
                time.sleep(0.1)
                pyautogui.moveTo(current_x - 1, current_y - 1)
                time.sleep(0.1)

        self.status_label["text"] = "Status: Idle"
        self.countdown_label["text"] = "Countdown: 15"  # Reset countdown label
        self.countdown_progress["value"] = 0  # Reset progress bar




root = tk.Tk()
app = MouseMovementApp(root)
root.mainloop()