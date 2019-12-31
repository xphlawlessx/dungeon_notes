from pynput import keyboard
import tkinter as tk
import win32gui
from random import randint, random
import threading
import time


def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == "f12":  # keys interested
        show_window()


def read_macro(_macro, _label):
    if(len(_macro) < 3):
        _label.config(text=randint(1, 20))
    else:
        _tMac = _macro.lower()
        _sMacro = _tMac.split()
        _sDice = _sMacro[0].split('d')
        total = 0
        dieList = []
        for x in range(int(_sDice[0])):
            die = randint(1, int(_sDice[1]))
            total += die
            dieList.append(die)
        if(len(_sMacro) > 1):
            total += int(_sMacro[1])
        _label.config(text=str(total)+'\n'+str(dieList))


def destroy_window(_window):
    _window.destroy()


def show_window():
    root = tk.Tk()
    root.title("Macro")
    root.attributes("-topmost", True)
    _entry = tk.Entry(root, font=("Calibri", 30), justify="center")
    _label = tk.Label(root, font=("Calibri", 30), justify="center")
    _entry.pack()
    _entry.bind('<Return>', (lambda event: read_macro(_entry.get(), _label)))
    _entry.bind('<Escape>', destroy_window)
    _entry.focus_set()
    _label.pack()
    board = keyboard.Controller()
    board.press(keyboard.Key.alt)
    win32gui.SetForegroundWindow(root.winfo_id())
    board.release(keyboard.Key.alt)
    root.mainloop()


def run():
    random()
    lis = keyboard.Listener(on_press=on_press)
    lis.start()
    lis.join()
    time.sleep(0.2)


def start():
    x = threading.Thread(target=run)
    x.start()


if __name__ == "__main__":
    start()
