﻿import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import os
import sys
import json
import ntcore
from PathDrawer import PathDrawer
from UserInterface import buttons


def setredteam():
    red_team()

def setblueteam():
    red_team(False)

def red_team(redteam=True):    
    fieldimage="Images/field-red.png" if redteam else "Images/field-blue.png"
    robotimage = "Images/robotred.png" if redteam else "Images/robotblue.png"    
    robot = ImageTk.PhotoImage(Image.open(robotimage))
    background = ImageTk.PhotoImage(Image.open(fieldimage))
    canvas.itemconfig(robot_icon, image=robot)
    canvas.itemconfig(background_id, image=background)
    canvas.images["robot_image"] = robot
    canvas.images["background_image"] = background
    

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
# Initialize NetworkTables
ntinst = ntcore.NetworkTableInstance.getDefault()
ntinst.startClient4("FieldCommander")
ntinst.setServer("localhost")
ntinst.startDSClient()
pose_table = ntinst.getTable("Pose")
objective_table = ntinst.getTable("Objectives")


redteam = False 
robotimage = "Images/robotred.png" if redteam else "Images/robotblue.png"
fieldimage = "Images/field-red.png" if redteam else "Images/field-blue.png"


# Initialize PathDrawer
path_drawer = PathDrawer(update_interval=0.1)

# Tkinter window setup
root = tk.Tk()
root.title("Reefscape Field Commander")

menubar = Menu(root)
FileMenu = Menu(menubar, tearoff=0)
FileMenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=FileMenu)

TeamColorMenu = Menu(menubar, tearoff=0)
TeamColorMenu.add_command(label="Red Team", command=setredteam)
TeamColorMenu.add_command(label="Blue Team", command=setblueteam)
menubar.add_cascade(label="Team", menu=TeamColorMenu)

root.config(menu=menubar)

canvas_width = 1439
canvas_height = 1050
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Load field background image
background_image = ImageTk.PhotoImage(Image.open(fieldimage))  
background_id = canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Add text overlay to list objectives
# Create a text item for objectives in the lower right corner
objectives_display = canvas.create_text(
    canvas_width - 470, canvas_height - 310,  # Adjust position as needed
    anchor=tk.NW,  # Southeast anchor aligns the text to the bottom-right corner
    text="No objectives set.", fill="white", font=("Arial", 10), justify=tk.LEFT
)
elevator_display = canvas.create_text(
    canvas_width - 470, canvas_height - 210,  # Adjust position as needed
    anchor=tk.NW,  # Southeast anchor aligns the text to the bottom-right corner
    text="No level set.", fill="white", font=("Arial", 10), justify=tk.LEFT
)
canvas.itemconfigure(objectives_display, width=450)
canvas.itemconfigure(elevator_display, width=450)

# Field dimensions (in feet)
field_width = 26.5  # 786 pixels
field_height = 29.5 # 800 pixels

# Scaling factors
scale_x = 800 / field_height  # Scale field height to canvas height
scale_y = 786 / field_width    # Scale field width to canvas width

# Load robot image
robot_base_image = Image.open(robotimage)  # Replace with your robot image path
robot_image = ImageTk.PhotoImage(robot_base_image)
robot_icon = canvas.create_image(0, canvas_height, image=robot_image, anchor=tk.CENTER)


canvas.images = {"background_image": background_image, "robot_image": robot_image}


# Variable to store current orientation (default to 0°)
current_orientation = 0

# Update position of robot image on canvas
def update_robot_position():
    """Periodically update the robot's position and orientation on the canvas."""
    field_x = pose_table.getNumber('X', 0)  # Field height (x -> canvas y)
    field_y = pose_table.getNumber('Y', 0)  # Field width (y -> canvas x)
    z = pose_table.getNumber('Z', current_orientation)  # Orientation (degrees)
    # print(f"Position: ({field_x},{field_y},{z})")

    # Convert field coordinates to canvas coordinates
    canvas_x = field_y * scale_y  # Field width -> Canvas width
    canvas_y = canvas_height - (field_x * scale_x)  # Invert y-axis for canvas

    # Rotate the robot image around its center
    global redteam
    robotimage = "Images/robotred.png" if redteam else "Images/robotblue.png"
    robot_base_image = Image.open(robotimage) 
    rotated_image = robot_base_image.rotate(z, expand=True, resample=Image.BICUBIC)

    # Create a Tkinter-compatible image
    rotated_image_tk = ImageTk.PhotoImage(rotated_image)

    # Center the rotated image on the canvas
    canvas.coords(robot_icon, canvas_x, canvas_y)  # Move icon to the correct position
    canvas.itemconfig(robot_icon, image=rotated_image_tk)
    canvas.image = rotated_image_tk  # Keep a reference to avoid garbage collection

    root.after(100, update_robot_position)


# Update objectives list 
def update_objectives_display(objectives_text):    
    canvas.itemconfig(objectives_display, text=objectives_text)

# Update elevator display
def update_elevator_display(level_text):    
    canvas.itemconfig(elevator_display, text=level_text)

