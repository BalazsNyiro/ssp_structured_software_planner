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
PathExample = os.path.join(DirPrgParent, "try", "riverbank.py")
Proc = debugger.prg_start(PathExample)

debugger.proc_output(Proc)
NameSpace = plan.NameSpace(Name="Main module", Type="module")
NameSpaceRoot = NameSpace

NameSpacesUsedInPrg = {}
while True:
    ProcReply = debugger.proc_step_next(Proc)
    if ProcReply.Call:
        Parent = NameSpace
        NameSpace = plan.NameSpace(ProcReply.DisplayedName, Type="Fun", Parent = Parent)
        NameSpace.Args = ProcReply.Args
        Parent.execCall(NameSpace)
        if NameSpace.Name not in NameSpacesUsedInPrg:
            NameSpacesUsedInPrg[NameSpace.Name] = NameSpace
        NameSpacesUsedInPrg[NameSpace.Name].CallCounter += 1
        NameSpacesUsedInPrg[NameSpace.Name].SourceCodeLinesOfCurrentNameSpace = ProcReply.SourceCodeLinesOfCurrentNameSpace

    # save every executed reply here
    NameSpace.exec(ProcReply)

    if ProcReply.Return and NameSpace.Parent:
        NameSpace.ReturnValue = ProcReply.ReturnValue
        NameSpace = NameSpace.Parent

    # print(">>  ", ProcReply.FunName)
    # print("  ->", ProcReply.Args)
    # print("  <-", ProcReply.ReturnValue)
    # print(" txt", ProcReply.Txt)
    # print("\n\n")
    if ProcReply.End:
        break

debugger.prg_end(Proc)

NameSpaceRoot.exec_tree()
plan.namespace_elems_info_cli(NameSpacesUsedInPrg)

# sys.exit(1)

CanvasWidget = None

# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
def win_main(Prg, CanvasWidth=800, CanvasHeight=600):

    global CanvasWidget
    Root, CanvasWidget = lib_tkinter.root_new(Prg, "SSP program planner")

    ObjSelected = CanvasWidget.create_rectangle(0, 0, 50, 50, fill="blue")
    ObjSelected = CanvasWidget.create_rectangle(CanvasWidth-50, CanvasHeight-50, CanvasWidth, CanvasHeight, fill="blue")

    for i, NameSpaceName in enumerate(NameSpacesUsedInPrg):
        NameSpace = NameSpacesUsedInPrg[NameSpaceName]
        lib_tkinter.namespace_draw(CanvasWidget, NameSpace, i)

    # it has to be AFTER DRAWING, on the contrary scrollbar won't detect ratio
    CanvasWidget.configure(scrollregion=CanvasWidget.bbox("all"))
    Root.mainloop()

win_main(Prg)