import sys
print(sys.path)

try:
    # Python2
    import Tkinter as tk
    import ttk
except ImportError:
    # Python3
    import tkinter as tk
    import tkinter.ttk as ttk
window = tk.Tk()
button = ttk.Button(window, text='hi')
button.pack()
window.mainloop()

