#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pickle
DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
sys.path.append(os.path.join(DirPrgParent, "try"))

import lib_tkinter_ssp, lib_debugger, util_ssp, lib_namespace

########################################
Prg = {"Saved": {
           "HideChildrenInTheseCalls": set(),
           "HiddenCallsPrgSpecific": set(),
           "ExecutionAll": [],
            },
       "DirPrgParent":  DirPrgParent,
       "Gui": dict(),
       "debugger": lib_debugger.Debugger(),
       "Player": {
           "ExecNext": -1,
           "ProcSteps": [],
           "ProcStepsInGui": {},  # stepid - gui obj dict
           "CanvasWidget": None,
           "ProcStepPointer": None,
           "GuiLinesObjects": {}
           }
        }

FilePickle = 'data.pickle'
if os.path.isfile(FilePickle):
    with open(FilePickle, 'rb') as f:
        Prg["Saved"] = pickle.load(f)
else:
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

        Prg["Saved"]["HideChildrenInTheseCalls"] = {"file_read_all"}
        Prg["Saved"]["HiddenCallsPrgSpecific"] = {
            "acc_info",
            "expanduser",
            #"file_read_all",
            "loads",
            "log",
            "utf8_conversion_with_warning",
        }
        Prg["debugger"].set_break("try/sentence-seeker/prg_start.py", 1)
        Prg["debugger"].run("prg_start.run()") # prg_start is created because I can import it, sentence-seeker has a dash

        Prg["Saved"]["ExecutionAll"] = Prg["debugger"].ExecutionAll
    ######################################################

    with open(FilePickle, 'wb') as f:
        pickle.dump(Prg["Saved"], f, pickle.HIGHEST_PROTOCOL)

NameSpaceRoot = lib_namespace.name_space_calls_create(Prg)
print(NameSpaceRoot)
util_ssp.file_write_simple("exec_all.txt", "\n".join([ ExecLine.to_file() for ExecLine in Prg["Saved"]["ExecutionAll"] if ExecLine.to_file()!=""]))


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