﻿import tkinter as tk
from PIL import Image, ImageTk
from networktables import NetworkTables
import json

# Initialize NetworkTables
NetworkTables.initialize(server='roborio-9668-frc.local')  # Replace with your team number
objective_table = NetworkTables.getTable('Objectives')

# Tkinter window setup
root = tk.Tk()
root.title("FieldCommander")
canvas_width = 500
canvas_height = 1000
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Load field background image
field_image = ImageTk.PhotoImage(file="field.png")  # Replace with your field image path
canvas.create_image(0, 0, anchor=tk.NW, image=field_image)

# Field dimensions (in feet)
field_width = 10
field_height = 20

# Scaling factors
scale_x = canvas_height / field_height  # Scale field height to canvas height
scale_y = canvas_width / field_width    # Scale field width to canvas width

# Load robot image
robot_base_image = Image.open("robot.png")  # Replace with your robot image path
robot_image = ImageTk.PhotoImage(robot_base_image)
robot_icon = canvas.create_image(0, canvas_height, image=robot_image, anchor=tk.SW)

# List to store current objectives
current_objectives = []

# Variable to store current orientation (default to 0°)
current_orientation = 0


def update_robot_position():
    """Periodically update the robot's position and orientation on the canvas."""
    robot_table = NetworkTables.getTable('RobotData')
    field_x = robot_table.getNumber('x', 0)  # Field height (x -> canvas y)
    field_y = robot_table.getNumber('y', 0)  # Field width (y -> canvas x)
    z = robot_table.getNumber('z', current_orientation)  # Orientation (degrees)

    # Convert field coordinates to canvas coordinates
    canvas_x = field_y * scale_y  # Field width -> Canvas width
    canvas_y = canvas_height - (field_x * scale_x)  # Invert y-axis for canvas

    # Update position
    canvas.coords(robot_icon, canvas_x, canvas_y)

    # Rotate robot image
    rotated_image = robot_base_image.rotate(-z)  # Rotate counterclockwise
    rotated_image_tk = ImageTk.PhotoImage(rotated_image)
    canvas.itemconfig(robot_icon, image=rotated_image_tk)
    canvas.image = rotated_image_tk  # Keep a reference to avoid garbage collection

    root.after(100, update_robot_position)


def set_target(event, overwrite=False):
    """Handle clicks to set navigation objectives."""
    global current_orientation

    # Translate canvas coordinates to field coordinates
    field_y = event.x / scale_y  # Canvas width -> Field width
    field_x = (canvas_height - event.y) / scale_x  # Canvas height -> Field height

    # Create a navigation objective
    objective = {"action": "navigate", "target": [field_x, field_y], "orientation": current_orientation}

    if overwrite:
        # Overwrite the entire objectives queue
        current_objectives.clear()
        current_objectives.append(objective)
        print(f"Overwritten objectives with: {objective}")
    else:
        # Append to the objectives queue
        current_objectives.append(objective)
        print(f"Appended objective: {objective}")

    # Upload objectives to NetworkTables
    upload_objectives(overwrite)


def change_orientation(event):
    """Handle keyboard arrow keys to change the robot's orientation."""
    global current_orientation

    if event.keysym == "Up":
        current_orientation = 0
    elif event.keysym == "Right":
        current_orientation = 90
    elif event.keysym == "Down":
        current_orientation = 180
    elif event.keysym == "Left":
        current_orientation = 270

    print(f"Orientation changed to: {current_orientation}°")


def upload_objectives(overwrite):
    """Upload the current objectives to NetworkTables."""
    if not current_objectives:
        print("No objectives to upload.")
        return

    # Convert objectives to JSON
    objectives_json = json.dumps(current_objectives)

    # Send to NetworkTables
    objective_table.putString("NewObjectives", objectives_json)
    objective_table.putBoolean("Overwrite", overwrite)
    print(f"Uploaded objectives: {objectives_json} (Overwrite: {overwrite})")


# Bind mouse clicks to set navigation objectives
canvas.bind("<Button-1>", lambda event: set_target(event, overwrite=True))  # Left-click to overwrite
canvas.bind("<Button-3>", lambda event: set_target(event, overwrite=False)) # Right-click to append

# Bind arrow keys for orientation adjustment
root.bind("<Up>", change_orientation)
root.bind("<Right>", change_orientation)
root.bind("<Down>", change_orientation)
root.bind("<Left>", change_orientation)

# Start tracking robot position
update_robot_position()
root.mainloop()
