def comp(chess, size): 
    return sum(chess)

def format_chess(chess, size): 
    c = "" 
    for i, v in enumerate(chess): 
        if i % size == 0: 
            c += "\n%2d" % v
        else: 
            c += ", %2d" % v
    return c 

class SearchAI: 
    def __init__(self, size): 
        self.size = size
    
    def deal(self, chess, color): 
        _, choosen = self.search(chess, color, comp, 6, color == -1, [None, None])
        assert choosen
        return choosen

    def search(self, chess, color, f, allow, is_minimum, limitation): 
        assert len(chess) == self.size * self.size 
        v = f(chess, self.size)
        if not allow: 
            return (v if not is_minimum else None, v if is_minimum else None), None 

        choosen = None 
        change_sequence = [] 
        tmp_seq = [] 
        MOVES = [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        for r in range(self.size): 
            for c in range(self.size): 
                if chess[r * self.size + c]: 
                    continue 
                change_sequence.clear() 
                for move in MOVES: 
                    tmp_seq.clear() 
                    tmp_r, tmp_c = r + move[0], c + move[1]
                    while True: 
                        if tmp_r < 0 or tmp_r >= self.size: 
                            break 
                        if tmp_c < 0 or tmp_c >= self.size: 
                            break 
                        if not chess[tmp_r * self.size + tmp_c]: 
                            break 
                        if chess[tmp_r * self.size + tmp_c] == color: 
                            change_sequence.extend(tmp_seq) 
                            break 
                        else: 
                            tmp_seq.append((tmp_r, tmp_c))
                        tmp_r += move[0] 
                        tmp_c += move[1] 
                if not change_sequence: 
                    continue 

                _cached_head = chess.copy() 

                for i in change_sequence: 
                    chess[i[0] * self.size + i[1]] = color 
                assert not chess[r * self.size + c]
                chess[r * self.size + c] = color 

                tmp_result, _ = self.search(chess, -color, f, allow - 1, not is_minimum, limitation.copy())
                if is_minimum and (limitation[1] is None or tmp_result[0] is not None and limitation[1] > tmp_result[0]): 
                    limitation[1] = tmp_result[0] 
                    choosen = (r, c)
                elif not is_minimum and (limitation[0] is None or tmp_result[1] is not None and limitation[0] < tmp_result[1]): 
                    limitation[0] = tmp_result[1] 
                    choosen = (r, c)
                
                for i in change_sequence: 
                    # assert chess[i[0] * self.size + i[1]] == color, f"chess[{i[0] * self.size + i[1]}] is {chess[i[0] * self.size + i[1]]}, i[0] = {i[0]}, i[1] = {i[1]}. "
                    chess[i[0] * self.size + i[1]] = -color 
                chess[r * self.size + c] = 0 

                if limitation[0] and limitation[1] and limitation[0] > limitation[1]: 
                    return limitation, None

                assert _cached_head == chess, f"\nchess before: \n{format_chess(_cached_head, self.size)}\n, "\
                    f"chess end: \n{format_chess(chess, self.size)}. \n"
        
        # assert choosen, f"{limitation}, {format_chess(chess, self.size)}, is_minimum = {is_minimum}"
        return limitation, choosen