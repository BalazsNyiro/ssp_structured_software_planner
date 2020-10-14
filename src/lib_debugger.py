import bdb, util

class NameSpaceObj():
    def __init__(self, Name="", FileName=None, LineNumDef=None,
                 Fun=False,
                 Parent=None,
                 Level = 0,
                 LinesSourceFile = None
                 ):
        self.ChildrenNameSpaces = []
        self.LinesExecuted = []
        self.Parent = Parent
        self.Fun = Fun
        self.LineNumDef = LineNumDef
        self.LineNumRetLatest = LineNumDef  # the latest Return Linenum
        self.FileName = FileName
        self.Name = Name
        self.RetVal = None
        self.Level = Level
        self.GuiElems = []

        # in list of all Namespaces, File and Linenum
        # is he best uniq id
        self.Id = (FileName, LineNumDef)
        self.LinesSourceFile = LinesSourceFile
        self.GuiLinesObjects = {} # (File, ExecutedLine) -> object in Gui

    def def_line(self):
        return self.LinesSourceFile[self.LineNumDef]

    def __str__(self):
        Prefix = " " * self.Level
        Out = []
        Out.append(f"{Prefix} -> {self.Name}")
        for Child in self.ChildrenNameSpaces:
            Out.append(Child.__str__())
        Out.append(f"{Prefix} <- {self.Name}: {self.RetVal}")
        return "\n".join(Out)

class ExecLine():
    def __init__(self, FileName, LineNum, Line, Locals):
        self.FileName = FileName
        self.LineNum = LineNum
        self.Line = Line
        self.Locals = Locals

class Debugger(bdb.Bdb):
    Root = NameSpaceObj(Name="Root")
    NameSpaceNames = {}
    NameSpaceActual = Root
    SourceFiles = {}
    ExecutionAll = []

    def user_call(self, frame, args):
        Name = frame.f_code.co_name or "<unknown>"
        FileName = self.canonic(frame.f_code.co_filename)
        LineNumDef = frame.f_lineno
        if FileName not in Debugger.SourceFiles:
            Debugger.SourceFiles[FileName] = ["# hidden zero line, debugger is 1 based'"]
            Debugger.SourceFiles[FileName].extend(util.file_read_lines(FileName))

        print("+++ call", Name, args, LineNumDef, FileName)

        Parent = Debugger.NameSpaceActual
        NameSpace = NameSpaceObj(Name=Name, FileName=FileName,
                                 LineNumDef=LineNumDef, Fun=True,
                                 Parent = Parent,
                                 Level = Parent.Level+1,
                                 LinesSourceFile= Debugger.SourceFiles[FileName])
        Debugger.NameSpaceActual.ChildrenNameSpaces.append(NameSpace)
        Debugger.NameSpaceActual = NameSpace

        # Save all namespaces Once
        if NameSpace.Id not in Debugger.NameSpaceNames:
            Debugger.NameSpaceNames[NameSpace.Id] = NameSpace

    def user_line(self, frame):
        import linecache
        name = frame.f_code.co_name
        if not name: name = '???'
        Fn = self.canonic(frame.f_code.co_filename)

        LineNo = frame.f_lineno
        Line = linecache.getline(Fn, LineNo, frame.f_globals)
        print('+++ USERLINE',Debugger.NameSpaceActual.Name, Fn, LineNo, name, ':', Line.strip(), "frame locals: ", frame.f_locals)

        LineInserted = f"{LineNo} {Line}"
        if Fn in Debugger.SourceFiles:
            LineInserted = f"{LineNo} {Debugger.SourceFiles[Fn][LineNo]}"

        LineObj = ExecLine(Fn, LineNo, LineInserted, frame.f_locals)
        # in Gui we display only
        Debugger.NameSpaceActual.LinesExecuted.append(LineObj)

    def user_return(self, Frame, RetVal):
        Name = Frame.f_code.co_name or "<unknown>"
        LineNumRet = Frame.f_lineno
        print('+++ return', Name, RetVal, LineNumRet)
        Debugger.NameSpaceActual.RetVal = RetVal

        if Debugger.NameSpaceActual.LineNumRetLatest is None:
            # root elem hasn't got LineNums
            Debugger.NameSpaceActual.LineNumRetLatest = LineNumRet
        else:
            if LineNumRet > Debugger.NameSpaceActual.LineNumRetLatest:
                Debugger.NameSpaceActual.LineNumRetLatest = LineNumRet

        Debugger.NameSpaceActual.LineNumRetLatest = RetVal
        Debugger.NameSpaceActual = Debugger.NameSpaceActual.Parent

    def user_exception(self, frame, exc_stuff):
        #print('+++ exception', exc_stuff)
        self.set_continue()