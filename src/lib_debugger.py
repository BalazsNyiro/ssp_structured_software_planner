import bdb, util

class NameSpaceDefinition():
    def __init__(self, Id,
                 Name,
                 FileName=None,
                 LineNumDef=None,
                 LinesSourceFile = None
                 ):
        self.FileName = FileName
        self.Name = Name
        self.LinesSourceFile = LinesSourceFile
        self.LinesExecuted = {}
        self.LineNumDef = LineNumDef
        self.Id = Id
        self.GuiElems = []
        self.LineNumRetLatest = LineNumDef  # the latest Return Linenum

    def def_line(self):
        return self.LinesSourceFile[self.LineNumDef]

class NameSpaceOneCall():
    def __init__(self, NameSpaceDef=None,
                 Fun=True,
                 Parent=None,
                 Level = 0):

        self.ChildrenCalls = []
        self.Parent = Parent
        self.Fun = Fun
        self.RetVal = None
        self.Level = Level

        # in list of all Namespaces, File and Linenum
        # is he best uniq id
        self.NameSpaceDef = NameSpaceDef

    def name(self):
        if self.NameSpaceDef:
            return self.NameSpaceDef.Name
        return "NoDefName"

    def id(self):
        if self.NameSpaceDef:
            return self.NameSpaceDef.Id
        return ("NoDefFile", "NoDefLineNo")

    def __str__(self):
        Prefix = " " * self.Level
        Out = []
        Out.append(f"{Prefix} -> {self.name()}")
        for Child in self.ChildrenCalls:
            Out.append(Child.__str__())
        Out.append(f"{Prefix} <- {self.name()}: {self.RetVal}")
        return "\n".join(Out)

class ExecLine():
    FileNameLenMax = 0
    LineLenMax = 0

    def __init__(self, FileName, LineNum, Line, Locals):
        self.FileName = FileName
        self.LineNum = LineNum
        self.Line = Line
        self.Locals = Locals

        if Len := len(FileName) > ExecLine.FileNameLenMax:
            ExecLine.FileNameLenMax = Len

        if Len := len(Line) > ExecLine.LineLenMax:
            ExecLine.LineLenMax = Len

    def __str__(self):
        return f"{self.LineNum} {self.Line} {self.FileName}"

class Debugger(bdb.Bdb):
    Root = NameSpaceOneCall()
    NameSpaceDefinitions = {}
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
        ##############################################################################
        NameSpaceDefId = (FileName, LineNumDef)
        # Save all namespaces Once
        if NameSpaceDefId not in Debugger.NameSpaceDefinitions:
            Debugger.NameSpaceDefinitions[NameSpaceDefId] = \
                NameSpaceDefinition(NameSpaceDefId,
                                    Name,
                                    FileName=FileName,
                                    LineNumDef=LineNumDef,
                                    LinesSourceFile = Debugger.SourceFiles[FileName])

        ##############################################################################
        NameSpace = NameSpaceOneCall(Debugger.NameSpaceDefinitions[NameSpaceDefId],
                                     Parent = Parent,
                                     Level = Parent.Level+1,
                                     )

        ##############################################################################
        Debugger.NameSpaceActual.ChildrenCalls.append(NameSpace)
        Debugger.NameSpaceActual = NameSpace


    def user_line(self, frame):
        import linecache
        name = frame.f_code.co_name
        if not name: name = '???'
        Fn = self.canonic(frame.f_code.co_filename)

        LineNo = frame.f_lineno
        Line = linecache.getline(Fn, LineNo, frame.f_globals)
        print('+++ USERLINE',Debugger.NameSpaceActual.name(), Fn, LineNo, name, ':', Line.strip(), "frame locals: ", frame.f_locals)

        LineInserted = f"{LineNo} {Line}"
        if Fn in Debugger.SourceFiles:
            LineInserted = f"{LineNo} {Debugger.SourceFiles[Fn][LineNo]}"

        LineObj = ExecLine(Fn, LineNo, LineInserted, frame.f_locals)

        Debugger.ExecutionAll.append(LineObj)
        if Debugger.NameSpaceActual.id() != ("NoDefFile", "NoDefLineNo"): # no Root
            Debugger.NameSpaceDefinitions[Debugger.NameSpaceActual.id()].LinesExecuted[LineNo] = LineObj

    def user_return(self, Frame, RetVal):
        Name = Frame.f_code.co_name or "<unknown>"
        LineNumRet = Frame.f_lineno
        print('+++ return', Name, RetVal, LineNumRet)

        NameSpaceActual = Debugger.NameSpaceActual
        NameSpaceActual.RetVal = RetVal

        NameSpaceDef = NameSpaceActual.NameSpaceDef
        if NameSpaceDef: # not root elem, it hasn't got name space def

            if NameSpaceDef.LineNumRetLatest is None:
                # root elem hasn't got LineNums
                NameSpaceDef.LineNumRetLatest = LineNumRet

            elif LineNumRet > NameSpaceDef.LineNumRetLatest:
                NameSpaceDef.LineNumRetLatest = LineNumRet

        if Debugger.NameSpaceActual.Parent:
            Debugger.NameSpaceActual = Debugger.NameSpaceActual.Parent

    def user_exception(self, frame, exc_stuff):
        #print('+++ exception', exc_stuff)
        self.set_continue()