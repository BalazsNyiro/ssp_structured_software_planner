#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
sys.path.append(os.path.join(DirPrgParent, "try"))

import lib_tkinter_ssp, lib_debugger, util_ssp

########################################
Prg = {"DirPrgParent":  DirPrgParent,
       "Gui": dict(),
       "debugger": lib_debugger.Debugger(),
       "hidden_calls_in_analyser": {
            "__enter__",
            "__exit__",
            "_get_sep",
            "__contains__",
            "_joinrealpath",
            "__getattr__",
            "__getitem__",
            "__init__",
            "join", "isfile","isdir", "shell","abspath", "walk",


            "acc_info",

           "expanduser",
           "file_read_all",
           "loads",
           "log",
           "utf8_conversion_with_warning",
       },
       "Player": {
           "ExecNext": -1,
           "ProcSteps": [],
           "ProcStepsInGui": {},  # stepid - gui obj dict
           "CanvasWidget": None,
           "ProcStepPointer": None,
           "GuiLinesObjects": {}
}
       }
######################################################
if False:
    import riverbank
    # because of set_break we can see all line execution
    Prg["debugger"].set_break("try/riverbank.py", 1)
    Prg["debugger"].run("riverbank.main()")
else:
    ######################################################
    sys.path.append(os.path.join(DirPrgParent, "try/sentence-seeker"))
    sys.path.append(os.path.join(DirPrgParent, "try/sentence-seeker/src"))
    import prg_start
    Prg["debugger"].set_break("try/sentence-seeker/prg_start.py", 1)
    Prg["debugger"].run("prg_start.run()") # prg_start is created because I can import it, sentence-seeker has a dash

######################################################

util_ssp.file_write_simple("callstack.txt", Prg["debugger"].Root.to_str(Prg))
#Prg["debugger"].Root.html_create(Prg)

for ExecNext in Prg["debugger"].ExecutionAll:
    print("\n\n", ExecNext)

util_ssp.file_write_simple("exec_all.txt", "\n".join([ ExecLine.to_file() for ExecLine in Prg["debugger"].ExecutionAll if ExecLine.to_file()!=""]))


# for Id, NameSpaceDef in Prg["debugger"].NameSpaceDefinitions.items():
#     print(NameSpaceDef)
sys.exit()

CanvasWidget = None

# https://stackoverflow.com/questions/43731784/tkinter-canvas-scrollbar-with-grid
def win_main(Prg, CanvasWidth=800, CanvasHeight=600):

    global CanvasWidget
    Root, CanvasWidget = lib_tkinter.root_new(Prg, "SSP program planner")

    ObjSelected = CanvasWidget.create_rectangle(0, 0, 50, 50, fill="blue")
    ObjSelected = CanvasWidget.create_rectangle(CanvasWidth-50, CanvasHeight-50, CanvasWidth, CanvasHeight, fill="blue")

    NameSpaceDefinitions = Prg["debugger"].NameSpaceDefinitions

    NameSpaceCounter = 0
    for NameSpaceId in NameSpaceDefinitions:
        NameSpaceDef = NameSpaceDefinitions[NameSpaceId]

        #if "NoDefName" not in NameSpaceDef.Name:
        if True:
            lib_tkinter.namespace_draw(Prg, CanvasWidget, NameSpaceDef, NameSpaceCounter)
            NameSpaceCounter += 1

    # it has to be AFTER DRAWING, on the contrary scrollbar won't detect ratio
    CanvasWidget.configure(scrollregion=CanvasWidget.bbox("all"))
    Root.mainloop()

win_main(Prg)