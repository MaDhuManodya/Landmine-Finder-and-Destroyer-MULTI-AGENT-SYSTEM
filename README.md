# Landmine Simulation

## Overview
This project simulates a landmine detection and destruction system using agents. It employs the **Mesa framework** for agent-based modeling and **Pygame** for visual representation. The simulation includes four types of agents:
- **LandmineAgent**: Represents landmines placed on the grid.
- **FinderAgent**: Finds landmines and records their locations.
- **DestroyerAgent**: Moves toward and destroys located landmines.
- **ScoutAgent**: Scouts the grid for potential landmine locations.

## Features
- Interactive simulation with agents moving in a grid.
- Visualization of agents and landmines using Pygame.
- Dynamic updates of agent states and statistics displayed on the screen.
- A background image and visualized grid cells for an enhanced experience.

## Prerequisites
Ensure you have the following installed:
- **Python 3.7+**
- **Mesa**
- **Pygame**

You can install the dependencies using:
bash
pip install mesa pygame


## File Structure
LandmineSimulation/
|── main.py                # Main script for running the simulation
|── Images/               # Folder for storing images
    |── background.jpg    # Background image for the grid
    |── landmine.jpg      # Image for landmines
    |── finder.jpg        # Image for FinderAgent
    |── destroyer.jpg     # Image for DestroyerAgent
    |── scout.jpg         # Image for ScoutAgent


## How to Run
1. Clone the repository:
   
bash
   git clone https://github.com/yourusername/LandmineSimulation.git
   cd LandmineSimulation


2. Place the required images inside the Images/ folder.

3. Run the simulation:
   
bash
   python main.py


4. The simulation window will display the grid with agents and landmines.

## Controls
- Close the simulation by clicking the **X** button on the window.

## Simulation Details
- **Grid**: A square grid of size 25x25 with each cell having a size of 30x30 pixels.
- **Agents**:
  - FinderAgent starts at (0, 0).
  - DestroyerAgent starts at (24, 24).
  - ScoutAgent starts at the grid's center.
- **Details Panel**: Displays agent positions, destroyer state, and the count of landmines found/destroyed.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork this repository.
2. Create a feature branch:
   
bash
   git checkout -b feature-name

3. Commit your changes:
   
bash
   git commit -m "Add new feature"

4. Push to the branch:
   
bash
   git push origin feature-name

5. Create a Pull Request.

## License
This project is licensed under the [MIT License](LICENSE).

## Author
[Your Name](https://github.com/yourusername)
