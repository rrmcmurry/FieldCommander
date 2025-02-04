import subprocess
import os
from src import (
    FieldCommander,
    ObjectiveManager
    )



def on_button_press(buttonname, data, ui, om):
    action = data["action"]
    tag = 1 if ui.redteam else 0
    om.set_current_objective(data, tag)
    
    
    
def on_mouse_press(event, ui, om):
    buttonpressed, buttonname, data = ui.buttonpressed_name(event)
    if buttonpressed:
        on_button_press(buttonname, data, ui, om)
    else:
        ui.update_objectives_display("No button pressed")
        ui.update_elevator_display("")


def main():
    ui = FieldCommander()
    om = ObjectiveManager()
    ui.bind_event("<Button-1>", lambda event: on_mouse_press(event, ui, om))
    ui.update_robot_position()
    path = os.path.abspath("src/WestPi.py")
    autonomousdriver = subprocess.Popen(["python", path])
    ui.run()

if __name__ == "__main__":
    main()
