import tkinter as tk
from gpiozero import LED
from time import sleep

# Setup LEDs (all treated as red)
red1 = LED(17)
red2 = LED(27)
red3 = LED(22)

# Make sure all LEDs are OFF at startup
red1.off()
red2.off()
red3.off()
sleep(0.1)

def turn_on(color):
    # Turn all off first
    red1.off()
    red2.off()
    red3.off()

    # Turn red3 ON no matter which button
    red3.on()

# GUI Setup
root = tk.Tk()
root.title("LED Controller")

choice = tk.StringVar(value="")  # no default selection

tk.Label(root, text="Select LED:").pack(pady=5)

# Buttons — all control red3
tk.Radiobutton(root, text="Red", variable=choice, value="red", command=lambda: turn_on("red")).pack()
tk.Radiobutton(root, text="Green", variable=choice, value="green", command=lambda: turn_on("green")).pack()
tk.Radiobutton(root, text="Blue", variable=choice, value="blue", command=lambda: turn_on("blue")).pack()

tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
