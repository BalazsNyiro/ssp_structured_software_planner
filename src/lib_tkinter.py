import tkinter

def cmd_empty():
    pass
def key(event):
    print("pressed", repr(event.char))
def mouse_button_press(event):
    print("clicked at", event.x, event.y)
def mouse_button_release(event):
    print("release at", event.x, event.y)
def mouse_button_pressed_and_moved(event):
    print("pressed and moving at", event.x, event.y)

def canvas_new(Parent, CanvasWidth, CanvasHeight):
    CanvasWidget = tkinter.Canvas(Parent, width=CanvasWidth, height=CanvasHeight)
    CanvasWidget.bind("<Key>", key)
    CanvasWidget.bind("<ButtonPress-1>", mouse_button_press)
    CanvasWidget.bind("<ButtonRelease-1>", mouse_button_release)
    CanvasWidget.bind("<B1-Motion>", mouse_button_pressed_and_moved)
    return CanvasWidget

def root_new(Title,Width=600, Height=400, CanvasWidth=800, CanvasHeight=600):
    Root = tkinter.Tk()
    Root.title(Title)

    Root.grid_columnconfigure(0, weight=1)
    Root.grid_rowconfigure(0, weight=1)

    MenuBar = tkinter.Menu(Root)

    MenuAbout = tkinter.Menu(MenuBar, tearoff=1)
    MenuBar.add_cascade(label='About', menu=MenuAbout)
    MenuAbout.add_command(label="Site", compound='left', command=cmd_empty)
    MenuAbout.add_command(label="Facebook group", compound='left', command=cmd_empty)
    MenuAbout.add_command(label="Contact", compound='left', command=cmd_empty)

    Root.geometry(f"{Width}x{Height}")
    Root.config(menu=MenuBar)

    CanvasWidget = canvas_new(Root, CanvasWidth, CanvasHeight)
    CanvasWidget.grid(row=0, column=0, sticky="news")

    # cell resizabe, flexible:
    ScrollVertical = tkinter.Scrollbar(Root, command=CanvasWidget.yview, orient="vertical")
    ScrollHorizontal = tkinter.Scrollbar(Root, command=CanvasWidget.xview, orient="horizontal")
    ScrollVertical.grid(row=0, column=1, sticky=tkinter.NS)
    ScrollHorizontal.grid(row=1, column=0, sticky=tkinter.EW)
    CanvasWidget.configure(yscrollcommand=ScrollVertical.set)
    CanvasWidget.configure(xscrollcommand=ScrollHorizontal.set)

    return Root, CanvasWidget, ScrollVertical, ScrollHorizontal
