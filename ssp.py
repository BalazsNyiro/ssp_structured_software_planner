#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pickle
DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
sys.path.append(os.path.join(DirPrgParent, "try"))

import lib_tkinter_ssp, lib_debugger, util_ssp, lib_namespace

########################################
PrgSaved = {
    "ExecutionAll": [],
}

Prg = {
    "HideChildrenInTheseCalls": set(),
    "HiddenCallsPrgSpecific": set(),

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
PickleLoaded = False
if os.path.isfile(FilePickle):
    with open(FilePickle, 'rb') as f:
        PrgSaved = pickle.load(f)
        PickleLoaded = True

######################################################
if False:
    # because of set_break we can see all line execution
    # import has to be IN RUN cmd
    import riverbank

    if not PickleLoaded:
        Prg["debugger"].run("riverbank.main()")
        for ExecutionLine in Prg["debugger"].ExecutionAll:
            PrgSaved["ExecutionAll"].append(ExecutionLine)
        #Prg["debugger"].run("test('.')")
else:
    ######################################################
    sys.path.append(os.path.join(DirPrgParent, "try/sentence-seeker"))
    sys.path.append(os.path.join(DirPrgParent, "try/sentence-seeker/src"))
    import prg_start

    Prg["HideChildrenInTheseCalls"] = {
    }
    Prg["HiddenCallsPrgSpecific"] = {
        "acc_info",
        "basename_without_extension",
        "basename_without_extension__ext",
        "basename_without_extension__ext",
        "dir_create_if_necessary",
        "dir_user_home",
        "dirname",
        "document_obj_create",
        "expanduser",
        "file_convert_to_txt_if_necessary",
        "file_create_if_necessary",
        "file_read_all",
        "file_write_utf8_error_avoid",
        "file_read_lines",
        "filename_extension",
        "files_abspath_collect_from_dir",
        "files_abspath_collect_from_dir",
        "info",
        "isfile",
        "PrgConfigCreate",
        "console_available",
        "web_get",
        "int_list_to_array",
        "loads",
        "log",
        "obj_from_file",
        "print_dev",
        "progressbar_close",
        "progressbar_refresh_if_displayed",
        "realpath",
        "resultSelectors",
        "sentence_result_all_display",
        "shell",
        "text_from_pdf",
        "token_explain_summa",
        "token_explain_summa_to_text",
        "token_group_finder",
        "token_interpreter",
        "token_split",
        "utf8_conversion_with_warning",
        "words_count_in_all_document",
        "words_wanted_from_tokens",
        # "config_get",
        #"file_read_all",
    }

    if not PickleLoaded:
        Prg["debugger"].run("prg_start.run()") # prg_start is created because I can import it, sentence-seeker has a dash

        for ExecutionLine in Prg["debugger"].ExecutionAll:
            PrgSaved["ExecutionAll"].append(ExecutionLine)

with open(FilePickle, 'wb') as f:
    pickle.dump(PrgSaved, f, pickle.HIGHEST_PROTOCOL)

NameSpaceRoot = lib_namespace.name_space_calls_create(Prg, PrgSaved)
print(NameSpaceRoot)
util_ssp.file_write_simple("happened.txt", str(NameSpaceRoot))
for ExecLine in PrgSaved["ExecutionAll"]:
    #print(ExecLine.Event, ExecLine.Name)
    pass
util_ssp.file_write_simple("exec_all.txt", "\n".join([ ExecLine.to_file() for ExecLine in PrgSaved["ExecutionAll"] if ExecLine.to_file()!=""]))


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

########################## TEST #########################
import time
def something():
    return int(time.time()) - 1

def test(DirRoot, Recursive=False):
    FilesAbsPath = []
    for DirPath, DirNames, FileNames in os.walk(DirRoot):
        for Elem in ([os.path.join(DirPath, File) for File in FileNames]):
            FilesAbsPath.append(Elem)
        if not Recursive:
            break
    S = something()
    return FilesAbsPath, S
########################## TEST #########################
win_main(Prg)