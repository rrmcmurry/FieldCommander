# FieldCommander

**FieldCommander** is an interactive map-based tool for controlling and navigating a robot on an FRC field. It allows users to set objectives like navigation, orientation, and alignment by clicking on a field map, with real-time robot position tracking. Designed to work with WPILibPi and NetworkTables, it simplifies robot task planning during matches or testing.

---

## Features

- **Interactive Map**: Click on a field map to set navigation objectives.
- **Orientation Control**: Use arrow keys to set the robot’s orientation (0°, 90°, 180°, 270°).
- **Real-Time Tracking**: Displays the robot’s position and orientation on the map in real time.
- **Dynamic Task Management**:
  - **Left-Click**: Appends new objectives to the task queue.
  - **Right-Click**: Overwrites the existing task queue with a single objective.
- **NetworkTables Integration**: Communicates objectives and receives real-time data from the robot.

---

## Installation

1. Clone the repository:

   git clone https://github.com/yourusername/FieldCommander.git  
   cd FieldCommander

2. Install dependencies:

   Ensure you have Python 3.12+ installed, then run:  
   pip install Pillow pynetworktables

3. Setup NetworkTables:

   Confirm your NetworkTables server is running on the robot or Raspberry Pi.  
   Update the `NetworkTables.initialize()` line in the script with the correct IP or hostname:  
   NetworkTables.initialize(server='roborio-TEAM-frc.local')  # Replace TEAM with your team number

4. Run the application:

   python FieldCommander.py

---

## Usage

### Mouse Controls
- **Left-Click**: Set a navigation objective with the current orientation and append it to the queue.
- **Right-Click**: Set a navigation objective with the current orientation and overwrite the queue.

### Keyboard Controls
- **Arrow Keys**:
  - `↑`: Set orientation to 0° (forward).
  - `→`: Set orientation to 90° (right).
  - `↓`: Set orientation to 180° (backward).
  - `←`: Set orientation to 270° (left).

---

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or optimizations:  
1. Fork the repository.  
2. Create a feature branch:  
   git checkout -b feature-name  
3. Commit your changes:  
   git commit -m "Add a new feature"  
4. Push your branch:  
   git push origin feature-name  
5. Open a Pull Request.

---

## Roadmap

Planned enhancements include:
- Adding support for AprilTag alignment zones.
- Displaying planned robot paths on the map.
- Allowing drag-and-drop adjustments to objectives.
- Adding UI for viewing and editing the task queue.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **FIRST Robotics Competition**: For inspiring innovative tools and technologies.
- **WPILibPi**: For seamless integration with the robot.
- **Pillow and NetworkTables**: For providing the core libraries used in this project.

---

## Contact

For questions, feedback, or collaboration, feel free to reach out!

- **Author**: Robby  
- **Email**: your.email@example.com  
- **GitHub**: [yourusername](https://github.com/yourusername)
