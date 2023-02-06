import pygame as pg
import time
from iteams import Checker1, Checker2
from extra import *
from board_data import *
import bot

pg.init()
pg.font.init()

class Playboard:
    def __init__(self, parent_surface: pg.Surface):
        self.font = pg.font.SysFont('ubuntu', 18, italic=True)
        self.__screen = parent_surface
        self.__table = board
        self.__count = CELL_COUNT
        self.__size = CELL_SIZE
        self.__item_types = types
        self.__current_turn = WHITE
        self.__cells_sprite = pg.sprite.Group()
        self.__items_sprite = pg.sprite.Group()
        self.__all_areas = pg.sprite.Group()
        self.__items_white = []
        self.__items_black = []
        self.__items_coords = []
        self.__pressed_cell = None
        self.__picked_checker = None
        self.__background()
        self.__draw_playboard()
        self.__draw_items()
        self.__possible_move = []
        pg.display.update()

        self.opponent = bot.Bot(self)
    
    def get_current_turn(self):
        return self.__current_turn
    
    def get_items_sprite(self):
        return self.__items_sprite

    # фон
    def __background(self):
        background_image = pg.image.load('images/' + 'back_gr.jpg')
        background_image = pg.transform.scale(background_image, WINDOW_SIZE)
        self.__screen.blit(background_image, (0, 0))

    def __draw_playboard(self):
        total_size = self.__count * self.__size
        # номера полей
        numbers_fields = self.__numbers_fields()
        self.__cells_sprite = self.__create_cells()
        # сами игровые поля
        width = numbers_fields[0].get_width()
        board_view = pg.Surface((2 * width + total_size, 2 * width + total_size), pg.SRCALPHA)

        contour_image = pg.image.load('images/' + 'frame.jpg')
        contour_image = pg.transform.scale(contour_image, (board_view.get_width(), board_view.get_height()))
        board_view.blit(contour_image, contour_image.get_rect())

        board_view.blit(numbers_fields[0], (0, width))
        board_view.blit(numbers_fields[0], (width + total_size, width))
        board_view.blit(numbers_fields[1], (width, 0))
        board_view.blit(numbers_fields[1], (width, width + total_size))

        board_rect = board_view.get_rect()
        board_rect.x += (self.__screen.get_width() - board_rect.width) // 2
        board_rect.y += (self.__screen.get_height() - board_rect.height) // 2
        # прикрепление поверхности к screen
        self.__screen.blit(board_view, board_rect)
        cells_direction = (board_rect.x + width, board_rect.y + width)
        self.__draw_cells(cells_direction)

    def __numbers_fields(self):
        n_lines = pg.Surface((self.__count * self.__size, self.__size // 2), pg.SRCALPHA)
        n_rows = pg.Surface((self.__size // 2, self.__count * self.__size), pg.SRCALPHA)
        # корректировка клеток

        for i in range(0, self.__count):
            letters = self.font.render(names[i], 1, WHITE)
            number = self.font.render(str(self.__count - i), 1, WHITE)
            n_lines.blit(letters, (i * self.__size + (self.__size - letters.get_rect().width) // 2,
                                   (n_lines.get_height() - letters.get_rect().height) // 2))
            n_rows.blit(number, ((n_rows.get_width() - letters.get_rect().width) // 2,
                                 i * self.__size + (self.__size - number.get_rect().height) // 2))
        return n_rows, n_lines

    def __create_cells(self):
        group = pg.sprite.Group()
        even_count = (self.__count % 2 == 0)
        cell_colour_index = 1 if even_count else 0
        # отрисовка ячеек
        for y in range(self.__count):
            for x in range(self.__count):
                cells = Cells(cell_colour_index, self.__size, (x, y), names[x] + str(self.__count - y))
                group.add(cells)
                cell_colour_index ^= True
            cell_colour_index = cell_colour_index ^ True if even_count else cell_colour_index
        return group

    # смещение и прорисовка ячеек со спрайтами
    def __draw_cells(self, direction):
        for cells in self.__cells_sprite:
            cells.rect.x += direction[0]
            cells.rect.y += direction[1]
        self.__cells_sprite.draw(self.__screen)

    # отрисовка фигурок на соответствующие поля
    def __draw_items(self):
        self.__run_board()
        self.__black_or_white()
        self.__items_sprite.draw(self.__screen)

    def __run_board(self):
        for j, row in enumerate(self.__table):
            for i, field_value in enumerate(row):
                if field_value != 0:
                    item = self.__create_item(field_value, (j, i))
                    self.__items_sprite.add(item)
        for item in self.__items_sprite:
            for cells in self.__cells_sprite:
                if item.field_name == cells.field_name:
                    item.colour = cells.colour
                    item.rect = cells.rect

    # table_coord = координаты в матрице
    def __create_item(self, item_symbol: str, table_coord: tuple):
        field_name = self.__to_field_name(table_coord)
        item_tuple = self.__item_types[item_symbol]
        classname = globals()[item_tuple[0]]
        return classname(self.__size, item_tuple[0], field_name)

    def __to_field_name(self, table_coord: tuple):
        return names[table_coord[1]] + str(self.__count - table_coord[0])

    def get_cells(self, position: tuple):
        for cells in self.__cells_sprite:
            if cells.rect.collidepoint(position):
                return cells
        return None

    def button_down(self, button_type: int, position: tuple):
        self.__pressed_cell = self.get_cells(position)

    def button_up(self, button_type: int, position: tuple):
        released_cell = self.get_cells(position)
        if (released_cell is not None) and (released_cell == self.__pressed_cell):
            if button_type == 3:
                self.__mark_cell(released_cell)
            if button_type == 1:
                self.pick_cell(released_cell)

    def __black_or_white(self):
        for item in self.__items_sprite:
            if item.icolour == Checker1.icolour:
               self.__items_white.append(item.field_name)
            elif item.icolour == Checker2.icolour:
                self.__items_black.append(item.field_name)
        return self.__items_white, self.__items_black

    def update(self):
        self.__cells_sprite.draw(self.__screen)
        self.__items_sprite.draw(self.__screen)

        pg.display.update()

    def check_user_color(self, piece):
        all_color = {Checker1: 'White', Checker2: 'Black'}
        return all_color[type(piece)]

    def pick_cell(self, cells):
        self.__unmark_all_cell()

        # Берет фишку
        if self.__picked_checker is None:
            for piece in self.__items_sprite:
                if piece.field_name == cells.field_name and piece.icolour == self.__current_turn:
                    pick = Area(cells, False)
                    self.__all_areas.add(pick)
                    self.__picked_checker = piece
                    self.__possible_move = self.find_possible_move(self.__picked_checker)
                    self.update()
                    break
            else:
                if cells.colour == 0:
                    self.__field_cell = cells.field_name
                    self.__jump_forward = []
                    self.__jump_backward = []
        
        # Кладет фишку
        elif cells.field_name in self.__possible_move:
            change_colour = {WHITE: BLACK, BLACK: WHITE}

            self.__picked_checker.rect = cells.rect
            self.__picked_checker.field_name = cells.field_name
            self.__picked_checker = None
            self.__current_turn = change_colour[self.__current_turn]  # меняем цвет хода
            self.update()
            end = self.check_end_game()
            
            if self.get_current_turn() == BLACK and end != 'end':
                self.opponent.turn()
            elif end == 'end':
                time.sleep(3)
                self.__init__(pg.display.set_mode(WINDOW_SIZE))

    def find_possible_move(self, piece) -> list:
        """
        Возвращает имена клеток с возможными вариантами хода
        """

        possible_move = []
        opposite = self.find_opposite_piece(piece.field_name)
        if self.__current_turn == WHITE:
            for i in range(1, int(opposite[1])):
                possible_move.append(opposite[0] + str(i))
        else:
            for i in range(len(board) - int(opposite[1])):
                possible_move.append(opposite[0] + str(len(board) - i))
        
        if piece.field_name in possible_move:
            possible_move.remove(piece.field_name)

        return possible_move
    
    def find_opposite_piece(self, field_name) -> str:
        """
        Возращает местоположение фишки (шашки) соперника
        """

        for piece in self.__items_sprite:
            column_comparison = piece.field_name[0] == field_name[0]
            colour_comparison = piece.icolour != self.__current_turn

            if column_comparison and colour_comparison:
                return piece.field_name

    def __unmark_all_cell(self):
        self.__all_areas.empty()
        for cell in self.__cells_sprite:
            cell.mark = False

    def __mark_cell(self,cells):
            mark = Area(cells)
            self.__all_areas.add(mark)
    
    def draw_text(self, text, colour):
        """
        Отрисовка текста о завершении игры
        """

        if 'arial' in pg.font.get_fonts():
            use_font = 'arial'
        else:
            use_font = 'ubuntu'

        font = pg.font.SysFont(use_font, 72)
        follow = font.render(text, 1, colour)

        self.__screen.blit(follow, (WINDOW_SIZE[0] / 9, WINDOW_SIZE[1] // 2.5))
        pg.display.update()

    def check_end_game(self):
        """
        Проверка на завершение игры (когда не осталось ходов у текущего игрока)
        """

        all_move = []

        for piece in self.__items_sprite:
            possible_move = self.find_possible_move(piece)
            if piece.icolour == self.__current_turn and possible_move:
                all_move.append(possible_move)
        
        if not all_move:
            if self.__current_turn == BLACK:
                self.draw_text('БЕЛЫЕ ВЫИГРАЛИ!', (212, 196, 55))
            elif self.__current_turn == WHITE:
                self.draw_text('ЧЕРНЫЕ ВЫИГРАЛИ!', (212, 196, 55))
            return 'end'


class Cells(pg.sprite.Sprite):
    def __init__(self, colour_index: int, size: int, coords: tuple, name: str):
        super().__init__()
        x, y = coords
        self.colour = colour_index
        self.field_name = name
        self.image = pg.image.load(COLOURS[colour_index])
        self.image = pg.transform.scale(self.image, (size, size))
        self.rect = pg.Rect(x * size, y * size, size, size)


class Area(pg.sprite.Sprite):
    def __init__(self, cells: Cells , type_of_area: bool = True):
        super().__init__()
        coords = (cells.rect.x, cells.rect.y)
        area_size = (cells.rect.width, cells.rect.height)
        if type_of_area:
            self.rect = pg.Rect(coords, area_size)
            self.field_name = cells.field_name
