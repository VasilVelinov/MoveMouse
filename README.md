# **Move Mouse App**

A lightweight Python application designed to simulate mouse movement and prevent the system from going idle. Ideal for scenarios where you need to keep your system active during long tasks, presentations, or video calls.

---

## **Features**
- ✨ **Customizable Radius and Speed**: Adjust the radius of movement and speed of the mouse to suit your needs.
- 🖱️ **Idle Prevention**: Keeps your system awake and active without manual interaction.
- 💻 **Graphical User Interface (GUI)**: Intuitive and easy-to-use interface built with `tkinter`.
- ⏱️ **Countdown Timer**: Displays a countdown before initiating mouse movement.
- 🛡️ **Sleep Prevention**: Uses Windows API to prevent the system from entering sleep mode while active.
- ✅ **Safe Operation**: Avoids accidental mouse clicks or intrusive activity.

---

## **Requirements**
- **Python**: 3.7 or later
- **Libraries**:
  - `tkinter`
  - `pyautogui`
  - `math`
  - `threading`

---

## **Usage**
1. Clone the repository:

2. Navigate to directory
   ```bash
   cd MoveMouse
   ```
3. Install needed requirements
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app
   ```bash
   python mouse_app.py
   ```
   
