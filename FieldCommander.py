import tkinter as tk
from PIL import Image, ImageTk
import json
import ntcore
from PathDrawer import PathDrawer


redteam=False
robotimage = "robotred.png" if redteam else "robotblue.png"
fieldimage = "field-red.png" if redteam else "field-blue.png"

# Initialize NetworkTables
ntinst = ntcore.NetworkTableInstance.getDefault()
ntinst.startClient4("FieldCommander")
ntinst.setServer("localhost")

pose_table = ntinst.getTable("Pose")
objective_table = ntinst.getTable("Objectives")
path_drawer = PathDrawer(update_interval=0.1)

# Tkinter window setup
root = tk.Tk()
root.title("FieldCommander")
canvas_width = 1439
canvas_height = 1050
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Load field background image
field_base_image = Image.open(fieldimage)
field_image = ImageTk.PhotoImage(field_base_image)  
canvas.create_image(0, 0, anchor=tk.NW, image=field_image)

# Field dimensions (in feet)
field_width = 10
field_height = 20

# Scaling factors
scale_x = canvas_height / field_height  # Scale field height to canvas height
scale_y = canvas_width / field_width    # Scale field width to canvas width

# Load robot image
robot_base_image = Image.open(robotimage)  # Replace with your robot image path
robot_image = ImageTk.PhotoImage(robot_base_image)
robot_icon = canvas.create_image(0, canvas_height, image=robot_image, anchor=tk.CENTER)

clickable_areas = {
    "barge":{
        "coords": [0, 0, 959, 0, 959, 176, 0, 176],
        "action": "select_barge",
        "apriltag": [ 14, 5]
    },
    "processor":{
        "coords": [829, 177, 959, 177, 959, 400, 829, 400],
        "action": "select_processor",
        "apriltag": [ 16, 3]
    },
    "reef2oclock":{
        "coords": [449, 508, 515, 398, 578, 508],
        "action": "select_reef",
        "apriltag": [ 22, 9]        
    },
    "reef4oclock":{
        "coords": [449, 508, 578, 508, 515, 623],
        "action": "select_reef",
        "apriltag": [ 17, 8]            
    },
    "reef6oclock":{
        "coords": [449, 508, 515, 623, 383, 623],
        "action": "select_reef",
        "apriltag": [ 18, 7]            
    },    
    "reef8oclock":{
        "coords": [449, 508, 383, 623, 318, 508],
        "action": "select_reef",
        "apriltag": [ 19, 6]            
    },
    "reef10oclock":{
        "coords": [449, 508, 318, 508, 382, 398],
        "action": "select_reef",
        "apriltag": [ 20, 11]            
    },
    "reef12oclock":{
        "coords": [449, 508, 382, 398, 515, 398],
        "action": "select_reef",
        "apriltag": [ 21, 10]            
    },
    "corallevel4left":{
        "coords": [959, 0, 1193, 0, 1193, 234, 959, 234],
        "action": "select_coral_level",
        "level": 4,
        "side": "left"
    },
    "corallevel4right":{
        "coords": [1193, 0, 1440, 0, 1440, 234, 1193, 234],
        "action": "select_coral_level",
        "level": 4,
        "side": "right"
    },
    "corallevel3left":{
        "coords": [959, 234, 1132, 234, 1132, 460, 959, 460],
        "action": "select_coral_level",
        "level": 3,
        "side": "left"
    },
    "corallevel3right":{
        "coords": [1260, 234, 1440, 234, 1440, 460, 1260, 460],
        "action": "select_coral_level",
        "level": 3,
        "side": "right"
    },
    "corallevel2left":{
        "coords": [959, 460, 1132, 460, 1132, 622, 959, 622],
        "action": "select_coral_level",
        "level": 2,
        "side": "left"
    },
    "corallevel2right":{
        "coords": [1260, 460, 1440, 460, 1440, 622, 1260, 622],
        "action": "select_coral_level",
        "level": 2,
        "side": "right"
    },
    "corallevel1":{
        "coords": [959, 622, 1440, 622, 1440, 720, 959, 720],
        "action": "select_coral_level",
        "level": 1,
        "side": "left"
    },
    "algaelevel3":{
        "coords": [1132, 234, 1260, 234, 1260, 414, 1132, 414],
        "action": "select_algae_level",
        "level": 3        
    },
    "algaelevel2":{
        "coords": [1132, 414, 1260, 414, 1260, 622, 1132, 622],
        "action": "select_algae_level",
        "level": 2        
    },
    "coralstationleft":{
        "coords": [0, 782, 55, 782, 183, 953, 183, 1050, 0, 1050],
        "action": "select_coralstation",
        "side": "left",
        "apriltag": [ 13, 1]            
    },
    "coralstationright":{
        "coords": [719, 1050, 719, 953, 838, 782, 959, 782, 959, 1050],
        "action": "select_coralstation",
        "side": "right",
        "apriltag": [ 12, 2]            
    },
    "clearbutton":{
        "coords": [959, 967, 1440, 967, 1440, 1050, 959, 1050],
        "action": "clearobjectives"
    }

}





