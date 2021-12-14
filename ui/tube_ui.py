from tkinter import messagebox

from tests.test_tube import test_multi_bend, Bend
import tkinter as tk
from tkinter import *
from typing import List, Tuple, Dict


C_ROWS = 40
C_COLS = 40
C_WIDTH = 10*(C_ROWS+2)
C_HEIGHT = 10*(C_COLS+2)

# https://realpython.com/python-gui-tkinter/
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas-methods.html


class Draft_Bend:
    """
    A Simple class structure for representing a draft bend. Differs from a Bend because rather than
    a set height and width, the Draft_Bend has a bendiness factor.
    """

    def __init__(self, position: int, bendiness: float, bend_dir: int):
        """
        :param position: where along the length of the snake the bend takes place
        :param bendiness: how tall the bend is in a number from 0 to 1
        :param bend_dir: which way the bend goes
        """
        self.position: int = position
        self.bendiness: float = bendiness
        self.bend_dir: int = bend_dir
        assert self.position is not None
        assert self.bendiness is not None
        assert self.bend_dir is not None
        assert bendiness >= 0
        assert bendiness <= 1

    def __str__(self):
        return f"bend {self.position} + {self.bendiness} + {self.bend_dir}"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self.position

    def __lt__(self, other):
        if isinstance(other, Draft_Bend):
            return self.position < other.position
        elif type(other) is int:
            return self.position < other
        else:
            raise AttributeError

    def __eq__(self, other):
        if isinstance(other, Draft_Bend):
            return self.position == other.position and self.bendiness == other.bendiness and \
                  self.bend_dir == other.bend_dir
        else:
            raise AttributeError


class ShortRows:
    """
    A Simple class structure for representing short rows
    """

    def __init__(self, x: int, y: int, col: int, row: int, height: float, width: int):
        """
        :param x: upper left point of short rows
        :param y: upper left point of short rows
        :param col: column of the tube where the short row begins
        :param row: row of the tube where the short row begins
        :param height: height of the PAIR
        :param width: width of base of shape
        """
        height = round(height)
        assert height % 10 == 0
        self.x: int = x
        self.y: int = y-height//2
        self.dot_y = y
        self.col = col
        self.row = row
        self.height: float = height
        self.width: int = width
        assert self.x is not None
        assert self.y is not None
        assert self.dot_y is not None
        assert self.col is not None
        assert self.row is not None
        assert self.height is not None
        assert self.width is not None
        assert height >= 0
        shift_down(y, self.height)
        self.draw()

    def __str__(self):
        return f"bend ({self.col}, {self.row}) {self.height} + {self.width}"

    def __repr__(self):
        return str(self)

    def draw(self):
        # draw two pairs of arcs, one where the mouse was clicked and one to represent the wraparound
        tag = str(self.col)+","+str(self.row)
        shrinks = self.x, self.y, self.x+self.width, self.height+self.y
        grows = self.x, self.height+self.y, self.x+self.width, self.height*2+self.y
        # These two attributes are defined after the shape is drawn so they can be found later by the canvas
        self.top = C.create_arc(shrinks, start=180, extent=180, outline="orange", width=2, tags=tag)
        self.bot = C.create_arc(grows, start=0, extent=180, outline="orange", width=2, tags=tag)
        # draw 2nd pair for overflow
        opposite = w.get()*10
        shrinks2 = self.x-opposite, self.y, self.x + self.width - opposite, self.height + self.y
        grows2 = self.x - opposite, self.height + self.y, self.x + self.width - opposite, self.height * 2 + self.y
        # This pair of shapes should eb the same shape and size as the two above, but they are horizontally offset
        # to represent the fact that the rectangle wraps around to make a tube, and that its left and right edges are
        # connected. These two attributes are defined after the shape is drawn so they can be found later by the canvas
        self.top2 = C.create_arc(shrinks2, start=180, extent=180, outline="orange", width=2, tags=tag)
        self.bot2 = C.create_arc(grows2, start=0, extent=180, outline="orange", width=2, tags=tag)

    def on_adjust_width(self):
        """
        Method for making adjustments to the renders of the short rows on the canvas so they are still proportional
        after the width has been modified
        """
        # self.y and self.dot_y might have been changed by the canvas during shifting
        x0, y0, x1, y1 = C.coords(self.top)
        self.y = y0
        self.dot_y = self.y + self.height//2

        # adjust size of arcs
        old_w = self.width
        new_w = w.get()//2*10
        multiplier = new_w/old_w
        old_h = self.height
        new_h = (old_h * multiplier)
        self.width = new_w
        self.height = round(new_h/10)*10
        assert self.height % 10 == 0
        dot_y = self.y + old_h//2
        self.y = dot_y - self.height//2
        # shift
        shift_down(dot_y, self.height-old_h)

        C.coords(self.top, self.x, self.y, self.x+self.width, self.height+self.y)
        C.coords(self.bot, self.x, self.height+self.y, self.x+self.width, self.height*2+self.y)

        opposite = w.get()*10
        C.coords(self.top2, self.x - opposite, self.y, self.x + self.width - opposite, self.height + self.y)
        C.coords(self.bot2, self.x - opposite, self.height + self.y, self.x + self.width - opposite, self.height * 2 +
                 self.y)

    def on_adjust_bend(self, b: float):
        """
        Method for making adjustments to the renders of the short rows on the canvas so they are still proportional
        after the bendiness has been modified
        """
        # self.y and self.dot_y might have been changed by the canvas during shifting
        x0, y0, x1, y1 = C.coords(self.top)
        self.y = y0
        self.dot_y = self.y + self.height//2

        # adjust height of arcs
        old_h = self.height
        new_h = b * self.width  # since height = width at bendiness of 1.0
        self.height = round(new_h/10)*10
        dot_y = self.y + old_h//2
        self.y = dot_y - self.height//2
        # shift
        shift_down(dot_y, self.height-old_h)

        C.coords(self.top, self.x, self.y, self.x+self.width, self.height+self.y)
        C.coords(self.bot, self.x, self.height+self.y, self.x+self.width, self.height*2+self.y)
        opposite = w.get()*10
        C.coords(self.top2, self.x - opposite, self.y, self.x+self.width - opposite, self.height+self.y)
        C.coords(self.bot2, self.x - opposite, self.height+self.y, self.x+self.width - opposite, self.height*2+self.y)


