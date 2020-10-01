# -*- coding: utf-8 -*-


class NameSpace:
    def __init__(self, Name, Parent=None, Type=None):
        self.Name = Name
        self.Parent = Parent
        self.ExecsAll = []
        self.ExecsCallsOnly = []
        self.Type = Type

        self.ReturnValue = None
        self.Args = dict()

    def exec(self, ProcReply):
        self.ExecsAll.append(ProcReply)

    def execCall(self, FunChild):
        self.ExecsCallsOnly.append(FunChild)


    def exec_level(self):
        Level = 1
        if self.Parent:
            Level += self.Parent.exec_level()
        return Level

    def exec_tree(self):
        Prefix = " " * self.exec_level()
        print(f"{Prefix}== {self.Name} ==")
        for ExecCall in self.ExecsCallsOnly:
            ExecCall.exec_tree()
