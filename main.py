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
icon = PhotoImage(file="graphics/chess_icon.png") #pyimage1
white_block = PhotoImage(file="graphics/white_block.PNG") #pyimage2
gray_block = PhotoImage(file="graphics/gray_block.PNG") #pyimage3
sel_block = PhotoImage(file="graphics/turquoise_block.PNG") #pyimage4
move_block = PhotoImage(file="graphics/purple_block.PNG") #pyimage6
capture_block = PhotoImage(file="graphics/red_block.PNG") #pyimage7
window.iconphoto(False, icon)
window.geometry("570x600")
window.resizable(False, False)

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


def convert_coordinates(i1, j1, i2, j2):
    x1 = "abcdefgh"[j1]
    x2 = "abcdefgh"[j2]
    y1 = "87654321"[i1]
    y2 = "87654321"[i2]
    return x1, y1, x2, y2


def end_turn(piece, coordinates, motion):
    global piece_selected, turn, select_memory
    x1, y1, x2, y2 = convert_coordinates(select_memory['coordinates']['x'], select_memory['coordinates']['y'], coordinates['x'], coordinates['y'])
    log = f"{select_memory['piece']} {x1}{y1} {motion} {piece} {x2}{y2}"
    if select_memory["piece"] == "♙" and select_memory["coordinates"]["x"] == 1 and coordinates["x"] == 0:
        promote("white")
    elif select_memory["piece"] == "♟" and select_memory["coordinates"]["x"] == 6 and coordinates["x"] == 7:
        promote("black")
    log_history.append(log)
    update_log()
    piece_selected = False
    select_memory = {"piece": None, "coordinates": None}
    if turn == "white":
        turn = "black"
        menu_bar.delete("White's Turn")
        menu_bar.add_cascade(label="Black's Turn")
    else:
        turn = "white"
        menu_bar.delete("Black's Turn")
        menu_bar.add_cascade(label="White's Turn")
    refresh_board()


def promote(c):
    global select_memory, promotion_window
    small_font = ("helvetica", 20)
    promotion_window = Tk()
    promotion_window.title("Select Promotion")
    promotion_window.geometry("260x55")
    promotion_window.resizable(False, False)
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


def promote_to(color, p, root):
    global piece, coordinates, select_memory
    tile["text"] = p
    board[coordinates["x"]][coordinates["y"]] = p
    promoted_to = p
    if color == "white":
        log_history.append(f"♙ ⚜ {promoted_to}")
    elif color == "black":
        log_history.append(f"♟ ⚜ {promoted_to}")
    update_log()
    root.destroy()


def compare(i, j, max):
    if max:
        if i >= j:
            return i
        else:
            return j
    else:
        if i >= j:
            return j
        else:
            return i


# TODO: Get rid of repetitiveness
def knight(i, j, text):
    if i >= 2:
        if j >= 1:  # 11:00 direction
            if buttons[i - 2][j - 1]["text"] == " ":
                buttons[i - 2][j - 1]["image"] = move_block
            elif buttons[i - 2][j - 1]["text"] in text:
                buttons[i - 2][j - 1]["image"] = capture_block
        if j <= 6:  # 1:00 direction
            if buttons[i - 2][j + 1]["text"] == " ":
                buttons[i - 2][j + 1]["image"] = move_block
            elif buttons[i - 2][j + 1]["text"] in text:
                buttons[i - 2][j + 1]["image"] = capture_block
    if i <= 5:
        if j >= 1:  # 7:00 direction
            if buttons[i + 2][j - 1]["text"] == " ":
                buttons[i + 2][j - 1]["image"] = move_block
            elif buttons[i + 2][j - 1]["text"] in text:
                buttons[i + 2][j - 1]["image"] = capture_block
        if j <= 6:  # 5:00 direction
            if buttons[i + 2][j + 1]["text"] == " ":
                buttons[i + 2][j + 1]["image"] = move_block
            elif buttons[i + 2][j + 1]["text"] in text:
                buttons[i + 2][j + 1]["image"] = capture_block
    if j >= 2:
        if i >= 1:  # 11:00 direction
            if buttons[i - 1][j - 2]["text"] == " ":
                buttons[i - 1][j - 2]["image"] = move_block
            elif buttons[i - 1][j - 2]["text"] in text:
                buttons[i - 1][j - 2]["image"] = capture_block
        if i <= 6:  # 8:00 direction
            if buttons[i + 1][j - 2]["text"] == " ":
                buttons[i + 1][j - 2]["image"] = move_block
            elif buttons[i + 1][j - 2]["text"] in text:
                buttons[i + 1][j - 2]["image"] = capture_block
    if j <= 5:
        if i >= 1:  # 2:00 direction
            if buttons[i - 1][j + 2]["text"] == " ":
                buttons[i - 1][j + 2]["image"] = move_block
            elif buttons[i - 1][j + 2]["text"] in text:
                buttons[i - 1][j + 2]["image"] = capture_block
        if i <= 6:  # 4:00 direction
            if buttons[i + 1][j + 2]["text"] == " ":
                buttons[i + 1][j + 2]["image"] = move_block
            elif buttons[i + 1][j + 2]["text"] in text:
                buttons[i + 1][j + 2]["image"] = capture_block


