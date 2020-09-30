# -*- coding: utf-8 -*-


class NameSpace:
    def __init__(self, Name, Parent=None, Type=None):
        self.Name = Name
        self.Parent = Parent
        self.Execs = []
        self.Type = Type
