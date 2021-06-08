import tkinter as tk
win = tk.Tk()

def changetext():
	a.config(text="changed text!")

a = tk.Label(win, text="hello world").pack()
tk.Button(win, text="Change Label Text", command=changetext).pack()

win.mainloop()