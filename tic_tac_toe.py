import tkinter as tk
import numpy as np

def define_sign(idx):
    def set_buttonval(idx):
        index = buttons[idx]
        global player_turn, board, won, moves, playable
        # won = locals()['won']
        # if won:
        #     print(f'Player{player_turn} has won')
        button = globals()[f'button{idx}']
        create_label = lambda text: tk.Label(root, text=text, 
                                            bg='purple', font= 'times 15').place(x=150 , y=550 )
        if (not board[index] == 'X' or board[index] == 'O') and playable:
            turn = player_dict[player_turn]
            button['text'] = turn
            button['bg'] = bgcolor[turn]
            button['fg'] = font_color[turn]
            # button['size'] = 
            board[index] = turn
            winner = get_winner(board)
            print(winner)
            if winner:
                print('has winner', turn, '\n')
                globals()['won'] = True
                create_label(f'player {player_turn} won')
                playable = False

            else:
                player_turn = turn_dict[player_turn]
                # print(index, 'pressed\n')
                print(display_turn.format(player_turn))

            moves += 1
            print(moves)
            # print(board)

        else:
            button['bg'] = 'white'
            button['text'] = None
            button['fg'] = None
            print('not playble\n')

            
        if moves == 9 and playable:
            create_label(f'draw')

        
    # if all(map(all, board)):
    #     print(board)

    return lambda: set_buttonval(idx)

# nonlocal won
moves = 0
won = False
playable = True
display_turn = 'player {} turn'
player_turn = '1'
turn_dict = {'2': '1', '1': '2'}
player_dict = {'1': 'X', '2': 'O'}
bgcolor = {'X': 'black', 'O': 'yellow'}
font_color = {'X': 'white', 'O': 'black'}
rows_columns = zip([0] * 3 + [1] * 3 + [2] * 3, 
                   [0, 1, 2] * 3)       

buttons = dict(zip(range(1, 10), rows_columns))
board = np.array([['n', 'c', 'm'],
                 ['v', 'l', 't'],
                 ['b', 'g', 'r']])

def get_winner(board):
    has_winner = []
    for letter in 'X', 'O':
        has_winner.append(
                          (
                           map(letter.__eq__, [board[(0, 0)], board[(0, 1)], board[(0, 2)]]), # horizontal win
                           map(letter.__eq__, [board[(1, 0)], board[(1, 1)], board[(1, 2)]]),
                           map(letter.__eq__, [board[(2, 0)], board[(2, 1)], board[(2, 2)]]),

                           map(letter.__eq__, [board[(0, 0)], board[(1, 0)], board[(2, 0)]]), # vertical win
                           map(letter.__eq__, [board[(0, 1)], board[(1, 1)], board[(2, 1)]]),
                           map(letter.__eq__, [board[(0, 2)], board[(1, 2)], board[(2, 2)]]),

                           map(letter.__eq__, [board[(0, 0)], board[(1, 1)], board[(2, 2)]]), # diagonal win
                           map(letter.__eq__, [board[(0, 2)], board[(1, 1)], board[(2, 0)]])
                                                                                            )
                                                                                             )
        has_winner.append(map(all, has_winner.pop(-1)))
    
    return any(map(any, has_winner))


root = tk.Tk()
root.title('tic tac toe')
root.geometry('600x600')


for i, letter in zip(range(1, 3), ['X', 'O']):
    tk.Label(root, text=f'Player {i}: {letter}',
          font='times 15').grid(row=0, column=i)

idx_column_row = zip(range(1, 10), 
                    [1, 2, 3] * 3, [1] * 3 + [4] * 3 + [7] * 3)

for idx, column, row in idx_column_row:
    globals()[f'button{idx}'] = tk.Button(root, width=20, height=10,
                                        command=define_sign(idx))

    button = globals()[f'button{idx}']
    button.grid(row=row, column=column)

print('player 1 turn')


root.mainloop()
