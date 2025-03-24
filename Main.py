from FieldCommander import FieldCommander


def on_button_press(buttonname, data, ui):
    action = data["action"]
    tag = 1 if ui.redteam else 0
    team = 0 if ui.redteam else 1

    match action:
        case "select_barge":
            tagid = data["apriltag"][team]
            orientation = data["orientation"]
            location = data["location"]
            objective = [
                {"action":"navigate", "target": location, "orientation": orientation},
                {"action":"align", "tag_id": tagid }
            ]
            ui.update_objectives_display(f"{objective}")            
            level = data["level"]
            ui.update_elevator_display(f"Barge level {level}")
        case "select_processor":
            tagid = data["apriltag"][team]
            orientation = data["orientation"]
            objective = [
                {"action":"navigate", "target": location, "orientation": orientation},
                {"action":"align", "tag_id": tagid }
            ]
            ui.update_elevator_display(f"Processor level {level}")    
            level = data["level"]            
            ui.update_objectives_display("Processor")
        case "select_reef":
            tagid = data["apriltag"][team]
            orientation = data["orientation"]
            location = data["location"]
            objective = [
                {"action":"navigate", "target": location, "orientation": orientation},
                {"action":"align", "tag_id": tagid }
            ]
            ui.update_objectives_display(f"{objective}")
        case "select_coralstation":
            side = data["side"]
            level = data["level"] 
            
            ui.update_objectives_display(f"{side} coral station")
            ui.update_elevator_display(f"Supply level {level}")  

        case "select_coral_level":
            level = data["level"]
            side = data["side"]
            if level > 1:
                ui.update_elevator_display(f"Coral level {level}, {side} side")
            else:
                ui.update_elevator_display(f"Coral level {level}")
        case "select_algae_level":
            level = data["level"]
            ui.update_elevator_display(f"Algae level {level}")
        case "select_coralstation":
            side = data["side"]
            level = data["level"]            
            ui.update_objectives_display(f"{side} coral station")
            ui.update_elevator_display(f"Supply level {level}")   

            ui.update_elevator_display(f"Algae level {level}") 
        case "clearobjectives":
            ui.update_objectives_display("")
        case _:
            ui.update_objectives_display("ERROR")



    
def on_mouse_press(event, ui):
    buttonpressed, buttonname, data = ui.buttonpressed_name(event)
    if buttonpressed:
        on_button_press(buttonname, data, ui)
    else:
        ui.update_objectives_display("No button pressed")
        ui.update_elevator_display("")


def main():
    ui = FieldCommander()
    ui.bind_event("<Button-1>", lambda event: on_mouse_press(event, ui))
    ui.update_robot_position()
    ui.run()

if __name__ == "__main__":
    main()
