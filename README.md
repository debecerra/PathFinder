# PathFinder

PathFinder is a python project that provides a visual representation of the A* pathfinding algorithm.

PathFinder provides the user with a two-dimensional grid in which obstacles can be placed down. The start and target nodes can also be modified. Once triggered by the user, PathFinder will find an optimal path between the start and target nodes on the grid using the A* pathfinding algorithm and show the resulting path in the graphical user interface.

If you would like to try it out, feel free to download the code and run it yourself. If you would like to see how it works but you don't have the time to download and run the code, I will be uploading a short demo video in the near future that shows PathFinder in action. In the meantime, you can get an idea of how the program works by taking a look at the images provided in the media section below.

<!-- A video demo of this project can be found [here](https://youtu.be/-vleEE84S-U) -->

## Requirements

This project is built with Python 3 and the pygame module. To run PathFinder, one must have python 3 installed along with the pygame python library.

The source code for the project can be downloaded from this GitHub repository page. Once the project folder has been downloaded, the project is run by executing main.py

## Using the visualizer

PathFinder will provide the user with a user menu that lets the user reset the grid or execute the A* pathfinding algorithm to solve the grid. The program can find an optimal path by showing all steps the algorithm takes visually (Solve with visual) or by finding an optimal path directly and only showing the final result (Solve without visual).

Holding down the left mouse button over the grid converts free grid nodes into obstacles and obstacles into free nodes. The left mouse button is also used to select a new position for the start and target nodes. The grid node selection mode is changed using the user menu options "Place obstacles," "Place start node," and "Place target node."

## Media

The start-up screen:

<p float="left">
	<img src="media/img-basic.jpg" alt="Screenshot-1" width="400">
</p>

Using PathFinder to solve two simple problems:

<p float="left">
	<img src="media/img-basic-2.jpg" alt="Screenshot-2" width="400"/>
	<img src="media/img-solve-1.jpg" alt="Screenshot-3" width="400"/>
</p>

Example with scattered obstacles (solved with visual):

<p float="left">
	<img src="media/img-unsolve-2.jpg" alt="Screenshot-4" width="400"/>
	<img src="media/img-solve-2.jpg" alt="Screenshot-5" width="400"/>
</p>

Example with a simple maze (solved without visual):

<p float="left">
	<img src="media/img-unsolve-3.jpg" alt="Screenshot-6" width="400"/>
	<img src="media/img-solve-3.jpg" alt="Screenshot-7" width="400"/>
</p>

## Author

Copyright Diego Becerra 2020