# Send Navigation Command
def send_passthrough_command(path):
    """Send the completed path as a passthrough action."""
    # Simplify the path to reduce the number of points
    lastpoint = path[-1]
    simplified_path = path[::2]  # Sample every 2nd point
 
    # If Path is less than five points, just navigate directly
    if len(path) < 5:
        objective = [{
            "action": "navigate",
            "target": [lastpoint[0], lastpoint[1]],
            "orientation": current_orientation
        }]
    
    # Otherwise, send a passthrough path
    else:
        objective = [{
            "action": "passthrough",
            "path": simplified_path
        },
        {
            "action": "navigate",
            "target": [lastpoint[0], lastpoint[1]],
            "orientation": current_orientation
        },
        {
            "action": "stop"
        }]
    
    # Convert to JSON and send to NetworkTables
    objectives_json = json.dumps(objective)
    objective_table.putString("NewObjectives", objectives_json)
    objective_table.putBoolean("Overwrite", True)
    update_objectives_display(f"{objectives_json}")
    print(f"Sent: {objectives_json}")



# Check whether a point is within a polygon
def is_point_in_polygon(x, y, polygon_coords):
    n = len(polygon_coords) // 2
    inside = False    
    p1x, p1y = polygon_coords[0], polygon_coords[1]
    for i in range(n):
        p2x, p2y = polygon_coords[2 * (i + 1) % (n*2)], polygon_coords[2 * (i + 1) % (n*2) + 1]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1y == p2y or x <= x_inters:
                        inside = not inside
        p1x, p1y, = p2x, p2y
    return inside


# Button actions
def buttonpressed(name):
    button = buttons.get(name)
    action = button.get("action")
    team = 1 if redteam else 0

    if action == "select_barge":        
        apriltagID = button.get("apriltag")[team]
        update_objectives_display(f"Navigate to Barge\nAprilTag: {apriltagID}")      
        update_elevator_display("Set elevator to Endgame level")     
    elif action == "select_processor": 
        apriltagID = button.get("apriltag")[team]
        update_objectives_display(f"Navigate to Processor\nAprilTag: {apriltagID}") 
        update_elevator_display("Set elevator to Processor level")          
    elif action == "select_coralstation":
        side = button.get("side")        
        apriltagID = button.get("apriltag")[team]
        update_objectives_display(f"Navigate to {side} side Coral Station\nAprilTag: {apriltagID}")   
        update_elevator_display("Set elevator to Coral Station level")
    elif action == "select_reef":               
        apriltagID = button.get("apriltag")[team]
        update_objectives_display(f"Navigate to {name}\nAprilTag: {apriltagID}")   
    elif action == "select_coral_level":
        level = button.get("level")
        side = button.get("side")
        if level > 1:
            update_elevator_display(f"Set elevator to level {level} and aim for {side} side")
        else:
            update_elevator_display(f"Set elevator to level {level}")
    elif action == "select_algae_level":
        level = button.get("level")
        update_elevator_display(f"Set elevator to level {level} and engage algae intake")
    elif action == "clearobjectives":
        update_objectives_display("")
        update_elevator_display("")
        


    
def on_mouse_press(event):
    x, y = event.x, event.y

    # Check if mouse pressed a button
    for name, area in buttons.items():
        if is_point_in_polygon(x, y, area["coords"]):
            # print(f"{name} clicked!")            
            buttonpressed(name)
            return
    # Check if mouse pressed in the arena
    if is_point_in_polygon(x,y, [56, 150, 842, 150, 842, 950, 56, 950]):
        """Start drawing the path on left mouse button press."""
        field_y = event.x / scale_y
        field_x = (canvas_height - event.y) / scale_x
        path_drawer.start_drawing((field_x, field_y))

def on_mouse_drag(event):
    """Update the path as the mouse moves."""
    field_y = event.x / scale_y
    field_x = (canvas_height - event.y) / scale_x
    path_drawer.update_path((field_x, field_y))
    draw_path(path_drawer.path)  # Visualize the path

def on_mouse_release(event):
    """Send the completed path as a passthrough action."""
    completed_path = path_drawer.stop_drawing()
    if completed_path:
        send_passthrough_command(completed_path)
        canvas.delete("path")  # Clear the drawn path

def draw_path(path):
    """Draw the path on the canvas."""
    canvas.delete("path")  # Remove old path
    for i in range(len(path) - 1):
        x1, y1 = path[i][1] * scale_y, canvas_height - (path[i][0] * scale_x)
        x2, y2 = path[i + 1][1] * scale_y, canvas_height - (path[i + 1][0] * scale_x)
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2, tags="path")



# Define clickable areas (e.g. coral, algae, reef segments, levels)
for name, area in buttons.items():
    canvas.create_polygon(area["coords"], fill="", outline="blue", tags=(name, "clickable"))


# Bind mouse clicks to set navigation objectives
canvas.bind("<Button-1>", on_mouse_press)  # Start drawing
canvas.bind("<B1-Motion>", on_mouse_drag)  # Continue drawing
canvas.bind("<ButtonRelease-1>", on_mouse_release)  # Finalize and send


# Start tracking robot position
update_robot_position()
root.mainloop()
