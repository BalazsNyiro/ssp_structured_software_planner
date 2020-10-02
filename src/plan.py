# -*- coding: utf-8 -*-


class NameSpace:
    NameMaxLen = 0

    def __init__(self, Name="unknown_namespace", Parent=None, Type=None):
        self.Name = Name
        if len(Name)> NameSpace.NameMaxLen:
            NameSpace.NameMaxLen = len(Name)

        self.Parent = Parent
        self.ExecsAllProcReply = []
        self.ExecsCallsOnlyNameSpaces = []
        self.Type = Type
        self.CallCounter = 0
        self.SourceCodeLines = []

        self.ReturnValue = None
        self.Args = dict()
        self.GuiElems = []

    def exec(self, ProcReply):
        self.ExecsAllProcReply.append(ProcReply)

    def execCall(self, NameSpaceFunChild):
        self.ExecsCallsOnlyNameSpaces.append(NameSpaceFunChild)

    def exec_level(self):
        Level = 1
        if self.Parent:
            Level += self.Parent.exec_level()
        return Level

    def exec_tree(self):
        Prefix = " " * self.exec_level()
        print()
        print(f"{Prefix}-> {self.Name}")
        print(f"{Prefix}   arg: {self.Args}")

        if self.ExecsCallsOnlyNameSpaces:
            print()
        for NameSpaceCall in self.ExecsCallsOnlyNameSpaces:
            NameSpaceCall.exec_tree()
        if self.ExecsCallsOnlyNameSpaces:
            print()

        print(f"{Prefix}   ret: {self.ReturnValue}")
        print(f"{Prefix}<- {self.Name}")

def namespace_elems_info_cli(NameSpaceElems):
    NameLen = NameSpace.NameMaxLen + 3
    print("namelen", NameLen)
    for NameSpaceElem in NameSpaceElems.values():
        # NameLen = 33
        print(f"namespace: {NameSpaceElem.Name:{NameLen}s} call: {NameSpaceElem.CallCounter}")
