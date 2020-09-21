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

def key(event):
    print("pressed", repr(event.char))

def mouse_button_press(event):
    print("clicked at", event.x, event.y)
def mouse_button_release(event):
    print("release at", event.x, event.y)
def mouse_button_pressed_and_moved(event):
    print("pressed and moving at", event.x, event.y)

def cmd_empty():
    pass
def win_main(Prg, CanvasWidth=600, CanvasHeight=400):

    Root = tkinter.Tk()
    Root.title("title")

    MenuBar = tkinter.Menu(Root)

    MenuAbout = tkinter.Menu(MenuBar, tearoff=1)
    MenuBar.add_cascade(label='About', menu=MenuAbout)
    MenuAbout.add_command(label="Site", compound='left', command=cmd_empty)
    MenuAbout.add_command(label="Facebook group", compound='left', command=cmd_empty)
    MenuAbout.add_command(label="Contact", compound='left', command=cmd_empty)

    Root.config(menu=MenuBar)

    # placeholder, small distance from left frame
    tkinter.Label(Root, text=" ").grid(row=0, column=0, sticky=tkinter.W)

    Container = ttk.Frame(Root)
    ################################################
    global CanvasWidget
    CanvasWidget = tkinter.Canvas(Container, width=CanvasWidth, height=CanvasHeight)
    CanvasWidget.bind("<Key>", key)
    CanvasWidget.bind("<ButtonPress-1>", mouse_button_press)
    CanvasWidget.bind("<ButtonRelease-1>", mouse_button_release)
    CanvasWidget.bind("<B1-Motion>", mouse_button_pressed_and_moved)

    ScrollableFrame = ttk.Frame(CanvasWidget)
    ScrollableFrame.bind(
        "<Configure>",
        lambda e: CanvasWidget.configure(
            scrollregion=CanvasWidget.bbox("all")
        )
    )
    CanvasWidget.create_window((0, 0), window=ScrollableFrame, anchor="nw")

    ObjSelected = CanvasWidget.create_rectangle(0, 0, 50, 50, fill="blue")
    ObjSelected = CanvasWidget.create_rectangle(CanvasWidth-50, CanvasHeight-50, CanvasWidth, CanvasHeight, fill="blue")

    CanvasWidget.grid() # tkinter.E
    Container.grid(row=3, column=1, sticky="nsew") # tkinter.E

    # cell resizabe, flexible:
    Root.grid_columnconfigure(1, weight=1)
    Root.grid_rowconfigure(3, weight=1)

    ScrollVertical = tkinter.Scrollbar(Root, command=CanvasWidget.yview, orient="vertical")
    ScrollHorizontal = tkinter.Scrollbar(Root, command=CanvasWidget.xview, orient="horizontal")
    CanvasWidget.configure(yscrollcommand=ScrollVertical.set)
    CanvasWidget.configure(xscrollcommand=ScrollHorizontal.set)
    ScrollVertical.grid(row=3, column=2, sticky=tkinter.NS)
    ScrollHorizontal.grid(row=4, column=1, sticky=tkinter.EW)
    Root.mainloop()

win_main(PrgGlobal)