import time
import extra
import board_data


class Bot:
    """
    Класс для работы бота, заменяющего игрока
    """

    def __init__(self, playboard):
        self.playboard = playboard
        self.all_black_pieces = []
        self.all_white_pieces = []
        self.count_forward_move = 0

        # Координаты центров клеток отдельно по осям
        self.cells_pos_col = {'A': 210, 'B': 280, 'C': 350, 'D': 420,
                              'E': 490, 'F': 560, 'G': 630, 'H': 700}
        self.cells_pos_row = {'1': 600, '2': 530, '3': 460, '4': 390,
                              '5': 320, '6': 250, '7': 180, '8': 110}

    def turn(self):
        """
        Действие хода
        """

        self.playboard.update()
        time.sleep(.5)  # Задержка перед ходом бота
        self.find_all_forward_move()

        if self.count_forward_move == 0:
            self.move_back_one()
        elif self.count_forward_move % 2 == 1:
            self.move_forward_end()
        elif self.count_forward_move % 2 == 0:
            self.move_forward_one()

    def find_all_forward_move(self):
        """
        Находит все варианты хода вперед
        """

        self.all_black_pieces = self.find_one_colour_pieces(extra.BLACK)
        self.all_white_pieces = self.find_one_colour_pieces(extra.WHITE)

        self.count_forward_move = self.find_count_forward_move()
    
    def move_forward_one(self):
        """
        Ход вперед на одну клетку
        """

        for i in range(len(self.all_black_pieces)):
            b = self.all_black_pieces[i]
            w = self.all_white_pieces[i]
            if int(b[1]) - int(w[1]) > 2:
                position_start = (self.cells_pos_col[b[0]], self.cells_pos_row[b[1]])
                position_end = (self.cells_pos_col[b[0]], self.cells_pos_row[str(int(b[1]) - 1)])

                self.move(position_start, position_end)
                break

    def move_forward_end(self):
        """
        Ход вперед до фишки (шашки) соперника
        """

        for i in range(len(self.all_black_pieces)):
            b = self.all_black_pieces[i]
            w = self.all_white_pieces[i]
            if int(b[1]) - int(w[1]) > 1:
                position_start = (self.cells_pos_col[b[0]], self.cells_pos_row[b[1]])
                position_end = (self.cells_pos_col[w[0]], self.cells_pos_row[str(int(w[1]) + 1)])

                self.move(position_start, position_end)
                break
    
    def move_back_one(self):
        """
        Ход назад на одну клетку
        """

        for i in range(len(self.all_black_pieces)):
            b = self.all_black_pieces[i]
            w = self.all_white_pieces[i]
            if int(b[1]) < len(board_data.board) and int(b[1]) - int(w[1]) == 1:
                position_start = (self.cells_pos_col[b[0]], self.cells_pos_row[b[1]])
                position_end = (self.cells_pos_col[b[0]], self.cells_pos_row[str(int(b[1]) + 1)])

                self.move(position_start, position_end)
                break
    
    def move(self, start, end):
        """
        Движение фишки (шашки) к заданой клетке
        """
        
        cell = self.playboard.get_cells(start)
        self.playboard.pick_cell(cell)

        cell = self.playboard.get_cells(end)
        self.playboard.pick_cell(cell)

    def find_one_colour_pieces(self, colour):
        """
        Находит местоположение всех фишек (шашек) одного цвета
        """

        one_colour = []

        for piece in self.playboard.get_items_sprite():
            colour_comparison = piece.icolour == colour

            if colour_comparison:
                one_colour.append(piece.field_name)
        
        one_colour.sort()
        return one_colour
    
    def find_count_forward_move(self):
        """
        Находит количество вариантов хода вперед
        """

        count = 0
        for i in range(len(self.all_black_pieces)):
            b = self.all_black_pieces[i]
            w = self.all_white_pieces[i]
            if int(b[1]) - int(w[1]) > 1:
                count += 1
        
        return count
