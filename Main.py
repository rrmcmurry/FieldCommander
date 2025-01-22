from FieldCommander import FieldCommander

def on_button_press(buttonname, data, ui):
    action = data["action"]

    match action:
        case "select_barge":
            level = data["level"]
            ui.update_objectives_display("Barge")
            ui.update_elevator_display(f"Barge level {level}")
        case "select_processor":
            level = data["level"]
            ui.update_elevator_display(f"Processor level {level}")            
            ui.update_objectives_display("Processor")
        case "select_reef":                                    
            ui.update_objectives_display(f"{buttonname}")
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
            ui.update_objectives_display(f"{side} coral station")
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