# List to store current objectives
current_objectives = []

# Variable to store current orientation (default to 0°)
current_orientation = 0


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
    rotated_image = robot_base_image.rotate(z, expand=True, resample=Image.BICUBIC)

    # Create a Tkinter-compatible image
    rotated_image_tk = ImageTk.PhotoImage(rotated_image)

    # Center the rotated image on the canvas
    canvas.coords(robot_icon, canvas_x, canvas_y)  # Move icon to the correct position
    canvas.itemconfig(robot_icon, image=rotated_image_tk)
    canvas.image = rotated_image_tk  # Keep a reference to avoid garbage collection

    root.after(100, update_robot_position)





def set_target(event, overwrite):
    """Handle clicks to set navigation objectives."""
    global current_orientation

    # Translate canvas coordinates to field coordinates
    field_y = event.x / scale_y  # Canvas width -> Field width
    field_x = (canvas_height - event.y) / scale_x  # Canvas height -> Field height

    # Create a navigation objective
    objective = {"action": "navigate", "target": [field_x, field_y], "orientation": current_orientation}
    current_objectives.clear()
    current_objectives.append(objective)
    
    
    # Upload objectives to NetworkTables
    upload_objectives(overwrite)


def change_orientation(event):
    """Handle keyboard arrow keys to change the robot's orientation."""
    global current_orientation

    if event.keysym == "Up":
        current_orientation = 0
    elif event.keysym == "Right":
        current_orientation = 270
    elif event.keysym == "Down":
        current_orientation = 180
    elif event.keysym == "Left":
        current_orientation = 90

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
    print(f"Objectives: {objectives_json} (Overwrite: {overwrite})")

def send_passthrough_command(path):
    """Send the completed path as a passthrough action."""
    # Simplify the path to reduce the number of points
    lengthofpath = len(path)
    
    lastpoint = path[-1]
    simplified_path = path[::2]  # Sample every 2nd point
    if len(path) < 5:
        objective = [{
            "action": "navigate",
            "target": [lastpoint[0], lastpoint[1]],
            "orientation": current_orientation
        }]
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
    print(f"Sent: {objectives_json}")
    
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

def buttonpressed(name):
    button = clickable_areas.get(name)
    action = button.get("action")
    team = 1 if redteam else 0

    if action == "select_barge":
        print("navigate to barge")
        apriltagID = button.get("apriltag")[team]
        print(f"AprilTag: {apriltagID}")  
        print("endgame")
    elif action == "select_processor": 
        apriltagID = button.get("apriltag")[team]
        print(f"AprilTag: {apriltagID}")       
        print("navigate to processor")
        print("algaeoutput")
    elif action == "select_coralstation":
        side = button.get("side")
        print(f"navigate to {side} coralstation")
        apriltagID = button.get("apriltag")[team]
        print(f"AprilTag: {apriltagID}")  
    elif action == "select_reef":       
        print(f"Navigate to reef {name}")
        apriltagID = button.get("apriltag")[team]
        print(f"AprilTag: {apriltagID}")  
    elif action == "select_coral_level":
        level = button.get("level")
        side = button.get("side")
        print(f"Update - Set elevator to level {level} and aim for {side} side")
    elif action == "select_algae_level":
        level = button.get("level")
        print(f"Update command - Set elevator to level {level} and engage algae intake")
    elif action == "clearobjectives":
        print("Clear objectives")
    



def on_mouse_press(event):
    x, y = event.x, event.y
    for name, area in clickable_areas.items():
        if is_point_in_polygon(x, y, area["coords"]):
            # print(f"{name} clicked!")            
            buttonpressed(name)
            return

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
for name, area in clickable_areas.items():
    canvas.create_polygon(area["coords"], fill="", outline="blue", tags=(name, "clickable"))


# Bind mouse clicks to set navigation objectives
canvas.bind("<Button-1>", on_mouse_press)  # Start drawing
canvas.bind("<B1-Motion>", on_mouse_drag)  # Continue drawing
canvas.bind("<ButtonRelease-1>", on_mouse_release)  # Finalize and send




# Bind arrow keys for orientation adjustment
root.bind("<Up>", change_orientation)
root.bind("<Right>", change_orientation)
root.bind("<Down>", change_orientation)
root.bind("<Left>", change_orientation)

# Start tracking robot position
update_robot_position()
root.mainloop()
