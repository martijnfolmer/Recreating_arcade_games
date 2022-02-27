# Import the pygame library and initialise the game engine
import pygame
import random
pygame.init()
import math

'''
    This script allows us to play tetris in pygame. It is an incomplete game and requires more fine tuning.
    It is part of 
    
    todo: 
    - bigger field in order to show gui elements
    - scoring + showing the score
    - black border around all the blocks
    - In game instructions for how to play (keyboard bindings)
    - A pause state
'''

'''
    How to play:
    - spacebar to start or restart
    - A/D to rotate
    - Arrow keys to move the tetromino

'''



class Tetris:

    def __init__(self):

        self.state = 0     # 0 = before, 1=during play, 2=game over

        # timer:
        time_between_movements = 250       # in milliseconds, how long between each update of the tetromino falling
        self.MOVEEVENT, t, trail = pygame.USEREVENT + 1, time_between_movements, []
        pygame.time.set_timer(self.MOVEEVENT, t)

        # Define some colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (155, 0, 0)
        self.GREEN = (0, 155, 0)
        self.LIGHTBLUE = (20, 20, 175)
        self.YELLOW = (155, 155, 0)
        self.ORANGE = (255, 165, 0)
        self.PINK = (255, 182, 193)
        self.PURPLE = (230, 230, 250)
        self.color_val = [self.YELLOW, self.LIGHTBLUE, self.RED, self.GREEN, self.ORANGE, self.PINK, self.PURPLE]

        # get the font
        self.font = pygame.font.SysFont(None, 35)

        # define the blocks
        self.all_tetromino = []
        self.all_tetromino.append([[0, 0], [1, 0], [0, 1], [1, 1]])     # Square
        self.all_tetromino.append([[0, 0], [1, 0], [2, 0], [3, 0]])     # Long Line
        self.all_tetromino.append([[1, 1], [1, 0], [0, 1], [0, 2]])     # S
        self.all_tetromino.append([[1, 1], [0, 0], [0, 1], [1, 2]])     # Z
        self.all_tetromino.append([[2, 0], [0, 0], [1, 0], [2, 1]])     # L
        self.all_tetromino.append([[2, 0], [0, 0], [1, 0], [2, -1]])    # J
        self.all_tetromino.append([[1, 0], [0, 0], [1, 1], [2, 0]])     # T

        self.tetromino_cur = []         # The tetromino we currently have
        self.tetromino_cur_loc = []     # The location of the tetromino
        self.tetromino_i = 1

        # field size
        self.field = []
        self.field_w, self.field_h = 10, 20           # self.field_w-1, self.field_h-1 = largest column/row value
        self.block_w = self.block_h = 20            # The pixel width and height of a single block
        self.create_field()                         # Initialize field

        # open a new window
        self.size = (self.block_w*self.field_w, self.block_h*self.field_h)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Tetris-clone")

    # game creation
    def create_field(self):
        self.field = []                     # Create an empty field (all values = 0)
        for i in range(self.field_h):
            self.field.append([0]*self.field_w)
        self.get_new_tetromino()

    def check_if_empty(self, location_list):  # is location >=0 and in bounds?
        for loc in location_list:
            if loc[0] < 0 or loc[0] >= self.field_h or loc[1] < 0 or loc[1] >= self.field_w:
                return False
            if self.field[loc[0]][loc[1]] > 0:
                return False

        return True

    def place_tetromino(self):          # get random tetromino and place it on top of the screen
        i_tetro = random.randint(0, len(self.all_tetromino)-1)
        self.tetromino_i = i_tetro+1
        self.tetromino_cur = self.all_tetromino[i_tetro]
        self.tetromino_cur_loc = []
        start_x,start_y = int(self.field_w/2), 0
        for loc in self.tetromino_cur:
            self.tetromino_cur_loc.append([start_y+loc[0], start_x+loc[1]])

        # check if valid
        valid = self.check_if_empty(self.tetromino_cur_loc)
        if valid:
            self.update_val(self.tetromino_cur_loc, -(i_tetro+1))
            return True
        else:
            return False

    def update_val(self, location_list, val):
        for loc in location_list:
            self.field[int(loc[0])][int(loc[1])] = int(val)

    def update_tetromino(self):
        for i_row, row in enumerate(self.field):
            for i_column, val in enumerate(row):
                if val < 0:
                    self.field[i_row][i_column] = 0
        self.update_val(self.tetromino_cur_loc, -self.tetromino_i)

    # move the tetromino in a direction
    def move_tetromino(self, diffx, diffy):

        cur_check = self.tetromino_cur_loc.copy()
        for i_block in range(len(cur_check)):
            cur_check[i_block] = [cur_check[i_block][0]+diffy,cur_check[i_block][1]+diffx]

        if self.check_if_empty(cur_check):  # if space is available, update the block
            self.tetromino_cur_loc = cur_check.copy()       # get the values back to tetromino_cur_loc
            self.update_tetromino()
            return True
        else:
            return False

    def rotate_tetromino(self, dir_rot):  # dir = 1 or -1, meaning a anti clockwise or clockwise movement
        new_tetrino = self.tetromino_cur_loc.copy()
        block_or_x, block_or_y = new_tetrino[0]
        for block_i in range(1, len(new_tetrino)):
            block_new_x, block_new_y = new_tetrino[block_i]

            qx = block_or_x + math.cos(dir_rot * math.pi/2) * (block_new_x-block_or_x) - math.sin(dir_rot * math.pi/2) * (block_new_y-block_or_y)
            qy = block_or_y + math.sin(dir_rot * math.pi / 2) * (block_new_x - block_or_x) + math.cos(dir_rot * math.pi / 2) * (block_new_y - block_or_y)
            new_tetrino[block_i] = [int(qx), int(qy)]

        if self.check_if_empty(new_tetrino): # check if empty, if yes, move on
            self.tetromino_cur_loc = new_tetrino.copy()
            self.update_tetromino()

    def get_new_tetromino(self):
        for loc in self.tetromino_cur_loc:  # turn block into regular blocks
            self.field[loc[0]][loc[1]] = abs(self.field[loc[0]][loc[1]])
        check = self.place_tetromino()      # get a new random tetromino
        return check    # if return false, means we couldn't put down a tetromino, so it is game over.

    def find_all_cleared_lines(self):       # check the field whether any of the rows are cleared or not.
        all_cleared_rows = []
        for i_row, row in enumerate(self.field):
            filled = False if 0 in row else True   # if any value in row = 0, means there are empty holes, so not filled
            if filled:
                all_cleared_rows.append(i_row)
        return all_cleared_rows

    def clear_lines_and_drop_down(self):

        cleared_lines = self.find_all_cleared_lines()
        for row in cleared_lines:
            for column in range(len(self.field[0])):
                self.field[row][column] = 0

            for i_row in range(row, 0, -1):
                for column in range(len(self.field[0])):
                    self.field[i_row][column] = self.field[i_row-1][column]


    # VISUALS
    # drawing the field
    def draw_field(self, update):
        self.screen.fill(self.WHITE)

        # draw our grid:
        for row_i, row in enumerate(self.field):
            for column_i, val in enumerate(row):
                if val != 0:
                    pygame.draw.rect(self.screen, self.color_val[abs(val)-1], [column_i * self.block_h,
                                                            row_i * self.block_w,
                                                            self.block_h,
                                                            self.block_w], 0)

        # --- Go ahead and update the screen with what we've drawn.
        if update:
            pygame.display.flip()

    def draw_start_screen(self):
        self.draw_field(False)

        pygame.draw.rect(self.screen, self.BLACK, [self.size[0]/2-70, self.size[1]/2-50,
                                                                     140, 100], 0)

        textsufrace = self.font.render("Spacebar", True, self.WHITE)
        self.screen.blit(textsufrace, (self.size[0]/2 - 55, self.size[1]/2-40))

        textsufrace = self.font.render("To", True, self.WHITE)
        self.screen.blit(textsufrace, (self.size[0] / 2 - 15, self.size[1] / 2 - 10))

        textsufrace = self.font.render("Start", True, self.WHITE)
        self.screen.blit(textsufrace, (self.size[0] / 2 - 30, self.size[1] / 2+15 ))

        pygame.display.flip()


    def draw_gameover_screen(self):
        self.draw_field(False)

        pygame.draw.rect(self.screen, self.BLACK, [self.size[0]/2-70, self.size[1]/2-50,
                                                                     140, 100], 0)

        textsufrace = self.font.render("Spacebar", True, self.WHITE)
        self.screen.blit(textsufrace, (self.size[0]/2 - 55, self.size[1]/2-40))

        textsufrace = self.font.render("To", True, self.WHITE)
        self.screen.blit(textsufrace, (self.size[0] / 2 - 15, self.size[1] / 2 - 10))

        textsufrace = self.font.render("Restart", True, self.WHITE)
        self.screen.blit(textsufrace, (self.size[0] / 2 - 40, self.size[1] / 2+15 ))

        pygame.display.flip()


    # bugtesting:
    def print_field_debug(self):
        print("Current field : ")
        for row in self.field:
            print(row)

    def runTetris(self):

        while True:

            # figure out whether we are quiting or not
            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    break

                # moving the tetrominos down every N milliseconds
                if event.type == self.MOVEEVENT and self.state == 1:
                    succes = self.move_tetromino(0, 1)
                    if not succes:  # means it is moving down
                        self.clear_lines_and_drop_down()    # check if any lines need to be cleared, and calculate score
                        check = self.get_new_tetromino()    # try to place a new tetromino
                        if not check:
                            self.state = 2       # move onto game over

                if event.type == pygame.KEYDOWN:
                    # self.print_field_debug()

                    if self.state == 1:  # means we are playing
                        # rotation of the tetromino
                        if event.key == pygame.K_a:
                            self.rotate_tetromino(1)
                        if event.key == pygame.K_d:
                            self.rotate_tetromino(-1)

                        # movement of the tetromino
                        if event.key == pygame.K_LEFT:
                            self.move_tetromino(-1, 0)
                        if event.key == pygame.K_RIGHT:
                            self.move_tetromino(1, 0)
                        # if event.key == pygame.K_UP:
                        #     self.move_tetromino(0, -1)
                        if event.key == pygame.K_DOWN:
                            self.move_tetromino(0, 1)
                    if self.state == 0: # means we are at the start
                        if event.key == pygame.K_SPACE:
                            self.state = 1                  # start playing
                    if self.state == 2: # meas we are at the gameover
                        if event.key == pygame.K_SPACE:
                            self.state = 1
                            # reset the field
                            self.create_field()


            # drawing the field
            if self.state==1:
                self.draw_field(True)
            elif self.state==0:     # starting
                self.draw_start_screen()
            elif self.state == 2:       # gameover screen
                self.draw_gameover_screen()

        # quiting pygame
        pygame.quit()


Tt = Tetris()
Tt.runTetris()
