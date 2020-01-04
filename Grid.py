""" Python script that contains Grid and Node class definitions.

Grid class is a two dimensional collection of Nodes that allows for a graphical and
interactive representation of the A* pathfinding algorithm.

Node class represents a single unit of the two-dimensional grid with varying states
to represent different phases of the A* pathfinding algorithm.
"""

import pygame
import MinPriorityQueue

class Grid:
    """ Represents the arrangment of nodes/cells in the two-dimensional array.

    Attributes:
        surface: the surface object on which to draw the grid onto
        nodes: the two-dimensional list arrangment of nodes that makes up the grid

    Constants:
        VERT_HORZ_COST: Cost of vertical/horizontal path movement
        DIAG_COST: Cost of diaginal path movement
        COLUMNS: Number of columns in grid
        ROWS: Number of rows in grid
    """

    VERT_HORZ_COST = 10
    DIAG_COST = 14

    PATHFIND_TIMEDELAY = 50

    DEFAULT_START_ROW = 9
    DEFAULT_START_COL = 4
    DEFAULT_TARGET_ROW = 9
    DEFAULT_TARGET_COL = -5

    def __init__(self, surface, rect, columns, rows):
        """ Initializes an instance of the Grid class. """

        self.__surface = surface
        self.__rect = rect
        self.__columns = columns
        self.__rows = rows
        self.__width = rect.width
        self.__height = rect.height

        self.__nodes = []
        self.__start = None
        self.__target = None

        self.create_grid()
        self.set_start_node()
        self.set_target_node()

        self.__solved = False

    def create_grid(self):
        """ Initializes the arrangment of grid nodes.

        Nodes are initialized and stored in the two-dimensional list attribute self.__nodes.
        There are no obstacle nodes at initialization. All nodes except start and target nodes
        are walkable.
        """

        self.__solved = False
        self.__nodes = []
        width = self.__width // self.__columns
        height = self.__height // self.__rows

        for row_index in range(self.__rows):
            row = []
            for column_index in range(self.__columns):
                node = Node(column_index, row_index, width, height)
                node.draw()
                row.append(node)
            self.__nodes.append(row)

    def draw(self):
        """ Draws the grid object.

        Draws the grid object by drawing all nodes in self.__nodes.
        """

        for row in self.__nodes:
            for node in row:
                node.draw()

    def set_as_obstacle(self, mouse_pos, selected_nodes):
        """ Handles click event on a grid node.

        Determines which node was selected. If selected node was UNDISCOVERED, it is changed to
        OBSTACLE, and vice versa.

        Args:
            mouse_pos: position of the mouse cursor when event occurred
            selected_nodes: set of Nodes that have been selected in current continous mouse-key-down

        Returns:
            Node that has toggled, or None if no Node was toggled
        """

        node = self.get_node(mouse_pos)
        if node not in selected_nodes:
            node.toggle_obstacle()
        return node

    def collidepoint(self, point):
        """ Tests if a point is inside the Grid area.

        Args:
            point: the (x, y) coordinates of the point

        Returns:
            True if point is on Grid area, False otherwise
        """

        return self.__rect.collidepoint(point)

    def set_start_node(self, node=None):
        """ Sets the start node of the Grid.

        Args:
            node: The Node object to be set as the start node. (If no argument given, the node
            is set to the default.)

        """

        # Set to default if no optional paramater given
        if node is None:
            node = self.__nodes[Grid.DEFAULT_START_ROW][Grid.DEFAULT_START_COL]

        # Let node be start node only if given node is not already target node
        if self.__target != node:

            if self.__start is not None:
                self.__start.make_undiscovered()

            node.set_start()
            self.__start = node


    def set_target_node(self, node=None):
        """ Sets the target node of the Grid.

        Args:
            node: The Node object to be set as the target node. (If no argument given, the node
            is set to the default.)

        """

        # Set to default if no optional paramater given
        if node is None:
            node = self.__nodes[Grid.DEFAULT_TARGET_ROW][Grid.DEFAULT_TARGET_COL]

        # Let node be target node only if given node is not already start node
        if self.__start != node:

            if self.__target is not None:
                self.__target.make_undiscovered()

            node.set_target()
            self.__target = node

    def get_node(self, pos):
        """ Gets the node at a given position on the surface.

        It is assummed that the position has already been checked to be a
        valid point that lies on the Grid. This can be checked with the Grid.collidepoint
        method.

        Args:
            pos: The (x, y) position to be checked

        Returns:
            The node at the given (x, y) position
        """

        x, y = pos
        j = x // (self.__width // self.__columns)
        i = y // (self.__height // self.__rows)
        return self.__nodes[i][j]


    # -------------------------------------------
    # Methods related to A* pathfinding algorithm
    # -------------------------------------------

    def solve(self, show_steps=True):
        """ Solves the current Grid layout.

        Solves the current Grid layout by finding a shortest path from the start node
        to the target node using the A* pathfinding algorithm. The path can be found with
        or without a visual demonstration of each step.

        Args:
            show_steps: bool that determines if steps should be shown
        """

        if self.__start is None or self.__target is None:
            raise AttributeError("Start Node and Target Node are not set.")

        try:
            if show_steps:
                self.find_path()
            else:
                self.find_path_nonvisual()
        except IndexError:
            self.print_no_solution()
        else:
            self.print_path()

    def find_path(self):
        """  Find a path from start position to target position. 

        Given the start and target attributes, finds the cheapest path from the
        start node to the target node using the A* pathfinding algorithm.

        Steps in the algorithm are shown graphically with time delays to show path
        progression.
        """

        opened = MinPriorityQueue.MinPriorityQueue()
        closed = set()
        self.calculate_all_h_costs()

        self.__start.relax_g_cost(0)
        opened.insert(self.__start.get_f_cost(), self.__start)

        current = None
        path_found = False
        while not path_found:
            pygame.time.delay(Grid.PATHFIND_TIMEDELAY)

            # Select node with smallest f_cost from opened
            current = opened.extract_min()

            # If found target, break the loop
            if current is self.__target:
                path_found = True
                self.__solved = True

            # If target not found, add neighbours to opened
            else:
                vh_neighbours = self.get_vert_horz_neighbours(current)
                d_neighbours = self.get_diag_neighbors(current)

                for node in vh_neighbours:
                    if node.relax_g_cost(current.get_g_cost() + Grid.VERT_HORZ_COST):
                        node.set_prev(current)
                        if opened.element_exists(node):
                            opened.decrease_key(node, node.get_f_cost())
                        else:
                            opened.insert(node.get_f_cost(), node)
                            node.make_open()

                for node in d_neighbours:
                    if node.relax_g_cost(current.get_g_cost() + Grid.DIAG_COST):
                        node.set_prev(current)
                        if opened.element_exists(node):
                            opened.decrease_key(node, node.get_f_cost())
                        else:
                            opened.insert(node.get_f_cost(), node)
                            node.make_open()

            # Finish with current
            closed.add(current)
            current.close()

            # Update UI, handle QUIT if necessary
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            self.draw()
            pygame.display.update()

    def find_path_nonvisual(self):
        """  Find a path from start position to target position. 

        Given the start and target attributes, finds the cheapest path from the
        start node to the target node using the A* pathfinding algorithm.
        """

        opened = MinPriorityQueue.MinPriorityQueue()
        closed = set()
        self.calculate_all_h_costs()

        self.__start.relax_g_cost(0)
        opened.insert(self.__start.get_f_cost(), self.__start)

        current = None
        path_found = False
        while not path_found:
            # Select node with smallest f_cost from opened
            current = opened.extract_min()

            # If found target, break the loop
            if current is self.__target:
                path_found = True
                self.__solved = True

            # If target not found, add neighbours to opened
            else:
                vh_neighbours = self.get_vert_horz_neighbours(current)
                d_neighbours = self.get_diag_neighbors(current)

                for node in vh_neighbours:
                    if node.relax_g_cost(current.get_g_cost() + Grid.VERT_HORZ_COST):
                        node.set_prev(current)
                        if opened.element_exists(node):
                            opened.decrease_key(node, node.get_f_cost())
                        else:
                            opened.insert(node.get_f_cost(), node)

                for node in d_neighbours:
                    if node.relax_g_cost(current.get_g_cost() + Grid.DIAG_COST):
                        node.set_prev(current)
                        if opened.element_exists(node):
                            opened.decrease_key(node, node.get_f_cost())
                        else:
                            opened.insert(node.get_f_cost(), node)

            # Finish with current
            closed.add(current)

    def is_solved(self):
        """ Gets if Grid has been solved.

        Returns:
            True is solved, False otherwise
        """
        return self.__solved

    def calculate_all_h_costs(self):
        """ Initialize the h_costs of all nodes for an execution of find_path.

        Sets the heuristic h_cost for all nodes in Grid at the beginning of an execution
        of find_path.
        """

        for row in self.__nodes:
            for node in row:
                # Calculate direct distance from node to target
                vdist = abs(node.get_row() - self.__target.get_row())
                hdist = abs(node.get_col() - self.__target.get_col())

                diag = min(vdist, hdist)
                updown = max(vdist, hdist) - min(vdist, hdist)

                dist = diag * Grid.DIAG_COST + updown * Grid.VERT_HORZ_COST
                node.set_h_cost(dist)

    def get_vert_horz_neighbours(self, node):
        """ Gets all walkable nodes that are directly above, below, left or
        right of the given node.

        Args:
            node: the Node object

        Returns:
            adjacent: list of Node objects that are vertically/horizontally adjacent
                to given node and walkable.
        """

        adjacent = []

        # Get the row and column of the node
        x, y = node.get_pos()
        col = x // (self.__width // self.__columns)
        row = y // (self.__height // self.__rows)

        for i, j in (-1, 0), (1, 0), (0, -1), (0, 1):
            if row + i >= 0 and col + j >= 0:
                try:
                    adj = self.__nodes[row+i][col+j]
                    if not adj.is_obstacle():
                        adjacent.append(adj)
                except IndexError:
                    pass

        return adjacent

    def get_diag_neighbors(self, node):
        """ Gets all walkable nodes that are adjacent and diagonal to the given node.

        Args:
            node: the Node object

        Returns:
            adjacent: list of Node objects that are vertically/horizontally adjacent
                to given node and walkable.
        """

        adjacent = []

        # Get the row and column of the node
        x, y = node.get_pos()
        col = x // (self.__width // self.__columns)
        row = y // (self.__height // self.__rows)

        for i, j in (-1, -1), (1, -1), (-1, 1), (1, 1):
            if row + i >= 0 and col + j >= 0:
                try:
                    adj = self.__nodes[row+i][col+j]
                    if not adj.is_obstacle():
                        adjacent.append(adj)
                except IndexError:
                    pass

        return adjacent

    def print_path(self):
        """ Changes state of all nodes in solution path.

        For every node that has been identified to be part of the optimal solution path, changes the
        state of the node. It is assumed that find_path has been executed and a solution has been found.
        """

        if self.__solved:
            current = self.__target.get_prev()
            while current is not self.__start:
                current.add_to_solution()
                current = current.get_prev()

    def print_no_solution(self):
        """ Displays pathfinding result when there is no solution. """

        self.__target.set_no_sol_target()


