#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Screen:
    """窗口类

    在标准窗口绘制网格和其他信息

    Attributes:
        stdscr: 标准窗口
        grid: 网格
        score: 当前分数
        higscore: 最高分数
        win: 是否胜利
        over: 是否结束
    """

    def __init__(self, stdscr=None, grid=None, win=False, over=False):
        self.stdscr = stdscr
        self.grid = grid
        self.score = grid.score
        self.highscore = grid.highscore
        self.win = win
        self.over = over

    def _cast(self, string):
        """在窗口添加一行内容"""
        self.stdscr.addstr(string + '\n')

    def _draw_hor_seperator(self):
        """绘制水平分割线"""
        line = '+-----' * self.grid.width + '+'
        self._cast(line)

    def _draw_row(self, row):
        """绘制一行单元格"""
        row_cells = '|' + '|'.join([f'{i:^5}' if i != 0 else f'{" ":5}' for i in row]) + '|'
        self._cast(row_cells)

    def draw(self):
        """绘制所有内容"""
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '    (R)Restart (Q)Exit'
        win_string = '        You Win!'
        over_string = '        GAME OVER'

        self.stdscr.clear()     # 清空屏幕

        self._cast(f'SCORE: {self.score}')
        if self.highscore != 0:
            self._cast(f'HIGHSCORE: {self.highscore}')

        for row in self.grid.cells:
            self._draw_hor_seperator()
            self._draw_row(row)
        self._draw_hor_seperator()

        if self.win:
            self._cast(win_string)
        elif self.over:
            self._cast(over_string)
        else:
            self._cast(help_string1)
        self._cast(help_string2)
