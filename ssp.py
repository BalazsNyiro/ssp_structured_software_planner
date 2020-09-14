#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
PrgGlobal = {"DirPrgParent":  DirPrgParent}

import lib_tkinter
# Root, CanvasWidget = lib_tkinter.win_root()
# Root.mainloop()


import tkinter as tk

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

    Root = tk.Tk()
    Root.title("title")

    MenuBar = tk.Menu(Root)

    MenuAbout = tk.Menu(MenuBar, tearoff=1)
    MenuBar.add_cascade(label='About', menu=MenuAbout)
    MenuAbout.add_command(label="Site", compound='left', command=cmd_empty)
    MenuAbout.add_command(label="Facebook group", compound='left', command=cmd_empty)
    MenuAbout.add_command(label="Contact", compound='left', command=cmd_empty)

    Root.config(menu=MenuBar)

    # placeholder, small distance from left frame
    tk.Label(Root, text=" ").grid(row=0, column=0, sticky=tk.W)

    ################################################
    global CanvasWidget
    CanvasWidget = tk.Canvas(Root, width=CanvasWidth, height=CanvasHeight)
    CanvasWidget.bind("<Key>", key)
    CanvasWidget.bind("<ButtonPress-1>", mouse_button_press)
    CanvasWidget.bind("<ButtonRelease-1>", mouse_button_release)
    CanvasWidget.bind("<B1-Motion>", mouse_button_pressed_and_moved)


    ObjSelected = CanvasWidget.create_rectangle(0, 0, 50, 50, fill="blue")
    ObjSelected = CanvasWidget.create_rectangle(CanvasWidth-50, CanvasHeight-50, CanvasWidth, CanvasHeight, fill="blue")

    CanvasWidget.grid(row=3, column=1, sticky="nsew", columnspan=3) # tk.E

    Root.grid_columnconfigure(1, weight=1)
    Root.grid_rowconfigure(3, weight=1)

    scroll = tk.Scrollbar(Root, command=CanvasWidget.yview)
    CanvasWidget.configure(yscrollcommand=scroll.set)
    scroll.grid(row=3, column=3, sticky=tk.NS)
    Root.mainloop()

win_main(PrgGlobal)