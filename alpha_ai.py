# import numba 

# alpha-beta 剪枝下的 AI 搜索策略

class AlphaAI: 
    def __init__(self, size, eva = lambda t: -sum(t), depth = 4): 
        self.size = size 
        self.evaluate_function = eva
        self.depth = depth 

    def deal(self, chess, color): 
        if sum(map(lambda _: 1, filter(lambda t: t, chess))) == self.size * self.size - self.depth - 1: 
            self.evaluate_function = lambda t: -sum(t) 
        position, _ = self.search(chess, color, None, None, self.depth)
        print (_)
        # print (position)
        assert position 
        return position

    # @numba.njit 
    def search(self, chess: list[int], color: int, alpha: int, beta: int, deep: int) -> tuple[tuple[int, int], tuple[int, int]]: # Result; ((select position index x, index y), solution(alpha, beta))
        # print ("search")
        if not deep: 
            v = self.evaluate_function(chess) 
            return None, (v, v)
            # return None, self.evaluate_function(chess)
        l = collect_result(chess, self.size, color)
        chosen = None 
        if not l: 
            _, (a, b) = self.search(chess, -color, alpha, beta, deep-1) 
            if color == 1: 
                if alpha is None or alpha < b: 
                    alpha = b 
            else: 
                if beta is None or beta > a: 
                    beta = a 
            return None, (alpha, beta)
        for ((x, y), changes) in l: 
            
            for _x, _y in changes: 
                chess[_x * self.size + _y] = color 
            chess[x * self.size + y] = color 

            (_, (a, b)) = self.search(chess, -color, alpha, beta, deep-1) 

            for _x, _y in changes: 
                chess[_x * self.size + _y] = -color; 
            chess[x * self.size + y] = 0 

            if color == 1: 
                if alpha is None or alpha < b: 
                    chosen = (x, y)
                    alpha = b 
                if beta and alpha > beta: 
                    return (chosen, (alpha, beta)) 
            else: 
                if beta is None or beta > a: 
                    chosen = (x, y)
                    beta = a 
                if alpha and alpha > beta: 
                    return (chosen, (alpha, beta))

        return chosen, (alpha, beta) 
            
MOVES = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]    

# @numba.njit
def collect_result(chess: list[int], size: int, color: int) -> list[tuple[tuple[int, int], list[tuple[int, int ]]]]: 
    result = [] 
    # 考虑 reserve 相关的元素操作
    for x in range(size): 
        for y in range(size): 
            if chess[x * size + y]: 
                continue 
            changes = [] 
            for move in MOVES: 
                tmp_x, tmp_y = x, y 
                tmps = [] 
                while True: 
                    tmp_x += move[0] 
                    tmp_y += move[1] 
                    if tmp_x < 0 or tmp_x >= size or tmp_y < 0 or tmp_y >= size: 
                        break 
                    _c = chess[tmp_x * size + tmp_y]
                    if _c == color: 
                        changes.extend(tmps) 
                        break 
                    elif not _c: 
                        break 
                    else: 
                        assert _c == -color 
                        tmps.append((tmp_x, tmp_y))
            if changes: 
                result.append(((x, y), changes))
    return result 

if __name__ == '__main__': 
    result = [] 
    size = 8
    # result.reserve(size * size) 
    print (result)

def get_mobility(chess): 
    return -\
        len(collect_result(chess, 8, 1)) + \
        len (collect_result(chess, 8, -1))

EVALUATE_CONSIDER = [
    [50, -13, 14, -7, -7, 14, -13, 50], 
    [-13, 3, 7, -3, -3, 7, 3, -13], 
    [14, 7, -13, 2, 2, -13, 7, 14], 
    [-7, -3, 2, 2, 2, 2, -3, -7], 
    [-7, -3, 2, 2, 2, 2, -3, -7], 
    [14, 7, -13, 2, 2, -13, 7, 14], 
    [-13, 3, 7, -3, -3, 7, 3, -13], 
    [50, -13, 14, -7, -7, 14, -13, 50], 
]

def evaluate_consider(chess): 
    assert len(chess) == 64 
    ans = 0 
    cnt = 0 
    for i in range(8): 
        for j in range(8): 
            ans += chess[i * 8 + j] * EVALUATE_CONSIDER[i][j] 
            if chess[i*8+j]: 
                cnt += 1 
    ans2 = get_mobility(chess) * 3
    print (f"ans2 = {ans2}, but ans = {-ans}. ") 
    if cnt < 40: 
        return ans2 - ans 
    else: 
        return -ans 