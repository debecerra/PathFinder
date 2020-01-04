""" Python script that contains Menu and TextBox class definitions """

import pygame

class Menu:
    """ Represents the menu interface for the program.

    A Menu object consists of several menu options (buttons) that can be selected by
    the user with the GUI. This menu interface is specific to the PathFinder project.

    The menu allows the user to perform the following options:
        - Toggle between placing down OBSTACLE, START, and TARGET Nodes on the Grid
        - Execute the A* pathfinding algorithm with or without showing steps
        - Reset the Grid

    Attributes:
        surface: The pygame.Surface object to draw onto
        rect: The pygame.Rect that captures the area of the Menu on the Surface
        col1_width: The width of the first column
        col2_width: The width of the second column
        row_height: The height of a row
        menu_options: The list of TextBox objects which correspond to Menu options
            that can be executed

    """

    BRDR_COLOR = (0, 0, 0)
    BG_COLOR = (80, 80, 80)

    NUM_OF_BUTTONS = 6
    ROWS = 3
    COLS = 3
    PADDING = 14

    OBSTACLE_MODE = "OBSTACLE"
    START_MODE = "START"
    TARGET_MODE = "TARGET"

    def __init__(self, surface, rect):
        """ Initiates the Menu.

        Args:
            surface: The pygame.Surface object to draw onto
            rect: The pygame.Rect that captures the area of the Menu on the Surface
        """

        self.__surface = surface
        self.__rect = rect

        self._col1_width = self.__rect.width // Menu.COLS
        self.__col2_width = self.__rect.width - self._col1_width
        self.__row_height = self.__rect.height // Menu.ROWS

        self.__menu_options = []
        self.create_menu_options()

        self.set_mode(Menu.OBSTACLE_MODE)


    def draw(self):
        """ Draws the entire Menu. """

        pygame.draw.rect(self.__surface, Menu.BG_COLOR, self.__rect)
        for button in self.__menu_options:
            button.draw()

    def create_menu_options(self):
        """ Creates all Menu options. """

        # Create obstacle nodes button
        pos = (self.__rect.left, self.__rect.top + 0*self.__row_height)
        dims = (self._col1_width, self.__row_height)
        obs_button = self.create_text_box(pos, dims, "Place obstacles")
        obs_button.set_alt_appearance()
        self.__menu_options.append(obs_button)

        # Create start node button
        pos = (self.__rect.left, self.__rect.top + 1*self.__row_height)
        dims = (self._col1_width, self.__row_height)
        start_button = self.create_text_box(pos, dims, "Place start node")
        start_button.set_alt_appearance()
        self.__menu_options.append(start_button)

        # Create target node button
        pos = (self.__rect.left, self.__rect.top + 2*self.__row_height)
        dims = (self._col1_width, self.__row_height)
        target_button = self.create_text_box(pos, dims, "Place target node")
        target_button.set_alt_appearance()
        self.__menu_options.append(target_button)

        # Create reset grid button
        pos = (self.__rect.left + self._col1_width, self.__rect.top + 0*self.__row_height)
        dims = (self.__col2_width, self.__row_height)
        reset_button = self.create_text_box(pos, dims, "Reset grid")
        self.__menu_options.append(reset_button)

        # Create solve with visual button
        pos = (self.__rect.left + self._col1_width, self.__rect.top + 1*self.__row_height)
        dims = (self.__col2_width, self.__row_height)
        v_solve_button = self.create_text_box(pos, dims, "Solve with visual")
        self.__menu_options.append(v_solve_button)

        # Create solve without visual button
        pos = (self.__rect.left + self._col1_width, self.__rect.top + 2*self.__row_height)
        dims = (self.__col2_width, self.__row_height)
        no_v_solve_button = self.create_text_box(pos, dims, "Solve without visual")
        self.__menu_options.append(no_v_solve_button)

    def create_text_box(self, input_pos, input_dims, text):
        """ Creates a TextBox instance with appropriate padding.

        The position and dimensions of the area in which to create the TextBox object. The
        TextBox is created in that area with the specified padding of empty space on all four sides.

        Args:
            input_pos: The (top, left) coordinates of the space in which to create the TextBox 
            input_dims: The (width, height) dimensions of the space in which to create the TextBox
            text: The string to display inside the TextBox

        Returns:
            The TextBox object which has been created

        """

        left, top = input_pos
        width, height = input_dims

        button_width = width - 2*Menu.PADDING
        button_height = height - Menu.PADDING
        x_pos = ((left + (left + width)) // 2) - (button_width // 2)
        y_pos = ((top + (top + height)) // 2) - (button_height // 2)

        pos = (x_pos, y_pos)
        dims = (button_width, button_height)

        button = TextBox(self.__surface, pygame.Rect(pos, dims), text)
        return button

    def collidepoint(self, point):
        """ Tests if a point is inside the Menu area.

        Args:
            point: the (x, y) coordinates of the point to test
        """

        return self.__rect.collidepoint(point)

    def get_selected_button(self, mouse_pos):
        """ Gets the menu item at a given coordinate position.

        Args:
            mouse_pos: The (x, y) coordinates to check

        Returns:
            The TextBox object at the given position

        """

        for but in self.__menu_options:
            if but.collidepoint(mouse_pos):
                return but

    def set_mode(self, mode):
        """ Updates Menu graphics to reflect change in mode.

        Args:
            mode: the new mode to change to
        """

        if mode == Menu.OBSTACLE_MODE:
            highlighted_button = self.__menu_options[0]
        elif mode == Menu.START_MODE:
            highlighted_button = self.__menu_options[1]
        elif mode == Menu.TARGET_MODE:
            highlighted_button = self.__menu_options[2]

        for i in range(3):
            self.__menu_options[i].has_thick_brdr(False)

        highlighted_button.has_thick_brdr(True)

class TextBox:
    """ Represents a rectangular body of text to be displayed on the screen.

    A TextBox is composed of a rectangle (pygame.Rect) shape and text that is centered in
    the rectangle. Can be used with the Menu class to represent simple menu options that can be
    clicked by the user.

    Attributes:
        surface: The pygame.Surface object to draw onto
        rect: The pygame.Rect that captures the area of the TextBox on the Surface
        pos: The (left, top) position of the pygame.Rect object
        text: The string to be displayed in the TextBox
        brdr_width: The width of the TextBox
        bg_color: The background color of the TextBox
    """

    BRDR_COLOR = pygame.Color('black')

    BG_COLOR = pygame.Color('grey')
    ALT_BG_COLOR = pygame.Color('white')

    NORMAL_BRDR_WIDTH = 3
    THICK_BRDR_WIDTH = 6

    pygame.font.init()
    FONT = pygame.font.SysFont("Helvetica", 20, True)
    FONT_COLOR = pygame.Color('black')

    def __init__(self, surface, rect, text):
        """ Creates an instance of TextBox.

        Args:
            surface: The pygame.Surface object to draw onto
            rect: The pygame.Rect that captures the area of the TextBox on the Surface
            text: The string to be displayed in the TextBox
        """

        self.__surface = surface
        self.__rect = rect
        self.__pos = (rect.left, rect.top)
        self.__text = text
        self.__brdr_width = TextBox.NORMAL_BRDR_WIDTH
        self.__bg_color = TextBox.BG_COLOR

    def has_thick_brdr(self, true_false):
        """ Sets the thickness of TextBox borders.

        If true_false is True, then border width of the TextBox object is set
        to THICK. Otherwise, border_width is set of NORMAL.
        """

        if true_false:
            self.__brdr_width = TextBox.THICK_BRDR_WIDTH
        else:
            self.__brdr_width = TextBox.NORMAL_BRDR_WIDTH

    def draw(self):
        """ Draws the TextBox on the pygame surface. """

        pygame.draw.rect(self.__surface, self.__bg_color, self.__rect)

        text_image = self.FONT.render(self.__text, True, self.FONT_COLOR)
        x = self.__pos[0] + (self.__rect.width//2) - (text_image.get_width()//2)
        y = self.__pos[1] + (self.__rect.height//2) - (text_image.get_height()//2)
        self.__surface.blit(text_image, (x, y))

        pygame.draw.rect(self.__surface, self.BRDR_COLOR, self.__rect, self.__brdr_width)

    def set_alt_appearance(self):
        """ Sets the TextBox object to be displayed with the alternate appearance. """

        self.__bg_color = TextBox.ALT_BG_COLOR

    def collidepoint(self, point):
        """ Tests if a point is inside the TextBox area. """

        return self.__rect.collidepoint(point)

    def __repr__(self):
        return {"Position": self.__pos, "Text": self.__text}

    def __str__(self):
        return "[{0}]".format(self.__text)
