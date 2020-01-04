# PathFinder

PathFinder is a python project that provides a visual representation of the A* path finding algorithm. 

PathFinder provides the user with a two-dimensional grid in which obstacles can be placed down. The start and target nodes can also be modified. Once triggered by the user, PathFinder will find a optimal path between the start and target nodes on the grid using the A* pathfinding algorithm and show the resulting path in the graphical user interface.

## Requirements

This project is built with python 3 and pygame. To run PathFinder, one must have python 3 installed along with the pygame python library.

The source code for the project can be downloaded from the GitHub repository page. Once the project folder has been downloaded, the project is run by executing main.py

## Using the visualizer

Once the project is running, a window will open. The bottom section of the window provides a user menu that allows for the user to reset the grid or execute the A* pathfinding algorithm to solve the grid. The path can be found by showing all steps the algorithm takes visually (Solve with visual) or the path can be found directly, and only the final result will be shown.

Holding down the left mouse button over the grid turns free grid nodes obstacles, and obstacles into free nodes. The left mouse button is also used to change the position of the start and target node. The grid selection mode is changed using the user menu options "Place obstacles", "Place start node", and "Place target node".

## Creator

This is a personal project made by Diego Becerra