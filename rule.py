from time import sleep
import time 

COLOR_NONE = 0 

COLOR_BLACK = -1
COLOR_WHITE = 1

COLOR_BLUE = -1 
COLOR_ORANGE = 1

COLORS = {COLOR_NONE, COLOR_BLACK, COLOR_WHITE}

# MOVES = [(1, 0), (0, 1), (-1, 0), (0, -1)]
MOVES = [] 

for i in range(9): 
    MOVES.append(((i % 3 - 1), (i // 3 - 1))) 
MOVES.remove((0, 0))

class Rule: 
    def __init__ (self, chess_board_size): 
        self.chess_board_size = chess_board_size
        # the first position describes the blue flag, and the opponent is orange. 
        self.players = [None, None] 
        self.player_index = None 
        self.registers = [] 
        self.game_controller = [] 
        self.fresh = None 
        # self.delay = 0.05
        self.delay = 0
        self.chess = [COLOR_NONE] * (chess_board_size * chess_board_size) 
        self.show = True     
        self.counter_for_victory = [0, 0] 

    def add_player(self, player) -> bool: 
        return self.set_blue_player(player) or self.set_orange_player(player)
    
    def add_registers(self, f): 
        self.registers.append(f)
    
    def set_blue_player(self, player) -> bool: 
        assert player  
        if (self.players[0]): 
            return False 
        self.players[0] = player 
        return True 

    def set_orange_player(self, player) -> bool: 
        assert player 
        if (self.players[1]): 
            return False 
        self.players[1] = player 
        return True 
    
    def get_scores(self): 
        if (not self.can_set(COLOR_BLUE)) and (not self.can_set(COLOR_ORANGE)): 
            blue_cnt, orange_cnt = 0, 0
            for i in range(self.chess_board_size * self.chess_board_size): 
                if self.chess[i] == COLOR_BLUE: 
                    blue_cnt += 1 
                elif self.chess[i] == COLOR_ORANGE: 
                    orange_cnt += 1 
            return (blue_cnt, orange_cnt) 
        else: 
            return None 

    def force_set_index_with_color(self, row, col, color, advanced=0) -> bool: 
        assert color in COLORS 
        if (row < 0 or row >= self.chess_board_size): 
            return False 
        if (col < 0 or col >= self.chess_board_size): 
            return False 
        self.chess[row * self.chess_board_size + col] = color 
        if self.show: 
            for i in self.registers: 
                i(row, col, color, advanced=advanced) 
    
    def can_set_index_with_color(self, row, col, color) -> bool: 
        assert color in [COLOR_BLUE, COLOR_ORANGE]
        if (self.chess[row * self.chess_board_size + col] != COLOR_NONE): 
            return False 
        for move_strategy in MOVES: 
            tmp_row, tmp_col = row, col
            count = 0 
            while True: 
                tmp_row += move_strategy[0] 
                tmp_col += move_strategy[1] 
                if tmp_row < 0 or tmp_row >= self.chess_board_size: 
                    break 
                if tmp_col < 0 or tmp_col >= self.chess_board_size: 
                    break 
                tmp_color = self.chess[tmp_row * self.chess_board_size + tmp_col]
                if tmp_color == COLOR_NONE: 
                    break 
                elif tmp_color == color: 
                    if count: 
                        return True 
                    else: 
                        break 
                else: 
                    count += 1 
        return False 
    
    def can_set(self, color) -> bool: 
        assert color in [COLOR_BLUE, COLOR_ORANGE] 
        for r in range(self.chess_board_size): 
            for c in range(self.chess_board_size): 
                if self.can_set_index_with_color(r, c, color): 
                    return True  
        return False 
    
    def flush(self): 
        for i in range(self.chess_board_size * self.chess_board_size): 
            if not self.fresh: 
                break 
            self.fresh(i // self.chess_board_size, i % self.chess_board_size, self.chess[i]) 
    
    def attempt_set_index_with_color(self, row, col, color) -> bool: 
        if not self.can_set_index_with_color(row, col, color): 
            return False 
        change_indexs = [[]] * 8 
        tmp_indexs = [] 
        for move_strategy in MOVES: 
            tmp_indexs.clear() 
            tmp_row, tmp_col = row, col
            while True: 
                tmp_row += move_strategy[0] 
                tmp_col += move_strategy[1] 
                if tmp_row < 0 or tmp_row >= self.chess_board_size: 
                    break 
                if tmp_col < 0 or tmp_col >= self.chess_board_size: 
                    break 
                tmp_color = self.chess[tmp_row * self.chess_board_size + tmp_col]
                if tmp_color == COLOR_NONE: 
                    break 
                elif tmp_color == color: 
                    # change_indexs.extend(tmp_indexs)
                    assert len(tmp_indexs) < 8
                    for i, index in enumerate(tmp_indexs): 
                        change_indexs[i].append(index) 
                    break 
                else: 
                    tmp_indexs.append((tmp_row, tmp_col))
        # change_indexs.append((row, col)) 
        if self.show: 
            self.flush() 
        self.force_set_index_with_color(row, col, color, advanced=2) 
        for indexes_to_change in change_indexs: 
            if self.delay: 
                sleep(self.delay)
            for index_to_change in indexes_to_change: 
                self.chess[index_to_change[0] * self.chess_board_size + index_to_change[1]] = color 
                if self.show: 
                    for r in self.registers: 
                        r(index_to_change[0], index_to_change[1], color, advanced=1)
        return True 

    def start(self, start_t = time.time()): 
        self.chess = [COLOR_NONE] * (self.chess_board_size * self.chess_board_size) 
        # the first position describes the blue flag, and the opponent is orange. 
        assert self.player_index is None 
        self.player_index = 0 
        if self.show: 
            for i in self.game_controller: 
                i(-1)
        assert self.chess_board_size & 1 == 0 
        mid_position = self.chess_board_size // 2
        self.force_set_index_with_color(mid_position - 1, mid_position - 1, COLOR_BLUE) 
        self.force_set_index_with_color(mid_position, mid_position - 1, COLOR_ORANGE) 
        self.force_set_index_with_color(mid_position - 1, mid_position, COLOR_ORANGE) 
        self.force_set_index_with_color(mid_position, mid_position, COLOR_BLUE) 
        winner = None 
        while True: 
            winner = self.get_scores() 
            if winner: 
                print ("Game over! ")
                print (f"??????????????????{winner[0]}, ??????????????????{winner[1]}. ")
                if winner[0] > winner[1]: 
                    self.counter_for_victory[1] += 1 
                elif winner[1] > winner[0]: 
                    self.counter_for_victory[0] += 1 
                break 
            if self.can_set(2 * self.player_index - 1): 
                result = self.players[self.player_index](self.chess.copy(), self.player_index * 2 - 1)
                assert len(result) == 2
                if not self.attempt_set_index_with_color(result[0], result[1], self.player_index * 2 - 1): 
                    continue 
            self.player_index = self.player_index ^ 1
            if self.show: 
                for f in self.game_controller: 
                    f(self.player_index * 2 - 1)
            # print ("???????????????{}. ".format("??????" if self.player_index == 0 else "??????"))
        if self.show is None: 
            if self.cnt > 0: 
                self.cnt -= 1 
                self.player_index = None 
                self.start(start_t)
            else: 
                end_p = time.time() 
                dura = end_p - start_t
                print (f"?????????????????????????????? {dura}s. ?????????????????????{self.counter_for_victory[0]}, ?????????????????????{self.counter_for_victory[1]}. ")
        elif not self.show: 
            self.flush()  
        
    def add_controller(self, f): 
        self.game_controller.append(f) 