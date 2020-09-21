#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
PrgGlobal = {"DirPrgParent":  DirPrgParent}

import lib_tkinter
# Root, CanvasWidget = lib_tkinter.win_root()
# Root.mainloop()


import tkinter
from tkinter import ttk
CanvasWidget = None

# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
def win_main(Prg, CanvasWidth=600, CanvasHeight=400):

    Root = lib_tkinter.root_new("SSP program planner")
    global CanvasWidget
    CanvasWidget = lib_tkinter.canvas_new(Root, CanvasWidth, CanvasHeight)
    CanvasWidget.grid(row=0, column=0, sticky="news")

    ObjSelected = CanvasWidget.create_rectangle(0, 0, 50, 50, fill="blue")
    ObjSelected = CanvasWidget.create_rectangle(CanvasWidth-50, CanvasHeight-50, CanvasWidth, CanvasHeight, fill="blue")

    # cell resizabe, flexible:

    ScrollVertical = tkinter.Scrollbar(Root, command=CanvasWidget.yview, orient="vertical")
    ScrollHorizontal = tkinter.Scrollbar(Root, command=CanvasWidget.xview, orient="horizontal")
    CanvasWidget.configure(yscrollcommand=ScrollVertical.set)
    CanvasWidget.configure(xscrollcommand=ScrollHorizontal.set)
    CanvasWidget.configure(scrollregion=CanvasWidget.bbox("all"))
    ScrollVertical.grid(row=0, column=1, sticky=tkinter.NS)
    ScrollHorizontal.grid(row=1, column=0, sticky=tkinter.EW)
    Root.mainloop()

win_main(PrgGlobal)