def shift_down(y, shift):
    """
    Method for shifting everything downwards if a short row needs to increase in height
    :param y: the y value the shift needs to start from
    :param shift: the number of pixels everything below y needs to be shifted by. y > 0 means a shift down, while
    y < 0 means a shift up
    """
    assert shift % 10 == 0
    assert y % 10 == 0
    if shift > 0:
        to_shift = C.find_enclosed(0, y-1, C_WIDTH, y + C_HEIGHT)
    elif shift < 0:
        to_shift = C.find_enclosed(0, y+1, C_WIDTH, y + C_HEIGHT)
    else:
        return
    for shape in to_shift:
        x0, y0, x1, y1 = C.coords(shape)
        C.coords(shape, x0, y0 + shift, x1, y1 + shift)


def open_menu(col: int, row: int, x: int, y: int, is_new: bool, ring):
    """
    Method for displaying the pop up menu that appears when a bend is made or edited
    The params col, row, x, and y all depend on where the mouse was when it was clicked
    :param col: the column corresponding to the bend
    :param row: the row corresponding to the bend
    :param x: the x value corresponding to the bend
    :param y: the y value corresponding to the bend
    :param is_new: True if a new bend is being created (mouse clicked on an empty square),
    False if an existing bend is being edited (mouse clicked on an existing bend)
    :param ring: the id of the ring shape that was created so it can be erased when the window is closed
    """
    menu = Toplevel(window)
    menu.grab_set()  # stop any interaction until the menu box is closed
    menu.title("Edit bend")
    menu.geometry("200x200")
    Label(menu, text="Edit bend at column "+str(col)+" and row "+str(row)).pack()
    # set default to be current val
    if is_new is True:
        default = 1.0
    else:
        default = bends[(col, row)].bendiness

    def close():
        C.delete(ring)
        menu.destroy()

    def set_bendiness(e):
        # adjust arcs
        srs[row].on_adjust_bend(bendiness.get())

    bendiness = DoubleVar()
    sc = Scale(menu, variable=bendiness, from_=0, to=1, resolution=0.01, length=150, orient=HORIZONTAL,
               label="Bendiness", command=set_bendiness)
    bendiness.set(default)
    sc.pack(side=TOP)

    def place():
        bends[(col, row)] = Draft_Bend(row, bendiness.get(), col)  # add new bend to bends array
        close()

    if is_new is True:
        place_button = Button(menu, text="Place", command=place, bg="green")
    else:
        place_button = Button(menu, text="Save", command=place, bg="green")
    place_button.pack(pady=5)

    def cancel():
        if is_new is True:  # If we are canceling in the middle of adding a new bend, we must erase the shape and shift
            # everything back up and delete it from the short rows array
            assert round(srs[row].height) % 10 == 0
            shift_down(y, -round(srs[row].height))
            C.delete(str(col)+","+str(row))
            del(srs[row])
        else:  # If we are canceling in the middle of editing a bend we must adjust the bendiness back to what it was
            # before
            srs[row].on_adjust_bend(default)
        close()

    cancel_button = Button(menu, text="Cancel", command=cancel)
    cancel_button.pack(pady=5)

    def remove():
        if is_new is False:
            assert round(srs[row].height) % 10 == 0
            shift_down(y, -round(srs[row].height))  # Must shift everything back up when removing a bend
            C.delete(str(col)+","+str(row))
            del(srs[row])
            del bends[(col, row)]  # remove bend from array
            close()

    if is_new is True:
        remove_button = Button(menu, text="Remove Bend", command=remove, state=DISABLED)
    else:
        remove_button = Button(menu, text="Remove Bend", command=remove, bg="red")
    remove_button.pack(pady=5)

    menu.protocol('WM_DELETE_WINDOW', cancel)


