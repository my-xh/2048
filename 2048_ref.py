#!/usr/bin/env python
# -*- coding:utf-8 -*-

import curses
from collections import defaultdict
from action import Action
from grid import Grid
from screen import Screen


class GameManager:
    """游戏管理器

    负责游戏启动，以及游戏状态的转换

    Attributes:
        size: 网格尺寸
        win_num: 胜利目标
    """

    def __init__(self, size=4, win_num=2048):
        self.grid = Grid(size)
        self.win_num = win_num
        self.reset()

    def __call__(self, stdscr):
        """主程序"""
        curses.use_default_colors()
        self.stdscr = stdscr
        self.action = Action(stdscr)

        while self.state != self._state_exit:
            self.state = getattr(self, '_state_' + self.state)

    @property
    def _screen(self):
        """根据给定信息生成对应的窗口对象"""
        return Screen(self.stdscr, self.grid, self.win, self.over)

    @property
    def _state_init(self):
        """初始状态"""
        self.reset()
        return 'game'

    @property
    def _state_game(self):
        """游戏状态"""
        self._screen.draw()
        action = self.action.get()

        if action == Action.RESTART:
            return 'init'
        if action == Action.EXIT:
            return 'exit'
        if self.grid.move(action):
            # 每次成功移动一步，则判断是否胜利或者游戏结束
            if self.is_win:
                return 'win'
            if self.is_over:
                return 'over'

        return 'game'

    def _restart_or_exit(self, state):
        """非游戏状态"""
        self._screen.draw()
        action = self.action.get()

        # 当用户行为不是RESTART或EXIT时，一直保持当前状态
        state_transform = defaultdict(lambda: state)
        state_transform[Action.RESTART] = 'init'
        state_transform[Action.EXIT] = 'exit'

        return state_transform[action]

    @property
    def _state_win(self):
        """游戏胜利状态"""
        return self._restart_or_exit('win')

    @property
    def _state_over(self):
        """游戏结束状态"""
        return self._restart_or_exit('over')

    @property
    def _state_exit(self):
        """游戏退出状态"""
        return 'exit'

    @property
    def is_win(self):
        """判断是否胜利"""
        self.win = any(any(i >= self.win_num for i in row)
                       for row in self.grid.cells)
        return self.win

    @property
    def is_over(self):
        """判断是否结束"""
        self.over = not any(self.grid.can_move(action)
                            for action in Action.actions)
        return self.over

    def reset(self):
        """重置游戏"""
        self.state = 'init'
        self.win = False
        self.over = False
        self.grid.reset()


if __name__ == '__main__':
    size = 4
    win_num = 2048
    curses.wrapper(GameManager(size=size, win_num=win_num))
