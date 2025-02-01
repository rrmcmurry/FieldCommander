import ntcore
import json

class ObjectiveManager:
    def __init__(self):
        self.ntinst = ntcore.NetworkTableInstance.getDefault()            
        self.GameTable = self.ntinst.getTable('GameManager')
        self.ObjectivesTable = self.ntinst.getTable('Objectives')
        self.currentobjectives = self.ObjectivesTable.getString('CurrentObjectives',"")

    def set_current_objective(self, data, team): 

        action = data["action"]

        objective = []

        try:
            orientation = data["orientation"]
            location = data["location"]
            navigation = {"action":"navigate", "target": location, "orientation": orientation}
            objective.append(navigation)
        except:
            pass

        try:
            tagid = data["apriltag"][team]
            align = {"action":"align", "tag_id": tagid}
            objective.append(align)
        except:
            pass


        if action == "clearobjectives":
            
            self.ObjectivesTable.putString("NewObjectives", json.dumps([{"action":"wait"}]))
            self.ObjectivesTable.putBoolean("Overwrite", True)

        else:
            objectives_json = json.dumps(objective)
            self.ObjectivesTable.putString("NewObjectives", objectives_json)
            self.ObjectivesTable.putBoolean("Overwrite", False)

        

    

