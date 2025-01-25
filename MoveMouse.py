import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import time
from PIL import Image, ImageTk
from threading import Thread
import ctypes


class MouseMovementApp:
    def __init__(self, master):
        self.master = master
        master.title("Move Mouse")
        master.geometry("400x500")

        # Configure rows and columns to center the content
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(10, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)

        # Menu bar
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)

        # Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="How to Use", command=self.show_help)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # Theme Menu
        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.theme_menu.add_command(label="Light Theme", command=self.set_light_theme)
        self.theme_menu.add_command(label="Dark Theme", command=self.set_dark_theme)
        self.menu_bar.add_cascade(label="Theme", menu=self.theme_menu)

        # Set initial theme
        self.style = ttk.Style(master)

        self.welcome_label = ttk.Label(master, text="Welcome to Move Mouse!", font=("Helvetica", 12, "bold"))
        self.welcome_label.grid(row=1, column=0, columnspan=3, pady=(20, 10))

        # Add image below the welcome label
        self.image = Image.open("assets/mouse.png")  # Use your image file here
        self.image = self.image.resize((100, 100))  # Resize image as needed
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = ttk.Label(master, image=self.photo)
        self.image_label.grid(row=2, column=0, columnspan=3, pady=(10, 20))

        self.start_button = ttk.Button(master, text="Start", command=self.start_mouse_movement)
        self.stop_button = ttk.Button(master, text="Stop", command=self.stop_mouse_movement)
        self.status_label = ttk.Label(master, text="Status: Idle")

        self.start_button.grid(row=3, column=0, columnspan=3, pady=(10, 5))
        self.stop_button.grid(row=4, column=0, columnspan=3, pady=(5, 20))
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)

        # Countdown progress bar
        self.countdown_progress = ttk.Progressbar(master, length=200, mode="determinate")
        self.countdown_progress.grid(row=6, column=0, columnspan=3, pady=10)

        # Slider for countdown timer
        self.min_label = ttk.Label(master, text="5", width=3)
        self.min_label.grid(row=7, column=0, sticky="e", padx=(0, 5))
        self.countdown_slider = ttk.Scale(master, from_=5, to=55, orient="horizontal", command=self.update_countdown_label)
        self.countdown_slider.set(15)  # Default value
        self.countdown_slider.grid(row=7, column=1, sticky="we", padx=(5, 5))
        self.max_label = ttk.Label(master, text="55", width=3)
        self.max_label.grid(row=7, column=2, sticky="w", padx=(5, 0))

        # Countdown label
        self.countdown_label = ttk.Label(master, text=f"Countdown: {int(self.countdown_slider.get())}")
        self.countdown_label.grid(row=8, column=0, columnspan=3, pady=10)

        self.mouse_movement_thread = None
        self.is_running = False
        self.set_light_theme()

    def set_light_theme(self):
        """Apply the light theme."""
        self.style.theme_use("default")
        self.style.configure("TLabel", background="white smoke", foreground="black")
        self.style.configure("TButton", background="white smoke", foreground="black")
        self.style.configure(
        "Custom.Horizontal.TProgressbar",
        troughcolor="lightgray",
        background="lime green",
        thickness=20,
    )
    
        # Configure slider (scale) styles
        self.style.layout(
            "Custom.TScale",
            [
                ("Scale.trough", {"sticky": "we"}),
                ("Scale.slider", {"side": "left", "sticky": ""}),
            ],
        )
        self.style.configure(
            "Custom.TScale",
            troughcolor="blue",
            sliderthickness=15,
            sliderlength=30,
            background="white smoke",
        )

        # Apply styles to specific widgets
        self.countdown_progress.configure(style="Custom.Horizontal.TProgressbar")
        self.countdown_slider.configure(style="Custom.TScale")
        self.master.configure(bg="white smoke")

    def set_dark_theme(self):
        """Apply the dark theme."""
        self.style.theme_use("default")
        self.style.configure("TLabel", background="black", foreground="white")
        self.style.configure("TButton", background="white", foreground="black")
        self.style.configure(
        "Custom.Horizontal.TProgressbar",
        troughcolor="lightgray",
        background="lime green",
        thickness=20,
    )
    
        # Configure slider (scale) styles
        self.style.layout(
            "Custom.TScale",
            [
                ("Scale.trough", {"sticky": "we"}),
                ("Scale.slider", {"side": "left", "sticky": ""}),
            ],
        )
        self.style.configure(
            "Custom.TScale",
            troughcolor="red",
            sliderthickness=15,
            sliderlength=30,
            background="black",
        )

        # Apply styles to specific widgets
        self.countdown_progress.configure(style="Custom.Horizontal.TProgressbar")
        self.countdown_slider.configure(style="Custom.TScale")
        self.master.configure(bg="#000000")

    def show_help(self):
        """Display the Help information."""
        messagebox.showinfo(
            "How to Use Move Mouse",
            "1. Set the countdown duration using the slider (5-55 seconds).\n"
            "2. Click 'Start' to begin mouse movement.\n"
            "3. The app prevents your system from going idle.\n"
            "4. Click 'Stop' to halt the mouse movement at any time."
        )

    def show_about(self):
        """Display the About information."""
        messagebox.showinfo(
            "About Move Mouse",
            "Move Mouse App\n"
            "Version: 1.0\n"
            "Author: Vasil Velinov\n"
            "Description: A simple tool to keep your system active by periodically moving the mouse."
        )

    def update_countdown_label(self, value):
        """Update the countdown label dynamically based on slider position."""
        if hasattr(self, 'countdown_label'):
            self.countdown_label["text"] = f"Countdown: {int(float(value))}"

    def start_mouse_movement(self):
        self.stop_flag = False  # Reset the stop flag when starting
        self.status_label["text"] = "Status: Running"
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)  # Prevent display and system sleep
        self.is_running = True
        self.mouse_movement_thread = Thread(target=self.move_mouse)
        self.mouse_movement_thread.start()

    def stop_mouse_movement(self):
        self.status_label["text"] = "Status: Stopped"
        ctypes.windll.kernel32.SetThreadExecutionState(0x00000002)  # Revert sleep prevention
        self.is_running = False
        self.stop_flag = True  # Set the flag to stop countdown and movement

    def move_mouse(self):
        countdown_time = int(self.countdown_slider.get())  # Get countdown time from slider
        while self.is_running:
            for countdown in range(countdown_time, 0, -1):
                if self.stop_flag:  # Check if stop flag is set, and break the loop immediately
                    break
                self.countdown_label["text"] = f"Countdown: {countdown}"
                self.countdown_progress["value"] = (countdown / countdown_time) * 100
                self.master.update()
                time.sleep(1)
                
            if self.stop_flag:  # Exit early if stop was pressed
                break

            self.countdown_label["text"] = f"Countdown: {countdown_time}"  # Reset countdown label
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
        self.countdown_label["text"] = f"Countdown: {countdown_time}"  # Reset countdown label
        self.countdown_progress["value"] = 0  # Reset progress bar


root = tk.Tk()
app = MouseMovementApp(root)
root.mainloop()
