from tkinter import *
import tkinter.ttk

board = [['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
         ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
         ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
         ]
buttons = []
cell_size = 60
piece_size = 40
piece_selected = False
turn = "white"
########################## Initialise #######################
window = Tk()
window.title("Chess")
icon = PhotoImage(file="chess_icon.png") #pyimage1
white_block = PhotoImage(file="white_block.PNG") #pyimage2
gray_block = PhotoImage(file="gray_block.PNG") #pyimage3
sel_block = PhotoImage(file="turquoise_block.PNG") #pyimage4
move_block = PhotoImage(file="purple_block.PNG") #pyimage6
capture_block = PhotoImage(file="red_block.PNG") #pyimage7
window.iconphoto(False, icon)
window.geometry("544x565")

####################### Functions #########################
def reset_board():
    global buttons
    skin = ("helvetica", piece_size)
    buttons = []
    set_buttons(skin)


# TODO: Need to find a new font
def change_skin_to_arial():
    global buttons
    skin = ("serif", piece_size)
    buttons = []
    set_buttons(skin)


def set_buttons(skin):
    for i in range(8):
        buttons.append([])
        for j in range(8):
            buttons[i].append(tkinter.Button(window, text=board[i][j]))
            buttons[i][j].configure(command= lambda i=i, j=j: piece_control(i, j))
            buttons[i][j].config(height=cell_size, width=cell_size, font=skin)
            buttons[i][j].grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
            if (i+j)%2 == 0:
                buttons[i][j].config(image=white_block, compound="center")
            else:
                buttons[i][j].config(image=gray_block, compound="center")


def refresh_board():
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                buttons[i][j].config(image=white_block, compound="center")
            else:
                buttons[i][j].config(image=gray_block, compound="center")

def end_turn():
    global piece_selected, turn, select_memory
    piece_selected = False
    select_memory = {"piece": None, "coordinates": None}
    if turn == "white":
        turn = "black"
    else:
        turn = "white"
    refresh_board()

##Start work from here
def piece_control(i, j):
    global piece_selected, turn, select_memory
    coordinates = {"x":i, "y":j}
    tile = buttons[i][j]
    piece = tile["text"]
    if piece in "♙♘♗♖♕♔":
        color = "white"
    elif piece in "♟♞♝♜♛♚":
        color = "black"
    else:
        color = None
    print(piece, coordinates)
    print(tile["image"],piece_selected,color,turn)

    #If a piece is newly selected and its the person's turn.
    if piece != " " and not piece_selected and color == turn: #Selecting a piece
        piece_selected = True
        tile["image"] = sel_block
        select_memory = {"piece":piece, "coordinates":coordinates}
        if piece == "♙": #White Pawn
            if i == 6: #Two space movement at first move
                buttons[i-1][j]["image"] = move_block
                buttons[i-2][j]["image"] = move_block
            elif buttons[i-1][j]["text"] == " ": #Single space movement for every other situation
                buttons[i-1][j]["image"] = move_block

            if buttons[i-1][j-1]["text"] in "♟♞♝♜♛♚": #Capture
                buttons[i-1][j-1]["image"] = capture_block
            elif buttons[i-1][j+1]["text"] in "♟♞♝♜♛♚":
                buttons[i-1][j+1]["image"] = capture_block


        elif piece == "♟": #Black Pawn
            if i == 1: #Two space movement at first move
                buttons[i+1][j]["image"] = move_block
                buttons[i+2][j]["image"] = move_block
            elif buttons[i+1][j]["text"] == " ": #Single space movement for every other situation
                buttons[i+1][j]["image"] = move_block

            if buttons[i+1][j-1]["text"] in "♙♘♗♖♕♔": #Capture
                buttons[i+1][j-1]["image"] = capture_block
            elif buttons[i+1][j+1]["text"] in "♙♘♗♖♕♔":
                buttons[i+1][j+1]["image"] = capture_block

    #If there was a piece previously selected and its the person's turn to move.
    elif tile["image"] == "pyimage5" and piece_selected: #Movement
        tile["text"] = select_memory["piece"]
        board[i][j] = select_memory["piece"]
        buttons[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]]["text"] = " "
        board[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]] = " "
        end_turn()

    #TODO: cancel when click another piece
    elif coordinates == select_memory["coordinates"]: #cancelation
        piece_selected = False
        select_memory = {"piece":None, "coordinates":None}
        refresh_board()

    if tile["image"] == "pyimage6" and piece_selected: #Capture
        tile["text"] = select_memory["piece"]
        board[i][j] = select_memory["piece"]
        buttons[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]]["text"] = " "
        board[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]] = " "
        end_turn()




##################### Menu Bar #####################
menu_bar = Menu(window)
skin_menu = Menu(menu_bar, tearoff=0)
skin_menu.add_command(label="Default", command=reset_board())
skin_menu.add_command(label="Arial", command=change_skin_to_arial)
menu_bar.add_cascade(label="Change Skin", menu=skin_menu)
window.config(menu=menu_bar)


#Equivalent to set_buttons()
reset_board()


window.mainloop()