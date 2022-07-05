import random
from time import sleep 

class RandomAI: 
    def __init__(self, size): 
        self.cached = None 
        self.rounds = [i for i in range(size * size)]
        random.shuffle(self.rounds)
        self.size = size
        self.sleep_flag = True 
    
    def deal(self, chess, _color): 
        if self.cached != chess: 
            self.rounds = [i for i in range(self.size * self.size)] 
            random.shuffle(self.rounds) 
            self.cached = chess
            self.sleep_flag = True 
        if self.sleep_flag: 
            self.sleep_flag = False 
            sleep(0.2)
        result = self.rounds.pop(-1) 
        assert result >= 0 and result < self.size * self.size
        return (result // self.size, result % self.size)