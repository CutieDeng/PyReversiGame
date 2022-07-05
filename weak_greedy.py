class GreedyAI: 
    def __init__(self, size): 
        self.size = size 
    
    def deal(self, chess, color): 
        size = self.size
        assert len(chess) == size * size
        MOVES = [(1, 1), (1, 0), (0, 1), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        selects = [] 
        for r in range(size): 
            for c in range(size): 
                count = 0 
                if chess[r * size + c]: 
                    continue 
                for move in MOVES: 
                    tmp_cnt = 0 
                    tmp_r, tmp_c = r + move[0], c + move[1] 
                    while True: 
                        if tmp_r < 0 or tmp_r >= size: 
                            break 
                        if tmp_c < 0 or tmp_c >= size: 
                            break 
                        if not chess[tmp_r * size + tmp_c]: 
                            break 
                        if chess[tmp_r * size + tmp_c] == color: 
                            count += tmp_cnt 
                            break 
                        else: 
                            tmp_cnt += 1
                        tmp_r += move[0] 
                        tmp_c += move[1] 
                if count: 
                    selects.append((count, (r, c)))
        selects.sort() 
        assert selects
        return selects[0][1]
                    
