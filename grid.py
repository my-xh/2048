#!/usr/bin/env python
# -*- coding:utf-8 -*-

from random import randrange, choice


class Grid:
    """网格类

    定义网格数据，以及单元格移动、合并的方法

    Attributes:
        size: 网格尺寸
    """

    def __init__(self, size):
        self.height = size  # 网格高
        self.width = size   # 网格宽
        self.cells = None   # 网格单元格
        self.score = 0
        self.highscore = 0
        self.reset()

    def _add_random_item(self):
        """随机选择一个空的单元格，并随机设置为2或者4"""
        item = 4 if randrange(100) > 89 else 2
        i, j = choice([(i, j) for i in range(self.width)
                       for j in range(self.height) if self.cells[i][j] == 0])
        self.cells[i][j] = item

    def _transpose(self):
        """网格转置，行列交换"""
        self.cells = [list(row)for row in zip(*self.cells)]

    def _invert(self):
        """网格逆转，行翻转"""
        self.cells = [row[::-1] for row in self.cells]

    def _move_row_left(self, row):
        """将一行单元格全部左移

        Returns:
            移动后的一行单元格
        """
        def tighten(row):
            """把非0单元挤到一块"""
            new_row = [i for i in row if i != 0]
            new_row += [0] * (len(row) - len(new_row))

            return new_row

        def merge(row):
            """合并相邻单元"""
            pair = False    # 相邻单元是否相等
            new_row = []

            for i in range(len(row)):
                if pair:
                    new_row.append(row[i] * 2)
                    self.score += (row[i] * 2)
                    pair = False
                else:
                    if (i + 1) < len(row) and row[i] == row[i + 1]:
                        pair = True
                    else:
                        new_row.append(row[i])
            new_row += [0] * (len(row) - len(new_row))

            return new_row

        return merge(tighten(row))

    def _move_left(self):
        """单元格左移"""
        self.cells = [self._move_row_left(row) for row in self.cells]

    def _move_right(self):
        """单元格右移"""
        self._invert()
        self._move_left()
        self._invert()

    def _move_up(self):
        """单元格上移"""
        self._transpose()
        self._move_left()
        self._transpose()

    def _move_down(self):
        """单元格下移"""
        self._transpose()
        self._move_right()
        self._transpose()

    @staticmethod
    def _can_move_row_left(row):
        """检测一行单元格是否能够左移"""
        def change(i):
            """检测第i个位置是否可以改变"""
            if row[i] == 0 and row[i + 1] != 0:  # 可以移动
                return True
            if row[i] == row[i + 1]:               # 可以合并
                return True
            return False
        return any(change(i) for i in range(len(row) - 1))

    def _can_move_left(self):
        """检测单元格能否向左移动"""
        return any(self._can_move_row_left(row) for row in self.cells)

    def _can_move_right(self):
        """检测单元格能否向右移动"""
        self._invert()
        can = self._can_move_left()
        self._invert()
        return can

    def _can_move_up(self):
        """检测单元格能否向上移动"""
        self._transpose()
        can = self._can_move_left()
        self._transpose()
        return can

    def _can_move_down(self):
        """检测单元格能否向下移动"""
        self._transpose()
        can = self._can_move_right()
        self._transpose()
        return can

    def reset(self):
        """重置网格"""
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.cells = [[0 for i in range(self.width)]
                      for j in range(self.height)]
        self._add_random_item()
        self._add_random_item()

    def can_move(self, direction):
        """检测单元格能否向指定方向移动"""
        def not_found():
            """默认处理方法"""
            return False
        return getattr(self, '_can_move_' + direction, not_found)()

    def move(self, direction):
        """单元格向指定方向移动

        Returns:
            是否成功移动
        """
        if self.can_move(direction):
            getattr(self, '_move_' + direction)()
            self._add_random_item()
            return True
        else:
            return False