class Node:
    """ Object which represents a unit on the two-dimensional grid.

    A node object has represents a single unit on a two dimensional grid. A node can be in
    one of several states. The state defines how the node is to be graphically represented and
    determines how it can interact with surrounding nodes on the grid.

    Possible Node states :
        UNDISCOVERED : Node is walkable and not directly accessable by an adjacent closed Node
        OPENED : Node is walkable and directly accessable by an adjacent closed Node
        CLOSED : Node is no longer walkable, was opened and all handling on Node has been completed
        START : Node is designated as the start position of the path
        TARGET : Node is designated as the target position of the path
        OBSTACLE : Node is not walkable
        SOLUTION : Node has been identified to be part of solution path

    Attributes :
        rect : the Rect object that graphically represents the Node
        pos : tuple representing the x-y position of the node on the surface
        prev : reference to the Node that opened current Node in the execution of path finding
        state : int representing the current state of the node
    """

    pygame.font.init()
    FONT = pygame.font.SysFont("Arial", 20, True)
    FONT_COLOR = pygame.Color('white')

    UNDISCOVERED = 'UNDISCOVERED'
    OPENED = 'DISCOVERED'
    CLOSED = 'CLOSED'
    START = 'START'
    TARGET = 'TARGET'
    OBSTACLE = 'OBSTACLE'
    SOLUTION = 'SOLUTION'
    NO_SOL_TARGET = 'NO_SOL_TARGET'

    BG_COLORS = {
        UNDISCOVERED : pygame.Color("white"),
        OPENED : pygame.Color('yellow'),
        CLOSED : pygame.Color('red'),
        START : pygame.Color("blue"),
        TARGET : pygame.Color("blue"),
        OBSTACLE : pygame.Color("black"),
        SOLUTION : pygame.Color("green"),
        NO_SOL_TARGET : pygame.Color("red")
        }

    BORDER_COLOR = pygame.Color("black")
    BRDER_WIDTH = 1

    surface = None

    @classmethod
    def set_surface(cls, surface):
        """ Sets the pygame drawing surface for all node objects. """

        cls.__surface = surface

    def __init__(self, col, row, width, height):
        """ Initializes an instance of the Node class. """

        self.__row = row
        self.__col = col
        self.__width = width
        self.__height = height
        self.__pos = (self.__width*self.__col, self.__height*self.__row)
        self.__rect = pygame.Rect(self.__pos, (width, height))

        self.__prev = None
        self.__state = Node.UNDISCOVERED
        self.__h_cost = None
        self.__g_cost = None

    def draw(self):
        """ Draws the node on the surface.

        Draws the node on the surface given as instance attribute. A node is drawn
        in accordance with its state.
        """

        pygame.draw.rect(self.__surface, Node.BG_COLORS[self.__state], self.__rect)

        if self.__state == Node.START:
            self.draw_node_text("S")
        if self.__state == Node.TARGET or self.__state == Node.NO_SOL_TARGET:
            self.draw_node_text("T")

        # if self.__state == Node.OPENED or self.__state == Node.CLOSED or self.__state == Node.SOLUTION:
            # self.draw_g_cost()
            # self.draw_h_cost()
            # self.draw_f_cost()

        pygame.draw.rect(self.__surface, self.BORDER_COLOR, self.__rect, Node.BRDER_WIDTH)

    def draw_node_text(self, text):
        """ Draws text centered in the current node. """

        text_image = self.FONT.render(text, True, self.FONT_COLOR)
        x = self.__pos[0] + (self.__rect.width//2) - (text_image.get_width()//2)
        y = self.__pos[1] + (self.__rect.height//2) - (text_image.get_height()//2)
        self.__surface.blit(text_image, (x, y))

    def draw_g_cost(self):
        """ Draws the g_cost of the node in the upper left corner of the Node rect. """

        text_image = self.FONT.render(str(self.__g_cost), True, self.BORDER_COLOR)
        x = self.__pos[0] + Node.BRDER_WIDTH
        y = self.__pos[1]
        self.__surface.blit(text_image, (x, y))

    def draw_h_cost(self):
        """ Draws the h_cost of the node in the upper right corner of the Node rect. """

        text_image = self.FONT.render(str(self.__h_cost), True, self.BORDER_COLOR)
        x = self.__pos[0] + self.__width - text_image.get_width() - Node.BRDER_WIDTH
        y = self.__pos[1]
        self.__surface.blit(text_image, (x, y))

    def draw_f_cost(self):
        """ Draws the f_cost of the node in the center of the Node rect. """

        text_image = self.FONT.render(str(self.__h_cost+self.__g_cost), True, self.BORDER_COLOR)
        x = self.__pos[0] + (self.__rect.width//2) - (text_image.get_width()//2)
        y = self.__pos[1] + (self.__rect.height//2) - (text_image.get_height()//2)
        self.__surface.blit(text_image, (x, y))

    def toggle_obstacle(self):
        """ Toggles node between undiscovered and obstacle states.

        If a node is currently undiscovered and not the target node, the node
        state will be changed to obstacle. If a node is currently an obstacle and
        not the start node, the node change will be changes to walkable.
        """

        if self.__state == Node.UNDISCOVERED:
            self.__state = Node.OBSTACLE
        elif self.__state == Node.OBSTACLE:
            self.__state = Node.UNDISCOVERED

    def set_start(self):
        """ Sets node to be the start node. """

        self.__state = Node.START

    def set_target(self):
        """ Sets node to be the target node. """

        self.__state = Node.TARGET

    def set_no_sol_target(self):
        """ Identified Node as an unreachable target Node. """

        self.__state = Node.NO_SOL_TARGET

    def make_undiscovered(self):
        """  Changes the state of the node to OPEN. """

        self.__state = Node.UNDISCOVERED

    def make_open(self):
        """  Changes the state of the node to OPEN. """

        if self.__state != Node.START and self.__state != Node.TARGET:
            self.__state = Node.OPENED

    def close(self):
        """ Changes the state of the node to CLOSED. """

        if self.__state != Node.START and self.__state != Node.TARGET:
            self.__state = Node.CLOSED

    def is_obstacle(self):
        """ Returns true if node state is obstacle """

        return self.__state == Node.OBSTACLE

    def add_to_solution(self):
        """ Identifies node state as part of solution. """

        self.__state = Node.SOLUTION

    def set_h_cost(self, h_cost):
        """ Initializes the h cost of the node. """
        assert isinstance(h_cost, int)
        self.__h_cost = h_cost

    def relax_g_cost(self, cost):
        """ Relaxes the g_cost of the current node.

        If the current g_cost is None or higher than the given cost, then cost is
        assigned to g_cost.

        Args:
            cost: The new potential g_cost for the Node

        Raises:
            AssertionError: cost paramater is not an int

        Returns:
            True if g_cost was relaxed/modified, False otherwise

        """
        assert isinstance(cost, int), "Cost must be an int"
        if self.__g_cost is None or cost < self.__g_cost:
            self.__g_cost = cost
            return True
        else:
            return False

    def get_g_cost(self):
        """ Gets the g cost of the node. """

        return self.__g_cost

    def get_f_cost(self):
        """ Gets the f cost of the node. """

        return self.__h_cost + self.__g_cost

    def set_prev(self, prev_node):
        """ Sets the prev attribute of the current node.

        Args:
            prev_node: Node object to set to the prev of this Node

        Raises:
            TypeError: prev_node is not of type Node
        """

        if not isinstance(prev_node, Node):
            raise TypeError('prev_node must be of type Node')
        self.__prev = prev_node

    def get_prev(self):
        """ Gets the prev node for the Node."""

        return self.__prev

    def get_row(self):
        """ Gets the row of the node. """

        return self.__row

    def get_col(self):
        """ Gets the column of the node. """

        return self.__col

    def get_pos(self):
        """ Gets the position of the Node. """

        return self.__pos

    def __repr__(self):
        """ Returns representation of Node object. """

        return {
            "Row":self.__row,
            "Column":self.__col,
            "F-cost":self.get_f_cost()
            }
