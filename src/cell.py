from graphics import Line, Point, Window


class Cell:
    def __init__(self, win = None):
        self.visited = False
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
    
        line = Line(Point(x1, y1), Point(x1, y2))
        if self.has_left_wall:
            self._win.draw_line(line,"black")
        else:
            self._win.draw_line(line,"white")
    
        line = Line(Point(x2, y1), Point(x2, y2))
        if self.has_right_wall:
            self._win.draw_line(line,"black")
        else:
            self._win.draw_line(line,"white")

        line = Line(Point(x1, y1), Point(x2, y1))
        if self.has_top_wall:
            self._win.draw_line(line,"black")
        else:
            self._win.draw_line(line,"white")
    
        line = Line(Point(x1, y2), Point(x2, y2))
        if self.has_bottom_wall:
            self._win.draw_line(line,"black")
        else:
            self._win.draw_line(line,"white")
    def draw_move(self, to_cell, undo=False):
        from_cell_center_x, from_cell_center_y = self.__get_center()
        to_cell_center_x, to_cell_center_y = to_cell.__get_center()
        line = Line(
            Point(from_cell_center_x, from_cell_center_y),
            Point(to_cell_center_x, to_cell_center_y),
        )
        color = None
        if not undo:
            color = "red"
        else:
            color = "gray"
        self._win.draw_line(line,color)

    def __get_center(self):
        return (self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2
