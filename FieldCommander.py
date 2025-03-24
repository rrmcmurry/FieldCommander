import tkinter as tk
from PIL import Image, ImageTk

class FieldCommander:

    def __init__(self):
        # Initialize App
        self.root = tk.Tk()
        self.root.title("Reefscape Field Commander")    
        self.canvas = tk.Canvas(self.root, width=1439, height=1050)
        self.canvas.pack()

        # Menu
        self.__init_menu()

        # Team
        self.redteam = False

        # Background
        self.background_image = ImageTk.PhotoImage(Image.open("Images/field-blue.png"))
        self.background_id = self.canvas.create_image(0,0, anchor=tk.NW, image=self.background_image)

        # Robot
        self.robot_base_image = Image.open("Images/robotblue.png")
        self.robot_image = ImageTk.PhotoImage(self.robot_base_image)
        self.robot_id = self.canvas.create_image(140, 210, image=self.robot_image, anchor=tk.CENTER)

        # Images
        self.canvas.images= {"background_image": self.background_image, "robot_image": self.robot_image}

        # Text Areas
        self.objectives_text = self.canvas.create_text(969, 740, anchor=tk.NW, text="", fill="white", font=("Arial", 10), width=450)
        self.elevator_text = self.canvas.create_text(969, 840, anchor=tk.NW, text="", fill="white", font=("Arial", 10), width=450)
        
        # Buttons
        self.__init_buttons()

    # Public Functions
    # ~~~~~~~~~~~~~~~~~
        
    def update_robot_position(self):
        robot=self.robot_base_image
        self.canvas.coords(self.robot_image, 150, 300)  
        self.canvas.itemconfig(self.robot_image, image=robot)
        self.canvas.images["robot_image"] = robot 
        self.root.after(100, self.update_robot_position)

    def update_objectives_display(self, objectives_text):    
        self.canvas.itemconfig(self.objectives_text, text=objectives_text)

    def update_elevator_display(self, level_text):    
        self.canvas.itemconfig(self.elevator_text, text=level_text)

    def get_redteam(self):
        return self.redteam

    def bind_event(self, event, event_handler):
        self.canvas.bind(event, event_handler)

    def run(self):
        self.root.mainloop()

    def buttonpressed_name(self, event):
        x,y = event.x, event.y
        for key, data in self.buttons.items():
            if self.__is_point_in_polygon(x, y, data["coords"]):
                return True, key, data
        return False, None, None


    # Private Functions
    # ~~~~~~~~~~~~~~~~~

    def __init_buttons(self):
        self.buttons =  {
            "barge":{
                "coords": [0, 0, 959, 0, 959, 176, 0, 176],
                "action": "select_barge",
                "apriltag": [ 14, 5],
                "orientation": 0,
                "level": 0,
                "location": (29, 4),
                "level": 0,
                "location": (0, 5)
            },
            "processor":{
                "coords": [829, 177, 959, 177, 959, 400, 829, 400],
                "action": "select_processor",
                "apriltag": [ 16, 3],
                "orientation": 90,
                "level": 0,
                "location": (23, 25),
                "level": 0,
                "location": (3, 10)
            },
            "reef2oclock":{
                "coords": [449, 508, 515, 398, 578, 508],
                "action": "select_reef",
                "apriltag": [ 22, 9],
                "orientation": 240,
                "location": (20.2, 19.5),
                "orientation": 240,
                "location": (7, 5)
            },
            "reef4oclock":{
                "coords": [449, 508, 578, 508, 515, 623],
                "action": "select_reef",
                "apriltag": [ 17, 8],
                "orientation": 300,
                "location": (13, 19.5),
                "orientation": 300,          
                "location": (7, 5)
            },
            "reef6oclock":{
                "coords": [449, 508, 515, 623, 383, 623],
                "action": "select_reef",
                "apriltag": [ 18, 7],
                "orientation": 0,
                "location": (10, 13),
                "orientation": 0,            
                "location": (7, 5)            
            },    
            "reef8oclock":{
                "coords": [449, 508, 383, 623, 318, 508],
                "action": "select_reef",
                "apriltag": [ 19, 6],
                "orientation": 60,
                "location": (13, 9),            
                "orientation": 60,            
                "location": (7, 5)            
            },
            "reef10oclock":{
                "coords": [449, 508, 318, 508, 382, 398],
                "action": "select_reef",
                "apriltag": [ 20, 11],
                "orientation": 120,
                "location": (20.2, 9),            
                "orientation": 120,            
                "location": (7, 5)            
            },
            "reef12oclock":{
                "coords": [449, 508, 382, 398, 515, 398],
                "action": "select_reef",
                "apriltag": [ 21, 10],
                "orientation": 180,
                "location": (23, 13),            
                "orientation": 180,            
                "location": (7, 5)            
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
                "level": 1,
                "apriltag": [ 13, 1],
                "orientation": 240,
                "location": (5, 4),                
                "orientation": 240,            
                "location": (7, 5)                
            },
            "coralstationright":{
                "coords": [719, 1050, 719, 953, 838, 782, 959, 782, 959, 1050],
                "action": "select_coralstation",
                "side": "right",
                "level": 1,
                "apriltag": [ 12, 2],
                "orientation": 120,
                "location": (5, 22.5),           
                "orientation": 120,            
                "location": (7, 5)           
            },
            "clearbutton":{
                "coords": [959, 967, 1440, 967, 1440, 1050, 959, 1050],
                "action": "clearobjectives"
            }
        }
        
        for name, area in self.buttons.items():
            self.canvas.create_polygon(area["coords"], fill="", outline="blue", tags=(name, "clickable"))


    def __init_menu(self):
        # Menu
        menubar = tk.Menu(self.root)

        # File Menu
        FileMenu = tk.Menu(menubar, tearoff=0)
        FileMenu.add_command(label="Exit", underline=1, command=self.root.quit)
        menubar.add_cascade(label="File", underline=0, menu=FileMenu)

        # Team Menu
        TeamColorMenu = tk.Menu(menubar, tearoff=0)
        TeamColorMenu.add_command(label="Red Team", underline=0, command=self.__set_red_team)
        TeamColorMenu.add_command(label="Blue Team", underline=0, command=self.__set_blue_team)
        menubar.add_cascade(label="Team", underline=0, menu=TeamColorMenu)

        # Start From Menu
        StartingPositionMenu = tk.Menu(menubar, tearoff=0)
        StartingPositionMenu.add_command(label="1", underline=0, command=lambda: self.__startfrom(1))
        StartingPositionMenu.add_command(label="2", underline=0, command=lambda: self.__startfrom(2))
        StartingPositionMenu.add_command(label="3", underline=0, command=lambda: self.__startfrom(3))
        menubar.add_cascade(label="Start From", underline=0, menu=StartingPositionMenu)

        self.root.config(menu=menubar)

    def __set_blue_team(self):        
        self.__set_red_team(False)

    def __set_red_team(self, redteam=True):
        self.redteam = redteam
        fieldimage="Images/field-red.png" if redteam else "Images/field-blue.png"
        robotimagefile = "Images/robotred.png" if redteam else "Images/robotblue.png"
        self.robot_base_image = Image.open(robotimagefile)
        self.robot_image = ImageTk.PhotoImage(self.robot_base_image)
        self.background_image = ImageTk.PhotoImage(Image.open(fieldimage))
        self.canvas.itemconfig(self.robot_id, image=self.robot_image)
        self.canvas.itemconfig(self.background_id, image=self.background_image)
        
    def __startfrom(self, level):
        print(f"Need to set the starting position to {level}")


    def __is_point_in_polygon(self, x, y, polygon_coords):
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
