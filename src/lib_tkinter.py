import tkinter

PrgLib = None
def cmd_empty():
    pass

def key(event):
    global PrgLib
    print("pressed", event.char)
    Player = PrgLib["Player"]

    if event.char == "j":
        if Player["ProcStepId"]+1 < len(Player["ProcSteps"]):
            Player["ProcStepId"] += 1
            print("Player id", Player["ProcStepId"])

    if event.char == "k":
        if Player["ProcStepId"]-1 > 0:
            Player["ProcStepId"] -= 1
            print("Player id", Player["ProcStepId"])

    if event.char in "jk":
        ProcStep = Player["ProcSteps"][Player["ProcStepId"]]

        # how can I set bold text directly?
        TextObjInGui = Player["ProcStepsInGui"][ProcStep.gui_id()]
        Bounds = Player["CanvasWidget"].bbox(TextObjInGui)
        Xl, Yl, Xr, Yr = Bounds

        PointerXl = Xl-20
        PointerYl = Yl
        PointerXr = PointerXl + 10
        PointerYr = PointerYl + 10
        if not Player["ProcStepPointer"]:
            Player["ProcStepPointer"] = Player["CanvasWidget"].create_rectangle(PointerXl, PointerYl, PointerXr, PointerYr, fill="green")
        # set position
        Player["CanvasWidget"].coords(Player["ProcStepPointer"], PointerXl, PointerYl, PointerXr, PointerYr)


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

def root_new(Prg, Title,Width=1200, Height=800, CanvasWidth=800, CanvasHeight=600):
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

    # user input detection binds are in canvas_new()
    CanvasWidget = canvas_new(Root, CanvasWidth, CanvasHeight)
    CanvasWidget.grid(row=0, column=0, sticky="news")
    PrgLib["Player"]["CanvasWidget"] = CanvasWidget

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

    #FontTitle = "Times 10 italic bold"
    FontTitle = "Times 10 bold"
    FontSrcLine = "Courier 10 "

    X = ShiftX + 0
    Y = ShiftY + 0
    BoxPadding = 10
    LineSpace = 3
    Ytext = Y + BoxPadding

    # box with default with/height, later we resize it
    Box = CanvasWidget.create_rectangle(X, Y, X+40, Y+40, fill="khaki1")
    TxtTitle = CanvasWidget.create_text(X+BoxPadding, Ytext,
                                        fill="darkblue",font=FontTitle,
                                        text=NameSpace.Name, anchor = tkinter.NW)
    Bounds = CanvasWidget.bbox(TxtTitle)  # returns a tuple like (x1, y1, x2, y2)
    TitleHeight = Bounds[3] - Bounds[1]
    Ytext += TitleHeight + LineSpace

    TxtSrcWidthMax = 0
    SrcTextElems = []
    for ProcStep in NameSpace.ExecsAllProcReply:
        # print(ProcStep.Txt)
        TxtSrcGui = CanvasWidget.create_text(X + BoxPadding, Ytext, fill="black", font=FontSrcLine,
                                          text=ProcStep.SourceCodeLineInFile, anchor=tkinter.NW)
        SrcTextElems.append(TxtSrcGui)
        PrgLib["Player"]["ProcStepsInGui"][ProcStep.gui_id()] = TxtSrcGui

        Bounds = CanvasWidget.bbox(TxtSrcGui)  # returns a tuple like (x1, y1, x2, y2)
        # xl, yl, xr, yr = Bounds
        TxtSrcWidth = Bounds[2] - Bounds[0]
        TxtSrcHeight = Bounds[3] - Bounds[1]

        Ytext += TxtSrcHeight + LineSpace
        if TxtSrcWidth > TxtSrcWidthMax: TxtSrcWidthMax= TxtSrcWidth

    CanvasWidget.coords(Box, X, Y, X+BoxPadding+TxtSrcWidthMax+BoxPadding, Ytext+BoxPadding)

    NameSpace.GuiElems.extend([Box, TxtTitle])
    NameSpace.GuiElems.extend(SrcTextElems)