def clicked_on_existing(row: int):
    """
    Check if the mouse clicked on a row with a bend already in it. We need to check this because we don't allow creating
    a bend in a row where there already is one
    """
    for b in bends.values():
        if b.position == row:
            return b
    return None


def place_bend(e):
    """
    Triggers drawing a bend and short row pair onto the canvas at the intersection nearest to where the mouse was
    clicked
    """
    r = 5
    # x, y = e.x, e.y
    x = round(e.x / 10) * 10
    y = round(e.y / 10) * 10
    if y <= 10+5:
        return
    # figure out which row we should add a bend to based on closest rectangle. If none, do nothing.
    row = None
    for i in rects:
        rect = rects[i]
        x0, y0, x1, y1 = C.coords(rect)
        if y == y1 and i < len(rects)-1:
            row = i+1
    if row is not None:
        existing = clicked_on_existing(row)
        col = round(x / 10) - 1
        x0, y0, x1, y1 = C.coords(rects[h.get()-1])
        if existing is not None:
            if existing.bend_dir == col:
                # bring up height and delete menu
                ring = C.create_oval(x - r, y - r, x + r, y + r, outline="pink", width="3")
                open_menu(col, row, x, y, False, ring)
        elif y1 >= y >= 10 and (w.get() * 10 + 10) >= x >= 10:  # clicked in a valid place
            circ = C.create_oval(x - r, y - r, x + r, y + r, fill="green", tags=(str(col)+","+str(row)))
            ring = C.create_oval(x - r, y - r, x + r, y + r, outline="pink", width="3")
            srs[row] = ShortRows(x, y, col, row, 10 * w.get() // 2, 10 * w.get() // 2)
            open_menu(col, row, x, y, True, ring)


def set_width(e):
    """
    Adjusts the tube to match the width selected by the width slider
    """
    width = w.get()
    for rect in rects.values():
        x0, y0, x1, y1 = C.coords(rect)
        x1 = 10 + 10 * float(e)
        C.coords(rect, x0, y0, x1, y1)
    C.tag_raise("gridline")

    for sr in srs:
        srs[sr].on_adjust_width()


def set_height(e):
    """
    Adjusts the tube to match the height selected by the height slider
    """
    height = h.get()
    max_key = len(rects)-1
    x0, y0, x1, y1 = C.coords(rects[max_key])
    max_height = int(e)
    if float(e) > max_key+1:  # expand
        for i in range(0, max_height-max_key-1):
            row = max_key+i+1
            tag = "r"+str(row)
            new_rect = C.create_rectangle(x0, y1+10*i, x1, y1+10+10*i, fill="yellow", tags=tag)
            rects[row] = new_rect
    elif float(e) < max_key+1:  # shrink
        for i in range(max_height, max_key+1):
            C.delete(rects[i])
            del(rects[i])
    C.tag_raise("gridline")


def adjust_params():
    """
    Converts Draft_Bends to Bends and checks for bends outside the height and width of the tube
    """
    # switch from draft_bends to bends here by calculating bendiness
    oob = []
    if len(bends.values()) > 0:
        processed_bends = []
        for b in bends.values():
            if b.bend_dir > w.get() or b.position > h.get():
                oob.append(b)
            else:
                shift = b.bend_dir
                if b.bend_dir == w.get():
                    shift = 0
                ht = round(b.bendiness*float(w.get()/4))
                processed_bends.append(Bend(b.position, ht, shift))
        print(processed_bends)
        if len(oob) > 0:  # warn if there are bends outside of width
            coords = ""
            for b in oob:
                d = str(b.bend_dir)
                p = str(b.position)
                coords += "("+d+", "+p+"), "

            action = messagebox.askokcancel("Warning", "Bends at the following coordinates" + coords +
                                            "are outside of the tube and will be ignored")
            if action is True:
                if len(processed_bends) > 0:
                    processed_bends.sort()
                    end_len = h.get() - processed_bends[len(processed_bends) - 1].position
                    export_knitout(w.get() // 2, end_len, processed_bends, E1.get())
                else:
                    export_tube()
        else:
            if len(processed_bends) > 0:
                processed_bends.sort()
                end_len = h.get()-processed_bends[len(processed_bends)-1].position
                export_knitout(w.get() // 2, end_len, processed_bends, E1.get())
            else:
                export_tube()
    else:
        export_tube()


def export_tube():
    test_multi_bend(w.get()//2, h.get(), [], E1.get(), 3)  # no bends


def export_knitout(w: int, end_len: int, b: List[Bend], fn):
    test_multi_bend(w, end_len, b, fn, 3)  # has bends


if __name__ == "__main__":
    bends = dict()  # map from coordinates to Draft_Bends
    filename = "snek"  # default file name

    window = tk.Tk()
    top = tk.Frame(master=window)
    top.pack()

    instructions = StringVar()
    label = Label(top, textvariable=instructions, justify=LEFT)
    instructions.set("Welcome to Snake Designer!\nPick your height and width.\nClick on the tube to place bends. "
                     "There can be at most one bend per row.\nClick on an existing bend to edit it.\nPretend that the "
                     "left and right edges of the rectangle are connected to form a tube.\nClick KNIT to generate the "
                     "Knitout file for your snake!\n")
    label.pack()

    tube = tk.Frame(master=window)
    tube.pack()

    # Width slider
    w = IntVar()
    sc = Scale(tube, variable=w, from_=8, to=C_COLS, length=C_COLS*10, resolution=2, orient=HORIZONTAL,
               label="circumference", command=set_width)
    sc.pack(side=TOP)

    # Height slider
    h = IntVar()
    sc = Scale(tube, variable=h, from_=2, to=C_ROWS, length=C_ROWS*10, resolution=1, orient=VERTICAL,
               label="num of rows", command=set_height)
    sc.pack(side=LEFT)

    # Create canvas and smallest possible tube--width of 8 and height of 2
    C = tk.Canvas(tube, bg="blue", height=C_HEIGHT, width=C_WIDTH)
    rects = {}
    srs = {}
    coord = 10, 50, 240, 210
    rect0 = C.create_rectangle(10, 10, 90, 20, fill="yellow", tags="r0")
    rect1 = C.create_rectangle(10, 20, 90, 30, fill="yellow", tags="r1")
    rects[0] = rect0
    rects[1] = rect1
    for n in range(0, C_COLS+1):
        C.create_line(10+n*10, 10, 10+n*10, 10*(C_COLS+1), fill="gray", tags="gridline")
    for m in range(0, C_ROWS+1):
        C.create_line(10, 10+m*10, 10*(C_ROWS+1), 10+m*10, fill="gray", tags="gridline")

    C.pack()

    C.bind('<Button-1>', place_bend)

    btm = tk.Frame(master=window)
    btm.pack()

    # Name the file
    L1 = Label(btm, text="File Name")
    L1.pack(side=LEFT)
    E1 = Entry(btm, bd=5, textvariable=filename)
    E1.pack(side=LEFT)

    # Generate KnitOut
    btn = Button(btm, text="KNIT", command=adjust_params)
    btn.pack(side=RIGHT)

    window.mainloop()
