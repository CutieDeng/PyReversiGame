from random import random
import tkinter

from rule import Rule, COLOR_ORANGE, COLOR_BLUE
from threading import Thread, Semaphore, main_thread

index = None 
waiting = Semaphore() 
waiting4index = Semaphore() 

main_window = tkinter.Tk()
main_window.config(bg='white')

def set_player(color): 
    if color == COLOR_ORANGE: 
        main_window.config(bg='#FF7006')
        # c.config(bg='#FF7006')
    elif color == COLOR_BLUE: 
        main_window.config(bg='#1CE1FF')
        # c.config(bg='#1CE1FF')
    else: 
        assert False 
    main_window.update()

main_frame = tkinter.Frame(main_window) 
main_frame.pack(padx=15, pady=15)
# main_frame.place()

BLOCK_SIZE = 100
CHESS_BOARD_SIZE = 8

blocks = [None] * (CHESS_BOARD_SIZE * CHESS_BOARD_SIZE)

rule = Rule(CHESS_BOARD_SIZE)
rule.add_controller(set_player)

for index in range(CHESS_BOARD_SIZE * CHESS_BOARD_SIZE): 

    c = tkinter.Canvas(main_frame, width=BLOCK_SIZE, height=BLOCK_SIZE)

    def click_event_handle_closure(index): 
        my_index = index 
        def click_event_handle(arg): 
            waiting.acquire(timeout=1)
            global index 
            index = my_index 
            waiting4index.release() 
        return click_event_handle

    c.bind('<ButtonRelease-1>', click_event_handle_closure(index))

    # c.config(highlightthickness=1.0, highlightcolor="green") 

    # 蓝方
    # c.config(bg='#1CE1FF')

    # 橙方
    # c.config(bg='#FF7006')

    # 普通格子
    c.config(bg='#DDFF31')

    c.grid(column=index % CHESS_BOARD_SIZE, row=index // CHESS_BOARD_SIZE)
    blocks[index] = c 

def change_colors(row, col, color): 
    assert color in [COLOR_BLUE, COLOR_ORANGE]
    blocks[row * CHESS_BOARD_SIZE + col].config(bg=
        '#1CE1FF' if color == COLOR_BLUE else '#FF7006')
rule.add_registers(change_colors)

def player_click(chess_board, color): 
    waiting.release() 
    waiting4index.acquire() 
    r, c = index // CHESS_BOARD_SIZE, index % CHESS_BOARD_SIZE
    return (r, c) 

import random_ai 

ai = random_ai.RandomAI(CHESS_BOARD_SIZE)

rule.add_player(player_click) 
rule.add_player(ai.deal)
# rule.add_player(player_click) 

new_thread = Thread(target=rule.start)
new_thread.start()

main_frame.mainloop() 