#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
Prg = {"DirPrgParent":  DirPrgParent, "Gui": dict()}

import lib_tkinter
# Root, CanvasWidget = lib_tkinter.win_root()
# Root.mainloop()

import debugger, plan
Proc = debugger.prg_start(os.path.join(DirPrgParent, "try", "calc.py"))

debugger.proc_output(Proc)
NameSpace = plan.NameSpace("RootNameSpace", Type="Root")
NameSpaceRoot = NameSpace
while True:
    ProcReply = debugger.proc_step_next(Proc)
    if ProcReply.Call:
        Parent = NameSpace
        NameSpace = plan.NameSpace(ProcReply.FileName + "/" + ProcReply.FunName, Type="Fun", Parent = Parent)
        NameSpace.Args = ProcReply.Args
        Parent.execCall(NameSpace)
    elif ProcReply.Return and NameSpace.Parent:
        NameSpace.ReturnValue = ProcReply.ReturnValue
        NameSpace = NameSpace.Parent
    else:
        NameSpace.exec(ProcReply)
    print(">>  ", ProcReply.FunName)
    print("  ->", ProcReply.Args)
    print("  <-", ProcReply.ReturnValue)
    # print(" txt", ProcReply.Txt)
    print("\n\n")
    if ProcReply.End:
        break

NameSpaceRoot.exec_tree()

debugger.prg_end(Proc)
sys.exit(1)

CanvasWidget = None

# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
def win_main(Prg, CanvasWidth=800, CanvasHeight=600):

    global CanvasWidget
    Root, CanvasWidget = lib_tkinter.root_new(Prg, "SSP program planner")

    ObjSelected = CanvasWidget.create_rectangle(0, 0, 50, 50, fill="blue")
    ObjSelected = CanvasWidget.create_rectangle(CanvasWidth-50, CanvasHeight-50, CanvasWidth, CanvasHeight, fill="blue")

    # it has to be AFTER DRAWING, on the contrary scrollbar won't detect ratio
    CanvasWidget.configure(scrollregion=CanvasWidget.bbox("all"))
    Root.mainloop()

win_main(Prg)