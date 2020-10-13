#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def config_PrgConfigCreate():
    return {
        "DocumentsDb": dict(),
        "DocumentObjectsLoaded": dict(),
        "LimitDisplayedSampleSentences": 20
    }

def document_obj_create():
    return {"FileOrigPathAbs": "FileOrigPathAbs",
            "FileTextPathAbs": "FileTextPathAbs",
            "FileIndex": "FileIndex",
            "FileSentences": "FileSentences",
            "WordPosition": "WordPosition",
            "Sentences": "Sentences"
            }

def document_document_objects_collect_from_working_dir(Prg):
    #Files = util.files_abspath_collect_from_dir(Prg["DirDocuments"])
    DocumentObjects = {}
    Files = ["file.txt"]
    print("file_convert_to_txt_if_necessary()")
    for File in Files:
        DocumentObjects["file_basename": document_obj_create()]

def be_ready_to_seeking(Prg):
    Prg["DocumentObjectsLoaded"] = \
        document_document_objects_collect_from_working_dir(Prg)

def main():
    Prg = config_PrgConfigCreate()
    be_ready_to_seeking(Prg)

    "<<PrgEnd>>"

breakpoint()
main()
