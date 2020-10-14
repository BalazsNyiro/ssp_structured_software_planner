#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
sys.path.append(os.path.join(DirPrgParent, "try"))

import lib_tkinter, lib_debugger

Prg = {"DirPrgParent":  DirPrgParent,
       "Gui": dict(),
       "debugger": lib_debugger.Debugger(),
       "Player": {
           "ProcStepId": -1,
           "ProcSteps": [],
           "ProcStepsInGui": {},  # stepid - gui obj dict
           "CanvasWidget": None,
           "ProcStepPointer": None
       }
       }

import riverbank
# because of set_break we can see all line execution
Prg["debugger"].set_break("try/riverbank.py", 1)
Prg["debugger"].run("riverbank.main()")
print(Prg["debugger"].Root)

CanvasWidget = None

# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
def win_main(Prg, CanvasWidth=800, CanvasHeight=600):

    global CanvasWidget
    Root, CanvasWidget = lib_tkinter.root_new(Prg, "SSP program planner")

    ObjSelected = CanvasWidget.create_rectangle(0, 0, 50, 50, fill="blue")
    ObjSelected = CanvasWidget.create_rectangle(CanvasWidth-50, CanvasHeight-50, CanvasWidth, CanvasHeight, fill="blue")

    NameSpaceNames = Prg["debugger"].NameSpaceGenerals
    for i, Key in enumerate(NameSpaceNames):
        NameSpace = NameSpaceNames[Key]
        lib_tkinter.namespace_draw(Prg, CanvasWidget, NameSpace, i)

    # it has to be AFTER DRAWING, on the contrary scrollbar won't detect ratio
    CanvasWidget.configure(scrollregion=CanvasWidget.bbox("all"))
    Root.mainloop()

win_main(Prg)