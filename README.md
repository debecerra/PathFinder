# PathFinder

PathFinder is a python project that provides a visual representation of the A* pathfinding algorithm.

PathFinder provides the user with a two-dimensional grid in which obstacles can be placed down. The start and target nodes can also be modified. Once triggered by the user, PathFinder will find an optimal path between the start and target nodes on the grid using the A* pathfinding algorithm and show the resulting path in the graphical user interface.

A video demo of this project can be found [here](https://youtu.be/-vleEE84S-U)

## Requirements

This project is built with python 3 and pygame. To run PathFinder, one must have python 3 installed along with the pygame python library.

The source code for the project can be downloaded from the GitHub repository page. Once the project folder has been downloaded, the project is run by executing main.py

## Using the visualizer

PathFinder will provide the user with a user menu that lets the user reset the grid or execute the A* pathfinding algorithm to solve the grid. The program can find an optimal path by showing all steps the algorithm takes visually (Solve with visual) or by finding an optimal path directly and only showing the final result (Solve without visual).

Holding down the left mouse button over the grid converts free grid nodes into obstacles and obstacles into free nodes. The left mouse button is also used to select a new position for the start and target nodes. The grid node selection mode is changed using the user menu options "Place obstacles," "Place start node," and "Place target node."

## Media

![image info](media/img-basic.jpg)
![Alt text](media/img-basic.jpg?raw=true "Title")

## Creator

This is a personal project made by Diego Becerra