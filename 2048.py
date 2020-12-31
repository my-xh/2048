import curses
from random import randrange, choice
from collections import defaultdict

actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
letter_codes = [ord(char) for char in 'WASDRQwasdrq']
actions_dict = dict(zip(letter_codes, actions * 2))


# 获取用户行为
def get_user_action(keyboard):
    char = 'N'
    while char not in actions_dict:
        # 返回按下键位的ASCII码值
        char = keyboard.getch()
    # 返回输入键位对应的行为
    return actions_dict[char]


# 矩阵转置
def transpose(field):
    return [list(row) for row in zip(*field)]


# 矩阵逆转
def invert(field):
    return [row[::-1] for row in field]


# 棋盘类
class GameField:

    def __init__(self, height=4, width=4, win=2048):
        self.height = height    # 棋盘高
        self.width = width      # 棋盘宽
        self.win_value = win    # 过关分数
        self.score = 0          # 当前分数
        self.highscore = 0      # 最高分
        self.reset()

    # 重置棋盘
    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)]
                      for j in range(self.height)]
        self.spawn()
        self.spawn()

    # 随机生成一个2或4
    def spawn(self):
        num = 4 if randrange(100) > 89 else 2
        i, j = choice([(i, j) for i in range(self.width)
                       for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = num

    # 判断输赢
    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions)

    # 棋盘单元向指定方向移动
    def move(self, direction):
        def move_row_left(row):
            """将一行左移"""
            def tighten(row):
                """把非0单元挤到一块"""
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                """合并相邻元素"""
                pair = False    # 相邻单元是否相等
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(row[i] * 2)
                        self.score += row[i] * 2
                        pair = False
                    else:
                        if (i + 1 < len(row)) and row[i] == row[i + 1]:
                            pair = True
                        else:
                            new_row.append(row[i])
                new_row += [0] * (len(row) - len(new_row))
                # 断言合并后不会改变行列大小，否则报错
                assert len(new_row) == len(row)
                return new_row

            return merge(tighten(row))

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(
            [move_row_left(row) for row in invert(field)])
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(
            moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    # 判断能否向指定方向移动
    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            """判断一行里面是否有单元进行左移动或合并"""
            def change(i):
                """检测第i个单元是否发生变化"""
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] == row[i + 1]:
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field: any(
            row_is_left_movable(row) for row in field)
        check['Right'] = lambda field: any(
            row_is_left_movable(row) for row in invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

    # 绘制棋盘
    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '    (R)Restart (Q)Exit'
        win_string = '        You Win!'
        gameover_string = '        GAME OVER'

        def cast(string):
            # 将传入的内容显示到终端
            screen.addstr(string + '\n')

        # 绘制水平分割线
        def draw_hor_separator():
            line = '+-----' * self.width + '+'
            cast(line)

        # 绘制垂直分割线
        def draw_row(row):
            line = '|' + '|'.join([f'{i:^5}' if i != 0 else ' ' * 5 for i in row]) + '|'
            cast(line)

        # 清空屏幕
        screen.clear()
        # 绘制分数和最高分
        cast(f'SCORE: {self.score}')
        if self.highscore != 0:
            cast(f'HIGHSCORE: {self.highscore}')
        # 绘制分割线和数字
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        # 绘制帮助文字
        if self.is_win():
            cast(win_string)
        elif self.is_gameover():
            cast(gameover_string)
        else:
            cast(help_string1)
        cast(help_string2)


# 主函数
def main(stdscr):
    def init():
        game_field.reset()
        return 'Game'

    def not_game(state):
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        # 当用户行为不是重置或退出时，一直保持当前状态
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Exit'] = 'Init', 'Exit'

        return responses[action]

    def game():
        game_field.draw(stdscr)
        action = get_user_action(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            # 每次成功移动一步，则判断是否胜利或者游戏结束
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    state_actions = {
        'Init': init,
        'Game': game,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
    }

    curses.use_default_colors()
    game_field = GameField(win=2048)

    state = 'Init'

    while state != 'Exit':
        state = state_actions[state]()


curses.wrapper(main)
