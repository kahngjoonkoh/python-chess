from tkinter import *

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
select_memory = {"piece": None, "coordinates": None}
log_history = []
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

# TODO: Create the alphabet and numeric notations on the sides
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
            buttons[i].append(Button(window, text=board[i][j]))
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


def end_turn(piece, coordinates, motion):
    global piece_selected, turn, select_memory
    log = f"{select_memory['piece']}[{select_memory['coordinates']['x']+1},{select_memory['coordinates']['y']+1}] {motion} {piece}[{coordinates['x']+1},{coordinates['y']+1}]"
    if select_memory["piece"] == "♙" and select_memory["coordinates"]["x"] == 1 and coordinates["x"] == 0:
        promote("white")
    elif select_memory["piece"] == "♟" and select_memory["coordinates"]["x"] == 6 and coordinates["x"] == 7:
        promote("black")
    print(log)
    piece_selected = False
    select_memory = {"piece": None, "coordinates": None}
    if turn == "white":
        turn = "black"
    else:
        turn = "white"
    refresh_board()


# TODO: fix this later
def update_turn(root):
    print("updating")
    if turn == "white":
        root.entryconfigure(0, label="White's turn")
        print("changed")
    elif turn == "black":
        root.entryconfigure(0, label="Black's turn")
    window.update()


def promote(c):
    global select_memory, promotion_window
    small_font = ("helvetica", 20)
    promotion_window = Tk()
    promotion_window.title("Select Promotion")
    promotion_window.geometry("260x55")
    if c == "white":
        Button(promotion_window, text="♙", font=small_font,
               command=lambda color=c, p="♙", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=0)
        Button(promotion_window, text="♘", font=small_font,
               command=lambda color=c, p="♘", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=1)
        Button(promotion_window, text="♗", font=small_font,
               command=lambda color=c, p="♗", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=2)
        Button(promotion_window, text="♖", font=small_font,
               command=lambda color=c, p="♖", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=3)
        Button(promotion_window, text="♕", font=small_font,
               command=lambda color=c, p="♕", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=4)

    elif c == "black":
        Button(promotion_window, text="♟", font=small_font,
               command=lambda color=c, p="♟", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=0)
        Button(promotion_window, text="♞", font=small_font,
               command=lambda color=c, p="♞", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=1)
        Button(promotion_window, text="♝", font=small_font,
               command=lambda color=c, p="♝", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=2)
        Button(promotion_window, text="♜", font=small_font,
               command=lambda color=c, p="♜", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=3)
        Button(promotion_window, text="♛", font=small_font,
               command=lambda color=c, p="♛", root=promotion_window: promote_to(color, p, root)).grid(row=0, column=4)

# TODO: Change all the print(log) to display_log() or something equivalent
def promote_to(color, p, root):
    global piece, coordinates, select_memory
    tile["text"] = p
    board[coordinates["x"]][coordinates["y"]] = p
    promoted_to = p
    if color == "white":
        log = f"♙-🎖️→{promoted_to}"
    elif color == "black":
        log = f"♟-🎖️→{promoted_to}"
    print(log)
    root.destroy()


def select_piece(i, j):
    global piece_selected, select_memory, tile
    piece_selected = True
    tile["image"] = sel_block
    select_memory = {"piece": piece, "coordinates": coordinates}
    if piece == "♙":  # White Pawn
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

    # If a piece is newly selected and its the person's turn.
    if piece != " " and not piece_selected and color == turn:  # Selecting a piece
        select_piece(i, j)

    # Movement
    elif tile["image"] == "pyimage5":
        tile["text"] = select_memory["piece"]
        board[i][j] = select_memory["piece"]
        buttons[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]]["text"] = " "
        board[select_memory["coordinates"]["x"]][select_memory["coordinates"]["y"]] = " "
        end_turn(piece, coordinates, "→")

    # Cancellation
    elif coordinates == select_memory["coordinates"]:
        piece_selected = False
        select_memory = {"piece": None, "coordinates": None}
        refresh_board()

    # coordinates != select_memory["coordinates"] is implied
    # Choosing a different piece.
    elif piece != " " and color == turn:
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
        end_turn(piece, coordinates, "⚔")  # Print the capture too






##################### Menu Bar #####################
menu_bar = Menu(window)


# TODO: Create a log history
def show_log():
    log_window = Tk()
    log_window.title("Log History")
    log_window.geometry("300x500")


skin_menu = Menu(menu_bar, tearoff=0)
skin_menu.add_command(label="Default", command=reset_board)
skin_menu.add_command(label="Arial", command=change_skin_to_arial)

overall_menu = Menu(menu_bar, tearoff=0)
overall_menu.add_cascade(label="Show Log", command=show_log)
overall_menu.add_cascade(label="Skin Settings", menu=skin_menu)
overall_menu.add_separator()
# TODO: Save & Quit feature
overall_menu.add_cascade(label="Quit", command=window.destroy)

menu_bar.add_cascade(label="☰", menu=overall_menu)

# TODO: Label should change after end_turn()
menu_bar.add_cascade(label="White's turn") # , command=lambda: update_turn(menu_bar)

window.config(menu=menu_bar)


#Equivalent to set_buttons()
reset_board()


window.mainloop()