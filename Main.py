import tkinter as tk
from PIL import Image, ImageTk


redteam=False

root = tk.Tk()
root.title("Reefscape Field Commander")
canvas = tk.Canvas(root, width=1439, height=1050)
canvas.pack()
fieldimage = "Images/field-red.png" if redteam else "Images/field-blue.png"
background = ImageTk.PhotoImage(Image.open(fieldimage))
background_id = canvas.create_image(0,0, anchor=tk.NW, image=background)
objectives_text = canvas.create_text(969, 740, anchor=tk.NW, text="test", fill="white", font=("Arial", 10), width=450)
elevator_text = canvas.create_text(969, 840, anchor=tk.NW, text="test", fill="white", font=("Arial", 10), width=450)

def on_mouse_press(event):
    global redteam
    redteam = not(redteam)
    fieldimage="Images/field-red.png" if redteam else "Images/field-blue.png"    
    background = ImageTk.PhotoImage(Image.open(fieldimage))
    canvas.itemconfig(background_id, image=background)
    canvas.image = background


canvas.bind("<Button-1>", on_mouse_press)

root.mainloop()



