#!/usr/bin/env python
# -*- coding:utf-8 -*-


class Action:
    """行为类

    定义用户允许的操作行为，并将用户输入映射到对应行为

    Attributes:
        stdscr: 从标准窗口获取用户输入
        actions_dict： 存储[按键->行动]映射关系的字典
    """

    UP = 'up'
    LEFT = 'left'
    DOWN = 'down'
    RIGHT = 'right'
    RESTART = 'restart'
    EXIT = 'exit'

    actions = [UP, LEFT, DOWN, RIGHT, RESTART, EXIT]
    letter_codes = [ord(char) for char in 'WASDRQwasdrq']
    actions_dict = dict(zip(letter_codes, actions * 2))

    def __init__(self, stdscr):
        self.stdscr = stdscr

    def get(self):
        """获取用户行为

        Returns:
            输入键位对应的行为
        """
        char = 'N'
        while char not in self.actions_dict:
            # 获取按下键位的ASCII码值
            char = self.stdscr.getch()
        return self.actions_dict[char]
