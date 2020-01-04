""" Contains the Program class. """

import pygame
from Grid import Grid, Node
import Menu

class Program:
    """ Represents an instance of the application.

    A instance of this class represents an execution of the program. The main method
    executes a loop that controls the main execution flow of the program.
    """

    OBS_MODE = "OBSTACLE"
    START_MODE = 'START'
    TARGET_MODE = 'TARGET'
    MODES = {OBS_MODE, START_MODE, TARGET_MODE}

    def __init__(self):
        """ Initialize an instance of the Program class. """

        self.__run = True
        self.__pause_time = 50

        self.__window_width = 750
        self.__window_height = 700
        self.__window_title = "Path Finder"
        self.__window = self.init_window()

        Node.set_surface(self.__window)

        self.__grid_rect = pygame.Rect(0, 0, 750, 500)
        self.__grid = Grid(self.__window, self.__grid_rect, 30, 20)

        self.__menu_rect = pygame.Rect(0, 500, 750, 200)
        self.__menu = Menu.Menu(self.__window, self.__menu_rect)

        self.__current_selection = set()
        self.__selection_mode = Program.OBS_MODE

    def main(self):
        """ Executes main program loop.
        """

        pygame.init()

        self.__run = True
        while self.__run:
            pygame.time.delay(self.__pause_time)
            self.handle_event()
            self.draw()
            self.update()

        pygame.quit()

    def init_window(self):
        """ Initializes the display window. """

        size = (self.__window_width, self.__window_height)
        window = pygame.display.set_mode(size)
        pygame.display.set_caption(self.__window_title)
        return window

    def draw(self):
        """ Draws all UI objects. """

        self.__grid.draw()
        self.__menu.draw()

    def update(self):
        """ Updates the state of pygame UI objects. """

        pygame.display.update()

    def handle_event(self):
        """ Handles all pygame events. """
        for event in pygame.event.get():

            # Exit the program
            if event.type == pygame.QUIT:
                self.__run = False

            # Mouse held down to select obstacle Nodes
            if pygame.mouse.get_pressed()[0]:
                try:
                    if self.__grid.collidepoint(event.pos) and not self.__grid.is_solved():
                        self.handle_grid_mouse_down(event.pos)
                    if self.__menu.collidepoint(event.pos):
                        button = self.__menu.get_selected_button(event.pos)
                        self.handle_menu_selection(button)
                except AttributeError:
                    pass

            # Mouse up clears cache of currently selected Nodes
            if event.type == pygame.MOUSEBUTTONUP:
                self.__current_selection.clear()

    def handle_grid_mouse_down(self, pos):
        """ Handles left mouse button down event on the Grid.

        Args:
            pos: The position of the mouse cursor at the time of event
        """

        if self.__selection_mode == Program.OBS_MODE:
            new_selection = self.__grid.set_as_obstacle(pos, self.__current_selection)
            self.__current_selection.add(new_selection)

        elif self.__selection_mode == Program.START_MODE:
            snode = self.__grid.get_node(pos)
            self.__grid.set_start_node(snode)

        else:
            tnode = self.__grid.get_node(pos)
            self.__grid.set_target_node(tnode)

    def handle_menu_selection(self, selected_textbox):
        """ Performs actions corresponding to menu selection.

        Args:
            selected_textbox: The TextBox object that was selected by the user
        """

        if str(selected_textbox) == '[Place obstacles]':
            self.change_selection_mode(Program.OBS_MODE)

        elif str(selected_textbox) == '[Place start node]':
            self.change_selection_mode(Program.START_MODE)

        elif str(selected_textbox) == '[Place target node]':
            self.change_selection_mode(Program.TARGET_MODE)

        elif str(selected_textbox) == '[Reset grid]':
            self.__grid.create_grid()
            self.__grid.set_start_node()
            self.__grid.set_target_node()

        elif str(selected_textbox) == '[Solve with visual]':
            self.__grid.solve(True)

        elif str(selected_textbox) == '[Solve without visual]':
            self.__grid.solve(False)

    def change_selection_mode(self, new_mode):
        """ Updates the selection mode of the program.

        The selection mode can be set to either OBS_MODE, START_MODE, or
        TARGET_MODE which identifies which type of Node can be placed on the grid
        by a holding down the left mouse button.

        Args:
            new_mode: One of Program.OBS_MODE, Program.START_MODE, Program.TARGET_MODE"""

        assert new_mode in self.MODES
        self.__selection_mode = new_mode
        self.__menu.set_mode(new_mode)
