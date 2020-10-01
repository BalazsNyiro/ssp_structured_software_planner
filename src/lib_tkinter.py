import tkinter

PrgLib = None
def cmd_empty():
    pass

def key(event):
    print("pressed", repr(event.char))

def coord_virtual_x(EventX):
    Gui = PrgLib["Gui"]
    return Gui["ZoomX"]*(Gui["CanvasWidth"] * Gui["ScrollHorizontalFirst"] + EventX)

def coord_virtual_y(EventY):
    Gui = PrgLib["Gui"]
    return Gui["ZoomY"]*(Gui["CanvasHeight"] * Gui["ScrollVerticalFirst"] + EventY)

def mouse_button_press(event):
    CoordXvirtual = coord_virtual_x(event.x)
    CoordYvirtual = coord_virtual_y(event.y)
    print("clicked at", event.x, event.y, CoordXvirtual, CoordYvirtual)

def mouse_button_release(event):
    CoordXvirtual = coord_virtual_x(event.x)
    CoordYvirtual = coord_virtual_y(event.y)
    print("release at", event.x, event.y, CoordXvirtual, CoordYvirtual)

def mouse_button_pressed_and_moved(event):
    print("pressed and moving at", event.x, event.y)

def scrollbar_horizontal_set_and_save(First, Last):
    PrgLib["Gui"]["ScrollHorizontalFirst"] = float(First) # str is the original type? why?
    PrgLib["Gui"]["ScrollHorizontalLast"] = float(Last)
    PrgLib["Gui"]["ScrollHorizontal"].set(First, Last)

def scrollbar_vertical_set_and_save(First, Last):
    PrgLib["Gui"]["ScrollVerticalFirst"] = float(First)
    PrgLib["Gui"]["ScrollVerticalLast"] = float(Last)
    PrgLib["Gui"]["ScrollVertical"].set(First, Last)


def canvas_new(Parent, CanvasWidth, CanvasHeight):
    CanvasWidget = tkinter.Canvas(Parent, width=CanvasWidth, height=CanvasHeight)
    CanvasWidget.focus_set() # set keyboard focus
    CanvasWidget.bind("<ButtonPress-1>", mouse_button_press)
    CanvasWidget.bind("<ButtonRelease-1>", mouse_button_release)
    CanvasWidget.bind("<B1-Motion>", mouse_button_pressed_and_moved)
    CanvasWidget.bind("<Key>", key)
    return CanvasWidget

def root_new(Prg, Title,Width=600, Height=400, CanvasWidth=800, CanvasHeight=600):
    global PrgLib
    PrgLib = Prg

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
    CanvasWidget.configure(yscrollcommand=scrollbar_vertical_set_and_save)
    CanvasWidget.configure(xscrollcommand=scrollbar_horizontal_set_and_save)

    Prg["Gui"]["ScrollVertical"] = ScrollVertical
    Prg["Gui"]["ScrollHorizontal"] = ScrollHorizontal
    Prg["Gui"]["Root"] = Root
    Prg["Gui"]["CanvasWidget"] = CanvasWidget
    Prg["Gui"]["CanvasWidth"] = CanvasWidth
    Prg["Gui"]["CanvasHeight"] = CanvasHeight
    Prg["Gui"]["ZoomX"] = 1.0
    Prg["Gui"]["ZoomY"] = 1.0

    return Root, CanvasWidget

def namespace_draw(CanvasWidget, NameSpace,  NameSpaceCounter):
    ShiftX = NameSpaceCounter * 160
    ShiftY = NameSpaceCounter * 160
    Width = 160
    Height = 40 # title
    #FontTitle = "Times 10 italic bold"
    FontTitle = "Times 10 bold"
    FontSrcLine = "Courier 10 "

    X = ShiftX + 0
    Y = ShiftY + 0
    BoxPadding = 5

    Box = CanvasWidget.create_rectangle(X, Y, X+Width, Y+Height, fill="khaki1")

    LineHeight = 20
    Ytext = Y + LineHeight
    TxtTitle = CanvasWidget.create_text(X+Width/2, Ytext,fill="darkblue",font=FontTitle,
                                        text=NameSpace.Name)


    SrcTextElems = []
    for Line in NameSpace.SourceCodeLines:
        Height += 30
        Ytext = Ytext + LineHeight
        TxtSrc = CanvasWidget.create_text(X+BoxPadding, Ytext,fill="black",font=FontSrcLine,
                                        text=Line, anchor=tkinter.NW)
        SrcTextElems.append(TxtSrc)

    CanvasWidget.coords(Box, X, Y, X+Width, Ytext+30)

    NameSpace.GuiElems.extend([Box, TxtTitle])
    NameSpace.GuiElems.extend(SrcTextElems)