def bishop(i, j, text):
    if i >= 1 and j >= 1:  # 10:30 direction
        for shift in range(1, compare(i, j, False) + 1):
            if buttons[i - shift][j - shift]["text"] == " ":
                buttons[i - shift][j - shift]["image"] = move_block
            elif buttons[i - shift][j - shift]["text"] in text:
                buttons[i - shift][j - shift]["image"] = capture_block
                break
            else:
                break
    if i >= 1 and j <= 6:  # 1:30 direction
        for shift in range(1, compare(i, 7 - j, False) + 1):
            if buttons[i - shift][j + shift]["text"] == " ":
                buttons[i - shift][j + shift]["image"] = move_block
            elif buttons[i - shift][j + shift]["text"] in text:
                buttons[i - shift][j + shift]["image"] = capture_block
                break
            else:
                break
    if i <= 6 and j >= 1:  # 7:30 direction
        for shift in range(1, compare(7 - i, j, False) + 1):
            if buttons[i + shift][j - shift]["text"] == " ":
                buttons[i + shift][j - shift]["image"] = move_block
            elif buttons[i + shift][j - shift]["text"] in text:
                buttons[i + shift][j - shift]["image"] = capture_block
                break
            else:
                break
    if i <= 6 and j <= 6:  # 4:30 direction
        for shift in range(1, compare(7 - i, 7 - j, False) + 1):
            if buttons[i + shift][j + shift]["text"] == " ":
                buttons[i + shift][j + shift]["image"] = move_block
            elif buttons[i + shift][j + shift]["text"] in text:
                buttons[i + shift][j + shift]["image"] = capture_block
                break
            else:
                break


def rook(i, j, text):
    if j >= 1:  # 9:00 direction
        for shift in range(1, j+1):
            if buttons[i][j - shift]["text"] == " ":
                buttons[i][j - shift]["image"] = move_block
            elif buttons[i][j - shift]["text"] in text:
                buttons[i][j - shift]["image"] = capture_block
                break
            else:
                break
    if i >= 1:  # 12:00 direction
        for shift in range(1, i+1):
            if buttons[i - shift][j]["text"] == " ":
                buttons[i - shift][j]["image"] = move_block
            elif buttons[i - shift][j]["text"] in text:
                buttons[i - shift][j]["image"] = capture_block
                break
            else:
                break
    if j <= 6:  # 3:00 direction
        for shift in range(1, 8-j):
            if buttons[i][j + shift]["text"] == " ":
                buttons[i][j + shift]["image"] = move_block
            elif buttons[i][j + shift]["text"] in text:
                buttons[i][j + shift]["image"] = capture_block
                break
            else:
                break
    if i <= 6:  # 6:00 direction
        for shift in range(1, 8-i):
            if buttons[i + shift][j]["text"] == " ":
                buttons[i + shift][j]["image"] = move_block
            elif buttons[i + shift][j]["text"] in text:
                buttons[i + shift][j]["image"] = capture_block
                break
            else:
                break


def king(i, j, text):
    if i >= 1 and j >= 1:  # 10:30 direction
        if buttons[i - 1][j - 1]["text"] == " ":
            buttons[i - 1][j - 1]["image"] = move_block
        elif buttons[i - 1][j - 1]["text"] in text:
            buttons[i - 1][j - 1]["image"] = capture_block
    if i >= 1 and j <= 6:  # 1:30 direction
        if buttons[i - 1][j + 1]["text"] == " ":
            buttons[i - 1][j + 1]["image"] = move_block
        elif buttons[i - 1][j + 1]["text"] in text:
            buttons[i - 1][j + 1]["image"] = capture_block

    if i <= 6 and j >= 1:  # 7:30 direction
        if buttons[i + 1][j - 1]["text"] == " ":
            buttons[i + 1][j - 1]["image"] = move_block
        elif buttons[i + 1][j - 1]["text"] in text:
            buttons[i + 1][j - 1]["image"] = capture_block

    if i <= 6 and j <= 6:  # 4:30 direction
        if buttons[i + 1][j + 1]["text"] == " ":
            buttons[i + 1][j + 1]["image"] = move_block
        elif buttons[i + 1][j + 1]["text"] in text:
            buttons[i + 1][j + 1]["image"] = capture_block
    if j >= 1:  # 9:00 direction
            if buttons[i][j - 1]["text"] == " ":
                buttons[i][j - 1]["image"] = move_block
            elif buttons[i][j - 1]["text"] in text:
                buttons[i][j - 1]["image"] = capture_block

    if i >= 1:  # 12:00 direction
        if buttons[i - 1][j]["text"] == " ":
            buttons[i - 1][j]["image"] = move_block
        elif buttons[i - 1][j]["text"] in text:
            buttons[i - 1][j]["image"] = capture_block

    if j <= 6:  # 3:00 direction
        if buttons[i][j + 1]["text"] == " ":
            buttons[i][j + 1]["image"] = move_block
        elif buttons[i][j + 1]["text"] in text:
            buttons[i][j + 1]["image"] = capture_block

    if i <= 6:  # 6:00 direction
        if buttons[i + 1][j]["text"] == " ":
            buttons[i + 1][j]["image"] = move_block
        elif buttons[i + 1][j]["text"] in text:
            buttons[i + 1][j]["image"] = capture_block


