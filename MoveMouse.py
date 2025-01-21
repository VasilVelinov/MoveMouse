import tkinter as tk
from tkinter import ttk
import pyautogui
import time
from PIL import Image, ImageTk
from threading import Thread
import ctypes


class MouseMovementApp:
    def __init__(self, master):
        self.master = master
        master.title("Move Mouse")
        master.geometry("400x400")
        
        # Configure rows and columns to center the content
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(10, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        self.welcome_label = ttk.Label(master, text="Welcome to Move Mouse!", font=("Helvetica", 12, "bold"))
        self.welcome_label.grid(row=1, column=0, columnspan=2, pady=(20, 10))

        # Add image below the welcome label
        self.image = Image.open("mouse.png")  # Use your image file here
        self.image = self.image.resize((100, 100))  # Resize image as needed
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = ttk.Label(master, image=self.photo)
        self.image_label.grid(row=2, column=0, columnspan=2, pady=(10, 20))
        
        self.start_button = ttk.Button(master, text="Start", command=self.start_mouse_movement)
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_mouse_movement)
        self.status_label = ttk.Label(master, text="Status: Idle")

        self.countdown_progress = ttk.Progressbar(master, length=200, mode="determinate")
        self.countdown_label = ttk.Label(master, text="Countdown: 15")
        self.signature_label = ttk.Label(master, text="@ Vasil Velinov", font=("Helvetica", 8, "bold"))

        self.start_button.grid(row=3, column=0, columnspan=2, pady=(10, 5))
        self.stop_button.grid(row=4, column=0, columnspan=2, pady=(5, 20))
        self.status_label.grid(row=5, column=0, columnspan=2, pady=10)
        self.countdown_progress.grid(row=6, column=0, columnspan=2, pady=10)
        self.countdown_label.grid(row=7, column=0, columnspan=2, pady=10)
        self.signature_label.grid(row=8, column=0, columnspan=2, pady=10)

        self.mouse_movement_thread = None
        self.is_running = False

    def start_mouse_movement(self):
        self.stop_flag = False  # Reset the stop flag when starting
        self.status_label["text"] = "Status: Running"
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002) # Prevent display and system sleep
        self.is_running = True
        self.mouse_movement_thread = Thread(target=self.move_mouse)
        self.mouse_movement_thread.start()

    def stop_mouse_movement(self):
        self.status_label["text"] = "Status: Stopped"
        # Allow sleep on Windows
        ctypes.windll.kernel32.SetThreadExecutionState(0x00000002)  # Revert sleep prevention
        self.is_running = False
        self.stop_flag = True  # Set the flag to stop countdown and movement

    def move_mouse(self):
        while self.is_running:
            for countdown in range(15, 0, -1):
                if self.stop_flag:  # Check if stop flag is set, and break the loop immediately
                    break
                self.countdown_label["text"] = f"Countdown: {countdown}"
                self.countdown_progress["value"] = (countdown / 15) * 100
                self.master.update()
                time.sleep(1)
                
            if self.stop_flag:  # Exit early if stop was pressed
                break

            self.countdown_label["text"] = "Countdown: 15"  # Reset countdown label
            self.countdown_progress["value"] = 0  # Reset progress bar
            current_x, current_y = pyautogui.position()

            # Jitter the mouse position slightly
            for _ in range(5):  # Repeat to ensure activity
                pyautogui.moveTo(current_x + 1, current_y + 1)
                time.sleep(0.1)
                pyautogui.moveTo(current_x - 1, current_y - 1)
                time.sleep(0.1)
                pyautogui.press('shift')

        self.status_label["text"] = "Status: Idle"
        self.countdown_label["text"] = "Countdown: 15"  # Reset countdown label
        self.countdown_progress["value"] = 0  # Reset progress bar




root = tk.Tk()
app = MouseMovementApp(root)
root.mainloop()