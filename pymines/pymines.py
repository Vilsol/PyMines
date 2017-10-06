from random import randint
import tkinter
import os


rows = 8
columns = 8
mine_count = 10
buttons = {}
images = {"counts": {}}

exploded = False
mines = []
normal_color = "SystemButtonFace"
revealed = []
flagged = []
face = None


def game_over():
    global buttons

    face.config(image=images["face_dead"])

    for row in range(rows):
        for col in range(columns):
            buttons[row][col].config(background="red")


def count_bombs_around(row, col):
    bombs = 0

    if (row - 1, col - 1) in mines:
        bombs = bombs + 1
    if (row - 1, col) in mines:
        bombs = bombs + 1
    if (row - 1, col + 1) in mines:
        bombs = bombs + 1

    if (row, col - 1) in mines:
        bombs = bombs + 1
    if (row, col + 1) in mines:
        bombs = bombs + 1

    if (row + 1, col - 1) in mines:
        bombs = bombs + 1
    if (row + 1, col) in mines:
        bombs = bombs + 1
    if (row + 1, col + 1) in mines:
        bombs = bombs + 1

    return bombs


def click_tile(row, col):
    def click():
        global buttons, exploded

        if (row, col) in flagged:
            return

        if exploded:
            return

        if (row, col) in mines:
            buttons[row][col].config(image=images["mine"])
            exploded = True
            game_over()
            return

        revealed.append((row, col))

        bombs = count_bombs_around(row, col)

        if bombs > 0:
            buttons[row][col].config(image=images["counts"][str(bombs)])
        else:
            buttons[row][col].config(image=images["clicked"])

    return click


def toggle_flag(row, col):
    def click(e):
        if exploded:
            return

        if (row, col) not in revealed:
            if (row, col) not in flagged:
                flagged.append((row, col))
                buttons[row][col].config(image=images["flag"])
            else:
                flagged.remove((row, col))
                buttons[row][col].config(image=images["plain"])

    return click


def new_game():
    global buttons, mines, exploded, normal_color

    mines.clear()
    revealed.clear()

    for row in range(rows):
        for col in range(columns):
            buttons[row][col].config(background=normal_color)

    mine_potential = []
    for row in range(rows):
        for col in range(columns):
            mine_potential.append((row, col))
            buttons[row][col].config(image=images["plain"])

    for i in range(mine_count):
        chosen = mine_potential[randint(0, len(mine_potential) - 1)]
        mines.append(chosen)
        mine_potential.remove(chosen)

    exploded = False

    face.config(image=images["face_normal"])


def press_f2(e):
    new_game()


def launch_game():
    global images, buttons, normal_color, face

    root = tkinter.Tk()

    root.title("Mines")
    root.resizable(width=False, height=False)

    dir = os.path.dirname(__file__)
    images["counts"]["1"] = (tkinter.PhotoImage(file=dir + "/images/tile_1.gif"))
    images["counts"]["2"] = (tkinter.PhotoImage(file=dir + "/images/tile_2.gif"))
    images["counts"]["3"] = (tkinter.PhotoImage(file=dir + "/images/tile_3.gif"))
    images["counts"]["4"] = (tkinter.PhotoImage(file=dir + "/images/tile_4.gif"))
    images["counts"]["5"] = (tkinter.PhotoImage(file=dir + "/images/tile_5.gif"))
    images["counts"]["6"] = (tkinter.PhotoImage(file=dir + "/images/tile_6.gif"))
    images["counts"]["7"] = (tkinter.PhotoImage(file=dir + "/images/tile_7.gif"))
    images["counts"]["8"] = (tkinter.PhotoImage(file=dir + "/images/tile_8.gif"))

    images["clicked"] = tkinter.PhotoImage(file=dir + "/images/tile_clicked.gif")
    images["flag"] = tkinter.PhotoImage(file=dir + "/images/tile_flag.gif")
    images["mine"] = tkinter.PhotoImage(file=dir + "/images/tile_mine.gif")
    images["plain"] = tkinter.PhotoImage(file=dir + "/images/tile_plain.gif")

    images["face_normal"] = tkinter.PhotoImage(file=dir + "/images/face_normal.png")
    images["face_dead"] = tkinter.PhotoImage(file=dir + "/images/face_dead.png")

    mine_potential = []
    for row in range(rows):
        buttons[row] = {}
        for col in range(columns):
            mine_potential.append((row, col))

            button = tkinter.Button(
                image=images["plain"],
                command=click_tile(row, col),
                relief="flat",
                background="white",
                activebackground="white",
                activeforeground="white",
                disabledforeground="white",
                highlightbackground="white",
                highlightcolor="white",
                highlightthickness=0,
                anchor="nw",
                borderwidth=2,
                width=16,
                height=16,
                padx=2,
                pady=2
            )

            button.grid(row=row + 1, column=col)
            button.bind("<Button-3>", toggle_flag(row, col))

            normal_color = button.cget("background")

            buttons[row][col] = button

    for i in range(mine_count):
        chosen = mine_potential[randint(0, len(mine_potential) - 1)]
        mines.append(chosen)
        mine_potential.remove(chosen)

    face = tkinter.Button(
        image=images["face_normal"],
        command=new_game,
        relief="flat",
        background="white",
        activebackground="white",
        activeforeground="white",
        disabledforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        highlightthickness=0,
        anchor="nw",
        borderwidth=2,
        width=16,
        height=16,
        padx=2,
        pady=2
    )

    face.grid(row=0, column=3, columnspan=2, pady=5)

    w = tkinter.Label(
        text="F2 = Reset",
        background="white",
        activebackground="white",
        activeforeground="white",
        disabledforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        highlightthickness=0,
        borderwidth=0,
        padx=0,
        pady=0,
        font=("Arial", 7)
    )

    w.grid(row=0, column=0, columnspan=3, pady=5)

    version = tkinter.Label(
        text="v1.0.2",
        background="white",
        activebackground="white",
        activeforeground="white",
        disabledforeground="white",
        highlightbackground="white",
        highlightcolor="white",
        highlightthickness=0,
        borderwidth=0,
        padx=0,
        pady=0,
        font=("Arial", 7)
    )

    version.grid(row=0, column=5, columnspan=3, pady=5)

    root.config(background="white")

    root.bind("<F2>", press_f2)

    root.iconify()
    root.update()
    root.deiconify()
    root.mainloop()


def execute():
    launch_game()


if __name__ == '__main__':
    launch_game()
