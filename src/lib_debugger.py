import bdb

class NameSpaceObj():
    def __init__(self, Name="", FileName=None, LineNum=None,
                 Fun=False,
                 Parent=None,
                 Level = 0
                 ):
        self.Children = []
        self.Parent = Parent
        self.Fun = Fun
        self.LineNum = LineNum
        self.FileName = FileName
        self.Name = Name
        self.RetVal = None
        self.Level = Level

    def __str__(self):
        Prefix = " " * self.Level
        Out = []
        Out.append(f"{Prefix} -> {self.Name}")
        for Child in self.Children:
            Out.append(Child.__str__())
        Out.append(f"{Prefix} <- {self.Name}: {self.RetVal}")
        return "\n".join(Out)

class Debugger(bdb.Bdb):
    Root = NameSpaceObj(Name="Root")
    NameSpaceActual = Root

    def user_call(self, frame, args):
        Name = frame.f_code.co_name or "<unknown>"
        FileName = self.canonic(frame.f_code.co_filename)
        LineNum = frame.f_lineno
        print("+++ call", Name, args, LineNum, FileName)
        Parent = Debugger.NameSpaceActual
        NameSpace = NameSpaceObj(Name=Name, FileName=FileName,
                                 LineNum=LineNum, Fun=True,
                                 Parent = Parent,
                                 Level = Parent.Level+1)
        Debugger.NameSpaceActual.Children.append(NameSpace)
        Debugger.NameSpaceActual = NameSpace


    def user_line(self, frame):
        import linecache
        name = frame.f_code.co_name
        if not name: name = '???'
        fn = self.canonic(frame.f_code.co_filename)
        line = linecache.getline(fn, frame.f_lineno, frame.f_globals)
        print('+++', fn, frame.f_lineno, name, ':', line.strip())
    def user_return(self, Frame, RetVal):
        Name = Frame.f_code.co_name or "<unknown>"
        print('+++ return', Name, RetVal)
        Debugger.NameSpaceActual.RetVal = RetVal
        Debugger.NameSpaceActual = Debugger.NameSpaceActual.Parent

    def user_exception(self, frame, exc_stuff):
        print('+++ exception', exc_stuff)
        self.set_continue()