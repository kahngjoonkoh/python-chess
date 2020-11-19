from tkinter import *
import tkinter.ttk

board = [['♜', '♞', '♝', '♛', '♚', '♝', '♞', '♜'],
         ['♟', '♟', '♟', '♟', '♟', '♟', '♟', '♟'],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['♙', '♙', '♙', '♙', '♙', '♙', '♙', '♙'],
         ['♖', '♘', '♗', '♕', '♔', '♗', '♘', '♖']
         ]
buttons = []
cell_size = 60
piece_size = 40
piece_selected = False
########################## Initialise #######################
window = Tk()
window.title("Chess")
icon = PhotoImage(file="chess_icon.png")
white_block = PhotoImage(file="white_block.PNG")
gray_block = PhotoImage(file="gray_block.PNG")
window.iconphoto(False, icon)
window.geometry("545x560")

####################### Functions #########################
def change_skin_to_default():
    global buttons
    skin = ("helvetica", piece_size)
    buttons = []
    set_buttons(skin)


#Need to find a new font
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

##Start work from here
def piece_control(i, j):
    global piece_selected, select_memory
    coordinates = [i, j]
    piece = buttons[i][j]["text"]
    print(piece, coordinates)

    if piece != "" and not piece_selected: #Selecting a piece
        piece_selected = True
        select_memory = [piece, coordinates]

    elif piece == "" and piece_selected: #Movement
        pass
    elif piece != "" and piece_selected: #Occupied Cell
        if piece:
            pass




##################### Menu Bar #####################
menu_bar = Menu(window)
skin_menu = Menu(menu_bar, tearoff=0)
skin_menu.add_command(label="Default", command=change_skin_to_default)
skin_menu.add_command(label="Arial", command=change_skin_to_arial)
menu_bar.add_cascade(label="Change Skin", menu=skin_menu)
window.config(menu=menu_bar)


#Equivalent to set_buttons()
change_skin_to_default()


window.mainloop()