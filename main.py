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
    refresh_board()


def refresh_board():
    for i in range(8):
        for j in range(8):
            if (i+j)%2 == 0:
                buttons[i][j].config(image=white_block, compound="center")
            else:
                buttons[i][j].config(image=gray_block, compound="center")


def end_turn(piece, coordinates):
    global piece_selected, turn, select_memory
    if select_memory["piece"] == "♟" and select_memory["coordinates"]["x"] == 6 and coordinates["x"] == 7:
        promote("black")
    elif select_memory["piece"] == "♙" and select_memory["coordinates"]["x"] == 1 and coordinates["x"] == 0:
        promote("white")
    piece_selected = False
    select_memory = {"piece": None, "coordinates": None}
    if turn == "white":
        turn = "black"
    else:
        turn = "white"
    refresh_board()


def promote(c):
    print("🎖️")
    small_font = ("helvetica", 20)
    promotion_window = Tk()
    promotion_window.title("Select Promotion")
    promotion_window.geometry("260x55")
    if c == "white":
        Button(promotion_window, text="♙", font=small_font,
               command=lambda p="♙", root=promotion_window: promote_to(p, root)).grid(row=0, column=0)
        Button(promotion_window, text="♘", font=small_font,
               command=lambda p="♘", root=promotion_window: promote_to(p, root)).grid(row=0, column=1)
        Button(promotion_window, text="♗", font=small_font,
               command=lambda p="♗", root=promotion_window: promote_to(p, root)).grid(row=0, column=2)
        Button(promotion_window, text="♖", font=small_font,
               command=lambda p="♖", root=promotion_window: promote_to(p, root)).grid(row=0, column=3)
        Button(promotion_window, text="♕", font=small_font,
               command=lambda p="♕", root=promotion_window: promote_to(p, root)).grid(row=0, column=4)

    elif c == "black":
        Button(promotion_window, text="♟", font=small_font,
               command=lambda p="♟", root=promotion_window: promote_to(p, root)).grid(row=0, column=0)
        Button(promotion_window, text="♞", font=small_font,
               command=lambda p="♞", root=promotion_window: promote_to(p, root)).grid(row=0, column=1)
        Button(promotion_window, text="♝", font=small_font,
               command=lambda p="♝", root=promotion_window: promote_to(p, root)).grid(row=0, column=2)
        Button(promotion_window, text="♜", font=small_font,
               command=lambda p="♜", root=promotion_window: promote_to(p, root)).grid(row=0, column=3)
        Button(promotion_window, text="♛", font=small_font,
               command=lambda p="♛", root=promotion_window: promote_to(p, root)).grid(row=0, column=4)


def promote_to(p, root):
    print("promoting")
    global piece, coordinates, select_memory
    tile["text"] = p
    board[coordinates["x"]][coordinates["y"]] = p
    root.destroy()


def select_piece(i, j):
    global piece_selected, select_memory, tile
    piece_selected = True
    tile["image"] = sel_block
    print(piece)
    select_memory = {"piece": piece, "coordinates": coordinates}
    if piece == "♙":  # White Pawn
        print("1")
        if i == 6:  # Two space movement at first move
            buttons[i - 1][j]["image"] = move_block
            buttons[i - 2][j]["image"] = move_block
        elif buttons[i - 1][j]["text"] == " " and i != 0:  # Single space movement for every other situation
            buttons[i - 1][j]["image"] = move_block

        try:
            if buttons[i - 1][j - 1]["text"] in "♟♞♝♜♛♚":  # Capture
                buttons[i - 1][j - 1]["image"] = capture_block
        except:
            pass
        try:
            if buttons[i - 1][j + 1]["text"] in "♟♞♝♜♛♚":
                buttons[i - 1][j + 1]["image"] = capture_block
        except:
            pass

    # TODO:En passant capture
    elif piece == "♟":  # Black Pawn
        print("2")
        if i == 1:  # Two space movement at first move
            buttons[i + 1][j]["image"] = move_block
            buttons[i + 2][j]["image"] = move_block
        elif buttons[i + 1][j]["text"] == " " and i != 7:  # Single space movement for every other situation
            buttons[i + 1][j]["image"] = move_block

        try:
            if buttons[i + 1][j - 1]["text"] in "♙♘♗♖♕♔":  # Capture
                buttons[i + 1][j - 1]["image"] = capture_block
        except:
            pass
        try:
            if buttons[i + 1][j + 1]["text"] in "♙♘♗♖♕♔":
                buttons[i + 1][j + 1]["image"] = capture_block
        except:
            pass
    print("3")

def piece_control(i, j):
    global piece_selected, turn, select_memory, piece, coordinates, tile
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

    # If a piece is newly selected and its the person's turn.
    if piece != " " and not piece_selected and color == turn:  # Selecting a piece
        select_piece(i, j)

    # Movement
    elif tile["image"] == "pyimage5":
        tile["text"] = select_memory["piece"]
        board[i][j] = select_memory["piece"]
        buttons[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]]["text"] = " "
        board[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]] = " "
        end_turn(piece, coordinates)

    # Cancellation
    elif coordinates == select_memory["coordinates"]:
        piece_selected = False
        select_memory = {"piece": None, "coordinates": None}
        refresh_board()

    # coordinates != select_memory["coordinates"] is implied
    # Choosing a different piece.
    elif piece != " " and color == turn:
        print("inline")
        piece_selected = False
        select_memory = {"piece": None, "coordinates": None}
        refresh_board()
        select_piece(i, j)

    # Capture
    if tile["image"] == "pyimage6":
        tile["text"] = select_memory["piece"]
        board[i][j] = select_memory["piece"]
        buttons[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]]["text"] = " "
        board[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]] = " "
        print("⚔", piece, coordinates)
        end_turn(piece, coordinates)




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