def select_piece(i, j):
    global piece_selected, select_memory, tile
    piece_selected = True
    tile["image"] = sel_block
    select_memory = {"piece": piece, "coordinates": coordinates}
    # TODO:En passant capture
    # TODO:Castling, Check and Checkmate features.
    if piece == "♙":  # White Pawn
        if i == 6 and buttons[i - 1][j]["text"] == " ":  # Two space movement at first move
            buttons[i - 1][j]["image"] = move_block
            if buttons[i - 2][j]["text"] == " ":
                buttons[i - 2][j]["image"] = move_block
        elif buttons[i - 1][j]["text"] == " " and i != 0:  # Single space movement for every other situation
            buttons[i - 1][j]["image"] = move_block

        if j != 0 and buttons[i - 1][j - 1]["text"] in "♟♞♝♜♛♚":  # Capture
            buttons[i - 1][j - 1]["image"] = capture_block
        if j != 7 and buttons[i - 1][j + 1]["text"] in "♟♞♝♜♛♚":
            buttons[i - 1][j + 1]["image"] = capture_block

    elif piece == "♟":  # Black Pawn
        if i == 1 and buttons[i+1][j]["text"] == " ":  # Two space movement at first move
            buttons[i + 1][j]["image"] = move_block
            if buttons[i + 2][j]["text"] == " ":
                buttons[i + 2][j]["image"] = move_block
        elif buttons[i + 1][j]["text"] == " " and i != 7:  # Single space movement for every other situation
            buttons[i + 1][j]["image"] = move_block

        if j != 0 and buttons[i + 1][j - 1]["text"] in "♙♘♗♖♕♔":  # Capture
            buttons[i + 1][j - 1]["image"] = capture_block
        if j != 7 and buttons[i + 1][j + 1]["text"] in "♙♘♗♖♕♔":
            buttons[i + 1][j + 1]["image"] = capture_block

    elif piece == "♘":  # White Knight
        knight(i, j, "♟♞♝♜♛♚")

    elif piece == "♞":  # Black Knight
        knight(i, j, "♙♘♗♖♕♔")

    elif piece == "♗":  # White Bishop
        bishop(i, j, "♟♞♝♜♛♚")

    elif piece == "♝":  # Black Bishop
        bishop(i, j, "♙♘♗♖♕♔")

    elif piece == "♖":  # White Rook
        rook(i, j, "♟♞♝♜♛♚")

    elif piece == "♜":  # Black Rook
        rook(i, j, "♙♘♗♖♕♔")

    elif piece == "♕":  # White Queen
        bishop(i, j, "♟♞♝♜♛♚")
        rook(i, j, "♟♞♝♜♛♚")

    elif piece == "♛":  # Black Queen
        bishop(i, j, "♙♘♗♖♕♔")
        rook(i, j, "♙♘♗♖♕♔")

    elif piece == "♔":  # White King
        king(i, j, "♟♞♝♜♛♚")

    elif piece == "♚":  # Black King
        king(i, j, "♙♘♗♖♕♔")


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


def show_log():
    global log_list
    log_window = Tk()
    log_window.title("Log History")
    log_window.geometry("250x300")
    scrollbar = Scrollbar(log_window, orient=VERTICAL)
    log_list = Listbox(log_window, yscrollcommand=scrollbar.set)
    log_list.config(font=("Helvetica", 20))
    log_list.config(height=300, width=250)
    scrollbar.config(command=log_list.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    log_list.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar.pack(side=RIGHT, fill=BOTH)
    log_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=log_list.yview)
    update_log()
    mainloop()


def update_log():
    try:
        log_list.delete(0, END)
        for l in log_history:
            log_list.insert(END, l)
        log_list.see("end")
    except:
        pass


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

# TODO: The turn should be updated every turn
menu_bar.add_cascade(label="White's Turn")

window.config(menu=menu_bar)


# Equivalent to set_buttons()
reset_board()
for k in range(8):
    alphabet = "abcdefgh"[k]
    num = "87654321"[k]
    Label(window, text=alphabet, font=("helvetica", 20)).grid(row=8, column=k)
    Label(window, text=num, font=("helvetica", 20)).grid(row=k, column=8)


window.mainloop()