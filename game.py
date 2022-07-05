from functools import partial
import tkinter

from rule import COLORS, Rule, COLOR_ORANGE, COLOR_BLUE
import weak_greedy

from threading import Thread, Semaphore

def set_bg_and_text(bg, text, o): 
    if o.text_obj is None: 
        # o.text_obj = o.create_text(option='text')
        o.text_obj = o.create_text(52.5, 52.5, text='', font=(None, 60))
    o.itemconfigure(o.text_obj, text=text)
    o.config(bg=bg)
    o.update()

BLUE_BASIC = '#c6e6e8'
ORANGE_BASIC = '#fba414'

graph_op = {'init': 
        partial(set_bg_and_text, '#e2d849', ''), 
    'blue': 
        partial(set_bg_and_text, BLUE_BASIC, ''), 
        # lambda t: 
        # t.config(bg='#c6e6e8', text=''), # 海天蓝
    'orange': 
        partial(set_bg_and_text, ORANGE_BASIC, ''), 
        # lambda t: 
        # t.config(bg='#fba414', text=''), # 淡橘橙
    'blue_changed': 
        # lambda t: t.config(bg='#1772b4', text=''), #群青色 
        partial(set_bg_and_text, '#1772b4', ''), 
    'orange_changed': 
        # lambda t: t.config(bg='#dc9123', text=''), # 风帆黄
        partial(set_bg_and_text, '#dc9123', ''), 
    'blue_clickd': 
        # lambda t: t.config(bg='#1772b4', text=u'\u00d7'.encode('utf-8')), 
        partial(set_bg_and_text, '#1772b4', str(u'\u2611')), 
    'orange_clickd': 
        # lambda t: t.config(bg='#dc9123', text=u'\u00d7'.encode('utf-8'))
        partial(set_bg_and_text, '#dc9123', str(u'\u2612'))
    } 

index = None 
waiting = Semaphore() 
waiting4index = Semaphore() 

main_window = tkinter.Tk()
main_window.config(bg='white')

def set_player(color): 
    if color == COLOR_ORANGE: 
        main_window.config(bg='#fba414')
    elif color == COLOR_BLUE: 
        main_window.config(bg='#c6e6e8')
    else: 
        assert False 
    main_window.update()

main_frame = tkinter.Frame(main_window) 
main_frame.pack(padx=15, pady=15)

BLOCK_SIZE = 100
CHESS_BOARD_SIZE = 8

blocks = [None] * (CHESS_BOARD_SIZE * CHESS_BOARD_SIZE)

rule = Rule(CHESS_BOARD_SIZE)
rule.add_controller(set_player)

def reset_color(row, col, color): 
    assert color in COLORS
    graph_op['blue' if color == COLOR_BLUE else \
        'orange' if color == COLOR_ORANGE else \
        'init'] (blocks[row * CHESS_BOARD_SIZE + col])
rule.fresh = reset_color

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
    # c.config(bg='#DDFF31')
    c.text_obj = None
    graph_op['init'](c)

    c.grid(column=index % CHESS_BOARD_SIZE, row=index // CHESS_BOARD_SIZE)
    blocks[index] = c 

def change_colors(row, col, color, advanced=2): 
    assert color in [COLOR_BLUE, COLOR_ORANGE]
    strategy = None 
    if advanced == 0: 
        strategy = 'blue' if color == COLOR_BLUE else \
            'orange' if color == COLOR_ORANGE else \
            'init' 
    elif advanced == 1: 
        strategy = 'blue_changed' if color == COLOR_BLUE else \
            'orange_changed' 
    elif advanced == 2: 
        strategy = 'blue_clickd' if color == COLOR_BLUE else \
            'orange_clickd'
    assert strategy
    graph_op[strategy] (blocks[row * CHESS_BOARD_SIZE + col])

rule.add_registers(change_colors)

def player_click(chess_board, color): 
    waiting.release() 
    waiting4index.acquire() 
    r, c = index // CHESS_BOARD_SIZE, index % CHESS_BOARD_SIZE
    return (r, c) 

import random_ai 

rule.add_player(random_ai.RandomAI(CHESS_BOARD_SIZE).deal)
rule.add_player(weak_greedy.GreedyAI(CHESS_BOARD_SIZE).deal)
# rule.add_player(player_click) 
# rule.add_player(player_click) 

new_thread = Thread(target=rule.start)
new_thread.start()

main_frame.mainloop() 