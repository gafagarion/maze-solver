from cell import Cell
import time
import random


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        if seed is not None:
            random.seed(seed)
        else:
            random.seed(0)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + self._cell_size_x * i
        y1 = self._y1 + self._cell_size_y * j
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.0005)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        # Mark current cell as visited
        self._cells[i][j].visited = True

        while True:
            to_visit = []

            # cell to the left
            if i > 0 and not self._cells[i - 1][j].visited:
                to_visit.append((i - 1, j))

            # cell to the right
            if i + 1 < self._num_cols and not self._cells[i + 1][j].visited:
                to_visit.append((i + 1, j))

            # cell to the top
            if j > 0 and not self._cells[i][j - 1].visited:
                to_visit.append((i, j - 1))

            # cell to the bottom
            if j + 1 < self._num_rows and not self._cells[i][j + 1].visited:
                to_visit.append((i, j + 1))

            # if blocked, break from the loop
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return

            # pick a random direction
            direction_index = random.randrange(len(to_visit))
            next_index = to_visit[direction_index]

            # knocking down the wall
            # left
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False

            # right
            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            # top
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            # bottom
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False

            # move to next cell
            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True

        # we reached the end of the maze
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        # If there is a cell in that direction, there is no wall blocking you, and that cell hasn't been visited
        # left
        if (
            i > 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i - 1][j].has_right_wall
            and not self._cells[i][j].has_left_wall
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], undo=True)

        # right
        if (
            i + 1 < self._num_cols
            and not self._cells[i + 1][j].visited
            and not self._cells[i + 1][j].has_left_wall
            and not self._cells[i][j].has_right_wall
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], undo=True)

        # top
        if (
            j > 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j - 1].has_bottom_wall
            and not self._cells[i][j].has_top_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], undo=True)

        # bottom
        if (
            j + 1 < self._num_rows
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j + 1].has_top_wall
            and not self._cells[i][j].has_bottom_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], undo=True)

        # no way out found
        return False
